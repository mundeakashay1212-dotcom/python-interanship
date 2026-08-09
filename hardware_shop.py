# Hardware Shop Management System

products = {
    1: {"name": "Hammer", "price": 250},
    2: {"name": "Screwdriver", "price": 120},
    3: {"name": "Plier", "price": 180},
    4: {"name": "Drill Machine", "price": 2500},
    5: {"name": "Nails (1 kg)", "price": 100},
    6: {"name": "Screws (1 box)", "price": 150},
    7: {"name": "PVC Pipe", "price": 300},
    8: {"name": "Measuring Tape", "price": 200}
}

cart = []


def show_products():
    print("\n========== HARDWARE SHOP ==========")
    print("No.  Product              Price")
    print("----------------------------------")

    for number, product in products.items():
        print(f"{number:<4} {product['name']:<20} ₹{product['price']}")

    print("----------------------------------")


def add_to_cart():
    show_products()

    try:
        choice = int(input("Enter product number: "))

        if choice not in products:
            print("Invalid product number!")
            return

        quantity = int(input("Enter quantity: "))

        if quantity <= 0:
            print("Quantity must be greater than 0!")
            return

        product = products[choice]

        cart.append({
            "name": product["name"],
            "price": product["price"],
            "quantity": quantity
        })

        print("Product added to cart successfully!")

    except ValueError:
        print("Please enter a valid number.")


def print_bill():
    if not cart:
        print("\nCart is empty!")
        return

    print("\n\n========== HARDWARE SHOP BILL ==========")
    print("Product              Qty    Price")
    print("----------------------------------------")

    total = 0

    for item in cart:
        amount = item["price"] * item["quantity"]
        total += amount

        print(
            f"{item['name']:<20} "
            f"{item['quantity']:<6} "
            f"₹{amount}"
        )

    print("----------------------------------------")
    print(f"Total Amount: ₹{total}")
    print("========================================")
    print("Thank you for shopping with us!")


def main():
    while True:
        print("\n========== MAIN MENU ==========")
        print("1. View Products")
        print("2. Add Product to Cart")
        print("3. Print Bill")
        print("4. Exit")
        print("===============================")

        choice = input("Enter your choice: ")

        if choice == "1":
            show_products()

        elif choice == "2":
            add_to_cart()

        elif choice == "3":
            print_bill()

        elif choice == "4":
            print("Thank you! Visit again.")
            break

        else:
            print("Invalid choice! Please try again.")


main()