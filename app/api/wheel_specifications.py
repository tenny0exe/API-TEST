from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.wheel_specifications import WheelSpecificationCreate, WheelSpecificationResponse
from app.models.wheel_specifications import WheelSpecification
from app.database import Base, engine
from datetime import datetime
from fastapi import Query
from typing import List, Optional
from app.database import get_db
router = APIRouter()





@router.get("/wheel-specifications", response_model=dict)
def get_wheel_specifications(
    formNumber: Optional[str] = Query(None),
    submittedBy: Optional[str] = Query(None),
    submittedDate: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    query = db.query(WheelSpecification)

    if formNumber:
        query = query.filter(WheelSpecification.form_number == formNumber)
    if submittedBy:
        query = query.filter(WheelSpecification.submitted_by == submittedBy)
    if submittedDate:
        try:
            date_obj = datetime.strptime(submittedDate, "%Y-%m-%d").date()
            query = query.filter(WheelSpecification.submitted_date == date_obj)
        except ValueError:
            raise HTTPException(status_code=400, detail="submittedDate must be in YYYY-MM-DD format")

    results = query.all()

    # Format output data
    data = []
    for item in results:
        data.append({
            "formNumber": item.form_number,
            "submittedBy": item.submitted_by,
            "submittedDate": item.submitted_date.isoformat(),
            "fields": item.fields
        })

    return {
        "success": True,
        "message": "Filtered wheel specification forms fetched successfully.",
        "data": data
    }




@router.post("/wheel-specifications", response_model=dict, status_code=201)
def create_wheel_specification(
    payload: WheelSpecificationCreate,
    db: Session = Depends(get_db)
):
    # Check if formNumber already exists
    existing = db.query(WheelSpecification).filter(WheelSpecification.form_number == payload.formNumber).first()
    if existing:
        raise HTTPException(status_code=400, detail="Form number already exists.")

    db_obj = WheelSpecification(
        form_number=payload.formNumber,
        submitted_by=payload.submittedBy,
        submitted_date=payload.submittedDate,
        fields=payload.fields.dict()
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)

    return {
        "success": True,
        "message": "Wheel specification submitted successfully.",
        "data": {
            "formNumber": db_obj.form_number,
            "submittedBy": db_obj.submitted_by,
            "submittedDate": db_obj.submitted_date.isoformat(),
            "status": "Saved"
        }
    }
