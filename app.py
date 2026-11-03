from flask import Flask, request, redirect, session, render_template_string, send_from_directory, abort
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from database import get_db_connection, init_db
import os

app = Flask(__name__)

# Generate a local secret key if one is not configured.
# For deployment, set SECRET_KEY as an environment variable.
app.secret_key = os.environ.get("SECRET_KEY") or os.urandom(32)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

init_db()


# AUDIT LOG FUNCTION
def log_action(user_id, action, document_id=None, details=None):

    connection = get_db_connection()

    connection.execute(
        """
        INSERT INTO audit_logs
        (user_id, action, document_id, details)
        VALUES (?, ?, ?, ?)
        """,
        (user_id, action, document_id, details)
    )

    connection.commit()
    connection.close()


# HOME PAGE
@app.route("/")
def home():

    if "user_id" in session:

        return render_template_string("""
            <h1>TrustVault</h1>
            <h2>Secure Document Sharing</h2>

            <h3>Welcome, {{ username }}!</h3>

            <form action="/upload" method="POST"
                  enctype="multipart/form-data">

                <input type="file" name="file" required>
                <button type="submit">Upload Document</button>

            </form>

            <br>
            <a href="/documents">View My Documents</a>

            <br><br>
            <a href="/shared">View Shared Documents</a>

            <br><br>
            <a href="/audit-logs">My Audit Logs</a>

            <br><br>
            <a href="/logout">Logout</a>

        """, username=session["username"])

    return render_template_string("""
        <h1>TrustVault</h1>
        <h2>Secure Document Sharing</h2>

        <h3>Register</h3>

        <form action="/register" method="POST">

            <input name="username"
                   placeholder="Username" required>

            <input name="password"
                   type="password"
                   placeholder="Password" required>

            <button type="submit">Register</button>

        </form>

        <h3>Login</h3>

        <form action="/login" method="POST">

            <input name="username"
                   placeholder="Username" required>

            <input name="password"
                   type="password"
                   placeholder="Password" required>

            <button type="submit">Login</button>

        </form>
    """)


# USER REGISTRATION
@app.route("/register", methods=["POST"])
def register():

    username = request.form["username"].strip()
    password = request.form["password"]

    if not username:
        return "Please enter a username."

    if len(password) < 8:
        return "Password must contain at least 8 characters."

    password_hash = generate_password_hash(password)

    connection = get_db_connection()

    try:

        connection.execute(
            """
            INSERT INTO users (username, password_hash)
            VALUES (?, ?)
            """,
            (username, password_hash)
        )

        connection.commit()

        user = connection.execute(
            "SELECT id FROM users WHERE username = ?",
            (username,)
        ).fetchone()

        user_id = user["id"]

        connection.close()

        log_action(
            user_id,
            "REGISTER",
            details="New account registered"
        )

    except Exception as e:

        connection.close()
        print("Registration Error:", e)

        return "Registration failed. Check VS Code terminal."

    return redirect("/")


# USER LOGIN
@app.route("/login", methods=["POST"])
def login():

    username = request.form["username"].strip()
    password = request.form["password"]

    connection = get_db_connection()

    user = connection.execute(
        "SELECT * FROM users WHERE username = ?",
        (username,)
    ).fetchone()

    connection.close()

    if user and check_password_hash(user["password_hash"], password):

        session.clear()

        session["user_id"] = user["id"]
        session["username"] = user["username"]

        log_action(
            user["id"],
            "LOGIN",
            details="User logged in"
        )

        return redirect("/")

    return "Invalid username or password."


# DOCUMENT UPLOAD
@app.route("/upload", methods=["POST"])
def upload():

    if "user_id" not in session:
        return redirect("/login")

    file = request.files.get("file")

    if not file or file.filename == "":
        return "Please select a file."

    filename = secure_filename(file.filename)

    if not filename:
        return "Invalid filename."

    user_folder = os.path.join(
        UPLOAD_FOLDER,
        str(session["user_id"])
    )

    os.makedirs(user_folder, exist_ok=True)

    file_path = os.path.join(user_folder, filename)

    if os.path.exists(file_path):
        return "A file with this name already exists."

    file.save(file_path)

    connection = get_db_connection()

    connection.execute(
        """
        INSERT INTO documents (filename, owner_id)
        VALUES (?, ?)
        """,
        (filename, session["user_id"])
    )

    connection.commit()

    document = connection.execute(
        """
        SELECT id FROM documents
        WHERE owner_id = ? AND filename = ?
        ORDER BY id DESC LIMIT 1
        """,
        (session["user_id"], filename)
    ).fetchone()

    connection.close()

    log_action(
        session["user_id"],
        "UPLOAD",
        document["id"],
        "Uploaded document: " + filename
    )

    return redirect("/documents")


# MY DOCUMENTS
@app.route("/documents")
def documents():

    if "user_id" not in session:
        return redirect("/login")

    connection = get_db_connection()

    files = connection.execute(
        """
        SELECT id, filename, uploaded_at
        FROM documents
        WHERE owner_id = ?
        """,
        (session["user_id"],)
    ).fetchall()

    connection.close()

    return render_template_string("""
        <h1>My Documents</h1>

        {% if files %}

            {% for file in files %}

                <div>

                    <p>
                        {{ file["filename"] }}
                        - {{ file["uploaded_at"] }}
                    </p>

                    <a href="/download/{{ file['id'] }}">
                        Download Document
                    </a>

                    <br><br>

                    <form action="/share/{{ file['id'] }}"
                          method="POST">

                        <input
                            type="text"
                            name="username"
                            placeholder="Enter registered username"
                            required
                        >

                        <button type="submit">
                            Share Document
                        </button>

                    </form>

                    <hr>

                </div>

            {% endfor %}

        {% else %}

            <p>No documents uploaded yet.</p>

        {% endif %}

        <a href="/">Back to Home</a>
        <br><br>

        <a href="/shared">View Shared Documents</a>
        <br><br>

        <a href="/audit-logs">My Audit Logs</a>
        <br><br>

        <a href="/logout">Logout</a>

    """, files=files)


# SHARE DOCUMENT
@app.route("/share/<int:document_id>", methods=["POST"])
def share_document(document_id):

    if "user_id" not in session:
        return redirect("/login")

    username = request.form.get("username", "").strip()

    if not username:
        return "Please enter a username."

    connection = get_db_connection()

    document = connection.execute(
        """
        SELECT * FROM documents
        WHERE id = ? AND owner_id = ?
        """,
        (document_id, session["user_id"])
    ).fetchone()

    if document is None:

        connection.close()

        return "Document not found or you are not the owner."

    user = connection.execute(
        "SELECT id FROM users WHERE username = ?",
        (username,)
    ).fetchone()

    if user is None:

        connection.close()

        return "User not found. Please enter a registered username."

    if user["id"] == session["user_id"]:

        connection.close()

        return "You cannot share a document with yourself."

    existing_share = connection.execute(
        """
        SELECT id FROM document_shares
        WHERE document_id = ? AND shared_with = ?
        """,
        (document_id, user["id"])
    ).fetchone()

    if existing_share:

        connection.close()

        return "Document is already shared with this user."

    connection.execute(
        """
        INSERT INTO document_shares
        (document_id, owner_id, shared_with, permission)
        VALUES (?, ?, ?, ?)
        """,
        (document_id, session["user_id"], user["id"], "view")
    )

    connection.commit()
    connection.close()

    log_action(
        session["user_id"],
        "SHARE",
        document_id,
        "Shared document with " + username
    )

    return """
        Document shared successfully!
        <br><br>
        <a href="/documents">Back to Documents</a>
    """


# SHARED DOCUMENTS
@app.route("/shared")
def shared_documents():

    if "user_id" not in session:
        return redirect("/login")

    connection = get_db_connection()

    files = connection.execute(
        """
        SELECT documents.id AS document_id,
               documents.filename,
               documents.uploaded_at,
               users.username AS owner

        FROM document_shares

        JOIN documents
        ON document_shares.document_id = documents.id

        JOIN users
        ON document_shares.owner_id = users.id

        WHERE document_shares.shared_with = ?
        """,
        (session["user_id"],)
    ).fetchall()

    connection.close()

    return render_template_string("""
        <h1>Documents Shared With Me</h1>

        {% if files %}

            {% for file in files %}

                <div>

                    <p>
                        {{ file["filename"] }}
                        <br>
                        Shared by: {{ file["owner"] }}
                        <br>
                        {{ file["uploaded_at"] }}
                    </p>

                    <a href="/download/{{ file['document_id'] }}">
                        Download Document
                    </a>

                    <hr>

                </div>

            {% endfor %}

        {% else %}

            <p>No documents have been shared with you.</p>

        {% endif %}

        <a href="/">Back to Home</a>
        <br><br>

        <a href="/logout">Logout</a>

    """, files=files)


# SECURE DOCUMENT DOWNLOAD
@app.route("/download/<int:document_id>")
def download_document(document_id):

    if "user_id" not in session:
        return redirect("/login")

    connection = get_db_connection()

    document = connection.execute(
        """
        SELECT * FROM documents
        WHERE id = ?
        """,
        (document_id,)
    ).fetchone()

    if document is None:

        connection.close()

        return "Document not found.", 404

    user_id = session["user_id"]

    is_owner = document["owner_id"] == user_id

    shared = connection.execute(
        """
        SELECT id FROM document_shares
        WHERE document_id = ? AND shared_with = ?
        """,
        (document_id, user_id)
    ).fetchone()

    connection.close()

    if not is_owner and not shared:
        abort(403)

    user_folder = os.path.join(
        UPLOAD_FOLDER,
        str(document["owner_id"])
    )

    file_path = os.path.join(
        user_folder,
        document["filename"]
    )

    if not os.path.isfile(file_path):
        return "File not found on server.", 404

    log_action(
        user_id,
        "DOWNLOAD",
        document_id,
        "Downloaded document: " + document["filename"]
    )

    return send_from_directory(
        user_folder,
        document["filename"],
        as_attachment=True
    )


# VIEW MY AUDIT LOGS
@app.route("/audit-logs")
def audit_logs():

    if "user_id" not in session:
        return redirect("/login")

    connection = get_db_connection()

    logs = connection.execute(
        """
        SELECT action, document_id, details, timestamp
        FROM audit_logs
        WHERE user_id = ?
        ORDER BY timestamp DESC
        """,
        (session["user_id"],)
    ).fetchall()

    connection.close()

    return render_template_string("""
        <h1>My Audit Logs</h1>

        {% if logs %}

            <table border="1" cellpadding="10">

                <tr>
                    <th>Action</th>
                    <th>Document ID</th>
                    <th>Details</th>
                    <th>Timestamp</th>
                </tr>

                {% for log in logs %}

                    <tr>
                        <td>{{ log["action"] }}</td>
                        <td>{{ log["document_id"] or "-" }}</td>
                        <td>{{ log["details"] or "-" }}</td>
                        <td>{{ log["timestamp"] }}</td>
                    </tr>

                {% endfor %}

            </table>

        {% else %}

            <p>No audit logs available.</p>

        {% endif %}

        <br>

        <a href="/">Back to Home</a>

    """, logs=logs)


# USER LOGOUT
@app.route("/logout")
def logout():

    if "user_id" in session:

        log_action(
            session["user_id"],
            "LOGOUT",
            details="User logged out"
        )

    session.clear()

    return redirect("/")


if __name__ == "__main__":
    app.run(debug=False)