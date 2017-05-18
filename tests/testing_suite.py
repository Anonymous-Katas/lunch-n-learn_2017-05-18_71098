__author__ = 'David Carroll'
import unittest
from src.vending_machine import VendingMachine

# size = mm diameter
# weight = g
quarter = {'weight': 5.6, 'size': 24.2, 'value': 0.25}
dime = {'weight': 2.2, 'size': 17.9, 'value': 0.10}
nickel = {'weight': 5, 'size': 21.2, 'value': 0.05}
penny = {'weight': 2.5, 'size': 19, 'value': 0.01}


class TestSuite(unittest.TestCase):

    VendingMachine = VendingMachine()

    def test_when_vending_machine_is_passed_a_coin_it_returns_that_coin(self):
        coin = quarter
        self.assertEqual(self.VendingMachine.accept_coins(coin), quarter)
        self.VendingMachine.vending_machine_reset()

    def test_when_vending_machine_is_passed_a_valid_coin_it_updates_current_amount(self):
        coin1 = quarter
        self.VendingMachine.accept_coins(coin1)
        self.assertEqual(self.VendingMachine.current_amount, 0.25)
        self.assertEqual(self.VendingMachine.coin_return, [])
        coin3 = dime
        self.VendingMachine.accept_coins(coin3)
        self.assertEqual(self.VendingMachine.current_amount, 0.35)
        self.assertEqual(self.VendingMachine.coin_return, [])

    def test_when_vending_machine_is_passed_an_invalid_coin_it_is_added_to_return(self):
        coin2 = penny
        self.VendingMachine.accept_coins(coin2)
        self.assertEqual(self.VendingMachine.current_amount, 0.35)
        self.assertEqual(self.VendingMachine.coin_return, [{'size': 19, 'weight': 2.5, 'value': 0.01}])

    def test_when_product_is_selected_price_is_set(self):
        self.VendingMachine.button_press("cola")
        self.assertEqual(self.VendingMachine.price, 1.00)
        self.VendingMachine.button_press("chips")
        self.assertEqual(self.VendingMachine.price, 0.50)
        self.VendingMachine.button_press("candy")
        self.assertEqual(self.VendingMachine.price, 0.65)

    def test_check_transaction_for_correct_balance(self):
        self.VendingMachine.vending_machine_reset()
        coin = quarter
        self.VendingMachine.accept_coins(coin)
        self.assertEqual(self.VendingMachine.current_amount, 0.25)
        self.VendingMachine.button_press("cola")
        self.assertEqual(self.VendingMachine.price, 1.00)
        self.VendingMachine._check_transaction()
        self.assertEqual(self.VendingMachine.balance, 0.75)

    def test_insert_coins_then_press_button_if_cola_transaction_amount_correct_dispense_cola(self):
        self.VendingMachine.vending_machine_reset()
        coin = quarter
        self.VendingMachine.accept_coins(coin)
        self.VendingMachine.accept_coins(coin)
        self.VendingMachine.accept_coins(coin)
        self.VendingMachine.accept_coins(coin)
        self.VendingMachine.button_press("cola")
        self.assertEqual(self.VendingMachine.dispensed_product, 'cola')

    def test_press_button_then_insert_coins_if_cola_transaction_amount_correct_dispense_cola(self):
        self.VendingMachine.vending_machine_reset()
        self.VendingMachine.button_press("cola")
        coin = quarter
        self.VendingMachine.accept_coins(coin)
        self.VendingMachine.accept_coins(coin)
        self.VendingMachine.accept_coins(coin)
        self.VendingMachine.accept_coins(coin)
        self.assertEqual(self.VendingMachine.dispensed_product, 'cola')

    def test_insert_coins_then_press_button_if_chips_transaction_amount_correct_dispense_chips(self):
        self.VendingMachine.vending_machine_reset()
        coin1 = quarter
        coin2 = quarter
        self.VendingMachine.accept_coins(coin1)
        self.VendingMachine.accept_coins(coin2)
        self.VendingMachine.button_press("chips")
        self.assertEqual(self.VendingMachine.dispensed_product, 'chips')

    def test_press_button_then_insert_coins_if_cola_transaction_amount_correct_dispense_chips(self):
        self.VendingMachine.vending_machine_reset()
        self.VendingMachine.button_press("chips")
        coin1 = quarter
        coin2 = quarter
        self.VendingMachine.accept_coins(coin1)
        self.VendingMachine.accept_coins(coin2)
        self.assertEqual(self.VendingMachine.dispensed_product, 'chips')

    def test_insert_coins_then_press_button_if_cola_transaction_amount_correct_dispense_candy(self):
        self.VendingMachine.vending_machine_reset()
        coin1 = quarter
        coin2 = quarter
        coin3 = dime
        coin4 = nickel
        self.VendingMachine.accept_coins(coin1)
        self.VendingMachine.accept_coins(coin2)
        self.VendingMachine.accept_coins(coin3)
        self.VendingMachine.accept_coins(coin4)
        self.VendingMachine.button_press("candy")
        self.assertEqual(self.VendingMachine.dispensed_product, 'candy')

    def test_press_button_then_insert_coins_if_cola_transaction_amount_correct_dispense_candy(self):
        self.VendingMachine.vending_machine_reset()
        self.VendingMachine.button_press("candy")
        coin1 = quarter
        coin2 = quarter
        coin3 = dime
        coin4 = nickel
        self.VendingMachine.accept_coins(coin1)
        self.VendingMachine.accept_coins(coin2)
        self.VendingMachine.accept_coins(coin3)
        self.VendingMachine.accept_coins(coin4)
        self.assertEqual(self.VendingMachine.dispensed_product, 'candy')

    def test_after_complete_transaction_reset_transaction(self):
        self.VendingMachine.vending_machine_reset()
        coin = quarter
        self.VendingMachine.accept_coins(coin)
        self.VendingMachine.accept_coins(coin)
        self.VendingMachine.accept_coins(coin)
        self.VendingMachine.accept_coins(coin)
        self.VendingMachine.button_press("cola")
        self.assertEqual(self.VendingMachine.selected_product, 'cola')
        self.assertEqual(self.VendingMachine.price, 1.00)
        self.assertEqual(self.VendingMachine.dispensed_product, 'cola')
        self.VendingMachine.accept_coins(coin)
        self.assertEqual(self.VendingMachine.selected_product, None)
        self.assertEqual(self.VendingMachine.price, 0)
        self.assertEqual(self.VendingMachine.dispensed_product, None)

    def test_machine_updates_display_for_current_amount_when_coins_are_accepted(self):
        self.VendingMachine.vending_machine_reset()
        coin = quarter
        self.VendingMachine.accept_coins(coin)
        self.VendingMachine.accept_coins(coin)
        self.assertEqual(self.VendingMachine.display, '0.5')

    def test_machine_displays_PRICE_if_not_enough_money_is_inserted(self):
        self.VendingMachine.vending_machine_reset()
        self.VendingMachine.button_press("candy")
        self.assertEqual(self.VendingMachine.display, 'PRICE:0.65')

    def test_make_change_correctly_reaches_zero_change_due(self):
        self.VendingMachine.vending_machine_reset()
        self.VendingMachine._make_change(-0.65)
        self.assertEqual(self.VendingMachine.change_due, 0)
        self.VendingMachine.vending_machine_reset()
        self.VendingMachine._make_change(-0.75)
        self.assertEqual(self.VendingMachine.change_due, 0)
        self.VendingMachine.vending_machine_reset()
        self.VendingMachine._make_change(-0.05)
        self.assertEqual(self.VendingMachine.change_due, 0)
        self.VendingMachine.vending_machine_reset()
        self.VendingMachine._make_change(-0.10)
        self.assertEqual(self.VendingMachine.change_due, 0)
        self.VendingMachine.vending_machine_reset()
        self.VendingMachine._make_change(-0.1005)
        self.assertEqual(self.VendingMachine.change_due, 0)

    def test_make_change_sums_correct_number_of_each_coin_in_change(self):
        self.VendingMachine.vending_machine_reset()
        self.VendingMachine._make_change(-0.65)
        # quarter, quarter, dime, nickle
        self.assertEqual(self.VendingMachine.coin_return, [{'size': 24.2, 'weight': 5.6, 'value': 0.25}, {'size': 24.2, 'weight': 5.6, 'value': 0.25}, {'size': 17.9, 'weight': 2.2, 'value': 0.10}, {'size': 21.2, 'weight': 5, 'value': 0.05}])
        self.VendingMachine.vending_machine_reset()
        self.VendingMachine._make_change(-0.75)
        # quarter, quarter, quarter
        self.assertEqual(self.VendingMachine.coin_return, [{'size': 24.2, 'weight': 5.6, 'value': 0.25}, {'size': 24.2, 'weight': 5.6, 'value': 0.25}, {'size': 24.2, 'weight': 5.6, 'value': 0.25}])
        self.VendingMachine.vending_machine_reset()
        self.VendingMachine._make_change(-0.05)
        # nickle
        self.assertEqual(self.VendingMachine.coin_return, [{'weight': 5, 'size': 21.2, 'value': 0.05}])
        self.VendingMachine.vending_machine_reset()
        self.VendingMachine._make_change(-0.10)
        # dime
        self.assertEqual(self.VendingMachine.coin_return, [{'weight': 2.2, 'size': 17.9, 'value': 0.10}])
        self.VendingMachine.vending_machine_reset()
        self.VendingMachine._make_change(-25000)
        # 100,000 quarters
        # self.assertEqual(len(self.VendingMachine.coin_return), 100000)

    def test_when_the_item_selected_by_the_customer_is_out_of_stock_the_machine_displays_SOLD_OUT(self):
        self.VendingMachine.vending_machine_reset()
        for sale_index in range(6):
            coin = quarter
            self.VendingMachine.accept_coins(coin)
            self.VendingMachine.accept_coins(coin)
            self.VendingMachine.accept_coins(coin)
            self.VendingMachine.accept_coins(coin)
            self.VendingMachine.button_press("cola")
        self.assertEqual(self.VendingMachine.display, "SOLD OUT")

    def test_vending_machine_correctly_checks_change_making_ability(self):
        self.VendingMachine.vending_machine_reset()
        self.VendingMachine.dime_quantity = 1
        self.VendingMachine.nickel_quantity = 1
        self.assertEqual(self.VendingMachine.display, "INSERT COIN")
        # candy = 0.65
        self.VendingMachine.button_press("candy")
        coin = quarter
        self.VendingMachine.accept_coins(coin)
        self.VendingMachine.accept_coins(coin)
        self.VendingMachine.accept_coins(coin)
        self.assertEqual(self.VendingMachine.display, "THANK YOU")
        self.assertEqual(self.VendingMachine.dime_quantity, 0)
        self.VendingMachine.new_transaction()
        self.assertEqual(self.VendingMachine.display, "EXACT CHANGE ONLY")

    def test_return_coins(self):
        self.VendingMachine.vending_machine_reset()
        self.VendingMachine.print_and_break_on_this_test = True
        coin1 = quarter
        self.VendingMachine.accept_coins(coin1)
        self.VendingMachine.accept_coins(coin1)
        self.VendingMachine.return_coins()
        self.assertEqual(self.VendingMachine.display, "INSERT COIN")
        self.assertEqual(self.VendingMachine.coin_return, [{'weight': 5.6, 'size': 24.2, 'value': 0.25}, {'weight': 5.6, 'size': 24.2, 'value': 0.25}])
        self.VendingMachine.new_transaction()
        coin2 = dime
        self.VendingMachine.accept_coins(coin2)
        self.VendingMachine.return_coins()
        self.assertEqual(self.VendingMachine.display, "INSERT COIN")
        self.assertEqual(self.VendingMachine.coin_return, [{'weight': 2.2, 'size': 17.9, 'value': 0.10}])
        self.VendingMachine.new_transaction()
        coin3 = nickel
        self.VendingMachine.accept_coins(coin3)
        self.VendingMachine.accept_coins(coin3)
        self.VendingMachine.accept_coins(coin3)
        self.VendingMachine.return_coins()
        self.assertEqual(self.VendingMachine.display, "INSERT COIN")
        self.assertEqual(self.VendingMachine.coin_return, [{'weight': 5, 'size': 21.2, 'value': 0.05}, {'weight': 5, 'size': 21.2, 'value': 0.05}, {'weight': 5, 'size': 21.2, 'value': 0.05}])


if __name__ == '__main__':
    unittest.main()
