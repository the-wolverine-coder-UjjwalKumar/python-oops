import os

from assignment.oops_assignment.records import Records


def display_menu():
    print("#################################################################################")
    print("1: Make a purchase")
    print("2: Display existing customers")
    print("3: Display existing orders")
    print("4: Exit the program")
    print("#################################################################################")


def read_data_local(record, customer_data_file_path, product_data_file_path):
    record.read_customers(customer_data_file_path)
    record.read_products(product_data_file_path)


def main():
    record = Records()
    customer_data_file_path = 'customers.txt'
    product_data_file_path = 'products.txt'

    if not (os.path.exists(customer_data_file_path) and os.path.exists(product_data_file_path)):
        print("Error: Missing customers.txt or products.txt file.")
        exit()

    # Read customer and product data from files
    read_data_local(record, customer_data_file_path, product_data_file_path)

    while True:
        # printing one line
        print()
        display_menu()
        option = int(input("Choose a option: "))
        if option == 4:
            exit()

        if option == 1:
            purchase()
        elif option == 2:
            print("Existing customers and their rewards ", customer_to_rewards_dict)
        elif option == 3:
            print("Existing product, their prices and prescription required ", product_price_dict)


# initialize the price and customer rewards dict
product_price_dict = {"vitaminC": 12.0, "vitaminE": 14.5, "coldTablet": 6.4, "vaccine": 32.6, "fragrance": 25.0}
customer_to_rewards_dict = {"Kate": 20, "Tom": 32}


def get_total_amount(product_name, product_quantity):
    amt = 0.0
    if product_name in product_price_dict.keys():
        amt = product_price_dict.get(product_name) * product_quantity
    return amt


def display_receipt(customers_name, product_name, product_quantity, total_amount, total_reward):
    print("--------------------------------------------------------------------------")
    print("\t\t\t\t\t\tReceipt")
    print("--------------------------------------------------------------------------")
    print("Name:\t\t\t\t\t", customers_name)
    print("Product:\t\t\t\t", product_name)
    print("Unit Price:\t\t\t\t", str(product_price_dict.get(product_name)) + " (AUD)")
    print("Quantity:\t\t\t\t", str(product_quantity))
    print("--------------------------------------------------------------------------")
    print("Total Cost:\t\t\t\t", str(total_amount) + "(AUD)")
    print("Earned Reward:\t\t\t", str(total_reward))


def update_reward(customers_name, total_reward):
    if customers_name in customer_to_rewards_dict.keys():
        customer_to_rewards_dict[customers_name] = customer_to_rewards_dict.get(customers_name) + total_reward
    else:
        customer_to_rewards_dict[customers_name] = total_reward


def purchase():
    # taking input of customer name, product and quantity
    customers_name = input("Please Enter customer's name :: ")
    product_name = input("Please Enter Product name e.g. [ " + str(list(product_price_dict.keys())) + " ] :: ")
    product_quantity = int(
        input("Please Enter Quantity e.g [ 1,2,3...] of product : " + product_name + " you want :: "))

    total_amount = get_total_amount(product_name, product_quantity)

    # taking the round of value only for rewards
    if total_amount - int(total_amount) < 0.5:
        total_reward = int(total_amount)
    else:
        total_reward = int(total_amount) + 1

    # update the customer to reward in customer_to_rewards_dict
    update_reward(customers_name, total_reward)

    # displaying the receipt
    display_receipt(customers_name, product_name, product_quantity, total_amount, total_reward)


if __name__ == "__main__":
    main()
