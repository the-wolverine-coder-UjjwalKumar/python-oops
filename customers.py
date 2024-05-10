class Customer:
    def __init__(self, ID, name, reward):
        self.ID = ID
        self.name = name
        self.reward = reward

    def get_ID(self):
        return self.ID

    def get_name(self):
        return self.name

    def get_reward(self):
        pass  # Empty super method

    def get_discount(self):
        pass

    def update_reward(self):
        pass

    def display_info(self):
        pass


class BasicCustomer(Customer):
    reward_rate = 1

    def __init__(self, ID, name, reward, reward_rate=1.0):
        super().__init__(ID, name, reward)
        self.reward_rate = reward_rate

    def get_reward_rate(self):
        return self.reward_rate

    def get_reward(self, total_cost):
        return round(total_cost * self.reward_rate)

    def update_reward(self, value):
        self.reward_rate += value

    def display_info(self):
        print("Basic Customer Information:")
        print(f"ID: {self.ID}")
        print(f"Name: {self.name}")
        print(f"Reward: {self.reward}")
        print(f"Reward Rate: {self.reward_rate}")

    @classmethod
    def set_reward_rate(cls, new_rate):
        cls.reward_rate = new_rate


class VIPCustomer(Customer):
    reward_rate = 1.0  # Default reward rate for all VIP customers

    def __init__(self, ID, name, reward, reward_rate=1.0, discount_rate=0.08):
        super().__init__(ID, name, reward)
        self.reward_rate = reward_rate
        self.discount_rate = discount_rate

    def get_reward_rate(self):
        return self.reward_rate

    def get_discount_rate(self):
        return self.discount_rate

    def get_discount(self, total_cost):
        return total_cost * self.discount_rate

    def get_reward(self, total_cost):
        discounted_cost = total_cost - self.get_discount(total_cost)
        return round(discounted_cost * self.reward_rate)

    def update_reward(self, value):
        self.reward_rate += value

    def display_info(self):
        print("VIP Customer Information:")
        print(f"ID: {self.ID}")
        print(f"Name: {self.name}")
        print(f"Reward: {self.reward}")
        print(f"Reward Rate: {self.reward_rate}")
        print(f"Discount Rate: {self.discount_rate}")

    @classmethod
    def set_reward_rate(cls, new_rate):
        cls.reward_rate = new_rate

    def set_discount_rate(self, new_rate):
        self.discount_rate = new_rate
