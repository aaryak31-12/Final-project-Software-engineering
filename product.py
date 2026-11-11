"""Simple validation and the dictionary used to represent one product."""

# SQLite can store whole numbers up to this size.
MAX_NUMBER = 9223372036854775807


def check_text(value, field_name):
    # A name, ID, or category must contain some text.
    if not isinstance(value, str):
        raise ValueError(field_name + " must be text.")

    value = value.strip()  # Remove spaces at the start and end.

    if value == "":
        raise ValueError(field_name + " cannot be empty.")

    return value


def check_number(value, field_name, allow_zero=True):
    # The GUI might send a number as text, such as "12".
    if type(value) == int:
        number = value
    elif isinstance(value, str) and value.strip().isascii() and value.strip().isdigit():
        number = int(value.strip())
    else:
        raise ValueError(field_name + " must be a whole number.")

    if number < 0:
        raise ValueError(field_name + " cannot be negative.")

    if not allow_zero and number == 0:
        raise ValueError(field_name + " must be greater than zero.")

    if number > MAX_NUMBER:
        raise ValueError(field_name + " is too large.")

    return number


def row_to_product(row):
    # Return None when the requested product does not exist.
    if row is None:
        return None

    # Each product is a plain dictionary, easy for the GUI to read.
    product = {
        "product_id": row["product_id"],
        "name": row["name"],
        "category": row["category"],
        "quantity": row["quantity"],
        "low_stock_threshold": row["low_stock_threshold"]
    }

    # A product is low stock when its quantity is at or below the threshold.
    if product["quantity"] <= product["low_stock_threshold"]:
        product["is_low_stock"] = True
        product["status"] = "Low Stock"
    else:
        product["is_low_stock"] = False
        product["status"] = "In Stock"

    return product