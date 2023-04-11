def add(num1: int, num2: int):
    return num1 + num2

def subtract(num1: int, num2: int):
    return num1 - num2

class BankAccount():
    def __init__(self, initial_bal = 0):
        self.balance = initial_bal

    def deposit(self, amt):
        self.balance += amt

    def withdraw(self, amt):
        if amt > self.balance:
            raise Exception("Insufficient funds")
        self.balance -= amt    