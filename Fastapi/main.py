from fastapi import FastAPI, Path, HTTPException, Query
import json

app = FastAPI()

def load_data():
    with open ("patients.json", "r") as f:
        data = json.load(f)
    return data

@app.get("/")
def read_root():
    return {"Hello": "welcome"}

@app.get("/about")
def read_about():
    return {"About": "this is an api for viewing patient data"}

@app.get("/patients/{patient_id}")
def get_patient(patient_id: str = Path(..., description="The ID of the patient to retrieve", example="P001")):
    data = load_data()
    if patient_id in data:
        return data[patient_id]
    raise HTTPException(status_code=404, detail="Patient not found")

@app.get("/sort")
def sort_patients(sort_by: str = Query(..., description="sort on the basis of height or weight", example="height"), order: str = Query("asc", description="order of sorting: asc or desc")):
    data = load_data()
    if sort_by not in ["height", "weight"]:
        raise HTTPException(status_code=400, detail="Invalid sort parameter")
    if order not in ["asc", "desc"]:
        raise HTTPException(status_code=400, detail="Invalid order parameter")
    reverse = True if order == "desc" else False
    sorted_data = dict(sorted(data.items(), key=lambda item: item[1][sort_by], reverse=reverse))
    return sorted_data
