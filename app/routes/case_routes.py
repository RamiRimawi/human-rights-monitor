from fastapi import APIRouter, HTTPException
from app.models.case_model import CaseCreate
from app.database import case_collection
from bson import ObjectId

router = APIRouter()

@router.post("/")
def create_case(case: CaseCreate):
    case_dict = case.dict()
    
    existing = case_collection.find_one({"case_id": case_dict["case_id"]})
    if existing:
        raise HTTPException(status_code=400, detail="Case ID already exists")
    
    result = case_collection.insert_one(case_dict)
    
    return {
        "message": "Case created successfully",
        "id": str(result.inserted_id)
    }
