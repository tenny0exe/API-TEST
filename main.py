from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  # <-- import this
from app.api import wheel_specifications, bogie_checksheet
from app.database import Base, engine
import uvicorn

# Create tables on startup
Base.metadata.create_all(bind=engine)

app = FastAPI(title="KPA Form Data APIs")

# Add CORS middleware here
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change "*" to your frontend URL(s) in production for security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(wheel_specifications.router, prefix="/api/forms", tags=["Wheel Specs"])
app.include_router(bogie_checksheet.router, prefix="/api/forms", tags=["Bogie Checksheet"])

@app.get("/")
def read_root():
    return {"message": "API is running!"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
