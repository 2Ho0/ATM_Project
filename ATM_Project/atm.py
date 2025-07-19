class Account:
    def __init__(self, account_id, balance = 0):
        self.account_id = account_id
        self.balance = balance
    
    def deposit(self, amount):
        if amount <= 0:
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

class Bank:
    def __init__(self):
        self.cards = {}
    
    def add_card(self, card_id, pin, accounts):
        self.cards[card_id] = {"pin": pin, "accounts": accounts}
    
    def verify_card(self, card_id, input_pin):
        return self.cards.get(card_id, {}).get("pin")==input_pin
    
    def get_accounts(self, card_id):
        if card_id not in self.cards:
            raise ValueError("Card not found")
        return self.cards[card_id]["accounts"]