from fastapi import APIRouter
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse, StreamingResponse
import gridfs
from database.client import db,fs

router=APIRouter(tags=["delete"],prefix="/delete")

@router.delete("/{filename}")
async def delete_file(filename: str):
    try:
        # Obtiene el _id del archivo por su nombre de archivo
        id=searchId(filename)
        
        # Elimina el archivo de MongoDB Atlas
        fs.delete(id)
   
   # Si el archivo no se encuentra, devuelve un error HTTP 404
    except gridfs.NoFile:
        raise HTTPException(status_code=404, detail="File not found")
    
    # Si el archivo se encuentra, devuelve un mensaje de éxito
    return {"message": "File deleted successfully"}


# Función para buscar el _id de un archivo por su nombre de archivo
def searchId(filename:str):
     # Busca el archivo por su nombre de archivo
    file = fs.find_one({"filename": filename})

    if file:
        # Si el archivo se encuentra, devuelve su _id
        return file._id
    else:
        # Si el archivo no se encuentra, devuelve un error HTTP 404
        raise HTTPException(status_code=404, detail="Archivo no encontrado")

