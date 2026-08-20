-- Week 1 Day 3 stretch challenge: add physical branches
-- Run after day3_fintrust_schema.sql.

USE fintrust_db;

CREATE TABLE branches (
    branch_id INT PRIMARY KEY AUTO_INCREMENT,
    branch_name VARCHAR(150) UNIQUE NOT NULL,
    province VARCHAR(50) NOT NULL,
    city VARCHAR(100) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
) ENGINE = InnoDB;

ALTER TABLE accounts
    ADD COLUMN branch_id INT NULL,
    ADD CONSTRAINT fk_accounts_branch
        FOREIGN KEY (branch_id) REFERENCES branches(branch_id);

INSERT INTO branches (branch_name, province, city)
VALUES
    ('Johannesburg Central', 'Gauteng', 'Johannesburg'),
    ('Cape Town CBD', 'Western Cape', 'Cape Town'),
    ('Durban Central', 'KwaZulu-Natal', 'Durban');

-- Online-opened accounts keep branch_id as NULL.
UPDATE accounts SET branch_id = 1 WHERE account_id = 1;
UPDATE accounts SET branch_id = 2 WHERE account_id = 5;

SELECT
    a.account_number,
    a.account_type,
    b.branch_name,
    b.city
FROM accounts AS a
LEFT JOIN branches AS b
    ON a.branch_id = b.branch_id
ORDER BY a.account_id;
