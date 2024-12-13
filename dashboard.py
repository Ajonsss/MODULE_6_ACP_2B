import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import mysql.connector
from mysql.connector import Error
from session import UserSession  # Import UserSession from session.py

class DashboardApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Dashboard")
        self.root.geometry("800x600")  # Adjusted size for better layout

        # Creating a frame for the buttons on the left side
        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack(side="left", fill="y", padx=10, pady=10)

        # Create Buttons to Switch Tabs
        self.create_buttons()

        # Creating the Notebook widget to handle tab switching
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(side="right", fill="both", expand=True)

        # Creating the tabs (frames)
        self.accounts_frame = ttk.Frame(self.notebook)
        self.dashboard_frame = ttk.Frame(self.notebook)
        self.qc_frame = self.create_qc_tab(self.notebook)  # Create the QC tab

        # Add tabs to the notebook
        self.notebook.add(self.accounts_frame, text="ACCOUNTS")
        self.notebook.add(self.qc_frame, text="QC")
        self.notebook.add(self.dashboard_frame, text="DASHBOARD")

        # Add tables to the Dashboard tab
        self.create_dashboard_tables()

        # Create table for Accounts tab
        self.create_accounts_table()

        # Bind tab change to refresh the dashboard
        self.notebook.bind("<<NotebookTabChanged>>", self.on_tab_change)

        # Fetch data for the logged-in user
        self.fetch_data_for_logged_in_user()

        # Bind double-click event to allow editing the "File Link"
        self.content_calendar_table.bind("<Double-1>", self.on_item_double_click)

    def create_buttons(self):
        """Create the buttons to switch between tabs."""
        accounts_button = tk.Button(
            self.button_frame, text="ACCOUNTS", width=20, command=lambda: self.switch_tab(self.accounts_frame)
        )
        accounts_button.pack(pady=10)

        qc_button = tk.Button(
            self.button_frame, text="QC", width=20, command=lambda: self.switch_tab(self.qc_frame)
        )
        qc_button.pack(pady=10)

        dashboard_button = tk.Button(
            self.button_frame, text="DASHBOARD", width=20, command=lambda: self.switch_tab(self.dashboard_frame)
        )
        dashboard_button.pack(pady=10)

    def switch_tab(self, frame):
        """Switch the current tab to the specified frame."""
        self.notebook.select(frame)

    def create_dashboard_tables(self):
        """Create tables in the dashboard tab to display contentcalendardb."""
        self.content_calendar_table = ttk.Treeview(
            self.dashboard_frame,
            columns=("Client Name", "File Link", "Member Assigned", "Month"),
            show="headings",
        )
        self.content_calendar_table.pack(fill="both", expand=True, padx=10, pady=10)

        for col in ["Client Name", "File Link", "Member Assigned", "Month"]:
            self.content_calendar_table.heading(col, text=col)
            self.content_calendar_table.column(col, width=150)

    def create_accounts_table(self):
        """Create a table in the accounts tab to display user-specific data."""
        self.accounts_table = ttk.Treeview(
            self.accounts_frame,
            columns=("Client Name", "File Link", "Username", "Month", "Remarks"),
            show="headings",
        )
        self.accounts_table.pack(fill="both", expand=True, padx=10, pady=10)

        for col in ["Client Name", "File Link", "Username", "Month", "Remarks"]:
            self.accounts_table.heading(col, text=col)
            self.accounts_table.column(col, width=150)

    def create_qc_tab(self, parent):
        """Creates the QC tab and all necessary components."""
        qc_frame = ttk.Frame(parent)

        # Labels and Entry fields for Client's Name, Member Assigned, and File Link
        tk.Label(qc_frame, text="Client's Name:").pack(pady=5)
        client_name_entry = tk.Entry(qc_frame, width=30)
        client_name_entry.pack(pady=5)

        tk.Label(qc_frame, text="Member Assigned:").pack(pady=5)
        member_assigned_entry = tk.Entry(qc_frame, width=30)
        member_assigned_entry.pack(pady=5)

        tk.Label(qc_frame, text="File Link:").pack(pady=5)
        file_link_entry = tk.Entry(qc_frame, width=30)
        file_link_entry.pack(pady=5)

        # Combobox for Month Selection
        tk.Label(qc_frame, text="Select Month:").pack(pady=5)
        months = [
            "January", "February", "March", "April", "May", "June", "July",
            "August", "September", "October", "November", "December"
        ]
        month_combobox = ttk.Combobox(qc_frame, values=months, state="readonly", width=28)
        month_combobox.pack(pady=5)

        # Submit Button
        submit_button = tk.Button(qc_frame, text="Submit", command=lambda: self.submit_qc_data(
            client_name_entry, member_assigned_entry, file_link_entry, month_combobox
        ))
        submit_button.pack(pady=20)

        return qc_frame

    def submit_qc_data(self, client_name_entry, member_assigned_entry, file_link_entry, month_combobox):
        """Submit the data from the form to the contentcalendardb table."""
        client_name = client_name_entry.get()
        member_assigned = member_assigned_entry.get()
        file_link = file_link_entry.get()
        month = month_combobox.get()

        # Check if any field is empty
        if not client_name or not member_assigned or not file_link or not month:
            messagebox.showwarning("Input Error", "All fields are required.")
            return

        try:
            # Establish connection to the database
            connection = mysql.connector.connect(
                host='localhost', user='root', password='May12003', database='project'
            )

            if connection.is_connected():
                cursor = connection.cursor()
                # SQL query to insert data into contentcalendardb table
                query = """
                    INSERT INTO contentcalendardb (client_name, file_link, Username, month)
                    VALUES (%s, %s, %s, %s)
                """
                # Using the logged-in username from the session
                username = UserSession.get_logged_in_username()
                cursor.execute(query, (client_name, file_link, username, month))
                connection.commit()

                messagebox.showinfo("Success", "Data submitted successfully!")
                # Clear the form fields after submission
                client_name_entry.delete(0, tk.END)
                member_assigned_entry.delete(0, tk.END)
                file_link_entry.delete(0, tk.END)
                month_combobox.set('')
        except Error as e:
            messagebox.showerror("Database Error", f"Error: {e}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def fetch_content_calendar_data(self):
        """Fetch all data from the contentcalendardb table (including all usernames)."""
        try:
            connection = mysql.connector.connect(
                host='localhost', user='root', password='May12003', database='project'
            )
            if connection.is_connected():
                cursor = connection.cursor(dictionary=True)
                query = """
                    SELECT client_name, file_link, Username, month 
                    FROM contentcalendardb
                """
                cursor.execute(query)
                return cursor.fetchall()
        except Error as e:
            print(f"Error fetching data: {e}")
            return []
        finally:
            if connection and connection.is_connected():
                cursor.close()
                connection.close()

    def refresh_dashboard(self):
        """Clear and refresh the dashboard table with the latest data from the database."""
        # Clear current data in the table
        for row in self.content_calendar_table.get_children():
            self.content_calendar_table.delete(row)

        # Fetch new data and populate the table
        records = self.fetch_content_calendar_data()
        for row in records:
            self.content_calendar_table.insert("", "end", values=(row["client_name"], row["file_link"], row["Username"], row["month"]))

    def fetch_data_for_logged_in_user(self):
        """Fetch data for the Accounts tab based on the logged-in user."""
        logged_in_username = UserSession.get_logged_in_username()
        try:
            connection = mysql.connector.connect(
                host='localhost', user='root', password='May12003', database='project'
            )
            if connection.is_connected():
                cursor = connection.cursor()
                query = """
                    SELECT client_name, file_link, Username, month, remarks 
                    FROM contentcalendardb 
                    WHERE Username = %s
                """
                cursor.execute(query, (logged_in_username,))
                records = cursor.fetchall()

                # Clear previous table data
                for row in self.accounts_table.get_children():
                    self.accounts_table.delete(row)

                # Insert new data
                for row in records:
                    self.accounts_table.insert("", "end", values=row)

        except Error as e:
            messagebox.showerror("Database Error", f"Error fetching data: {e}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def on_item_double_click(self, event):
        """Handles double-clicks on the "File Link" column."""
        selected_item = self.content_calendar_table.selection()[0]  # Get the selected row
        col = self.content_calendar_table.identify_column(event.x)  # Get the column clicked

        if col == "#2":  # If the "File Link" column is double-clicked
            current_value = self.content_calendar_table.item(selected_item, "values")[1]  # Get the current "File Link"
            self.edit_file_link(selected_item, current_value)

    def edit_file_link(self, selected_item, current_value):
        """Edit the file link directly in the table cell."""
        # Create an Entry widget to edit the file link
        entry = tk.Entry(self.dashboard_frame)
        entry.insert(0, current_value)  # Insert current value into the Entry widget
        entry.place(x=self.content_calendar_table.bbox(selected_item, "#2")[0], y=self.content_calendar_table.bbox(selected_item, "#2")[1])

        def save_edit(event):
            new_value = entry.get()
            if new_value != current_value:
                self.update_file_link_in_db(selected_item, new_value)
                self.content_calendar_table.item(selected_item, values=(self.content_calendar_table.item(selected_item, "values")[0], new_value, self.content_calendar_table.item(selected_item, "values")[2], self.content_calendar_table.item(selected_item, "values")[3]))
            entry.destroy()  # Destroy the Entry widget after saving

        entry.bind("<Return>", save_edit)  # Save on pressing Enter
        entry.bind("<FocusOut>", lambda e: entry.destroy())  # Destroy on losing focus

    def update_file_link_in_db(self, selected_item, new_value):
        """Update the file link in the database."""
        client_name = self.content_calendar_table.item(selected_item, "values")[0]
        member_assigned = self.content_calendar_table.item(selected_item, "values")[2]
        month = self.content_calendar_table.item(selected_item, "values")[3]

        try:
            connection = mysql.connector.connect(
                host='localhost', user='root', password='May12003', database='project'
            )
            if connection.is_connected():
                cursor = connection.cursor()
                update_query = """
                    UPDATE contentcalendardb
                    SET file_link = %s
                    WHERE client_name = %s AND Username = %s AND month = %s
                """
                cursor.execute(update_query, (new_value, client_name, member_assigned, month))
                connection.commit()

                messagebox.showinfo("Success", "File Link updated successfully!")
        except Error as e:
            messagebox.showerror("Database Error", f"Error updating File Link: {e}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def on_tab_change(self, event):
        """Handle tab change event and refresh content if needed."""
        selected_tab = event.widget.tab(event.widget.index("current"), "text")
        if selected_tab == "DASHBOARD":
            self.refresh_dashboard()  # Fetch all data for the dashboard tab when selected
        elif selected_tab == "ACCOUNTS":
            self.fetch_data_for_logged_in_user()  # Fetch data for accounts tab if selected
