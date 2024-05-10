class Customer:
    def __init__(self, ID, name, reward):
        self.id = ID
        self.name = name
        self.reward = reward

    def get_ID(self):
        return self.id

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