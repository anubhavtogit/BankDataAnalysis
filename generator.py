from faker import Faker
import random

import json
from pathlib import Path

# from models import Customer, Branch, Merchant, Account

from models import (
    Customer,
    Branch,
    Merchant,
    Account,
    Transaction
)

from datetime import datetime, timedelta

fake = Faker("en_IN")


# --------------------------------------------------
# Branch Generator
# --------------------------------------------------

def generate_branches(count: int = 10) -> list[Branch]:
    branches = []

    cities = [
        ("Kolkata", "West Bengal"),
        ("Mumbai", "Maharashtra"),
        ("Delhi", "Delhi"),
        ("Bangalore", "Karnataka"),
        ("Hyderabad", "Telangana"),
        ("Chennai", "Tamil Nadu"),
        ("Pune", "Maharashtra"),
        ("Ahmedabad", "Gujarat"),
        ("Jaipur", "Rajasthan"),
        ("Lucknow", "Uttar Pradesh")
    ]

    for i in range(1, count + 1):

        city, state = random.choice(cities)

        branch = Branch(
            branch_id=f"B{i:04d}",
            branch_name=f"{city} Branch {i}",
            city=city,
            state=state
        )

        branches.append(branch)

    return branches


# --------------------------------------------------
# Merchant Generator
# --------------------------------------------------

def generate_merchants(count: int = 20) -> list[Merchant]:
    merchants = []

    merchant_categories = [
        "E-Commerce",
        "Food",
        "Grocery",
        "Travel",
        "Fuel",
        "Healthcare",
        "Entertainment",
        "Electronics",
        "Education",
        "Retail"
    ]

    merchant_names = [
        "Amazon",
        "Flipkart",
        "Swiggy",
        "Zomato",
        "BigBasket",
        "IRCTC",
        "Uber",
        "Ola",
        "Apollo Pharmacy",
        "Reliance Digital",
        "Myntra",
        "BookMyShow",
        "Decathlon",
        "DMart",
        "MakeMyTrip",
        "Ajio",
        "Croma",
        "Blinkit",
        "Zepto",
        "Tata 1mg"
    ]

    cities = [
        "Kolkata",
        "Mumbai",
        "Delhi",
        "Bangalore",
        "Hyderabad",
        "Chennai",
        "Pune"
    ]

    for i in range(1, count + 1):

        merchant = Merchant(
            merchant_id=f"M{i:04d}",
            merchant_name=merchant_names[(i - 1) % len(merchant_names)],
            category=random.choice(merchant_categories),
            city=random.choice(cities)
        )

        merchants.append(merchant)

    return merchants


# --------------------------------------------------
# Customer Generator
# --------------------------------------------------

def generate_customers(
    count: int,
    branches: list[Branch]
) -> list[Customer]:

    customers = []

    occupations = [
        "Software Engineer",
        "Teacher",
        "Doctor",
        "Business Owner",
        "Accountant",
        "Student",
        "Government Employee",
        "Sales Manager",
        "Consultant",
        "Designer"
    ]

    for i in range(1, count + 1):

        branch = random.choice(branches)

        age = random.randint(18, 70)

        customer = Customer(
            customer_id=f"C{i:06d}",
            name=fake.name(),
            age=age,
            gender=random.choice(["Male", "Female"]),
            occupation=random.choice(occupations),
            city=branch.city,
            income=round(random.uniform(200000, 2500000), 2)
        )

        customers.append(customer)

    return customers


# --------------------------------------------------
# Account Generator
# --------------------------------------------------

def generate_accounts(
    customers: list[Customer],
    branches: list[Branch]
) -> list[Account]:

    accounts = []

    account_types = [
        "Savings",
        "Current"
    ]

    for i, customer in enumerate(customers, start=1):

        branch = random.choice(branches)

        account = Account(
            account_id=f"A{i:06d}",
            customer_id=customer.customer_id,
            account_type=random.choice(account_types),
            balance=round(random.uniform(5000, 500000), 2),
            branch_id=branch.branch_id
        )

        accounts.append(account)

    return accounts


if __name__ == "__main__":
    import json
    import os

    # generate sample data
    branches = generate_branches(10)
    merchants = generate_merchants(20)
    customers = generate_customers(50, branches)
    accounts = generate_accounts(customers, branches)

    output = {
        "branches": [b.__dict__ for b in branches],
        "merchants": [m.__dict__ for m in merchants],
        "customers": [c.__dict__ for c in customers],
        "accounts": [a.__dict__ for a in accounts],
    }

    os.makedirs("data", exist_ok=True)
    out_path = os.path.join("data", "generated.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f"Generated: branches={len(branches)} merchants={len(merchants)} customers={len(customers)} accounts={len(accounts)} -> {out_path}")

    import json
from pathlib import Path


def generate_master_data(
    branch_count: int = 10,
    merchant_count: int = 20,
    customer_count: int = 50
):
    # Generate branches
    branches = generate_branches(branch_count)

    # Generate merchants
    merchants = generate_merchants(merchant_count)

    # Generate customers
    customers = generate_customers(
        count=customer_count,
        branches=branches
    )

    # Generate accounts
    accounts = generate_accounts(
        customers=customers,
        branches=branches
    )

    # Prepare output
    data = {
        "branches": [
            branch.model_dump(mode="json")
            for branch in branches
        ],
        "merchants": [
            merchant.model_dump(mode="json")
            for merchant in merchants
        ],
        "customers": [
            customer.model_dump(mode="json")
            for customer in customers
        ],
        "accounts": [
            account.model_dump(mode="json")
            for account in accounts
        ]
    }

    # Create data directory
    output_dir = Path("data")
    output_dir.mkdir(exist_ok=True)

    # Output file
    output_file = output_dir / "generated.json"

    # Write JSON
    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

    return {
        "branches": len(branches),
        "merchants": len(merchants),
        "customers": len(customers),
        "accounts": len(accounts),
        "file": str(output_file)
    }


from datetime import datetime, timedelta


# -----------------------------------------
# Transaction Generator
# -----------------------------------------

def generate_transactions(
    accounts: list[Account],
    merchants: list[Merchant],
    count: int = 100
) -> list[Transaction]:

    transactions = []

    transaction_types = [
        "Purchase",
        "Withdrawal",
        "Deposit",
        "Transfer"
    ]

    payment_methods = [
        "UPI",
        "CARD",
        "ATM",
        "NEFT",
        "IMPS"
    ]

    for i in range(1, count + 1):

        # Pick an existing account
        account = random.choice(accounts)

        transaction_type = random.choice(transaction_types)

        payment_method = random.choice(payment_methods)

        amount = round(
            random.uniform(100, 50000),
            2
        )

        merchant_id = None

        # -----------------------------------------
        # PURCHASE
        # -----------------------------------------

        if transaction_type == "Purchase":

            merchant = random.choice(merchants)

            merchant_id = merchant.merchant_id

            if account.balance >= amount:

                status = "SUCCESS"

                # Deduct money
                account.balance -= amount

            else:

                status = "FAILED"

        # -----------------------------------------
        # WITHDRAWAL
        # -----------------------------------------

        elif transaction_type == "Withdrawal":

            payment_method = "ATM"

            if account.balance >= amount:

                status = "SUCCESS"

                account.balance -= amount

            else:

                status = "FAILED"

        # -----------------------------------------
        # DEPOSIT
        # -----------------------------------------

        elif transaction_type == "Deposit":

            payment_method = "CASH"

            status = "SUCCESS"

            account.balance += amount

        # -----------------------------------------
        # TRANSFER
        # -----------------------------------------

        else:

            payment_method = random.choice([
                "NEFT",
                "IMPS"
            ])

            if account.balance >= amount:

                status = "SUCCESS"

                account.balance -= amount

            else:

                status = "FAILED"

        # -----------------------------------------
        # Timestamp
        # -----------------------------------------

        timestamp = datetime.now() - timedelta(
            minutes=random.randint(0, 1440)
        )

        # -----------------------------------------
        # Create transaction
        # -----------------------------------------

        transaction = Transaction(
            transaction_id=f"T{i:08d}",
            account_id=account.account_id,
            customer_id=account.customer_id,
            merchant_id=merchant_id,
            amount=amount,
            transaction_type=transaction_type,
            payment_method=payment_method,
            status=status,
            timestamp=timestamp
        )

        transactions.append(transaction)

    return transactions