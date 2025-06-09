from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import Literal
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

@router.get("/")
def get_all_cases(skip: int = 0, limit: int = 10):
    try:
        cases_cursor = case_collection.find({"archived": {"$ne": True}}).skip(skip).limit(limit)
        cases = []
        for case in cases_cursor:
            case["_id"] = str(case["_id"])
            cases.append(case)
        return {"cases": cases}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{case_id}")
def get_case_by_id(case_id: str):
    case = case_collection.find_one({"case_id": case_id})
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")
    
    case["_id"] = str(case["_id"])
    return case

class CaseStatusUpdate(BaseModel):
    status: Literal["new", "under_investigation", "resolved"]

@router.patch("/{case_id}")
def update_case_status(case_id: str, status_update: CaseStatusUpdate):
    result = case_collection.update_one(
        {"case_id": case_id},
        {"$set": {"status": status_update.status}}
    )

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Case not found")
    
    return {"message": f"Case status updated to '{status_update.status}'"}

@router.delete("/{case_id}")
def archive_case(case_id: str):
    result = case_collection.update_one(
        {"case_id": case_id},
        {"$set": {"archived": True}}
    )

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Case not found")

    return {"message": f"Case '{case_id}' has been archived."}

