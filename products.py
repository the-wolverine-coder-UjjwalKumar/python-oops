class Product:
    def __init__(self, ID, name, price):
        self.ID = ID
        self.name = name
        self.price = price

    def display_info(self):
        print("Product Information:")
        print(f"ID: {self.ID}")
        print(f"Name: {self.name}")
        print(f"Price: ${self.price:.2f}")