from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from routers import files, delete
from database.client import db, fs
import gridfs #libreria para trabajar con archivos en mongoDB por encima de 16MB


app = FastAPI()
app.include_router(files.router)
app.include_router(delete.router)



#solo las url permitidas para utilizar la API
origins = [
    "http://127.0.0.1:5500",  #puerto de desarrollo
    "http://localhost:5500",  #puerto de desarrollo
    "https://calm-alfajores-b3ba98.netlify.app/",
    "https://calm-alfajores-b3ba98.netlify.app",
    "https://adrianvalvi.netlify.app/",
    "https://adrianvalvi.netlify.app"
]

#Agrega el middleware de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins= origins, 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



#end point para verificar la conexion a la base de datos
@app.get("/verify_connection")
def verify_connection():
    try:
        # Reemplaza 'my_collection' con el nombre de tu colección
        count = db.my_collection.count_documents({})
        return {"message": "Connection successful", "count": count}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Ruta para subir archivos
@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    file_contents = await file.read()

    # Guarda el archivo en MongoDB Atlas
    fs.put(file_contents, filename=file.filename)

    return {"archivo subido con exito": file.filename}
