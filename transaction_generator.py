import json
import random
from datetime import datetime
from pathlib import Path

from models import Transaction

import json
import random

from datetime import datetime
from pathlib import Path

from models import Transaction
from banking_rules import process_transaction

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

    for i in range(1, count + 1):

        account = random.choice(accounts)

        transaction_type = random.choice(
            transaction_types
        )

        if transaction_type == "ATM Withdrawal":

            merchant_id = None

        else:

            merchant = random.choice(merchants)
            merchant_id = merchant.merchant_id

        transaction = Transaction(
            transaction_id=f"T{i:08d}",

            account_id=account.account_id,

            customer_id=account.customer_id,

            merchant_id=merchant_id,

            amount=round(
                random.uniform(100, 100000),
                2
            ),

            transaction_type=transaction_type,

            payment_method=random.choice(
                payment_methods
            ),

            status=random.choices(
                ["SUCCESS", "FAILED", "PENDING"],
                weights=[90, 7, 3]
            )[0],

            timestamp=datetime.now()
        )

        transaction, fraud_event = process_transaction(
            transaction,
            account
        )

        transactions.append(transaction)

        if fraud_event:

            fraud_events.append(
                fraud_event
            )

    return transactions, fraud_events


def save_transactions(transactions):

    output_directory = Path(
        "data/raw/transactions"
    )

    output_directory.mkdir(
        parents=True,
        exist_ok=True
    )

    timestamp = datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )

    file_path = (
        output_directory
        / f"transactions_{timestamp}.json"
    )

    records = [
        transaction.model_dump()
        for transaction in transactions
    ]

    with open(
        file_path,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            records,
            file,
            indent=4,
            ensure_ascii=False,
            default=str
        )

    print(f"Created: {file_path}")

    return file_path

def save_fraud_events(fraud_events):

    output_directory = Path(
        "data/raw/fraud"
    )

    output_directory.mkdir(
        parents=True,
        exist_ok=True
    )

    timestamp = datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )

    file_path = (
        output_directory
        / f"fraud_{timestamp}.json"
    )

    records = [
        event.model_dump()
        for event in fraud_events
    ]

    with open(
        file_path,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            records,
            file,
            indent=4,
            default=str
        )

    print(
        f"Created fraud file: {file_path}"
    )

    return file_path