class Account:
    def __init__(self, account_id, balance = 0):
        self.account_id = account_id
        self.balance = balance
    
    def deposit(self, amount):
        if amount > 0:
            raise ValueError("Deposit amount must be positive")
        self.balance += amount
    
    def withdraw(self, amount):
        if amount > self.balance:
            raise ValueError("Insufficient Funds")
        if amount <= 0:
            raise ValueError("Withdraw amount must be positive")

        self.balance -= amount
    
    def get_balance(self):
        return self.balance
