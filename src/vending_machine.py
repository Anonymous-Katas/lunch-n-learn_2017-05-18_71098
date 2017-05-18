__author__ = 'David Carroll'

# size = mm diameter
# weight = g
quarter = {'weight': 5.6, 'size': 24.2, 'value': 0.25}
dime = {'weight': 2.2, 'size': 17.9, 'value': 0.10}
nickel = {'weight': 5, 'size': 21.2, 'value': 0.05}
penny = {'weight': 2.5, 'size': 19, 'value': 0.01}


class VendingMachine:

    current_amount = 0
    coin_return = []
    coins_customer_has_inserted_during_this_transaction = []
    change_due = 0
    display = "INSERT COIN"
    price = 0
    balance = 0
    selected_product = None
    dispensed_product = None
    cola_quantity = 5
    chips_quantity = 5
    candy_quantity = 5
    quarter_quantity = 8
    dime_quantity = 8
    nickel_quantity = 8
    # used in test suite to indicate that we only want printouts and breakpoints on data
    # from the specified test.
    print_and_break_on_this_test = False

    def vending_machine_reset(self):
        self.current_amount = 0
        self.coin_return = []
        self.display = "INSERT COIN"
        self.price = 0
        self.balance = 0
        self.selected_product = None
        self.dispensed_product = None
        self.cola_quantity = 5
        self.chips_quantity = 5
        self.candy_quantity = 5
        self.quarter_quantity = 8
        self.dime_quantity = 8
        self.nickel_quantity = 8
        self.print_and_break_on_this_test = False
        self.coins_customer_has_inserted_during_this_transaction = []

    def new_transaction(self):
        self.current_amount = 0
        self.coin_return = []
        need_exact_change= self.check_change_making_ability()
        if need_exact_change == False:
            self.display = "INSERT COIN"
        self.price = 0
        self.balance = 0
        self.selected_product = None
        self.dispensed_product = None
        self.coins_customer_has_inserted_during_this_transaction = []

    def check_change_making_ability(self):
        """
        The most change that can be required is 0.20
        However, because the machine can always return any coin above the price of the item,
        the total change needed will only ever be .10, or .05, plus the excess coins the user entered.
        For this reason all change can be handled with either a single nickle or a single time.
        Per the recs doc, we are setting the display to "EXACT CHANGE ONLY" if any of those 2
        conditions cannot be met.
        """
        need_exact_change = False
        # cannot make change for any purchase
        if self.dime_quantity < 1 or self.nickel_quantity < 1:
            self.display = "EXACT CHANGE ONLY"
            need_exact_change = True
        return need_exact_change

    def accept_coins(self, coin):
        coin_type = self.is_valid_coin(coin)
        if coin_type:
            self.add_coin_value_to_current_amount(coin_type)
        else:
            self.coin_return.append(coin)
        return coin

    def is_valid_coin(self, coin):
        coin_type = None
        # quarter
        if coin['weight'] == quarter['weight'] and coin['size'] == quarter['size']:
            coin_type = quarter
        # dime
        elif coin['weight'] == dime['weight'] and coin['size'] == dime['size']:
            coin_type = dime
        # nickel
        elif coin['weight'] == nickel['weight'] and coin['size'] == nickel['size']:
            coin_type = nickel
        return coin_type

    def add_coin_value_to_current_amount(self, coin_type):
        self._check_for_new_transaction()
        # quarter
        if coin_type == quarter:
            self.current_amount += coin_type['value']
            self.quarter_quantity += 1
            self.coins_customer_has_inserted_during_this_transaction.append(quarter)
        # dime
        elif coin_type == dime:
            self.current_amount += coin_type['value']
            self.dime_quantity += 1
            self.coins_customer_has_inserted_during_this_transaction.append(dime)
        # nickel
        elif coin_type == nickel:
            self.current_amount += coin_type['value']
            self.nickel_quantity += 1
            self.coins_customer_has_inserted_during_this_transaction.append(nickel)
        self._coin_display()
        self._check_transaction()

    def _coin_display(self):
        self.check_change_making_ability()
        # display current amount
        current_amount = str(self.current_amount)
        self.display = current_amount

    def button_press(self, button):
        """
        This is an abstracted "button press" handler.
        In a real life system there would be be an implementation detail to handle.
        """
        self._check_for_new_transaction()
        self.check_change_making_ability()

        if button == 'cola':
            self.cola_button_press()
        elif button == "chips":
            self.chips_button_press()
        elif button == "candy":
            self.candy_button_press()

        self._button_display()
        self._check_transaction()

    def cola_button_press(self):
        if self.cola_quantity > 0:
            self.price = 1.00
            self.selected_product = "cola"
        else:
            self.display = "SOLD OUT"

    def chips_button_press(self):
        if self.chips_quantity > 0:
            self.price = 0.50
            self.selected_product = "chips"
        else:
            self.display = "SOLD OUT"

    def candy_button_press(self):
        if self.candy_quantity > 0:
            self.price = 0.65
            self.selected_product = "candy"
        else:
            self.display = "SOLD OUT"

    def _button_display(self):
        if self.price != 0:
            self.balance = self.price - self.current_amount
            # display price
            if self.balance > 0:
                price = "PRICE:"
                price += str(self.price)
                self.display = price

    def _check_transaction(self):
        if self.price != 0:
            self.balance = self.price - self.current_amount
            self.balance = round(self.balance, 2)
            # if balance == 0, dispense and end transaction.
            if self.balance == 0:
                self._dispense_product()
            # if balance < 0, do "make change" things.
            if self.balance < 0:
                self._dispense_product()
                self._make_change(self.balance)

    def _check_for_new_transaction(self):
        if self.display == "THANK YOU":
            self.new_transaction()

    def _dispense_product(self):
        self.dispensed_product = self.selected_product
        self.display = "THANK YOU"
        if self.selected_product == "cola":
            self.cola_quantity -= 1
        elif self.selected_product == "chips":
            self.chips_quantity -= 1
        elif self.selected_product == "candy":
            self.candy_quantity -= 1

    def _make_change(self, balance):
        returning_quarters = 0
        returning_dimes = 0
        returning_nickels = 0
        self.change_due = abs(balance)
        # calculate how many of each coin is needed
        # quarters
        while self.change_due > 0:
            if self.quarter_quantity > 0:
                self.change_due -= 0.25
                # change_due = round(change_due, 2)
                returning_quarters += 1
                self.quarter_quantity -= 1
            else:
                break
        if round(self.change_due, 2) < 0:
            self.change_due += 0.25
            # change_due = round(change_due, 2)
            returning_quarters -= 1
            self.quarter_quantity += 1
        # dimes
        while self.change_due > 0:
            if self.dime_quantity > 0:
                self.change_due -= 0.10
                # change_due = round(change_due, 2)
                returning_dimes += 1
                self.dime_quantity -= 1
            else:
                break
        if round(self.change_due, 2) < 0:
            self.change_due += 0.10
            # change_due = round(change_due, 2)
            returning_dimes -= 1
            self.dime_quantity += 1
        # nickels
        while self.change_due > 0:
            if self.nickel_quantity > 0:
                self.change_due -= 0.05
                # change_due = round(change_due, 2)
                returning_nickels += 1
                self.nickel_quantity -= 1
            else:
                break
        if round(self.change_due, 2) < 0:
            self.change_due += 0.05
            self.change_due = round(self.change_due, 2)
            returning_nickels -= 1
            self.nickel_quantity += 1
        # total
        self.change_due = round(self.change_due, 2)

        # return coins
        for quarter_index in range(returning_quarters):
            self.coin_return.append(quarter)
        for dime_index in range(returning_dimes):
            self.coin_return.append(dime)
        for nickel_index in range(returning_nickels):
            self.coin_return.append(nickel)

    def return_coins(self):
        self.coin_return.extend(self.coins_customer_has_inserted_during_this_transaction)
        for coin in self.coins_customer_has_inserted_during_this_transaction:
            # quarter
            if coin['weight'] == 5.6 and coin['size'] == 24.2:
                self.quarter_quantity -= 1
            # dime
            elif coin['weight'] == 2.2 and coin['size'] == 17.9:
                self.dime_quantity -= 1
            # nickel
            elif coin['weight'] == 5 and coin['size'] == 21.2:
                self.nickel_quantity -= 1
        coin_return_buffer = self.coin_return
        self.new_transaction()
        self.coin_return = coin_return_buffer
        self.coins_customer_has_inserted_during_this_transaction = []
