from fastapi import FastAPI
from generator import generate_master_data


app = FastAPI(
    title="BankFlow AI",
    description="Banking Data Engineering Platform",
    version="1.0.0"
)


@app.get("/")
def root():
    return {
        "message": "BankFlow AI Running"
    }


@app.post("/generate/master")
def generate_master():
    result = generate_master_data()

    return {
        "status": "success",
        "message": "Master data generated successfully",
        "data": result
    }