from fastapi import FastAPI, File, UploadFile
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import User
from schemas import UserCreate
import pandas as pd
import os

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


Base.metadata.create_all(bind=engine)

@app.post("/uploadfile/")
def uploadfile(file: UploadFile = File(...), skiprows: int = 0, db: Session = Depends(get_db)):
    filename = file.filename
    if not filename.endswith(".csv"):
        return {"error": "Only CSV files are supported."}

    df = pd.read_csv(file.file, skiprows=skiprows)

    if "name" not in df.columns or "age" not in df.columns:
        return {"error": "Please map the 'Name' and 'Age' columns."}

    db.bulk_insert_mappings(User, df.to_dict(orient="records"))
    db.commit()

    return {"message": "Data has been saved to the SQLite database."}