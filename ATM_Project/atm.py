
class ATMError(Exception):
    pass

class PositiveError(ATMError):
    pass

class InvalidCardError(ATMError):
    pass

class IncorrectPINError(ATMError):
    pass

class AccountNotFoundError(ATMError):
    pass

class NoCardInsertedError(ATMError):
    pass

class AccountNotSelectedError(ATMError):
    pass

class InsufficientFundsError(ATMError):
    pass


class Account:
    def __init__(self, account_id, balance = 0):
        self.account_id = account_id
        self.balance = balance
    
    def deposit(self, amount):
        if amount <= 0:
            raise PositiveError("Deposit amount must be positive")
        self.balance += amount
    
    def withdraw(self, amount):
        if amount > self.balance:
            raise InsufficientFundsError("Insufficient funds")
        if amount <= 0:
            raise PositiveError("Withdraw amount must be positive")

        self.balance -= amount
    
    def get_balance(self):
        return self.balance

class Bank:
    def __init__(self):
        self.cards = {}
    
    def add_card(self, card_id, pin, accounts):
        self.cards[card_id] = {"pin": pin, "accounts": accounts}
    
    def verify_pin(self, card_id, input_pin):
        return self.cards.get(card_id, {}).get("pin")==input_pin
    
    def get_accounts(self, card_id):
        if card_id not in self.cards:
            raise NoCardInsertedError("Insert card first")
        return self.cards[card_id]["accounts"]

class ATMController:
    def __init__(self, bank):
        self.bank = bank
        self.current_card = None
        self.current_account = None

    def insert_card(self, card_id):
        if card_id not in self.bank.cards:
            raise InvalidCardError("Invalid card")
        self.current_card = card_id
    
    def enter_pin(self, pin):
        if self.current_card is None:
            raise NoCardInsertedError("Insert card first")
        if not self.bank.verify_pin(self.current_card, pin):
            raise IncorrectPINError("Incorrect PIN")

    def select_account(self, account_id):
        if self.current_card is None:
            raise NoCardInsertedError("Insert card and verify PIN first")
        accounts = self.bank.get_accounts(self.current_card)
        for account in accounts:
            if account.account_id == account_id:
                self.current_account = account
                return
        raise AccountNotFoundError("Account not found")

    def check_balance(self):
        if self.current_account is None:
            raise AccountNotSelectedError("Select account first")
        return self.current_account.get_balance()

    def deposit(self, amount):
        if self.current_account is None:
            raise AccountNotSelectedError("Select account first")
        self.current_account.deposit(amount)

    def withdraw(self, amount):
        if self.current_account is None:
            raise AccountNotSelectedError("Select account first")
        self.current_account.withdraw(amount)