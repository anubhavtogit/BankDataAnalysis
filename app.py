from fastapi import FastAPI

from contextlib import asynccontextmanager

from scheduler import (
    start_scheduler,
    stop_scheduler
)

from generator import (
    generate_master_data,
    save_master_data
)

from transaction_generator import (
    generate_transactions,
    save_transactions
)

@asynccontextmanager
async def lifespan(app: FastAPI):

    start_scheduler()

    yield

    stop_scheduler()

# app = FastAPI(
#     title="BankFlow AI",
#     description="Banking Data Engineering Platform",
#     version="1.0.0"
# )

app = FastAPI(
    title="BankFlow AI",
    description="Banking Data Engineering Platform",
    version="1.0.0",
    lifespan=lifespan
)

# =========================================================
# ROOT
# =========================================================

@app.get("/")
def root():

    return {
        "message": "BankFlow AI Running"
    }


# =========================================================
# GENERATE MASTER DATA
# =========================================================

@app.post("/generate/master")
def generate_master():

    data = generate_master_data()

    save_master_data(data)

    return {
        "status": "success",
        "message": "Master banking data generated successfully",
        "datasets": {
            "branches": len(data["branches"]),
            "merchants": len(data["merchants"]),
            "customers": len(data["customers"]),
            "accounts": len(data["accounts"])
        }
    }


# =========================================================
# GENERATE TRANSACTIONS
# =========================================================

@app.post("/generate/transactions")
def generate_transaction_data(
    count: int = 100
):

    # ---------------------------------------------
    # Generate master data
    # ---------------------------------------------

    data = generate_master_data()

    accounts = data["accounts"]

    merchants = data["merchants"]


    # ---------------------------------------------
    # Generate transactions
    # ---------------------------------------------

    transactions, fraud_events = generate_transactions(
        accounts=accounts,
        merchants=merchants,
        count=count
    )


    # ---------------------------------------------
    # Save transactions
    # ---------------------------------------------

    transaction_file = save_transactions(
        transactions
    )


    # ---------------------------------------------
    # Response
    # ---------------------------------------------

    return {
        "status": "success",

        "message": "Transactions generated successfully",

        "transactions_generated": len(
            transactions
        ),

        "fraud_events_detected": len(
            fraud_events
        ),

        "transaction_file": str(
            transaction_file
        )
    }
