from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.database import Base, engine
from datetime import datetime
from fastapi import Query
from typing import List, Optional
from sqlalchemy import and_
from app.models.bogie_checksheet import BogieChecksheet
from app.schemas.bogie_checksheet import BogieChecksheetCreate, BogieChecksheetResponse


router = APIRouter()

@router.post("/bogie-checksheet", response_model=dict, status_code=status.HTTP_201_CREATED)
def create_bogie_checksheet(data: BogieChecksheetCreate, db: Session = Depends(get_db)):
    # Check if formNumber exists
    existing = db.query(BogieChecksheet).filter(BogieChecksheet.form_number == data.formNumber).first()
    if existing:
        raise HTTPException(status_code=400, detail="Form number already exists")

    bogie_checksheet = BogieChecksheet(
        form_number=data.formNumber,
        inspection_by=data.inspectionBy,
        inspection_date=data.inspectionDate,
        bogie_no=data.bogieDetails.bogieNo,
        maker_year_built=data.bogieDetails.makerYearBuilt,
        incoming_div_and_date=data.bogieDetails.incomingDivAndDate,
        deficit_components=data.bogieDetails.deficitComponents,
        date_of_ioh=data.bogieDetails.dateOfIOH,
        bogie_frame_condition=data.bogieChecksheet.bogieFrameCondition,
        bolster=data.bogieChecksheet.bolster,
        bolster_suspension_bracket=data.bogieChecksheet.bolsterSuspensionBracket,
        lower_spring_seat=data.bogieChecksheet.lowerSpringSeat,
        axle_guide=data.bogieChecksheet.axleGuide,
        cylinder_body=data.bmbcChecksheet.cylinderBody,
        piston_trunnion=data.bmbcChecksheet.pistonTrunnion,
        adjusting_tube=data.bmbcChecksheet.adjustingTube,
        plunger_spring=data.bmbcChecksheet.plungerSpring,
    )

    db.add(bogie_checksheet)
    db.commit()
    db.refresh(bogie_checksheet)

    return {
        "success": True,
        "message": "Bogie checksheet submitted successfully.",
        "data": {
            "formNumber": bogie_checksheet.form_number,
            "inspectionBy": bogie_checksheet.inspection_by,
            "inspectionDate": bogie_checksheet.inspection_date.isoformat(),
            "status": "Saved"
        }
    }




@router.get("/bogie-checksheet", response_model=dict)
def get_bogie_checksheets(
    formNumber: Optional[str] = Query(None),
    inspectionBy: Optional[str] = Query(None),
    inspectionDate: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    query = db.query(BogieChecksheet)

    filters = []
    if formNumber:
        filters.append(BogieChecksheet.form_number == formNumber)
    if inspectionBy:
        filters.append(BogieChecksheet.inspection_by == inspectionBy)
    if inspectionDate:
        try:
            inspection_date_obj = datetime.strptime(inspectionDate, "%Y-%m-%d").date()
            filters.append(BogieChecksheet.inspection_date == inspection_date_obj)
        except ValueError:
            raise HTTPException(status_code=400, detail="inspectionDate must be in YYYY-MM-DD format")

    if filters:
        query = query.filter(and_(*filters))

    results = query.all()

    # Convert results to list of dicts
    data = []
    for r in results:
        data.append({
            "formNumber": r.form_number,
            "inspectionBy": r.inspection_by,
            "inspectionDate": r.inspection_date.isoformat(),
            "bogieDetails": {
                "bogieNo": r.bogie_no,
                "makerYearBuilt": r.maker_year_built,
                "incomingDivAndDate": r.incoming_div_and_date,
                "deficitComponents": r.deficit_components,
                "dateOfIOH": r.date_of_ioh.isoformat() if r.date_of_ioh else None
            },
            "bogieChecksheet": {
                "bogieFrameCondition": r.bogie_frame_condition,
                "bolster": r.bolster,
                "bolsterSuspensionBracket": r.bolster_suspension_bracket,
                "lowerSpringSeat": r.lower_spring_seat,
                "axleGuide": r.axle_guide,
            },
            "bmbcChecksheet": {
                "cylinderBody": r.cylinder_body,
                "pistonTrunnion": r.piston_trunnion,
                "adjustingTube": r.adjusting_tube,
                "plungerSpring": r.plunger_spring,
            }
        })

    return {
        "success": True,
        "message": "Filtered bogie checksheet forms fetched successfully.",
        "data": data
    }
