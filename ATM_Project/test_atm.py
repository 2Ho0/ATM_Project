# test_atm.py

from atm import Bank, Account, ATMController

def test_basic_flow():
    bank = Bank()
    account = Account("acc123", 100)
    bank.add_card("card1", "1234", [account])
    atm = ATMController(bank)

    atm.insert_card("card1")
    atm.enter_pin("1234")
    atm.select_account("acc123")

    assert atm.check_balance() == 100

    atm.deposit(50)
    assert atm.check_balance() == 150

    atm.withdraw(70)
    assert atm.check_balance() == 80
    print("Test basic flow passed")

def test_incorrect_pin():
    bank = Bank()
    account = Account("acc1", 100)
    bank.add_card("card2", "9999", [account])
    atm = ATMController(bank)

    atm.insert_card("card2")
    try:
        atm.enter_pin("0000")
    except ValueError as e:
        assert str(e) == "Incorrect PIN"
    print("Test incorrect pin passed")

def test_withdraw_too_much():
    bank = Bank()
    account = Account("acc2", 50)
    bank.add_card("card3", "1111", [account])
    atm = ATMController(bank)

    atm.insert_card("card3")
    atm.enter_pin("1111")
    atm.select_account("acc2")

    try:
        atm.withdraw(100)
    except ValueError as e:
        assert str(e) == "Insufficient funds"

    print("Test withdraw too much passed")


test_basic_flow()
test_incorrect_pin()
test_withdraw_too_much()