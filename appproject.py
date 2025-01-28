import tkinter as tk
from user_login import SignUpGUI
from data_link import LoginGUI, DataLink

def main():
    window = tk.Tk()
    window.title("Online Auction")
    window.geometry("300x200")

    welcome_label = tk.Label(window, text="Welcome to Online Auction")
    welcome_label.pack(side=tk.TOP, pady=10)

    new_user_label = tk.Label(window, text="Are you a new user?")
    new_user_label.pack(side=tk.TOP, pady=10)

    button_frame = tk.Frame(window)
    button_frame.pack(side=tk.TOP, pady=10)

    data_link = DataLink()  # Create an instance of DataLink

    def open_sign_up_page():
        sign_up_page = SignUpGUI(data_link)
        sign_up_page.show_sign_up_page()  # Display the sign-up page
        window.withdraw()  # Hide the main window

    def open_login_page():
        login_page = LoginGUI(data_link)
        login_page.show_login_page()  # Display the login page
        window.withdraw()  # Hide the main window

    yes_button = tk.Button(button_frame, text="Yes", command=open_sign_up_page)
    yes_button.pack(side=tk.LEFT, padx=10)

    no_button = tk.Button(button_frame, text="No", command=open_login_page)
    no_button.pack(side=tk.RIGHT, padx=10)

    window.protocol("WM_DELETE_WINDOW", window.quit)  # Handle window close event
    window.mainloop()

if __name__ == "__main__":
    main()
