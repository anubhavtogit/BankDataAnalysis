from datetime import datetime

from models import FraudEvent


def process_transaction(
    transaction,
    account
):

    # -----------------------------------------
    # Balance check
    # -----------------------------------------

    if transaction.status == "SUCCESS":

        if transaction.amount > account.balance:

            transaction.status = "FAILED"

        else:

            account.balance -= transaction.amount

    # -----------------------------------------
    # Fraud detection
    # -----------------------------------------

    fraud_event = None

    if transaction.status == "SUCCESS":

        if transaction.amount >= 75000:

            fraud_event = FraudEvent(
                fraud_id=f"F{transaction.transaction_id[1:]}",
                transaction_id=transaction.transaction_id,
                customer_id=transaction.customer_id,
                account_id=transaction.account_id,
                amount=transaction.amount,
                risk_score=90,
                reason="High value transaction",
                timestamp=datetime.now()
            )

    return transaction, fraud_event