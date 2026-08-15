from generator import generate_master_data

from transaction_generator import (
    generate_transactions,
    save_transactions
)


# -----------------------------------------
# Generate master data
# -----------------------------------------

data = generate_master_data()

accounts = data["accounts"]
merchants = data["merchants"]


# -----------------------------------------
# Generate transactions
# -----------------------------------------

transactions, fraud_events = generate_transactions(
    accounts=accounts,
    merchants=merchants,
    count=100
)


# -----------------------------------------
# Display results
# -----------------------------------------

print(
    f"Transactions generated: {len(transactions)}"
)

print(
    f"Fraud events detected: {len(fraud_events)}"
)


# -----------------------------------------
# Save transactions
# -----------------------------------------

save_transactions(
    transactions
)