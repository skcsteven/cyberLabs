import http.server
import socketserver
import ssl

class CORSRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        super().end_headers()

# Define server address and port
PORT = 8085
ADDRESS = ("", PORT)

# Load SSL context
ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
ssl_context.load_cert_chain(certfile="x.pem", keyfile="x.key")

# Create HTTP server
httpd = socketserver.TCPServer(ADDRESS, CORSRequestHandler)

# Wrap the existing socket with SSL
httpd.socket = ssl_context.wrap_socket(httpd.socket, server_side=True)

print(f"Serving HTTPS on port {PORT}")
httpd.serve_forever()