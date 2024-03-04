from fastapi import APIRouter
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse, StreamingResponse
import gridfs
from database.client import db,fs




router=APIRouter(tags=["files"],
    prefix="/files")

@router.get("")
async def list_files():
    # Obtiene los nombres de los archivos en MongoDB Atlas
    files = [file.filename for file in fs.find()]

    return {"files": files}

@router.get("/{filename}")
async def get_file(filename: str):
    try:
        # Obtiene el archivo de MongoDB Atlas
        file = fs.get_last_version(filename=filename)
    except gridfs.NoFile:
        raise HTTPException(status_code=404, detail="File not found")

    # Crea una respuesta que se puede descargar
    response = StreamingResponse(file, media_type='application/octet-stream')
    response.headers["Content-Disposition"] = f'attachment; filename="{filename}"'
    return response

