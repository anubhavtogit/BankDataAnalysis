from apscheduler.schedulers.background import BackgroundScheduler

from generator import generate_master_data

# from transaction_generator import (
#     generate_transactions,
#     save_transactions
# )

from transaction_generator import (
    generate_transactions,
    save_transactions,
    save_fraud_events
)


scheduler = BackgroundScheduler()


# ---------------------------------------------------------
# Bank state
# ---------------------------------------------------------

bank_state = {
    "branches": [],
    "merchants": [],
    "customers": [],
    "accounts": []
}


# ---------------------------------------------------------
# Initialize bank
# ---------------------------------------------------------

def initialize_bank():

    global bank_state

    print("Initializing BankFlow AI...")

    bank_state = generate_master_data()

    print(
        f"Customers: {len(bank_state['customers'])}"
    )

    print(
        f"Accounts: {len(bank_state['accounts'])}"
    )

    print(
        f"Merchants: {len(bank_state['merchants'])}"
    )

    print("Bank initialized successfully.")


# ---------------------------------------------------------
# Generate transactions
# ---------------------------------------------------------

def generate_transaction_batch():

    print("\nGenerating transaction batch...")

    transactions, fraud_events = generate_transactions(

        accounts=bank_state["accounts"],

        merchants=bank_state["merchants"],

        count=100
    )

    transaction_file = save_transactions(
        transactions
    )

    fraud_file = save_fraud_events(
        fraud_events
    )

    print(
        f"Transactions generated: {len(transactions)}"
    )

    print(
        f"Fraud events detected: {len(fraud_events)}"
    )

    print(
        f"Transaction file: {transaction_file}"
    )


# ---------------------------------------------------------
# Start scheduler
# ---------------------------------------------------------

def start_scheduler():

    initialize_bank()

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
        "Generating 100 transactions every 30 seconds."
    )


# ---------------------------------------------------------
# Stop scheduler
# ---------------------------------------------------------

def stop_scheduler():

    if scheduler.running:

        scheduler.shutdown()

        print(
            "Transaction scheduler stopped."
        )