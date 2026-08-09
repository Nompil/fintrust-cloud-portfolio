Diagram: FinTrust ER (Week 1)

Suggested filename: fintrust_er.drawio (export to PNG as fintrust_er.drawio.png)

Purpose:
- Show core entities: `customers`, `accounts`, `transactions` and key relationships.
- Mark primary keys and foreign keys, sample columns used in SQL examples.

Layers / elements to include:
- Customers (customer_id PK, name, email)
- Accounts (account_id PK, customer_id FK, account_type, balance)
- Transactions (transaction_id PK, account_id FK, amount, timestamp, merchant_category)

Notes:
- Export to `week01/diagrams/fintrust_er.drawio.png` and reference from `week01/README.md` and `db-architecture-diagram.md`.
