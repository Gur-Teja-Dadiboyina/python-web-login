from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse, os

USERNAME = "admin"
PASSWORD = "1234"

class SimpleLoginHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            html = """
            <html>
            <head><title>Login Page</title></head>
            <body style="font-family:Arial; background-color:#f0f0f0; text-align:center;">
                <h2>Login Page</h2>
                <form method="POST" action="/login">
                    <label>Username:</label><br>
                    <input type="text" name="username"><br><br>
                    <label>Password:</label><br>
                    <input type="password" name="password"><br><br>
                    <input type="submit" value="Login">
                </form>
            </body>
            </html>
            """
            self.wfile.write(html.encode("utf-8"))

    def do_POST(self):
        if self.path == '/login':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            form_data = urllib.parse.parse_qs(post_data.decode('utf-8'))
            
            username = form_data.get('username', [''])[0]
            password = form_data.get('password', [''])[0]

            if username == USERNAME and password == PASSWORD:
                message = f"<h2>Welcome, {username}!</h2>"
            else:
                message = "<h2>Invalid username or password!</h2><a href='/'>Try again</a>"

            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(message.encode('utf-8'))

def run(port=8082):
    server_address = ('0.0.0.0', port)  # Bind to all network interfaces
    httpd = HTTPServer(server_address, SimpleLoginHandler)
    print(f"Server running on port {port}")
    httpd.serve_forever()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8082))
    run(port)
