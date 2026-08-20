-- Author: Nompilo Eugenia Mchunu
-- Week 6 analytics practice data for PostgreSQL 15 or later

DROP TABLE IF EXISTS transactions;
DROP TABLE IF EXISTS customers;

CREATE TABLE customers (
    customer_id INTEGER PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    province VARCHAR(50) NOT NULL
);

CREATE TABLE transactions (
    transaction_id BIGSERIAL PRIMARY KEY,
    customer_id INTEGER NOT NULL REFERENCES customers(customer_id),
    branch_code VARCHAR(10) NOT NULL,
    amount NUMERIC(15, 2) NOT NULL CHECK (amount > 0),
    transaction_date TIMESTAMP NOT NULL,
    is_suspicious BOOLEAN NOT NULL DEFAULT FALSE
);

INSERT INTO customers (customer_id, first_name, last_name, province) VALUES
    (1, 'Thabo', 'Nkosi', 'Gauteng'),
    (2, 'Amahle', 'Dlamini', 'KwaZulu-Natal'),
    (3, 'Sipho', 'Mokoena', 'Gauteng'),
    (4, 'Lerato', 'Sithole', 'Western Cape'),
    (5, 'Nomvula', 'Dube', 'Eastern Cape'),
    (6, 'Zanele', 'Khumalo', 'Western Cape'),
    (7, 'Bongani', 'Zulu', 'Eastern Cape'),
    (8, 'Fatima', 'Moosa', 'Gauteng'),
    (9, 'Nomsa', 'Ndlovu', 'Mpumalanga'),
    (10, 'Ayesha', 'Petersen', 'Western Cape'),
    (11, 'Kagiso', 'Molefe', 'Gauteng'),
    (12, 'Naledi', 'Maseko', 'Limpopo'),
    (13, 'Sibusiso', 'Nkomo', 'KwaZulu-Natal'),
    (14, 'Palesa', 'Mokoena', 'Free State'),
    (15, 'Kabelo', 'Sithole', 'North West'),
    (16, 'Ayanda', 'Dube', 'Eastern Cape'),
    (17, 'Lethabo', 'Khumalo', 'Gauteng'),
    (18, 'Themba', 'Zulu', 'KwaZulu-Natal'),
    (19, 'Karabo', 'Ndlovu', 'Northern Cape'),
    (20, 'Refilwe', 'Moosa', 'Gauteng');

INSERT INTO transactions (
    customer_id,
    branch_code,
    amount,
    transaction_date,
    is_suspicious
)
SELECT
    c.customer_id,
    CASE MOD(c.customer_id, 4)
        WHEN 0 THEN 'CPT01'
        WHEN 1 THEN 'JHB01'
        WHEN 2 THEN 'DBN01'
        ELSE 'PTA01'
    END,
    ROUND(
        (500::NUMERIC + c.customer_id * 123 + month_number * 77 + item_number * 41)
        * CASE
            WHEN month_number = 4 AND MOD(c.customer_id, 4) = 0 THEN 4
            ELSE 1
        END,
        2
    ),
    MAKE_TIMESTAMP(
        2024,
        month_number,
        LEAST(5 + item_number * 6 + MOD(c.customer_id, 10), 28),
        9 + item_number,
        0,
        0
    ),
    MOD(c.customer_id + month_number + item_number, 5) = 0
FROM customers AS c
CROSS JOIN GENERATE_SERIES(1, 6) AS month_number
CROSS JOIN GENERATE_SERIES(1, 2) AS item_number;

CREATE INDEX idx_transactions_customer_date
    ON transactions (customer_id, transaction_date);

CREATE INDEX idx_transactions_branch_date
    ON transactions (branch_code, transaction_date);
