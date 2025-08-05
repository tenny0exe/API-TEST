from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base, engine




class BogieChecksheet(Base):
    __tablename__ = "bogie_checksheet"

    id = Column(Integer, primary_key=True, index=True)
    form_number = Column(String, unique=True, index=True)
    inspection_by = Column(String, index=True)
    inspection_date = Column(Date)

    # Bogie details
    bogie_no = Column(String)
    maker_year_built = Column(String)
    incoming_div_and_date = Column(String)
    deficit_components = Column(String)
    date_of_ioh = Column(Date)

    # Bogie checksheet fields
    bogie_frame_condition = Column(String)
    bolster = Column(String)
    bolster_suspension_bracket = Column(String)
    lower_spring_seat = Column(String)
    axle_guide = Column(String)

    # BMBC checksheet fields
    cylinder_body = Column(String)
    piston_trunnion = Column(String)
    adjusting_tube = Column(String)
    plunger_spring = Column(String)
