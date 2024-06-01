from typing import List, Optional, Dict
import os
import sys
from datetime import datetime


class Customer:
    def __init__(self, ID, name, reward):
        self.ID = ID
        self.name = name
        self.reward = reward

    def get_ID(self):
        return self.ID

    def get_name(self):
        return self.name

    # Empty super method
    def get_reward(self, value):
        pass

    def get_discount(self, value):
        pass

    def update_reward(self, value):
        pass

    def display_info(self):
        pass


class BasicCustomer(Customer):
    reward_rate = 1

    def __init__(self, ID, name, reward=0, reward_rate=1.0):
        super().__init__(ID, name, reward)
        self.reward_rate = reward_rate

    def get_reward_rate(self):
        return self.reward_rate

    def get_reward(self, total_cost):
        return round(total_cost * self.reward_rate)

    def update_reward(self, value):
        self.reward += value

    def display_info(self):
        print("Basic Customer Information:")
        print(f"ID: {self.ID}")
        print(f"Name: {self.name}")
        print(f"Reward: {self.reward}")
        print(f"Reward Rate: {self.reward_rate}")
        print()

    @classmethod
    def set_reward_rate(cls, new_rate):
        cls.reward_rate = new_rate


class UserKey:

    def __init__(self):
        self.user_key = 1001

    def get_user_key(self):
        return self.user_key

    def update_user_key(self):
        self.user_key = self.user_key + 1


class VIPCustomer(Customer):
    reward_rate = 1.0  # Default reward rate for all VIP customers
    discount_rate = 0.08

    def __init__(self, ID, name, reward=0, reward_rate=1.0, discount_rate=0.08):
        super().__init__(ID, name, reward)
        self.reward_rate = reward_rate
        self.discount_rate = discount_rate

    def get_reward_rate(self):
        return self.reward_rate

    def get_discount_rate(self):
        return self.discount_rate

    def get_discount(self, total_cost):
        discount_amt = total_cost * self.discount_rate
        return round(discount_amt, 1)

    def get_reward(self, total_cost):
        discounted_cost = total_cost - self.get_discount(total_cost)
        return round(discounted_cost * self.reward_rate)

    def update_reward(self, value):
        self.reward += value

    def display_info(self):
        print("VIP Customer Information:")
        print(f"ID: {self.ID}")
        print(f"Name: {self.name}")
        print(f"Reward: {self.reward}")
        print(f"Reward Rate: {self.reward_rate}")
        print(f"Discount Rate: {self.discount_rate}")
        print()

    @classmethod
    def set_reward_rate(cls, new_rate):
        cls.reward_rate = new_rate

    @classmethod
    def set_discount_rate(cls, new_rate):
        cls.discount_rate = new_rate


class Product:
    def __init__(self, ID, name, price, dr_prescription="n"):
        self.ID = ID
        self.name = name
        self.price = price
        self.dr_prescription = dr_prescription

    def display_info(self):
        print("Product Information:")
        print(f"ID: {self.ID}")
        print(f"Name: {self.name}")
        print(f"Price: ${self.price:.2f}")
        print(f"Dr. Prescription required: {self.dr_prescription}")
        print()

    def get_unit_price(self):
        return self.price

    def get_name(self):
        return self.name


class Bundle(Product):

    def __init__(self, ID, name, product_list):
        # self.ID = ID
        # self.name = name
        self.product_list: List[Product] = product_list
        amt = 0
        dr_prescription = "n"
        for product in product_list:
            if product.dr_prescription == "y":
                dr_prescription = "y"
            amt = amt + product.price
        amt = amt * 0.8  # 80 percent of total amt
        self.price = round(amt, 2)
        super().__init__(ID, name, self.price, dr_prescription)

    def display_info(self):
        print("Bundle Information:")
        print(f"ID: {self.ID}")
        product_ids = ','.join(str(product.ID) for product in self.product_list)
        print(f"Name : {self.name}")
        print(f"Component Ids : {product_ids}")
        print(f"Price: ${self.price:.2f}")
        print(f"Doctor Prescription required: {self.dr_prescription}")
        print()


class Order:

    def __init__(self, customer, product, quantity, total_cost=0.0, discount=0.0, reward=0, discounted_price=0.0,
                 date=None):
        self.customer = customer
        self.product = product
        self.quantity = quantity
        self.total_cost = total_cost
        self.discount = discount
        self.discounted_price = discounted_price
        self.reward = reward
        self.date = date

    def compute_cost(self):
        total_cost = self.product.price * self.quantity
        discount = 0
        if isinstance(self.customer, VIPCustomer) and hasattr(self.customer, 'get_discount'):
            discount = self.customer.get_discount(total_cost)
        final_cost = total_cost - discount
        reward = 0
        if hasattr(self.customer, 'get_reward'):
            reward = self.customer.get_reward(final_cost)
        return round(total_cost, 2), discount, round(final_cost, 2), reward


def def_product_value() -> Optional[Product]:
    return None


def def_customer_value() -> Optional[Customer]:
    return None


class Records:

    def __init__(self):
        self.customers: List[Customer] = []
        self.customers_details: Dict[str, Customer] = dict()
        self.customer_id_to_name = dict()
        self.products: List[Product] = []
        self.product_details: Dict[str, Product] = dict()
        self.product_id_to_name = dict()
        self.orders: List[Order] = []

    def read_customers(self, file_name):
        with open(file_name, 'r') as file:
            for line in file:
                customer_data = line.strip().split(', ')
                customer_id, customer_name = customer_data[:2]
                reward_rate = float(customer_data[2].strip('%'))
                if len(customer_data) == 5:
                    discount_rate = float(customer_data[3].strip('%'))
                    reward = int(customer_data[4])
                elif len(customer_data) == 4:
                    reward = int(customer_data[3])

                if customer_id.startswith('V'):
                    # Create a new VIP customer object and add it to the customers list
                    customer = VIPCustomer(customer_id, customer_name, reward, reward_rate, discount_rate)
                elif customer_id.startswith('B'):
                    # Create a new basic customer object and add it to the customers list
                    customer = BasicCustomer(customer_id, customer_name, reward, reward_rate)

                self.customers.append(customer)
                self.customers_details[customer_name] = customer
                self.customer_id_to_name[customer_id] = customer_name

    def read_products(self, file_name):
        with open(file_name, 'r') as file:
            for line in file:
                product_data = line.strip().split(', ')  # splitting with , and space
                product_id, product_name = product_data[:2]
                unit_price = float(product_data[2].strip('%'))

                product = Product(product_id, product_name, unit_price)
                self.products.append(product)
                self.product_details[product_name] = product

    def read_products_with_prescription(self, file_name):
        with open(file_name, 'r') as file:
            for line in file:
                product_data = line.strip().split(', ')  # splitting with , and space
                product_id, product_name = product_data[:2]
                unit_price = float(product_data[2].strip('%'))
                dr_prescription = product_data[3]

                product = Product(product_id, product_name, unit_price, dr_prescription)
                self.products.append(product)
                self.product_details[product_name] = product

    def read_bundled_products(self, file_name):
        with open(file_name, 'r') as file:
            bundle_products = []
            products: List[Product] = []
            product_details: Dict[str, Product] = dict()
            product_id_to_name = dict()
            for line in file:
                product_data = line.strip().split(', ')  # splitting with , and space
                product_id, product_name = product_data[:2]

                if product_id.startswith("B"):
                    bundle_products.append(product_data)
                else:
                    unit_price = float(product_data[2].strip('%'))
                    dr_prescription = product_data[3]

                    product = Product(product_id, product_name, unit_price, dr_prescription)

                    products.append(product)
                    product_details[product_name] = product
                    product_id_to_name[product_id] = product_name

            # now normal products are added, appending bundle products
            for product_data in bundle_products:
                product_id, product_name = product_data[:2]
                product_component_ids = product_data[2:]
                product_list = []
                for pid in product_component_ids:
                    bundle_product_data = product_details.get(product_id_to_name.get(pid))
                    if bundle_product_data is not None:
                        product_list.append(bundle_product_data)

                bundle_product = Bundle(product_id, product_name, product_list)
                products.append(bundle_product)
                product_details[product_name] = bundle_product
                product_id_to_name[product_id] = product_name

            self.products = products
            self.product_details = product_details
            self.product_id_to_name = product_id_to_name

    def read_orders(self, order_data_file):
        with open(order_data_file, 'r') as file:
            for line in file:
                order_data = line.strip().split(', ')
                customer_key = order_data[0]  # customer_key can be customer id or name
                customer = self.find_customer(customer_key)

                # The last three elements are total cost, total reward, and date
                total_cost = float(order_data[len(order_data) - 3])
                total_reward = int(order_data[len(order_data) - 2])
                date = order_data[len(order_data) - 1]

                # Extract products
                for i in range(1, len(order_data) - 3, 2):
                    product_key = order_data[i]  # this can be id or name
                    quantity = int(order_data[i + 1])

                    product = self.find_product(product_key)  # assumption all entries are valid

                    order = Order(customer, product, quantity, total_cost, 0.0, total_reward, 0.0, date)
                    # to update the discount and discounted rate
                    order.total_cost, order.discount, order.discounted_price, order.reward = order.compute_cost()
                    self.orders.append(order)

                    # updating the reward with new data
                    customer.update_reward(order.reward)

    def find_customer(self, search_value):
        for customer in self.customers:
            if customer.ID == search_value or customer.name == search_value:
                return customer
        return None

    def find_product(self, search_value):
        for product in self.products:
            if product.ID == search_value or product.name == search_value:
                return product
        return None

    def list_customer(self):
        for customer in self.customers:
            customer.display_info()

    def list_product(self):
        for product in self.products:
            product.display_info()

    def list_product_names(self):
        return self.product_details.keys()

    def is_prescription_req(self, product_name):
        existing_product = self.product_details.get(product_name, None)
        return existing_product.dr_prescription if existing_product is not None else None


######################################################################################################################


def display_menu():
    print("#################################################################################")
    print("1: Make a purchase")
    print("2: Display existing customers")
    print("3: Display existing products")
    print("4: Exit the program")
    print("#################################################################################")


def display_new_menu():
    print("#################################################################################")
    print("1: Make a purchase")
    print("2: Display existing customers")
    print("3: Display existing products")
    print("4: Add/Update product information ")
    print("5: Display customer order history")
    print("6: Adjust reward rate for all Basic Customer")
    print("7: Adjust discount rate for all VIP Customer")
    print("8: Display all orders ")
    print("9: Exit the program")
    print("#################################################################################")


def read_data_local(record: Records, customer_data_file_path, product_data_file_path):
    record.read_customers(customer_data_file_path)
    record.read_products(product_data_file_path)


def upsert_customer_data(record: Records, customers_name, user_key_suffix: UserKey):
    existing_customer = record.customers_details.get(customers_name, None)

    # means new customer hence adding it as Basic consumer
    if existing_customer is None:
        user_id = "B" + str(user_key_suffix.get_user_key())
        user_key_suffix.update_user_key()

        new_basic_customer = BasicCustomer(user_id, customers_name, 0)
        record.customers.append(new_basic_customer)
        record.customers_details[customers_name] = new_basic_customer
        existing_customer = new_basic_customer
    else:
        is_basic = existing_customer.get_ID().startswith("B")
        if is_basic:
            print("Customer Type :: Basic")
        else:
            print("Customer Type :: VIP")

    return existing_customer


def purchase(record: Records, user_key_suffix: UserKey):
    # taking input of customer name, product and quantity
    customers_name = input("Please Enter customer's name :: ")
    product_name = input("Please Enter Product name e.g. [ " + str(list(record.list_product_names())) + " ] :: ")
    product_quantity = int(
        input("Please Enter Quantity e.g [ 1,2,3...] of product : " + product_name + " you want :: "))

    # adding the customer if required or getting the existing one
    existing_customer = upsert_customer_data(record, customers_name, user_key_suffix)

    # now customer data is stored in existing_customer
    # will proceed with purchase
    product = record.product_details.get(product_name, None)

    if product is not None:
        # creating order and update the further details
        order = Order(existing_customer, product, int(product_quantity))
        order.total_cost, order.discount, order.discounted_price, order.reward = order.compute_cost()

        # update the customer to reward in customer_to_rewards_dict
        update_reward(existing_customer, order.reward)

        # displaying the receipt
        display_receipt(existing_customer, product, product_quantity, order.total_cost, order.reward, order.discount)

        return order


def purchase_with_handled_exception(record: Records, user_key_suffix: UserKey):
    # taking input of customer name, product and quantity
    # taking valid customer_name
    while True:
        customer_name = input("Please Enter customer's name :: ")

        if customer_name.isalpha():
            break
        else:
            print("provided customer name is not valid one, it should have only alphabet characters\n")

    # taking valid product name
    while True:
        product_name = input("Please Enter Product name e.g. [ " + str(list(record.list_product_names())) + " ] :: ")

        if product_name.isalpha() and product_name in (list(record.list_product_names())):
            break
        else:
            print("Input product name is not valid one, "
                  "it should have only alphabet characters & must be from " + str(list(record.list_product_names())) +
                  "\n")

    while True:
        product_quantity = input("Please Enter Quantity e.g [ 1,2,3...] of product : " + product_name + " you want :: ")

        if product_quantity.isnumeric() and int(product_quantity) > 0:
            product_quantity = int(product_quantity)
            break
        else:
            print("Please Enter valid Quantity e.g [ 1,2,3...] of product\n")

    product = record.product_details.get(product_name, None)

    if product is not None:

        is_prescription_req = record.product_details.get(product_name).dr_prescription == "y"
        # collection doctor's prescription if required
        prescription_present = "n"
        if is_prescription_req:
            while True:
                prescription_present = input("Product : " + product_name + " required doctor's prescription, "
                                                                           "do you have drs prescription :: ")

                if prescription_present.isalpha() and prescription_present in ["y", "n"]:
                    break
                else:
                    print("Please Enter valid value for doctor prescription e.g [ y, n]\n")

        if is_prescription_req and prescription_present == "y" or \
                not is_prescription_req and prescription_present == "n":

            # adding the customer if required or getting the existing one
            existing_customer = upsert_customer_data(record, customer_name, user_key_suffix)

            # creating order and update the further details
            order = Order(existing_customer, product, int(product_quantity))
            order.total_cost, order.discount, order.discounted_price, order.reward = order.compute_cost()

            # update the customer to reward in customer_to_rewards_dict
            update_reward(existing_customer, order.reward)

            # displaying the receipt
            display_receipt(existing_customer, product, product_quantity, order.total_cost, order.reward,
                            order.discount)

            return order
        else:
            return None


def purchase_multiple_products(record: Records, user_key_suffix: UserKey):
    # taking input of customer name, product and quantity
    # taking valid customer_name
    while True:
        customer_name = input("Please Enter customer's name :: ")

        if customer_name.isalpha():
            break
        else:
            print("provided customer name is not valid one, it should have only alphabet characters\n")

    # taking valid product name list separated by space
    product_list_ordered: List[Product] = []
    while True:
        product_name_list = list(input("Please Enter Product names e.g. [ "
                                       + str(list(record.list_product_names())) + "] :: ").split(" "))

        # validating the input product name list
        is_valid = True
        valid_products_to_by = []
        for product_name in product_name_list:
            if product_name.isalpha():
                product = record.product_details.get(product_name, None)
                if product is not None:
                    if product.dr_prescription == "y":
                        ans = input("The product " + product_name + " require a doctor's prescription, do you have ? ")
                        if ans.isalpha():
                            if ans == "n":
                                continue
                            elif ans == "y":
                                valid_products_to_by.append(product_name)
                            else:
                                print("Please enter supported value : y / n")
                                is_valid = False
                                break
                    else:
                        valid_products_to_by.append(product_name)
            else:
                print("Input product name list is not valid one, "
                      "it should have only alphabet characters & must be from " + str(list(record.list_product_names()))
                      + "\n")
                is_valid = False
                break

        if is_valid:
            break

    for product_name in valid_products_to_by:
        product_list_ordered.append(record.product_details.get(product_name))

    while True:
        product_quantity_list = list(input("Please Enter Quantity e.g [ 1,2,3...] of products : ").split(" "))

        is_valid = True
        for product_quantity in product_quantity_list:
            if product_quantity.isnumeric() and int(product_quantity) > 0:
                continue
            else:
                is_valid = False
                print("Please Enter valid Quantity e.g [ 1,2,3...] of product\n")
                break
        if is_valid:
            break

    # adding the customer if required or getting the existing one
    existing_customer = upsert_customer_data(record, customer_name, user_key_suffix)
    # user_id = existing_customer.get_ID()
    ordered_list: List[Order] = []

    current_date_time = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")

    for i in range(0, len(product_list_ordered)):
        product = product_list_ordered[i]
        product_quantity = product_quantity_list[i]

        order = Order(existing_customer, product, int(product_quantity))
        order.total_cost, order.discount, order.discounted_price, order.reward = order.compute_cost()
        order.date = current_date_time
        ordered_list.append(order)

        # update the customer to reward in customer_to_rewards_dict
        update_reward(existing_customer, order.reward)

    # displaying the receipt
    display_receipt_with_multiple_orders(existing_customer, ordered_list)

    return ordered_list


def update_reward(customer: Customer, reward):
    customer.update_reward(reward)


def display_receipt_with_multiple_orders(customer: Customer, ordered_list: List[Order]):
    print("--------------------------------------------------------------------------")
    print("\t\t\t\t\t\tReceipt")
    print("--------------------------------------------------------------------------")
    print("Name:\t\t\t\t\t", customer.name)
    original_cost = 0.0
    discount = 0.0
    final_cost = 0.0
    reward = 0
    for i in range(0, len(ordered_list)):
        order = ordered_list[i]
        product = order.product

        product_name = product.name
        product_quantity = order.quantity
        print("Product:\t\t\t\t", product_name)
        print("Unit Price:\t\t\t\t", str(product.price) + " (AUD)")
        print("Quantity:\t\t\t\t", str(product_quantity))
        original_cost = original_cost + order.total_cost
        discount = discount + order.discount
        final_cost = final_cost + order.discounted_price
        reward = reward + order.reward

    print("--------------------------------------------------------------------------")
    if customer.get_ID().startswith("V"):
        print("Original Cost:\t\t\t", str(original_cost) + " (AUD)")
        print("Discount :\t\t\t\t", str(discount) + " (AUD)")
    print("Total Cost:\t\t\t\t", str(final_cost) + " (AUD)")
    print("Earned Reward:\t\t\t", str(reward))


def display_receipt(customer: Customer, product: Product, product_quantity, total_amount, total_reward, discount):
    print("--------------------------------------------------------------------------")
    print("\t\t\t\t\t\tReceipt")
    print("--------------------------------------------------------------------------")
    print("Name:\t\t\t\t\t", customer.get_name())
    print("Product:\t\t\t\t", product.get_name())
    print("Unit Price:\t\t\t\t", str(product.get_unit_price()) + " (AUD)")
    print("Quantity:\t\t\t\t", str(product_quantity))
    print("--------------------------------------------------------------------------")
    if customer.get_ID().startswith("V"):
        print("Original Cost:\t\t\t", str(product.get_unit_price() * product_quantity) + " (AUD)")
        print("Discount :\t\t\t\t", str(discount) + " (AUD)")

    print("Total Cost:\t\t\t\t", str(total_amount) + " (AUD)")
    print("Earned Reward:\t\t\t", str(total_reward))


def operation_level_pass():
    records = Records()
    user_key_suffix = UserKey()
    order_details = []
    customer_data_file_path = 'customers.txt'
    product_data_file_path = 'products.txt'

    if not (os.path.exists(customer_data_file_path) and os.path.exists(product_data_file_path)):
        print("Error: Missing customers.txt or products.txt file.")
        exit()

    # Read customer and product data from files
    read_data_local(records, customer_data_file_path, product_data_file_path)

    while True:
        # printing one line
        print()
        display_menu()
        option = int(input("Choose a option: "))
        if option == 4:
            exit()

        if option == 1:
            order = purchase(records, user_key_suffix)
            if order is not None:
                order_details.append(order)
        elif option == 2:
            print("Existing customers and their rewards \n")
            records.list_customer()
        elif option == 3:
            print("Existing product, their prices and prescription required \n")
            records.list_product()


def read_data_with_bundle(record, customer_data_file_path, product_data_file_path):
    record.read_customers(customer_data_file_path)
    record.read_bundled_products(product_data_file_path)  # reading products with bundle information and dr prescription


def read_orders_data(record: Records, orders_data_file_path):
    if orders_data_file_path is not None:
        record.read_orders(orders_data_file_path)


def operation_level_credit():
    records = Records()
    user_key_suffix = UserKey()
    order_details = []
    customer_data_file_path = 'customers.txt'
    product_data_file_path = 'products.txt'

    if not (os.path.exists(customer_data_file_path) and os.path.exists(product_data_file_path)):
        print("Error: Missing customers.txt or products.txt file.")
        exit()

    # Read customer and product data from files
    read_data_with_bundle(records, customer_data_file_path, product_data_file_path)

    while True:
        # printing one line
        print()
        display_menu()
        option = int(input("Choose a option: "))
        if option == 4:
            exit()

        if option == 1:
            order = purchase_with_handled_exception(records, user_key_suffix)
            if order is not None:
                order_details.append(order)
        elif option == 2:
            print("Existing customers and their rewards \n")
            records.list_customer()
        elif option == 3:
            print("Existing product, their prices and prescription required \n")
            records.list_product()


def operation_level_di():
    records = Records()
    user_key_suffix = UserKey()
    order_details = []
    customer_data_file_path = 'customers.txt'
    product_data_file_path = 'products.txt'

    if not (os.path.exists(customer_data_file_path) and os.path.exists(product_data_file_path)):
        print("Error: Missing customers.txt or products.txt file.")
        exit()

    # Read customer and product data from files
    read_data_with_bundle(records, customer_data_file_path, product_data_file_path)

    while True:
        # printing one line
        print()
        display_menu()
        option = int(input("Choose a option: "))
        if option == 4:
            exit()

        if option == 1:
            orders = purchase_multiple_products(records, user_key_suffix)
            if orders is not None:
                order_details = order_details + orders
                records.orders = records.orders + order_details
        elif option == 2:
            print("Existing customers and their rewards \n")
            records.list_customer()
        elif option == 3:
            print("Existing product, their prices and prescription required \n")
            records.list_product()


def write_data(file_name, data):
    with open(file_name, 'w') as file:
        file.write(data)


def upsert_product_data(records, user_key_suffix, product_file_name):
    print("Enter product details :: ")
    product_key = input("Please enter the product name / id :: ")

    if records.find_customer(product_key) is None:
        p_name = input("Please enter product name :: ")
        unit_price = float(input("Please enter the product unit price :: "))
        is_prescription_req = input("Is doctor's prescription is required or not <y / n>")

        # assuming all the input values are valid
        p_id = "P" + str(user_key_suffix)
        product = Product(p_id, p_name, unit_price, is_prescription_req)
        records.products.append(product)
        records.product_details[p_name] = product
        records.product_id_to_name[p_id] = p_name
        user_key_suffix.update_user_key()
        data = product.ID + ", " + product.name + ", " + str(product.price) + ", " + product.dr_prescription
        write_data(product_file_name, data)
    else:
        product = records.find_customer(product_key)
        print("What you want to update for given product :: ")
        records.find_customer(product_key).display_info()
        key = input("Please enter the property name")
        if key == "name":
            p_name = input("Please enter new name :: ")
            product.name = p_name
        elif key == "dr_prescription":
            is_prescription_req = input("Is doctor's prescription is required or not <y / n>")
            product.dr_prescription = is_prescription_req
        elif key == "price":
            unit_price = float(input("Please enter the product unit price :: "))
            product.price = unit_price


def print_order_row(key, product_item, total_cost, total_reward):
    print(key + "\t\t\t" + product_item + "\t\t\t" + str(total_cost) + "\t\t\t" + str(total_reward))


def print_order_history(customer, records):
    orders = []
    for order in records.orders:
        if order.customer.name == customer.name:
            orders.append(order)
    key = "Order-"
    i = 1
    for order in orders:
        print("This is the order history of ", customer.name)
        print("\t\t\t\tProduct\t\t\t\tTotal Cost\t\t\tTotal Reward")
        key = key + i
        i = i + 1
        print_order_row(key, order.product.name, order.total_cost, order.reward)


def operation_level_hd():
    records = Records()
    user_key_suffix = UserKey()
    order_details = []
    customer_data_file_path = 'customers.txt'
    product_data_file_path = 'products.txt'
    orders_data_file = 'orders.txt'

    if len(sys.argv) != 3:
        print("Please enter the filename via console to initialize customer and products !!")
        print("Usage: python script.py <file_name1> <file_name2> <file_name3>")
        sys.exit(1)

    # Get the file name from the command line argument
    customer_data_file_path = sys.argv[1]
    product_data_file_path = sys.argv[2]

    orders_data_file = None
    if len(sys.argv) == 4:
        orders_data_file = sys.argv[3]

    if not (os.path.exists(customer_data_file_path) and os.path.exists(product_data_file_path)):
        print("Error: Missing customers.txt or products.txt file.")
        exit()

    # Read customer and product data from files
    read_data_with_bundle(records, customer_data_file_path, product_data_file_path)

    # inside record object we  have
    # customers - [] list of customer object (both Basic & VIP )
    # customer_details - {} map of customer_name as key and customer object as value
    # customer_id_to_name - {} map of customer_id as key and customer_name as value
    # products - [] list of product object (both Product & Bundle)
    # product_details - {} map of product_name as key and product object as value
    # product_id_to_name - {} map of product_id as key and product_name as value

    read_orders_data(records, orders_data_file)

    while True:
        # printing one line
        print()
        display_new_menu()
        option = int(input("Choose a option: "))
        if option == 8:
            exit()

        if option == 1:
            orders = purchase_multiple_products(records, user_key_suffix)
            if orders is not None:
                order_details = order_details + orders
                records.orders = records.orders + order_details
        elif option == 2:
            print("Existing customers and their rewards \n")
            records.list_customer()
        elif option == 3:
            print("Existing product, their prices and prescription required \n")
            records.list_product()
        elif option == 4:
            upsert_product_data(records, user_key_suffix, product_data_file_path)
        elif option == 5:
            c_name = input("Please enter the customer key/ name")
            # assuming it is valid one
            customer = records.find_customer(c_name)
            print_order_history(customer, records)
        elif option == 6:
            reward_rate = float(input("Please enter new reward rate for all Basic Customer :: "))
            BasicCustomer.set_reward_rate(reward_rate)
        elif option == 7:
            discount_rate = float(input("Please enter new discount rate for all VIP Customer :: "))
            VIPCustomer.set_discount_rate(discount_rate)


def main():
    # Level 1
    # operation_level_pass()
    # level 2
    # operation_level_credit()
    # Level 3
    operation_level_di()
    # Level 4
    # operation_level_hd()


if __name__ == "__main__":
    main()
