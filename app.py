
<!DOCTYPE html>
<html>
<head>
    <title>TrustVault Dashboard</title>
</head>
<body>

    <h1>TrustVault</h1>
    <h2>Secure Document Sharing</h2>

    <h3>Welcome, {{ username }}!</h3>

    <hr>

    <h3>Upload Document</h3>

    <form action="/upload" method="POST" enctype="multipart/form-data">
        <input type="file" name="file" required>
        <button type="submit">Upload Document</button>
    </form>

    <hr>

    <h3>My Documents</h3>
    <a href="/documents">View My Documents</a>

    <hr>

    <h3>Shared Documents</h3>
    <a href="/shared">View Shared Documents</a>

    <hr>

    <h3>My Audit Logs</h3>
    <a href="/audit-logs">My Audit Logs</a>

    <hr>

    <br>
    <a href="/logout">Logout</a>

</body>
</html>
