from datetime import datetime
from pydantic import BaseModel


class Customer(BaseModel):
    customer_id: str
    name: str
    age: int
    gender: str
    occupation: str
    city: str
    income: float


class Branch(BaseModel):
    branch_id: str
    branch_name: str
    city: str
    state: str


class Merchant(BaseModel):
    merchant_id: str
    merchant_name: str
    category: str
    city: str


class Account(BaseModel):
    account_id: str
    customer_id: str
    account_type: str
    balance: float
    branch_id: str


class Transaction(BaseModel):
    transaction_id: str
    account_id: str
    customer_id: str
    merchant_id: str | None = None
    amount: float
    transaction_type: str
    payment_method: str
    status: str
    timestamp: datetime


class FraudEvent(BaseModel):
    fraud_id: str
    transaction_id: str
    risk_score: int
    reason: str
    timestamp: datetime


class LoginEvent(BaseModel):
    login_id: str
    customer_id: str
    device: str
    city: str
    success: bool
    timestamp: datetime