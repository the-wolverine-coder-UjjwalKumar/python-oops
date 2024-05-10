from assignment.oops_assignment.customers import VIPCustomer


class Order:
    def __init__(self, customer, product, quantity):
        self.customer = customer
        self.product = product
        self.quantity = quantity

    def compute_cost(self):
        total_cost = self.product.price * self.quantity
        discount = 0
        if isinstance(self.customer, VIPCustomer) and hasattr(self.customer, 'get_discount'):
            discount = self.customer.get_discount(total_cost)
        final_cost = total_cost - discount
        reward = 0
        if hasattr(self.customer, 'get_reward'):
            reward = self.customer.get_reward(final_cost)
        return total_cost, discount, final_cost, reward
