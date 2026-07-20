-- Create and select database

CREATE DATABASE IF NOT EXISTS fintrust_db;

USE fintrust_db;

-- ============================================
-- TABLE 1: customers
-- ============================================

CREATE TABLE customers (
    customer_id INT PRIMARY KEY AUTO_INCREMENT,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email VARCHAR(200) UNIQUE NOT NULL,
    province VARCHAR(50),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- ============================================
-- TABLE 2: accounts
-- ============================================

CREATE TABLE accounts (
    account_id INT PRIMARY KEY AUTO_INCREMENT,
    customer_id INT NOT NULL,
    account_type ENUM(
        'CHEQUE',
        'SAVINGS',
        'CREDIT',
        'BUSINESS'
    ) NOT NULL,
    account_number VARCHAR(20) UNIQUE NOT NULL,
    balance DECIMAL(15,2) DEFAULT 0.00,
    FOREIGN KEY (customer_id)
        REFERENCES customers(customer_id)
);

-- ============================================
-- TABLE 3: transactions
-- ============================================

CREATE TABLE transactions (
    transaction_id INT PRIMARY KEY AUTO_INCREMENT,
    account_id INT NOT NULL,
    transaction_type ENUM(
        'DEBIT',
        'CREDIT',
        'PAYMENT'
    ) NOT NULL,
    amount DECIMAL(15,2) NOT NULL,
    merchant_category VARCHAR(100),
    transaction_date DATETIME
        DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (account_id)
        REFERENCES accounts(account_id)
);

-- ============================================
-- Insert Customers
-- ============================================

INSERT INTO customers
(first_name, last_name, email, province)
VALUES
('Thabo', 'Nkosi', 'thabo.nkosi@gmail.com', 'Gauteng'),
('Amahle', 'Dlamini', 'amahle.dlamini@outlook.com', 'KwaZulu-Natal'),
('Sipho', 'Mokoena', 'sipho.m@fintrust.co.za', 'Gauteng'),
('Zanele', 'Khumalo', 'zanele.k@gmail.com', 'Western Cape'),
('Bongani', 'Zulu', 'b.zulu@webmail.co.za', 'Eastern Cape');

-- ============================================
-- Insert Accounts
-- ============================================

INSERT INTO accounts
(customer_id, account_type,
 account_number, balance)
VALUES
(1, 'CHEQUE', 'FT-CHQ-000001', 15250.00),
(1, 'SAVINGS', 'FT-SAV-000001', 42000.75),
(2, 'CHEQUE', 'FT-CHQ-000002', 8900.50),
(3, 'BUSINESS', 'FT-BUS-000001', 120000.00),
(4, 'SAVINGS', 'FT-SAV-000002', 3250.25);

-- ============================================
-- Insert Transactions
-- ============================================

INSERT INTO transactions
(account_id, transaction_type,
 amount, merchant_category)
VALUES
(1, 'DEBIT', 250.00, 'Groceries'),
(1, 'DEBIT', 1500.00, 'Electronics'),
(2, 'CREDIT', 5000.00, 'Salary'),
(3, 'DEBIT', 89.99, 'Fuel'),
(4, 'PAYMENT', 350.00, 'Utilities');

-- ============================================
-- Verification Queries
-- ============================================

SELECT * FROM customers;

SELECT * FROM accounts;

SELECT * FROM transactions;

SELECT 'customers' AS table_name,
       COUNT(*) AS row_count
FROM customers

UNION ALL

SELECT 'accounts',
       COUNT(*)
FROM accounts

UNION ALL

SELECT 'transactions',
       COUNT(*)
FROM transactions;


