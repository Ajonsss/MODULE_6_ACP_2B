import tkinter as tk
from tkinter import messagebox
import subprocess  # To run another Python script (login.py)
from mysql_connector import connect_to_database

def register_user(username, password):
    """Register a new user with a plain password."""
    connection = connect_to_database()
    if not connection:
        return False

    try:
        cursor = connection.cursor()
        query = "INSERT INTO register (Username, Password) VALUES (%s, %s)"
        cursor.execute(query, (username, password))  # No hashing
        connection.commit()
        return True
    except Exception as e:
        print(f"Error during registration: {e}")
        return False
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def on_register():
    """Handle the register button click."""
    username = username_entry.get()
    password = password_entry.get()

    if not username or not password:
        messagebox.showwarning("Input Error", "Please provide both a username and a password.")
        return

    success = register_user(username, password)
    if success:
        messagebox.showinfo("Registration Successful", f"User '{username}' registered successfully!")
        username_entry.delete(0, tk.END)
        password_entry.delete(0, tk.END)
    else:
        messagebox.showerror("Registration Error", "There was an error during registration.")

def open_login_window(event):
    """Open the login.py script when the hyperlink is clicked."""
    try:
        subprocess.run(["python", "login.py"], check=True)  # Will raise an error if the script fails
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", f"Failed to open login window: {e}")

# Set up the main application window
root = tk.Tk()
root.title("User Registration")
root.geometry("400x300")

# Create labels and input fields for username and password
username_label = tk.Label(root, text="Username:")
username_label.pack(pady=10)

username_entry = tk.Entry(root)
username_entry.pack(pady=10)
password_label = tk.Label(root, text="Password:")
password_label.pack(pady=10)

password_entry = tk.Entry(root, show="*")
password_entry.pack(pady=10)

# Create a register button
register_button = tk.Button(root, text="Register", command=on_register)
register_button.pack(pady=20)

# Hyperlink for login screen
login_link = tk.Label(root, text="Already have an account? Login here.", fg="blue", cursor="hand2")
login_link.pack(pady=10)
login_link.bind("<Button-1>", open_login_window)

# Start the application
root.mainloop()
