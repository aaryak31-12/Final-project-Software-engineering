"""Simple inventory operations used by the GUI."""

import sqlite3

from database import create_database, get_connection
from product import check_text, check_number, row_to_product


class InventoryManager:
    def __init__(self, database_file=None):
        # Use one database file for all the inventory operations.
        self.database_file = database_file

        # Create the products table the first time the program runs.
        create_database(self.database_file)

    # FR-01 and FR-05: Add a product and reject duplicate IDs.
    def add_product(self, product_id, name, category, quantity, low_stock_threshold):
        # Check inputs before trying to save them.
        product_id = check_text(product_id, "Product ID")
        name = check_text(name, "Product name")
        category = check_text(category, "Category")
        quantity = check_number(quantity, "Quantity")
        low_stock_threshold = check_number(low_stock_threshold, "Low-stock threshold")

        connection = get_connection(self.database_file)
        try:
            # Question marks safely pass values to SQLite.
            connection.execute("""
                INSERT INTO products
                (product_id, name, category, quantity, low_stock_threshold)
                VALUES (?, ?, ?, ?, ?)
            """, (product_id, name, category, quantity, low_stock_threshold))

            connection.commit()  # Make the saved product permanent.
        except sqlite3.IntegrityError:
            raise ValueError("A product with ID '" + product_id + "' already exists.")
        finally:
            connection.close()

        return self.get_product(product_id)

    # Find one product using its unique ID.
    def get_product(self, product_id):
        product_id = check_text(product_id, "Product ID")
        connection = get_connection(self.database_file)
        try:
            row = connection.execute(
                "SELECT * FROM products WHERE product_id = ?", (product_id,)
            ).fetchone()
        finally:
            connection.close()

        return row_to_product(row)

    # FR-02: Get all products so the GUI can show them in a table.
    def get_all_products(self):
        connection = get_connection(self.database_file)
        try:
            rows = connection.execute(
                "SELECT * FROM products ORDER BY name COLLATE NOCASE"
            ).fetchall()
        finally:
            connection.close()

        products = []
        for row in rows:
            products.append(row_to_product(row))

        return products

    # FR-03: Edit information, but never change the product ID.
    def edit_product(self, product_id, name=None, category=None,
                     quantity=None, low_stock_threshold=None):
        product = self.get_product(product_id)
        if product is None:
            raise ValueError("Product not found: " + product_id)

        # If the GUI leaves a field unchanged, keep its old value.
        if name is None:
            name = product["name"]
        if category is None:
            category = product["category"]
        if quantity is None:
            quantity = product["quantity"]
        if low_stock_threshold is None:
            low_stock_threshold = product["low_stock_threshold"]

        # Validate all final values.
        name = check_text(name, "Product name")
        category = check_text(category, "Category")
        quantity = check_number(quantity, "Quantity")
        low_stock_threshold = check_number(low_stock_threshold, "Low-stock threshold")

        connection = get_connection(self.database_file)
        try:
            connection.execute("""
                UPDATE products
                SET name = ?, category = ?, quantity = ?, low_stock_threshold = ?
                WHERE product_id = ?
            """, (name, category, quantity, low_stock_threshold, product_id))
            connection.commit()
        finally:
            connection.close()

        return self.get_product(product_id)

    # FR-04: A product can be deleted only when quantity equals zero.
    def remove_product(self, product_id):
        product = self.get_product(product_id)
        if product is None:
            raise ValueError("Product not found: " + product_id)
        if product["quantity"] != 0:
            raise ValueError("Reduce this product's quantity to 0 before deleting it.")

        connection = get_connection(self.database_file)
        try:
            # The quantity check in SQL adds another safeguard.
            cursor = connection.execute(
                "DELETE FROM products WHERE product_id = ? AND quantity = 0",
                (product_id,)
            )
            if cursor.rowcount == 0:
                raise ValueError("Product could not be deleted. Check its quantity.")
            connection.commit()
        finally:
            connection.close()

        return True

    # FR-06: Add received stock to an existing product.
    def increase_stock(self, product_id, amount):
        amount = check_number(amount, "Amount", allow_zero=False)
        product = self.get_product(product_id)
        if product is None:
            raise ValueError("Product not found: " + product_id)

        new_quantity = product["quantity"] + amount
        new_quantity = check_number(new_quantity, "New quantity")

        # Reuse the edit method to save the changed quantity.
        return self.edit_product(product_id, quantity=new_quantity)

    # FR-07 to FR-09: Remove stock without allowing a negative quantity.
    def decrease_stock(self, product_id, amount):
        amount = check_number(amount, "Amount", allow_zero=False)
        product = self.get_product(product_id)
        if product is None:
            raise ValueError("Product not found: " + product_id)

        if amount > product["quantity"]:
            raise ValueError(
                "Not enough stock. Only " + str(product["quantity"]) + " available."
            )

        new_quantity = product["quantity"] - amount
        return self.edit_product(product_id, quantity=new_quantity)

    # FR-10 to FR-11: Search, filter, and show low-stock products.
    def list_products(self, search="", category=None, low_stock_only=False):
        if not isinstance(search, str):
            raise ValueError("Search text must be text.")
        if category is not None and not isinstance(category, str):
            raise ValueError("Category filter must be text.")

        search = search.strip().lower()
        if category is not None:
            category = category.strip().lower()

        matching_products = []

        for product in self.get_all_products():
            # Skip products that do not contain the search word in their ID or name.
            if search != "":
                name_match = search in product["name"].lower()
                id_match = search in product["product_id"].lower()
                if not name_match and not id_match:
                    continue

            # Skip products outside the selected category.
            if category is not None and category != "":
                if product["category"].lower() != category:
                    continue

            # When requested, keep only products that are low in stock.
            if low_stock_only and not product["is_low_stock"]:
                continue

            matching_products.append(product)

        return matching_products

    def search_products(self, text):
        return self.list_products(search=text)

    def filter_products(self, category):
        return self.list_products(category=category)

    def get_low_stock_products(self):
        return self.list_products(low_stock_only=True)

    # Return unique categories for a GUI dropdown.
    def get_categories(self):
        categories = []
        for product in self.get_all_products():
            if product["category"] not in categories:
                categories.append(product["category"])
        categories.sort()
        return categories

    # FR-12: Calculate the three dashboard numbers using a simple loop.
    def get_dashboard_stats(self):
        products = self.get_all_products()
        total_quantity = 0
        low_stock_count = 0

        for product in products:
            total_quantity = total_quantity + product["quantity"]
            if product["is_low_stock"]:
                low_stock_count = low_stock_count + 1

        return {
            "total_products": len(products),
            "total_inventory_quantity": total_quantity,
            "low_stock_products": low_stock_count
        }