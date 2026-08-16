from apscheduler.schedulers.background import (
    BackgroundScheduler
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


scheduler = BackgroundScheduler()


# =========================================================
# BANK STATE
# =========================================================

bank_state = {

    "branches": [],

    "merchants": [],

    "customers": [],

    "accounts": []
}


# =========================================================
# INITIALIZE BANK
# =========================================================

def initialize_bank():

    global bank_state

    print(
        "Initializing BankFlow AI..."
    )


    # Generate master data

    bank_state = generate_master_data()


    timestamp = get_timestamp()


    # -----------------------------------------------------
    # Upload branches
    # -----------------------------------------------------

    upload_records(

        bank_state["branches"],

        f"raw/master/branches/"
        f"branches_{timestamp}.json"
    )


    # -----------------------------------------------------
    # Upload merchants
    # -----------------------------------------------------

    upload_records(

        bank_state["merchants"],

        f"raw/master/merchants/"
        f"merchants_{timestamp}.json"
    )


    # -----------------------------------------------------
    # Upload customers
    # -----------------------------------------------------

    upload_records(

        bank_state["customers"],

        f"raw/master/customers/"
        f"customers_{timestamp}.json"
    )


    # -----------------------------------------------------
    # Upload accounts
    # -----------------------------------------------------

    upload_records(

        bank_state["accounts"],

        f"raw/master/accounts/"
        f"accounts_{timestamp}.json"
    )


    print(
        f"Customers: "
        f"{len(bank_state['customers'])}"
    )

    print(
        f"Accounts: "
        f"{len(bank_state['accounts'])}"
    )

    print(
        f"Merchants: "
        f"{len(bank_state['merchants'])}"
    )

    print(
        "Master data uploaded successfully."
    )


# =========================================================
# GENERATE TRANSACTION BATCH
# =========================================================

def generate_transaction_batch():

    print(
        "\nGenerating transaction batch..."
    )


    # Generate transactions

    transactions, fraud_events = (
        generate_transactions(

            accounts=bank_state["accounts"],

            merchants=bank_state["merchants"],

            count=100
        )
    )


    timestamp = get_timestamp()


    # -----------------------------------------------------
    # Upload transactions
    # -----------------------------------------------------

    transaction_object = (

        f"raw/transactions/"

        f"transactions_{timestamp}.json"
    )


    upload_records(

        transactions,

        transaction_object
    )


    # -----------------------------------------------------
    # Upload fraud events
    # -----------------------------------------------------

    if fraud_events:

        fraud_object = (

            f"raw/fraud/"

            f"fraud_{timestamp}.json"
        )


        upload_records(

            fraud_events,

            fraud_object
        )


    # -----------------------------------------------------
    # Logging
    # -----------------------------------------------------

    print(
        f"Transactions generated: "
        f"{len(transactions)}"
    )

    print(
        f"Fraud events detected: "
        f"{len(fraud_events)}"
    )


# =========================================================
# START SCHEDULER
# =========================================================

def start_scheduler():

    # Generate master data once

    initialize_bank()


    # Generate transactions every 30 seconds

    scheduler.add_job(

        generate_transaction_batch,

        "interval",

        seconds=30,

        id="transaction_generator",

        replace_existing=True
    )


    scheduler.start()


    print(
        "Transaction scheduler started."
    )

    print(
        "Generating 100 transactions "
        "every 30 seconds."
    )


# =========================================================
# STOP SCHEDULER
# =========================================================

def stop_scheduler():

    if scheduler.running:

        scheduler.shutdown()

        print(
            "Transaction scheduler stopped."
        )