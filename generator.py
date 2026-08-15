import json
import random
from pathlib import Path

from faker import Faker

from models import Customer, Branch, Merchant, Account


fake = Faker("en_IN")


# =========================================================
# BRANCH GENERATOR
# =========================================================

def generate_branches(count: int = 10) -> list[Branch]:

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

    branches = []

    for i in range(1, count + 1):

        city, state = cities[(i - 1) % len(cities)]

        branch = Branch(
            branch_id=f"B{i:04d}",
            branch_name=f"{city} Branch {i}",
            city=city,
            state=state
        )

        branches.append(branch)

    return branches


# =========================================================
# MERCHANT GENERATOR
# =========================================================

def generate_merchants(count: int = 20) -> list[Merchant]:

    merchant_data = [
        ("Amazon", "E-Commerce"),
        ("Flipkart", "E-Commerce"),
        ("Swiggy", "Food"),
        ("Zomato", "Food"),
        ("BigBasket", "Grocery"),
        ("IRCTC", "Travel"),
        ("Uber", "Transport"),
        ("Ola", "Transport"),
        ("Apollo Pharmacy", "Healthcare"),
        ("Reliance Digital", "Electronics"),
        ("Myntra", "Fashion"),
        ("BookMyShow", "Entertainment"),
        ("Decathlon", "Retail"),
        ("DMart", "Grocery"),
        ("MakeMyTrip", "Travel"),
        ("Ajio", "Fashion"),
        ("Croma", "Electronics"),
        ("Blinkit", "Grocery"),
        ("Zepto", "Grocery"),
        ("Tata 1mg", "Healthcare")
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

    merchants = []

    for i in range(1, count + 1):

        merchant_name, category = merchant_data[
            (i - 1) % len(merchant_data)
        ]

        merchant = Merchant(
            merchant_id=f"M{i:04d}",
            merchant_name=merchant_name,
            category=category,
            city=random.choice(cities)
        )

        merchants.append(merchant)

    return merchants


# =========================================================
# CUSTOMER GENERATOR
# =========================================================

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

        customer = Customer(
            customer_id=f"C{i:06d}",
            name=fake.name(),
            age=random.randint(18, 70),
            gender=random.choice(["Male", "Female"]),
            occupation=random.choice(occupations),
            city=branch.city,
            income=round(
                random.uniform(200000, 2500000),
                2
            )
        )

        customers.append(customer)

    return customers


# =========================================================
# ACCOUNT GENERATOR
# =========================================================

def generate_accounts(
    customers: list[Customer],
    branches: list[Branch]
) -> list[Account]:

    accounts = []

    account_types = [
        "Savings",
        "Current"
    ]

    # Group branches by city
    branches_by_city = {}

    for branch in branches:

        if branch.city not in branches_by_city:
            branches_by_city[branch.city] = []

        branches_by_city[branch.city].append(branch)

    for i, customer in enumerate(customers, start=1):

        customer_branches = branches_by_city.get(
            customer.city,
            branches
        )

        branch = random.choice(customer_branches)

        account = Account(
            account_id=f"A{i:06d}",
            customer_id=customer.customer_id,
            account_type=random.choice(account_types),
            balance=round(
                random.uniform(5000, 500000),
                2
            ),
            branch_id=branch.branch_id
        )

        accounts.append(account)

    return accounts


# =========================================================
# MASTER DATA GENERATOR
# =========================================================

def generate_master_data():

    print("Generating branches...")

    branches = generate_branches(10)

    print("Generating merchants...")

    merchants = generate_merchants(20)

    print("Generating customers...")

    customers = generate_customers(
        count=100,
        branches=branches
    )

    print("Generating accounts...")

    accounts = generate_accounts(
        customers=customers,
        branches=branches
    )

    return {
        "branches": branches,
        "merchants": merchants,
        "customers": customers,
        "accounts": accounts
    }


# =========================================================
# SAVE DATA TO JSON
# =========================================================

def save_master_data(data):

    output_directory = Path("data/raw")

    output_directory.mkdir(
        parents=True,
        exist_ok=True
    )

    for dataset_name, records in data.items():

        file_path = (
            output_directory /
            f"{dataset_name}.json"
        )

        records_as_dict = [
            record.model_dump()
            for record in records
        ]

        with open(
            file_path,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                records_as_dict,
                file,
                indent=4,
                ensure_ascii=False
            )

        print(f"Created: {file_path}")