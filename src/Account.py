class Account:
    """ Container class for account information and functionality """
    def __init__(self, name, startAmount=0.00):
        assert type(name) == str, "Name must be a string"
        startAmount = "{:.2f}".format(startAmount)
        self.owner = name
        self.balance = float(startAmount)
        self.budgets = {}
        self.budgetLabels = {}

    def getOwner(self):
        """ Returns account owner's name """
        return self.owner

    def getBalance(self):
        """ Returns account balance """
        return "%.2f" % float(self.balance)

    def getBudgetBalance(self, budgetName):
        """ Returns balance of specified budget """
        assert budgetName in self.budgets, "Specified budget doesn't exist"
        return "%.2f" % float(self.budgets[budgetName])

    def deposit(self, amount, budget):
        """ Adds amount to existing budget and/or balance """
        if budget != "Total Balance":
            assert budget in self.budgets, "Specified budget doesn't exist"
            self.budgets[budget] += float(amount)
        self.balance += float(amount)

    def withdraw(self, amount, budget):
        """ Subtracts amount from existing budget and/or balance """
        if budget != "Total Balance":
            assert budget in self.budgets, "Specified budget doesn't exist"
            self.budgets[budget] -= float(amount)
        self.balance -= float(amount)