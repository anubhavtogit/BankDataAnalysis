import random
from datetime import datetime

from models import Transaction

from banking_rules import process_transaction


# =========================================================
# GENERATE TRANSACTIONS
# =========================================================

def generate_transactions(
    accounts,
    merchants,
    count=100
):

    transactions = []

    fraud_events = []

    transaction_types = [

        "Purchase",

        "ATM Withdrawal",

        "Bank Transfer",

        "Bill Payment",

        "UPI Payment"
    ]

    payment_methods = [

        "UPI",

        "Debit Card",

        "ATM",

        "Net Banking",

        "Mobile Banking"
    ]


    # -----------------------------------------------------
    # Generate transactions
    # -----------------------------------------------------

    for i in range(
        1,
        count + 1
    ):

        account = random.choice(
            accounts
        )


        # -------------------------------------------------
        # Transaction type
        # -------------------------------------------------

        transaction_type = random.choice(
            transaction_types
        )


        # -------------------------------------------------
        # Merchant
        # -------------------------------------------------

        if transaction_type == "ATM Withdrawal":

            merchant_id = None

        else:

            merchant = random.choice(
                merchants
            )

            merchant_id = (
                merchant.merchant_id
            )


        # -------------------------------------------------
        # Create transaction
        # -------------------------------------------------

        transaction = Transaction(

            #transaction_id=f"T{i:08d}",
            transaction_id=(
                f"T{datetime.now().strftime('%Y%m%d%H%M%S')}"
                f"{i:04d}"
                ),
            account_id=account.account_id,

            customer_id=account.customer_id,

            merchant_id=merchant_id,

            amount=round(
                random.uniform(
                    100,
                    100000
                ),
                2
            ),

            transaction_type=transaction_type,

            payment_method=random.choice(
                payment_methods
            ),

            status=random.choices(

                [
                    "SUCCESS",
                    "FAILED",
                    "PENDING"
                ],

                weights=[
                    90,
                    7,
                    3
                ]

            )[0],

            timestamp=datetime.now()
        )


        # -------------------------------------------------
        # Fraud processing
        # -------------------------------------------------

        transaction, fraud_event = (
            process_transaction(

                transaction,

                account
            )
        )


        transactions.append(
            transaction
        )


        # -------------------------------------------------
        # Store fraud event
        # -------------------------------------------------

        if fraud_event:

            fraud_events.append(
                fraud_event
            )


    return (
        transactions,
        fraud_events
    )