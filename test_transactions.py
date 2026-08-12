from generator import (
    generate_branches,
    generate_merchants,
    generate_customers,
    generate_accounts,
    generate_transactions
)


branches = generate_branches(10)

merchants = generate_merchants(20)

customers = generate_customers(
    count=50,
    branches=branches
)

accounts = generate_accounts(
    customers=customers,
    branches=branches
)


transactions = generate_transactions(
    accounts=accounts,
    merchants=merchants,
    count=100
)


print("\n--- TRANSACTIONS ---")

for transaction in transactions[:10]:
    print(transaction.model_dump())


print("\n--- ACCOUNT BALANCES ---")

for account in accounts[:10]:
    print(
        account.account_id,
        account.customer_id,
        account.balance
    )