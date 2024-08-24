from pymongo import MongoClient
import gridfs #libreria para trabajar con archivos en mongoDB por encima de 16MB

db_client = MongoClient("mongodb+srv://AdrianValvi:AdrianValvi@cluster0.tz1cgit.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")

db = db_client.test #conecta a la base de datos test
fs = gridfs.GridFS(db) #pasar la base de datos a la gridfs
