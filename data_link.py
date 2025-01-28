import subprocess
import tkinter as tk
from tkinter import messagebox
import mysql.connector

class DataLink:
    def __init__(self):
        self.connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="123456789",
            database="app_users"
        )
        self.cursor = self.connection.cursor()

class SignUpGUI:
    def __init__(self, data_link):
        self.data_link = data_link
        self.signwin = tk.Tk()
        self.signwin.title("Sign Up")

        self.userIdLabel = tk.Label(self.signwin, text="Enter User ID:")
        self.userIdLabel.grid(row=0, column=0)
        self.userIdField = tk.Entry(self.signwin)
        self.userIdField.grid(row=0, column=1)

        self.nameLabel = tk.Label(self.signwin, text="Enter Your Name:")
        self.nameLabel.grid(row=1, column=0)
        self.nameField = tk.Entry(self.signwin)
        self.nameField.grid(row=1, column=1)

        self.passwordLabel = tk.Label(self.signwin, text="Enter Password:")
        self.passwordLabel.grid(row=2, column=0)
        self.passwordField = tk.Entry(self.signwin, show="*")
        self.passwordField.grid(row=2, column=1)

        self.mobileLabel = tk.Label(self.signwin, text="Enter Mobile Number:")
        self.mobileLabel.grid(row=3, column=0)
        self.mobileField = tk.Entry(self.signwin)
        self.mobileField.grid(row=3, column=1)

        self.addressLabel = tk.Label(self.signwin, text="Enter Address:")
        self.addressLabel.grid(row=4, column=0)
        self.addressField = tk.Entry(self.signwin)
        self.addressField.grid(row=4, column=1)

        self.emailLabel = tk.Label(self.signwin, text="Enter Email:")
        self.emailLabel.grid(row=5, column=0)
        self.emailField = tk.Entry(self.signwin)
        self.emailField.grid(row=5, column=1)

        self.userTypeLabel = tk.Label(self.signwin, text="Select User Type:")
        self.userTypeLabel.grid(row=6, column=0)
        self.userTypeComboBox = tk.StringVar(self.signwin)
        self.userTypeComboBox.set("seller")
        self.userTypeMenu = tk.OptionMenu(self.signwin, self.userTypeComboBox, "seller", "buyer")
        self.userTypeMenu.grid(row=6, column=1)

        self.signUpButton = tk.Button(self.signwin, text="Sign Up", command=self.sign_up)
        self.signUpButton.grid(row=7, columnspan=2)

    def sign_up(self):
        id = self.userIdField.get()
        name = self.nameField.get()
        userPassword = self.passwordField.get()
        mobile = self.mobileField.get()
        address = self.addressField.get()
        email = self.emailField.get()
        userType = self.userTypeComboBox.get()

        try:
            self.data_link.cursor.execute(
                "INSERT INTO user_details (user_id, user_name, password, phone_num, address, email, user_type) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                (id, name, userPassword, mobile, address, email, userType)
            )
            self.data_link.connection.commit()
            messagebox.showinfo("Sign Up successful!", "Sign Up successful.")
            self.signwin.destroy()  # Close the sign-up window
            login_gui = LoginGUI(self.data_link)
            login_gui.show_login_page()
        except Exception as e:
            print(e)
            messagebox.showerror("Error", "Registration failed. Please try again.")

class LoginGUI:
    def __init__(self, data_link):
        self.data_link = data_link
        self.loginFrame = tk.Tk()
        self.loginFrame.title("Login")

        self.userIdLabel = tk.Label(self.loginFrame, text="Enter User ID:")
        self.userIdLabel.grid(row=0, column=0)
        self.userIdField = tk.Entry(self.loginFrame)
        self.userIdField.grid(row=0, column=1)

        self.passwordLabel = tk.Label(self.loginFrame, text="Enter Password:")
        self.passwordLabel.grid(row=1, column=0)
        self.passwordField = tk.Entry(self.loginFrame, show="*")
        self.passwordField.grid(row=1, column=1)

        self.loginButton = tk.Button(self.loginFrame, text="Login", command=self.login)
        self.loginButton.grid(row=2, columnspan=2)

    def show_login_page(self):
        self.loginFrame.deiconify()

    def login(self):
        id = self.userIdField.get()
        password = self.passwordField.get()

        try:
            self.data_link.cursor.execute(
                "SELECT * FROM user_details WHERE user_id = %s AND password = %s",
                (id, password)
            )
            user = self.data_link.cursor.fetchone()
            if user:
                user_type = user[6]
                if user_type == "buyer":
                    messagebox.showinfo("Login successful!", "Login successful! User is a buyer.")
                    # Add code to open the buyer page
                    subprocess.run(["python","BuyerGUI.py"])
                elif user_type == "seller":
                    messagebox.showinfo("Login successful!", "Login successful! User is a seller.")
                    subprocess.run(["python","SellerGUI.py"])
            else:
                messagebox.showerror("Invalid credentials", "Invalid user ID or password.")
        except Exception as e:
            print(e)

if __name__ == "__main__":
    data_link = DataLink()
    signup_gui = SignUpGUI(data_link)

    main_window = tk.Tk()
    main_window.title("Online Auction")
    main_window.geometry("300x200")

    welcome_label = tk.Label(main_window, text="Welcome to Online Auction")
    welcome_label.pack(side=tk.TOP, pady=10)

    new_user_label = tk.Label(main_window, text="Are you a new user?")
    new_user_label.pack(side=tk.TOP, pady=10)

    button_frame = tk.Frame(main_window)
    button_frame.pack(side=tk.TOP, pady=10)

    yes_button = tk.Button(button_frame, text="Yes", command=signup_gui.signwin.deiconify)
    yes_button.pack(side=tk.LEFT, padx=10)

    login_gui = LoginGUI(data_link)
    no_button = tk.Button(button_frame, text="No", command=login_gui.show_login_page)
    no_button.pack(side=tk.RIGHT, padx=10)

    main_window.protocol("WM_DELETE_WINDOW", main_window.quit)  # Handle window close event
    main_window.mainloop()
