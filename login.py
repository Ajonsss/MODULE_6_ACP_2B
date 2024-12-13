import tkinter as tk
from tkinter import messagebox

import mysql.connector
from mysql.connector import Error
from session import UserSession  # Import UserSession from session.py
from dashboard import DashboardApp  # Import DashboardApp

def validate_login():
    username = username_entry.get()
    password = password_entry.get()

    if not username or not password:
        messagebox.showwarning("Input Error", "Username and password are required.")
        return

    try:
        connection = mysql.connector.connect(
            host='localhost', user='root', password='May12003', database='project'
        )

        if connection.is_connected():
            cursor = connection.cursor()
            query = "SELECT * FROM register WHERE Username = %s AND Password = %s"
            cursor.execute(query, (username, password))
            result = cursor.fetchone()

            if result:
                UserSession.set_logged_in_username(username)
                messagebox.showinfo("Login Success", "Login successful!")

                # Launch Dashboard
                login_window.destroy()  # Close login window
                root = tk.Tk()  # Create a new Tkinter root for the dashboard
                app = DashboardApp(root)  # Start the dashboard
                root.mainloop()
            else:
                messagebox.showerror("Login Error", "Invalid username or password.")
    except Error as e:
        messagebox.showerror("Database Error", f"Error: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


def create_login_window():
    global username_entry, password_entry, login_window
    login_window = tk.Tk()
    login_window.title("Login")
    login_window.geometry("400x300")

    username_label = tk.Label(login_window, text="Username:")
    username_label.pack(pady=10)
    username_entry = tk.Entry(login_window)
    username_entry.pack(pady=10)

    password_label = tk.Label(login_window, text="Password:")
    password_label.pack(pady=10)
    password_entry = tk.Entry(login_window, show="*")
    password_entry.pack(pady=10)

    login_button = tk.Button(login_window, text="Login", command=validate_login)
    login_button.pack(pady=20)

    login_window.mainloop()


if __name__ == "__main__":
    create_login_window()
