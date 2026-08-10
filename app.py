from fastapi import FastAPI

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