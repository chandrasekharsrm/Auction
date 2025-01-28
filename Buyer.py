import mysql.connector

def place_bid(con, item_id, buyer_id, buyer_name, bid_amount):
    def get_base_price_from_database(con, item_id):
        query = "SELECT base_price FROM new_table WHERE user_id = %s"
        with con.cursor() as cursor:
            cursor.execute(query, (item_id,))
            result = cursor.fetchone()
            if result:
                return result[0]
            else:
                raise ValueError("Item not found in the database.")

    def update_base_price_in_database(con, item_id, new_price):
        query = "UPDATE new_table SET base_price = %s WHERE user_id = %s"
        with con.cursor() as cursor:
            cursor.execute(query, (new_price, item_id))
            if cursor.rowcount == 0:
                raise ValueError("Failed to update base price.")

    def store_buyer_details(con, item_id, buyer_id, buyer_name, bid_amount):
        query = "INSERT INTO buyer_details (item_id, user_id, buyer_name, bid_amount) VALUES (%s, %s, %s, %s)"
        with con.cursor() as cursor:
            cursor.execute(query, (item_id, buyer_id, buyer_name, bid_amount))

    base_price = get_base_price_from_database(con, item_id)
    if bid_amount > base_price:
        update_base_price_in_database(con, item_id, bid_amount)
        store_buyer_details(con, item_id, buyer_id, buyer_name, bid_amount)
    else:
        raise ValueError("Bid amount should be greater than the base price.")

# Assuming you have established a MySQL connection (con) before calling the function
place_bid(con,"item123", "buyer456", "John Doe", 150.0)
