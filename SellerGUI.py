import tkinter as tk
from tkinter import messagebox, simpledialog
import pymysql

class SellerGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Auction Seller")

        self.userIdField = tk.Entry(self.root)
        self.itemNameField = tk.Entry(self.root)
        self.itemDescField = tk.Entry(self.root)
        self.baseBidField = tk.Entry(self.root)
        self.bidTimeField = tk.Entry(self.root)

        submitButton = tk.Button(self.root, text="Submit", command=self.insertItemToDatabase)

        tk.Label(self.root, text="Enter the user ID: ").pack()
        self.userIdField.pack()
        tk.Label(self.root, text="Enter the item name: ").pack()
        self.itemNameField.pack()
        tk.Label(self.root, text="Enter item description: ").pack()
        self.itemDescField.pack()
        tk.Label(self.root, text="Enter the base bid amount: ").pack()
        self.baseBidField.pack()
        tk.Label(self.root, text="Enter the time period of the bid (in days): ").pack()
        self.bidTimeField.pack()
        submitButton.pack()

        self.connection = pymysql.connect(host='localhost',
                                          user='root',
                                          password='123456789',
                                          db='seller_details')

    def insertItemToDatabase(self):
        try:
            with self.connection.cursor() as cursor:
                query = "INSERT INTO new_table (user_id, item_name, item_des, base_price, time_period) VALUES (%s, %s, %s, %s, %s)"
                values = (self.userIdField.get(), self.itemNameField.get(), self.itemDescField.get(), int(self.baseBidField.get()), int(self.bidTimeField.get()))
                cursor.execute(query, values)
                self.connection.commit()
                messagebox.showinfo("Success", "The item has been added to the database.")
        except Exception as e:
            print(e)
            messagebox.showerror("Error", "Error occurred while adding item to the database.")

    def run(self):
        self.root.mainloop()

    def __del__(self):
        self.connection.close()

def monitor(userId):
    try:
        connection = pymysql.connect(host='localhost',
                                     user='root',
                                     password='123456789',
                                     db='seller_details')
        with connection.cursor() as cursor:
            sql = "SELECT * FROM buyer_details WHERE item_id = %s"
            cursor.execute(sql, userId)
            result = cursor.fetchone()

            if result:
                itemId, buyerUserId, buyerName, bidAmount = result
                messagebox.showinfo("Item Details", f"Item ID: {itemId}\nBuyer User ID: {buyerUserId}\nBuyer Name: {buyerName}\nBid Amount: {bidAmount}")
            else:
                messagebox.showinfo("Item Not Found", "Item not found.")
    except Exception as e:
        print(e)
        messagebox.showerror("Error", "Error occurred while monitoring item.")
    finally:
        connection.close()

def main():
    choice = messagebox.askquestion("Menu", "Select an option: Add Item or Monitor Items")

    if choice == "yes":
        gui = SellerGUI()
        gui.run()
    elif choice == "no":
        userId = simpledialog.askstring("Monitor Items", "Enter User ID to monitor:")
        if userId:
            monitor(userId)
        else:
            messagebox.showerror("Invalid User ID", "Invalid User ID.")
    else:
        messagebox.showerror("Invalid Option", "Invalid option or dialog closed.")

if __name__ == "__main__":
    main()
