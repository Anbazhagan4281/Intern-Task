from abc import ABC, abstractmethod

class BankAccount(ABC):
    
    bank_name = "ABC Bank"  
    
    def __init__(self, name, balance):
        self.name = name             
        self.__balance = balance     

    def get_balance(self):
        return self.__balance

    def set_balance(self, amount):
        self.__balance = amount

    @abstractmethod
    def transaction(self):
        pass

    def __str__(self):
        return f"Account Holder: {self.name}"

    @classmethod
    def bank_info(cls):
        print("Welcome to", cls.bank_name)

    @staticmethod
    def greet():
        print("Thank you for using our ATM")


class SavingsAccount(BankAccount):

    def transaction(self):
        print("Savings Account Transaction")

    def deposit(self, amount):
        balance = self.get_balance()
        balance += amount
        self.set_balance(balance)
        print("Deposited:", amount)

    def withdraw(self, amount):
        balance = self.get_balance()
        if amount > balance:
            print("Insufficient balance da")
        else:
            balance -= amount
            self.set_balance(balance)
            print("Withdrawn:", amount)

acc1 = SavingsAccount("Aishu", 1000)

print(acc1)

SavingsAccount.bank_info()

SavingsAccount.greet()

acc1.transaction()

acc1.deposit(500)
acc1.withdraw(300)

print("Current Balance:", acc1.get_balance())