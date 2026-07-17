# Exercise 1

def classify_transaction(amount):
    if 0 < amount <= 100:
        return "MICRO"
    elif 100 < amount <= 1000:
        return "SMALL"
    elif 1000 < amount <= 10000:
        return "STANDARD"
    elif amount > 10000:
        return "LARGE"
    else:
        return "INVALID"


print(classify_transaction(50))
print(classify_transaction(9999))
print(classify_transaction(-5))


# Exercise 2

def get_interest_rate(credit_score):
    if credit_score >= 750:
        return 7.5
    elif credit_score >= 700:
        return 9.5
    elif credit_score >= 650:
        return 12.0
    else:
        return 18.5


print(get_interest_rate(720))
print(get_interest_rate(800))


# Exercise 3

def atm_withdraw(balance, amount):
    if amount <= 0:
        return (False, "Invalid amount")
    elif amount > 5000:
        return (False, "ATM daily limit is R5 000")
    elif amount > balance:
        return (False, "Insufficient funds")
    else:
        return (True, f"Dispensing R{amount:.2f}")


print(atm_withdraw(3000, 1500))
print(atm_withdraw(500, 600))


# Exercise 4

def tag_transaction(tx_type, merchant_category, amount):
    if tx_type == "REFUND":
        return "REFUND"
    elif merchant_category == "GAMBLING":
        return "HIGH_RISK"
    elif merchant_category == "GROCERY" and amount < 500:
        return "ROUTINE"
    elif amount > 10000:
        return "LARGE_PURCHASE"
    else:
        return "STANDARD"


print(tag_transaction("REFUND", "GROCERY", 100))
print(tag_transaction("PURCHASE", "GAMBLING", 200))
print(tag_transaction("PURCHASE", "GROCERY", 300))
print(tag_transaction("PURCHASE", "TRAVEL", 20000))
print(tag_transaction("PURCHASE", "TRAVEL", 1000))