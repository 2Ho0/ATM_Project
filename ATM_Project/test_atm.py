# test_atm.py

from atm import (
    Bank, Account, ATMController,
    InvalidCardError, IncorrectPINError,
    AccountNotFoundError, NoCardInsertedError,
    AccountNotSelectedError, InsufficientFundsError
)

def run_tests():

    # Test basic flow
    bank = Bank()
    account = Account("a1", 100)
    bank.add_card("card1", "1111", [account])
    atm = ATMController(bank)

    atm.insert_card("card1")
    atm.enter_pin("1111")
    atm.select_account("a1")

    assert atm.check_balance() == 100

    atm.deposit(50)
    assert atm.check_balance() == 150

    atm.withdraw(70)
    assert atm.check_balance() == 80

    # Test invalid card

    try:
        ATMController(bank).insert_card("invalid_card")
    except InvalidCardError:
        pass
    else:
        assert False, "InvalidCardError not raised"

    # Test incorrect pin
    atm = ATMController(bank)
    atm.insert_card("card1")
    try:
        atm.enter_pin("9999")
    except IncorrectPINError:
        pass
    else:
        assert False, "IncorrectPINError not raised"

    # Test account not found
    atm = ATMController(bank)
    atm.insert_card("card1")
    atm.enter_pin("1111")
    try:
        atm.select_account("invalid_account")
    except AccountNotFoundError:
        pass
    else:
        assert False, "AccountNotFoundError not raised"

    # Test account not selected before withdraw
    atm = ATMController(bank)
    atm.insert_card("card1")
    atm.enter_pin("1111")
    try:
        atm.withdraw(10)
    except AccountNotSelectedError:
        pass
    else:
        assert False, "AccountNotSelectedError not raised"
    
    # Test account not selected before deposit
    atm = ATMController(bank)
    atm.insert_card("card1")
    atm.enter_pin("1111")
    try:
        atm.deposit(10)
    except AccountNotSelectedError:
        pass
    else:
        assert False, "AccountNotSelectedError not raised"

    # Test insufficient funds
    atm = ATMController(bank)
    atm.insert_card("card1")
    atm.enter_pin("1111")
    atm.select_account("a1")

    try:
        atm.withdraw(999)
    except InsufficientFundsError:
        pass
    else:
        assert False, "InsufficientFundsError not raised"

    # Test check balance before selecting account
    atm = ATMController(bank)
    atm.insert_card("card1")
    atm.enter_pin("1111")
    try:
        atm.check_balance()
    except AccountNotSelectedError:
        pass
    else:
        assert False, "AccountNotSelectedError not raised"

    # Test PIN verification state
    atm = ATMController(bank)
    atm.insert_card("card1")
    
    try:
        atm.select_account("a1")
    except NoCardInsertedError:
        pass
    else:
        assert False, "NoCardInsertedError not raised when PIN not verified"
    
    atm.enter_pin("1111")
    atm.select_account("a1")
    
    # Test eject card functionality
    atm2 = ATMController(bank)
    atm2.insert_card("card1")
    atm2.enter_pin("1111")
    atm2.select_account("a1")
    
    assert atm2.current_card == "card1"
    assert atm2.current_account is not None
    assert atm2.pin_verified == True
    
    atm2.eject_card()
    
    assert atm2.current_card is None
    assert atm2.current_account is None
    assert atm2.pin_verified == False
    
    # Test operations fail after ejecting card
    try:
        atm2.check_balance()
    except AccountNotSelectedError:
        pass
    else:
        assert False, "AccountNotSelectedError not raised after ejecting card"
    
    try:
        atm2.withdraw(10)
    except AccountNotSelectedError:
        pass
    else:
        assert False, "AccountNotSelectedError not raised after ejecting card"
    
    try:
        atm2.deposit(10)
    except AccountNotSelectedError:
        pass
    else:
        assert False, "AccountNotSelectedError not raised after ejecting card"
    
    # Test PIN entry fails after ejecting card
    try:
        atm2.enter_pin("1111")
    except NoCardInsertedError:
        pass
    else:
        assert False, "NoCardInsertedError not raised after ejecting card"

    print("All tests passed")

if __name__ == "__main__":
    run_tests()