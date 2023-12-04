fastapi-startapp csv_to_db
cd csv_to_db
pip install fastapi[all]
pip install uvicorn[standard]
pip install pydantic
pip install pandas
pip install sqlalchemy
pip install databases[sqlite]

uvicorn main:app --reload