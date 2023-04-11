from app.calculate import add, subtract, BankAccount
import pytest

@pytest.fixture
def bank_account():
    return BankAccount(50)

@pytest.mark.parametrize("x, y, sum",[
    (3,2,5),
    (4,6,10),
    (12,4,16)
])
def test_add(x, y, sum):
    assert add(x,y) == sum

def test_subtract():
    assert subtract(5,3) == 2

def test_deposit(bank_account):
    bank_account.deposit(30)
    assert bank_account.balance == 80

def test_withdraw(bank_account):
    bank_account.withdraw(30)
    assert bank_account.balance == 20    

@pytest.mark.parametrize("deposited, withdrew, expected",[
    (30,20,60),
    (100,50,100)
])
def test_bank_transaction(bank_account, deposited, withdrew, expected):
    bank_account.deposit(deposited)
    bank_account.withdraw(withdrew)
    assert bank_account.balance == expected  