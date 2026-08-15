# 🏦 BankFlow AI

End-to-end banking data engineering project that simulates a
realistic banking environment and prepares data for downstream
analytics.

## 🚀 Project Status

Version: 1.0

Current stage:

FastAPI → Banking Simulation → Scheduler → JSON

Upcoming:

FastAPI → MinIO → Databricks → Power BI

---

## 🏗️ Current Architecture

```text
                    FastAPI
                       │
                       ▼
               Master Data Generator
                       │
          ┌────────────┼────────────┐
          ▼            ▼            ▼
      Customers     Accounts     Merchants
          │            │            │
          └────────────┼────────────┘
                       │
                       ▼
             Transaction Generator
                       │
                       ▼
                Banking Rules
                       │
             ┌─────────┴─────────┐
             ▼                   ▼
       Balance Update       Fraud Detection
             │                   │
             └─────────┬─────────┘
                       ▼
                    Scheduler
                       │
                       ▼
                   JSON Files
```
