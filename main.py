from fastapi import FastAPI
from app.routes.case_routes import router as case_router

app = FastAPI()

app.include_router(case_router, prefix="/cases", tags=["Cases"])

@app.get("/")
def root():
    return {"message": "Human Rights Monitor API is running"}
