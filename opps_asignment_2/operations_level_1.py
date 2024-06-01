import os
import sys
from datetime import datetime
from typing import List

from object_inventory import Records, UserKey, BasicCustomer, Customer, Product, Order, VIPCustomer


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

    # if len(sys.argv) != 3:
    #     print("Please enter the filename via console to initialize customer and products !!")
    #     print("Usage: python script.py <file_name1> <file_name2> <file_name3>")
    #     sys.exit(1)
    #
    # # Get the file name from the command line argument
    # customer_data_file_path = sys.argv[1]
    # product_data_file_path = sys.argv[2]
    #
    # orders_data_file = None
    # if len(sys.argv) == 4:
    #     orders_data_file = sys.argv[3]

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
