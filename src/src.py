from config import *



### GUI ###

# FRAMES
frame_top = Frame(WINDOW, width=WIN_W, height=int(WIN_H*(1/3)))
frame_top.config(borderwidth=5, relief="raised")
frame_top.pack(side=TOP)
frame_top.pack_propagate(0)

frame_buttons = Frame(WINDOW, width=WIN_W, height=50)
frame_buttons.pack(side=TOP)

frame_budgets = Frame(WINDOW, width=WIN_W, height=int(WIN_H*(2/3)-50), borderwidth=1, relief=SUNKEN)
frame_budgets.pack(side=BOTTOM, fill=BOTH)
frame_budgets.pack_propagate(0)



# BUTTONS
button_deposit = Button(frame_buttons, text="Deposit", font=(FONT, 16), bg="lightgray", padx=20, pady=5,
                        command=lambda: openTransactionWindow(deposit=True, withdraw=False))
button_deposit.pack(side=LEFT, padx=20, pady=5)
button_withdraw = Button(frame_buttons, text="Withdraw", font=(FONT, 16), bg="lightgray", padx=20, pady=5,
                        command=lambda: openTransactionWindow(deposit=False, withdraw=True))
button_withdraw.pack(side=LEFT, padx=20, pady=5)
button_new_budget = Button(frame_buttons, text="New Budget", font=(FONT, 16), bg="lightgray", padx=20, pady=5,
                        command=lambda: openNewBudgetWindow())
button_new_budget.pack(side=LEFT, padx=20, pady=5)



# LABELS
label_account = Label(frame_top, text=ACCOUNT.getOwner()+"'s Account Balance", borderwidth=0, font=(FONT, 16))
label_account.place(relx=0.5, rely=0.3, anchor="center")

label_balance = Label(frame_top, text=str(ACCOUNT.getBalance()), borderwidth=0, font=(FONT, 36))
label_balance.place(relx=0.5, rely=0.6, anchor="center")

label_budgets = Label(frame_budgets, text="Budgets", borderwidth=0, font=(FONT, 16))
label_budgets.pack(side=TOP, pady=10)

i=0
for name, amount in ACCOUNT.budgets.items():
   ACCOUNT.budgetLabels[i] = Label(frame_budgets, text=name+": "+"%.2f"%float(amount), borderwidth=0, font=(FONT, 20))
   i += 1
for name, label in ACCOUNT.budgetLabels.items():
    ACCOUNT.budgetLabels[name].pack(side=TOP, pady=10)





### FUNCTIONS ###

def openTransactionWindow(deposit=False, withdraw=False):
    def check_input(*args):
        """ Check for and enforce valid inputs """
        value = user_input.get()
        if len(value) > 0:
            if len(value) > 4: user_input.set(value[:4])
            if value[-1].isalpha(): user_input.set(value[0:len(value)-1])

    def update_balance(amount, budget, *args):
        """ Update budget amount and/or existing balance """
        if float(amount) < 0: amount = 0
        if deposit:
            ACCOUNT.deposit(float(amount), budget)
        if withdraw:
            ACCOUNT.withdraw(float(amount), budget)
        update_labels(budget)
        newWindow.grab_release()
        newWindow.destroy()

    def update_labels(budget, *args):
        """ Update labels for balance and/or budget amounts """
        label_balance['text'] = ACCOUNT.getBalance()
        if float(ACCOUNT.getBalance()) < 0.00:
            label_balance['fg'] = "red"
        else:
            label_balance['fg'] = "black"
        if budget != "Total Balance":
            ACCOUNT.budgetLabels[budget]['text'] = budget + ": " + "%.2f" % float(ACCOUNT.getBudgetBalance(budget))

    assert not(deposit==True and withdraw == True), "Deposit and withdraw cannot both be true"
    assert not(deposit==False and withdraw==False), "Deposit and withdraw cannot both be false"

    newWindow = Toplevel(WINDOW)
    newWindow.title("Deposit")
    newWindow.geometry("+{}+{}".format(int(SCREEN_W/2 - newWindow.winfo_reqwidth()/2), int(SCREEN_H/2+85)))
    newWindow.grab_set()

    frame = Frame(newWindow)
    frame.pack()

    if deposit:
        label_deposit = Label(frame, text="Deposit Amount", borderwidth=0, font=(FONT, 10))
        label_deposit.pack(padx=50, pady=(10, 5))
    if withdraw:
        label_withdraw = Label(frame, text="Withdraw Amount", borderwidth=0, font=(FONT, 10))
        label_withdraw.pack(padx=50, pady=(10, 5))

    user_input = StringVar(frame, value="0.00")
    user_input.trace('w', check_input)
    entry_box = Entry(frame, textvariable=user_input)
    entry_box.pack(pady=(0, 10))

    label_where = Label(frame, borderwidth=0, font=(FONT, 10))
    if deposit:
        label_where['text'] = "Deposit To"
    if withdraw:
        label_where['text'] = "Withdraw From"
    label_where.pack(padx=50, pady=(10, 5))

    dropdown_options = ["Total Balance"]
    for b in list(ACCOUNT.budgets.keys()): dropdown_options.append(b)
    dropdown_chosen = StringVar()
    dropdown_chosen.set(dropdown_options[0])
    dropdown_menu = OptionMenu(frame, dropdown_chosen, *dropdown_options)
    dropdown_menu.pack(pady=(0, 10))

    button_enter = Button(frame, text="Enter", font=(FONT, 8), bg="lightgray", padx=10, pady=5,
                          command=lambda: update_balance(entry_box.get(), dropdown_chosen.get()))
    button_enter.pack(side=BOTTOM, pady=(10, 10))



def openNewBudgetWindow():
    def check_amount(*args):
        """ Check for and enforce valid inputs """
        value = user_input_amount.get()
        if len(value) > 0:
            if value[-1].isalpha(): user_input_amount.set(value[0:len(value) - 1])
            if len(value) > 4:
                if value[-4] == ".": user_input_amount.set(value[:len(value) - 1])

    def add_budget(name, amount, *args):
        """ Create new budget """
        assert name not in ACCOUNT.budgets, "Budget already exists"
        ACCOUNT.budgets[name] = float("%.2f" % float(amount))
        ACCOUNT.budgetLabels[name] = Label(frame_budgets, text=name+": "+"%.2f"%float(amount),
                                                                borderwidth=0, font=(FONT, 20))
        ACCOUNT.budgetLabels[name].pack(side=TOP, pady=10)
        newWindow.grab_release()
        newWindow.destroy()

    newWindow = Toplevel(WINDOW)
    newWindow.title("New Budget")
    newWindow.geometry("+{}+{}".format(int(SCREEN_W / 2 - newWindow.winfo_reqwidth() / 2), int(SCREEN_H / 2 + 85)))
    newWindow.grab_set()

    frame = Frame(newWindow)
    frame.pack()

    label_name = Label(frame, text="Budget Name", borderwidth=0, font=(FONT, 10))
    label_name.pack(padx=50, pady=(10, 5))

    user_input_name = StringVar(frame, value="Name")
    entry_box_name = Entry(frame, textvariable=user_input_name)
    entry_box_name.pack(pady=(0, 10))

    label_name = Label(frame, text="Budget Amount", borderwidth=0, font=(FONT, 10))
    label_name.pack(padx=50, pady=(10, 5))

    user_input_amount = StringVar(frame, value="0.00")
    user_input_amount.trace('w', check_amount)
    entry_box_amount = Entry(frame, textvariable=user_input_amount)
    entry_box_amount.pack()

    button_enter = Button(frame, text="Enter", font=(FONT, 8), bg="lightgray", padx=10, pady=5,
                          command=lambda: add_budget(entry_box_name.get(), entry_box_amount.get()))
    button_enter.pack(side=BOTTOM, pady=10)