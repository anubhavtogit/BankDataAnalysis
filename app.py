from fastapi import FastAPI

from contextlib import asynccontextmanager

from scheduler import (
    start_scheduler,
    stop_scheduler
)

from generator import (
    generate_master_data
)

from transaction_generator import (
    generate_transactions
)

from minio_storage import (
    upload_records,
    get_timestamp
)


# =========================================================
# LIFESPAN
# =========================================================

@asynccontextmanager
async def lifespan(app: FastAPI):

    print(
        "Starting BankFlow AI..."
    )

    start_scheduler()

    yield

    stop_scheduler()


# =========================================================
# APPLICATION
# =========================================================

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
# MANUAL MASTER GENERATION
# =========================================================

@app.post("/generate/master")
def generate_master():

    data = generate_master_data()

    timestamp = get_timestamp()


    for dataset_name, records in data.items():

        object_name = (

            f"raw/master/"

            f"{dataset_name}/"

            f"{dataset_name}_{timestamp}.json"
        )


        upload_records(

            records,

            object_name
        )


    return {

        "status": "success",

        "message": (
            "Master banking data generated "
            "and uploaded to MinIO"
        ),

        "datasets": {

            "branches": len(
                data["branches"]
            ),

            "merchants": len(
                data["merchants"]
            ),

            "customers": len(
                data["customers"]
            ),

            "accounts": len(
                data["accounts"]
            )
        }
    }


# =========================================================
# MANUAL TRANSACTION GENERATION
# =========================================================

@app.post("/generate/transactions")
def generate_transaction_data(

    count: int = 100

):

    data = generate_master_data()


    transactions, fraud_events = (
        generate_transactions(

            accounts=data["accounts"],

            merchants=data["merchants"],

            count=count
        )
    )


    timestamp = get_timestamp()


    # Upload transactions

    transaction_object = (

        f"raw/transactions/"

        f"transactions_{timestamp}.json"
    )


    upload_records(

        transactions,

        transaction_object
    )


    # Upload fraud events

    fraud_object = None


    if fraud_events:

        fraud_object = (

            f"raw/fraud/"

            f"fraud_{timestamp}.json"
        )


        upload_records(

            fraud_events,

            fraud_object
        )


    return {

        "status": "success",

        "message": (
            "Transactions generated "
            "and uploaded to MinIO"
        ),

        "transactions_generated": len(
            transactions
        ),

        "fraud_events_detected": len(
            fraud_events
        ),

        "transaction_object": (
            transaction_object
        ),

        "fraud_object": fraud_object
    }