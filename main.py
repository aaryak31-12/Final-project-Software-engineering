"""Simple text menu to test the backend before the PySide6 GUI is ready."""

from inventory_backend import InventoryManager


def show_products(products):
    if len(products) == 0:
        print("No products found.")
        return

    for product in products:
        print(
            product["product_id"], "|", product["name"], "|",
            product["category"], "| Quantity:", product["quantity"],
            "| Threshold:", product["low_stock_threshold"],
            "|", product["status"]
        )


def main():
    inventory = InventoryManager()

    while True:
        print("\n=== INVENTORY MANAGEMENT SYSTEM ===")
        print("1. Add product")
        print("2. View all products")
        print("3. Edit product")
        print("4. Remove product")
        print("5. Increase stock")
        print("6. Decrease stock")
        print("7. Search products")
        print("8. Filter by category")
        print("9. Show low-stock products")
        print("10. Show dashboard")
        print("0. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "0":
            print("Goodbye!")
            break

        # Catch invalid input or inventory errors without ending the program.
        try:
            if choice == "1":
                product_id = input("Product ID: ")
                name = input("Product name: ")
                category = input("Category: ")
                quantity = input("Quantity: ")
                threshold = input("Low-stock threshold: ")
                inventory.add_product(product_id, name, category, quantity, threshold)
                print("Product added successfully.")

            elif choice == "2":
                show_products(inventory.get_all_products())

            elif choice == "3":
                product_id = input("ID of product to edit: ")
                # Blank text means keep the current value.
                name = input("New name (Enter to keep): ")
                category = input("New category (Enter to keep): ")
                quantity = input("New quantity (Enter to keep): ")
                threshold = input("New threshold (Enter to keep): ")

                if name == "":
                    name = None
                if category == "":
                    category = None
                if quantity == "":
                    quantity = None
                if threshold == "":
                    threshold = None

                inventory.edit_product(product_id, name, category, quantity, threshold)
                print("Product updated successfully.")

            elif choice == "4":
                product_id = input("Product ID to remove: ")
                confirm = input("Type YES to confirm deletion: ")
                if confirm == "YES":
                    inventory.remove_product(product_id)
                    print("Product removed successfully.")
                else:
                    print("Deletion cancelled.")

            elif choice == "5":
                product_id = input("Product ID: ")
                amount = input("Amount received: ")
                inventory.increase_stock(product_id, amount)
                print("Stock increased successfully.")

            elif choice == "6":
                product_id = input("Product ID: ")
                amount = input("Amount sold or discarded: ")
                inventory.decrease_stock(product_id, amount)
                print("Stock decreased successfully.")

            elif choice == "7":
                search = input("Search by product name or ID: ")
                show_products(inventory.search_products(search))

            elif choice == "8":
                category = input("Category (blank for all): ")
                show_products(inventory.filter_products(category))

            elif choice == "9":
                show_products(inventory.get_low_stock_products())

            elif choice == "10":
                stats = inventory.get_dashboard_stats()
                print("Total products:", stats["total_products"])
                print("Total inventory quantity:", stats["total_inventory_quantity"])
                print("Low-stock products:", stats["low_stock_products"])

            else:
                print("Please choose one of the menu options.")

        except ValueError as error:
            print("Error:", error)


if __name__ == "__main__":
    main()