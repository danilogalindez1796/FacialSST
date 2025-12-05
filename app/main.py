from fastapi import FastAPI, HTTPException, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from app.database import SessionLocal
from app.models import Face
from app.utils import image_to_embedding
import face_recognition
import pickle
import base64
import traceback
from contextlib import contextmanager

app = FastAPI()

# Configurar CORS simplificado
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite todos los orígenes en desarrollo
    allow_methods=["*"],
    allow_headers=["*"],
)

@contextmanager
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/face/register")
def register_face(id_usuario: int = Form(...), image: str = Form(...)):
    try:
        embedding = image_to_embedding(image)
        if embedding is None:
            raise HTTPException(status_code=400, detail="No se detectó rostro")
        
        with get_db() as db:
            if db.query(Face).filter(Face.id_usuario == id_usuario).first():
                raise HTTPException(status_code=400, detail="Usuario ya registrado")
            
            descriptor_serialized = pickle.dumps(embedding)
            face = Face(id_usuario=id_usuario, descriptor=descriptor_serialized)
            db.add(face)
            db.commit()
        
        return {"message": "Rostro registrado exitosamente"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@app.post("/face/login")
async def login_face(file: UploadFile = File(...)):
    try:
        # Validar tipo de archivo
        if not file.content_type.startswith('image/'):
            raise HTTPException(status_code=400, detail="Solo se permiten imágenes")
        
        # Leer imagen
        image_data = await file.read()
        if len(image_data) == 0:
            raise HTTPException(status_code=400, detail="Imagen vacía")
        
        # Convertir a base64
        image_base64 = base64.b64encode(image_data).decode('utf-8')
        
        # Obtener embedding
        embedding = image_to_embedding(image_base64)
        if embedding is None:
            raise HTTPException(status_code=400, detail="No se detectó rostro")
        
        # Buscar coincidencias
        with get_db() as db:
            faces = db.query(Face).all()
            
            for face in faces:
                db_embedding = pickle.loads(face.descriptor)
                matches = face_recognition.compare_faces([db_embedding], embedding)
                
                if matches[0]:
                    return {
                        "authenticated": True,
                        "id_usuario": face.id_usuario,
                        "id_face": face.id_face
                    }
        
        return {"authenticated": False, "message": "Rostro no reconocido"}
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")
