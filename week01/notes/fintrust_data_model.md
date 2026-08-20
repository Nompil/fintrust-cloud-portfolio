# FinTrust Data Model

The Week 1 Day 3 schema has three core entities: customers, accounts, and transactions.

| Entity | Primary key | Important fields | Relationship |
| --- | --- | --- | --- |
| `customers` | `customer_id` | name, email, province, created timestamp | One customer can own many accounts |
| `accounts` | `account_id` | `customer_id`, type, account number, balance | Each account belongs to one customer and can have many transactions |
| `transactions` | `transaction_id` | `account_id`, type, amount, merchant category, date | Each transaction belongs to one account |

## Design decisions

- Integer auto-increment keys provide stable row identifiers for the lab.
- Foreign keys enforce the customer-to-account and account-to-transaction relationships.
- `DECIMAL(15,2)` stores currency without the binary rounding behaviour of `FLOAT`.
- `ENUM` limits account and transaction types to the values accepted by the exercise.
- Unique email addresses and account numbers prevent accidental duplicates.
- `DATETIME DEFAULT CURRENT_TIMESTAMP` records creation or transaction time when no explicit value is supplied.
- InnoDB is specified so MySQL enforces foreign keys.

The optional branches challenge adds a nullable `branch_id` to `accounts`. A null value represents an account opened online rather than at a physical branch.
