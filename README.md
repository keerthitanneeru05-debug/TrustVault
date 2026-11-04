
# TrustVault – Secure Document Sharing

## Project Overview

TrustVault is a secure document-sharing web application developed using Python and Flask.

It allows users to register, log in, upload documents, share documents with other registered users, and securely download documents.

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
- database.py – Database creation and management (if included)
- README.md – Project documentation
- uploads/ – Uploaded documents folder
- trustvault.db – SQLite database (if present)

## Installation and Setup

Step 1: Install Python on your computer.

Step 2: Open the project folder in VS Code.

Step 3: Install dependencies:

```bash
pip install -r requirements.txt
```

Step 4: Run the application:

```bash
python app.py
```

Step 5: Open your browser and visit:

http://127.0.0.1:5000

## Security Features

- Passwords are stored using secure password hashing.
- Only authenticated users can access protected pages.
- Document sharing is intended for registered users.
- Authorized users can download accessible documents.
- User activities are recorded through audit logs.

## Testing

The following functionalities have been tested successfully:

- User Registration
- User Login and Logout
- Dashboard
- Document Upload
- My Documents
- Document Download

Pending Testing:

- Document Sharing
- Shared Document Access
- Audit Log Recording
- Unauthorized Download Prevention

## Future Enhancements

- Email Verification
- Two-Factor Authentication
- Cloud Storage Integration
- Improved User Interface
- Advanced Document Permissions

## Conclusion

TrustVault provides a platform for document management and sharing. This project demonstrates Python Flask development, database management, user authentication, access control, and audit logging.

## Developer

Developed using Python and Flask.
