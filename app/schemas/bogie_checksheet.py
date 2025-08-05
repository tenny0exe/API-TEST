from pydantic import BaseModel
from typing import Optional
from datetime import date

class BmbcChecksheet(BaseModel):
    cylinderBody: Optional[str]
    pistonTrunnion: Optional[str]
    adjustingTube: Optional[str]
    plungerSpring: Optional[str]

class BogieChecksheetFields(BaseModel):
    bogieFrameCondition: Optional[str]
    bolster: Optional[str]
    bolsterSuspensionBracket: Optional[str]
    lowerSpringSeat: Optional[str]
    axleGuide: Optional[str]

class BogieDetails(BaseModel):
    bogieNo: Optional[str]
    makerYearBuilt: Optional[str]
    incomingDivAndDate: Optional[str]
    deficitComponents: Optional[str]
    dateOfIOH: Optional[date]

class BogieChecksheetCreate(BaseModel):
    formNumber: str
    inspectionBy: str
    inspectionDate: date
    bogieDetails: BogieDetails
    bogieChecksheet: BogieChecksheetFields
    bmbcChecksheet: BmbcChecksheet

class BogieChecksheetResponse(BaseModel):
    formNumber: str
    inspectionBy: str
    inspectionDate: date
    status: str
