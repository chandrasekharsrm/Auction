import tkinter as tk
from tkinter import messagebox
import mysql.connector
from tkinter import ttk

def fetch_items_from_database(table):
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="123456789",
            database="seller_details"
        )
        cursor = conn.cursor()
        query = "SELECT user_id, item_name, item_des, base_price, time_period FROM new_table"
        cursor.execute(query)
        for row in cursor.fetchall():
            table.insert('', 'end', values=row)
        cursor.close()
        conn.close()
    except mysql.connector.Error as e:
        messagebox.showerror("Error", f"Failed to fetch items from the database: {str(e)}")

def get_base_price_from_database(con, user_id):
    try:
        query = "SELECT base_price FROM new_table WHERE user_id = %s"
        with con.cursor() as cursor:
            cursor.execute(query, (user_id,))
            result = cursor.fetchone()
            if result is not None:
                return result[0]
            else:
                raise Exception("Item not found in the database.")
    except Exception as e:
        raise e

def update_base_price_in_database(con, user_id, new_price):
    try:
        query = "UPDATE new_table SET base_price = %s WHERE user_id = %s"
        query1 = "UPDATE buyer_details SET bid_amount = %s WHERE item_id = %s"
        with con.cursor() as cursor:
            cursor.execute(query, (new_price, user_id))
            con.commit()
            if cursor.rowcount == 0:
                raise Exception("Failed to update base price.")
            cursor.execute(query1, (new_price, user_id))
            con.commit()
            if cursor.rowcount == 0:
                raise Exception("Failed to update base price.")
    except Exception as e:
        raise e

def place_bid():
    item_id = item_id_entry.get()
    buyer_id = buyer_id_entry.get()
    buyer_name = buyer_name_entry.get()
    bid_amount = float(bid_amount_entry.get())

    try:
        con = mysql.connector.connect(
            host="localhost",
            user="root",
            password="123456789",
            database="seller_details"
        )
        base_price = get_base_price_from_database(con, item_id)

        if bid_amount > base_price:
            update_base_price_in_database(con, item_id, bid_amount)
            messagebox.showinfo("Bid Placed", "Bid placed successfully!")
        else:
            messagebox.showerror("Invalid Bid", "Bid amount should be greater than the base price.")

        con.close()
    except mysql.connector.Error as e:
        messagebox.showerror("Error", f"Failed to place the bid: {str(e)}")

# Create the main application window
root = tk.Tk()
root.title("Auction Buyer")
root.geometry("600x400")

# Create and place a table
columns = ("User ID", "Item Name", "Item Description", "Base Price", "Time Period")
table = ttk.Treeview(root, columns=columns, show="headings")
for col in columns:
    table.heading(col, text=col)
table.pack()

# Fetch items from the database and populate the table
fetch_items_from_database(table)

# Create and place input fields and buttons
form_panel = tk.Frame(root)
form_panel.pack()

item_id_label = tk.Label(form_panel, text="Item ID:")
item_id_label.grid(row=0, column=0)
item_id_entry = tk.Entry(form_panel)
item_id_entry.grid(row=0, column=1)

buyer_id_label = tk.Label(form_panel, text="Your ID:")
buyer_id_label.grid(row=1, column=0)
buyer_id_entry = tk.Entry(form_panel)
buyer_id_entry.grid(row=1, column=1)

buyer_name_label = tk.Label(form_panel, text="Your Name:")
buyer_name_label.grid(row=2, column=0)
buyer_name_entry = tk.Entry(form_panel)
buyer_name_entry.grid(row=2, column=1)

bid_amount_label = tk.Label(form_panel, text="Bid Amount:")
bid_amount_label.grid(row=3, column=0)
bid_amount_entry = tk.Entry(form_panel)
bid_amount_entry.grid(row=3, column=1)

place_bid_button = tk.Button(form_panel, text="Place Bid", command=place_bid)
place_bid_button.grid(row=4, column=0, columnspan=2)

root.mainloop()
