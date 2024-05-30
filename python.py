class User:
    def _init_(self, user_id, pin):
        self.user_id = user_id
        self.pin = pin
        self.accounts = []

    def verify_pin(self, pin):
        return self.pin == pin

    def add_account(self, account):
        self.accounts.append(account)

    def get_account(self, account_number):
        for account in self.accounts:
            if account.account_number == account_number:
                return account
        return None


class Account:
    def _init_(self, account_number, initial_balance=0):
        self.account_number = account_number
        self.balance = initial_balance
        self.transactions = []

    def deposit(self, amount):
        self.balance += amount
        self.transactions.append(f"Deposited: ${amount}")
        return self.balance

    def withdraw(self, amount):
        if self.balance >= amount:
            self.balance -= amount
            self.transactions.append(f"Withdrew: ${amount}")
            return self.balance
        else:
            raise ValueError("Insufficient funds")

    def transfer(self, amount, target_account):
        self.withdraw(amount)
        target_account.deposit(amount)
        self.transactions.append(f"Transferred: ${amount} to account {target_account.account_number}")
        return self.balance

    def get_transaction_history(self):
        return self.transactions


class ATM:
    def _init_(self, bank):
        self.bank = bank
        self.current_user = None
        self.current_account = None

    def authenticate_user(self, user_id, pin):
        user = self.bank.get_user(user_id)
        if user and user.verify_pin(pin):
            self.current_user = user
            return True
        return False

    def select_account(self, account_number):
        account = self.current_user.get_account(account_number)
        if account:
            self.current_account = account
            return True
        return False

    def show_transaction_history(self):
        if self.current_account:
            for transaction in self.current_account.get_transaction_history():
                print(transaction)

    def deposit(self, amount):
        if self.current_account:
            self.current_account.deposit(amount)

    def withdraw(self, amount):
        if self.current_account:
            self.current_account.withdraw(amount)

    def transfer(self, amount, target_account_number):
        if self.current_account:
            target_account = self.bank.get_account(target_account_number)
            if target_account:
                self.current_account.transfer(amount, target_account)

    def quit(self):
        self.current_user = None
        self.current_account = None


class Bank:
    def _init_(self):
        self.users = {}

    def add_user(self, user):
        self.users[user.user_id] = user

    def get_user(self, user_id):
        return self.users.get(user_id)

    def get_account(self, account_number):
        for user in self.users.values():
            account = user.get_account(account_number)
            if account:
                return account
        return None


# Example usage
def main():
    bank = Bank()

    # Adding a user and accounts
    user1 = User('user1', '1234')
    account1 = Account('acc1', 500)
    account2 = Account('acc2', 1000)
    user1.add_account(account1)
    user1.add_account(account2)
    bank.add_user(user1)

    atm = ATM(bank)

    # ATM operations
    if atm.authenticate_user('user1', '1234'):
        print("User authenticated")

        if atm.select_account('acc1'):
            print("Account selected")

            atm.deposit(200)
            atm.withdraw(100)
            atm.transfer(50, 'acc2')

            atm.show_transaction_history()
            atm.quit()
        else:
            print("Account selection failed")
    else:
        print("Authentication failed")


if _name_ == "_main_":
    main()