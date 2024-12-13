# Project README

## Project Overview

This project is a Python-based graphical user interface (GUI) application that provides a registration and login system with a dashboard for managing and displaying user-specific data. The application leverages Tkinter for the GUI and MySQL for data storage.

---

## Features

1. *User Registration*
   - Allows new users to register with a username and password.
   - Stores user credentials in a MySQL database.

2. *User Login*
   - Authenticates users using their registered username and password.
   - Redirects users to the dashboard upon successful login.

3. *Dashboard*
   - Provides a multi-tab interface for users to manage their accounts and data.
   - Includes tabs for:
     - ACCOUNTS: Displays user-specific data.
     - QC: Allows users to submit and manage Quality Control (QC) information.
     - DASHBOARD: Displays a content calendar with various data.

---

## File Descriptions

### 1. mysql_connector.py

This script contains functionality to establish and manage a connection to a MySQL database.

#### Key Functions:

- **connect_to_database()**:
  - Connects to the MySQL database using the specified credentials and database name.
  - Prints messages indicating the success or failure of the connection.
  - Returns a mysql.connector connection object if the connection is successful; otherwise, returns None.

#### Configuration:

Replace the placeholder values in the connect_to_database function with your actual database credentials:

- host: Database host (e.g., localhost or a remote address).
- user: Your MySQL username.
- password: Your MySQL password.
- database: The name of the database to connect to.

#### Usage:

Execute the script to test the database connection:

python mysql_connector.py

---

### 2. session.py

This script provides a simple static class for managing user session information.

#### Key Components:

- **Class: UserSession**:
  - *Static Methods:*
    - set_logged_in_username(username): Sets the logged-in username.
    - get_logged_in_username(): Retrieves the currently logged-in username.
    - clear(): Clears the logged-in username.

#### Usage Example:

from session import UserSession

# Set a username for the session
UserSession.set_logged_in_username("JohnDoe")

# Retrieve the logged-in username
username = UserSession.get_logged_in_username()
print(f"Logged in user: {username}")

# Clear the session
UserSession.clear()

---

### 3. login.py

- Handles user authentication.
- Opens the dashboard upon successful login.
- Provides error handling for invalid credentials and database connection issues.

### 4. register.py

- Manages user registration.
- Provides input validation and error handling.
- Includes a hyperlink to navigate to the login window.

### 5. dashboard.py

- Implements the dashboard interface.
- Displays and allows manipulation of user and QC data.
- Provides features like tab switching, data submission, and database updates.

---

## Requirements

- Python 3.8 or higher
- MySQL database
- Python Libraries:
  - tkinter: For GUI development.
  - mysql-connector: For MySQL database connection.
  - subprocess: To run external scripts.

## Setup

1. *Database Setup*
   - Create a MySQL database named project.
   - Add the following tables:
     - register: For storing user credentials (Username, Password).
     - contentcalendardb: For storing dashboard data (client_name, file_link, Username, month, etc.).

2. *Clone Repository*
   - Clone or download the project files to your local system.

3. *Install Dependencies*
   - Install required Python libraries using pip:

     
pip install mysql-connector-python

4. *Run the Application*
   - Start the registration window by running register.py:

     
python register.py

5. Replace placeholder values in mysql_connector.py with your database credentials.

6. Ensure all scripts are in the same project directory.

## Usage

1. Launch the application by running register.py.
2. Register a new user or log in with existing credentials.
3. Access the dashboard to manage and view user-specific and QC-related data.

---

## Security Considerations

- *Password Storage*: Currently, passwords are stored in plain text. It is highly recommended to implement password hashing (e.g., using bcrypt or hashlib) for secure storage.
- *Database Credentials*: Ensure sensitive database credentials are not hardcoded and use environment variables or configuration files instead.

---

## Future Improvements

1. Implement secure password storage with hashing.
2. Enhance input validation and error handling.
3. Improve the dashboard layout and user experience.
4. Add role-based access control for different user types.

---

## Contact
For questions or contributions, please contact: Group Members:
Patal, Mark Angelo (09951638329)
Haboc, David Emanuel (09266222452)
Ajon, Andrae (099249569430)
