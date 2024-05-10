from assignment.oops_assignment.customers import VIPCustomer, BasicCustomer
from assignment.oops_assignment.products import Product


class Records:

    def __init__(self):
        self.customers = []
        self.products = []

    def read_customers(self, file_name):
        with open(file_name, 'r') as file:
            for line in file:
                customer_data = line.strip().split(',')
                customer_id, customer_name = customer_data[:2]
                reward_rate = float(customer_data[2].strip('%')) / 100
                if len(customer_data) == 5:
                    discount_rate = float(customer_data[3].strip('%')) / 100
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

    def read_products(self, file_name):
        with open(file_name, 'r') as file:
            for line in file:
                product_data = line.strip().split(',')
                product_id, product_name = product_data[:2]
                unit_price = float(product_data[2].strip('%'))

                product = Product(product_id, product_name, unit_price)
                self.products.append(product)

    def find_customer(self, search_value):
        for customer in self.customers:
            if customer.id == search_value or customer.name == search_value:
                return customer
        return None

    def find_product(self, search_value):
        for product in self.products:
            if product.id == search_value or product.name == search_value:
                return product
        return None

    def list_customer(self):
        for customer in self.customers:
            if isinstance(customer, VIPCustomer):
                customer.display_info()
            elif isinstance(customer, BasicCustomer):
                customer.display_info()

    def list_product(self):
        for product in self.products:
            product.display_info()
