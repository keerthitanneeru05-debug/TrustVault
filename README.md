# TrustVault – Secure Document Sharing

## Project Overview

TrustVault is a secure document-sharing web application developed using Python and Flask.

It allows users to register, log in, upload documents, share documents with other registered users, and securely download shared documents.

## Features

1. User Registration
2. User Login and Logout
3. Secure Password Hashing
4. Document Upload
5. My Documents
6. Document Sharing
7. Shared Documents
8. Secure Document Download
9. User Access Control
10. Audit Logs

## Technologies Used

- Python
- Flask
- SQLite
- HTML
- Werkzeug

## Project Files

- app.py – Main Flask application
- database.py – Database creation and management
- README.md – Project documentation
- uploads/ – Uploaded documents folder
- trustvault.db – SQLite database

## Installation and Setup

Step 1: Install Python on your computer.

Step 2: Open the project folder in VS Code.

Step 3: Install Flask using the terminal:

pip install flask

Step 4: Initialize the database:

python database.py

Step 5: Run the application:

python app.py

Step 6: Open your browser and visit:

http://127.0.0.1:5000

## Security Features

- Passwords are stored using secure password hashing.
- Only authenticated users can access protected pages.
- Users can share documents with registered users.
- Only authorized users can download shared documents.
- Unauthorized download attempts are blocked.
- User activities are recorded in audit logs.

## Testing

The following functionalities have been tested successfully:

- User Registration
- User Login and Logout
- Document Upload
- Document Sharing
- Shared Document Access
- Authorized Document Download
- Unauthorized Download Prevention
- Audit Log Recording

## Future Enhancements

- Email Verification
- Two-Factor Authentication
- Cloud Storage Integration
- Improved User Interface
- Advanced Document Permissions

## Conclusion

TrustVault provides a secure and simple platform for document sharing. This project demonstrates Python Flask development, database management, user authentication, access control, and audit logging.

## Developer

Developed using Python and Flask.