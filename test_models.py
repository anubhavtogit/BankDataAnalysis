from models import Customer


customer = Customer(
    customer_id="C001",
    name="Rahul Sharma",
    age=28,
    gender="Male",
    occupation="Software Engineer",
    city="Kolkata",
    income=850000
)

print(customer)
print(customer.model_dump())