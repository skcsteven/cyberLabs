from http.server import BaseHTTPRequestHandler, HTTPServer
import requests

class RequestLoggerHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        print("\n ======================")
        
        # print headers
        print(self.headers)

        # Send a simple response
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b"test2")

    def do_POST(self):
        print("\n📌 Received POST Request:")
        print(f"🔹 Path: {self.path}")

        # print headers
        print(self.headers)

        # Read and print the body of the POST request
        content_length = int(self.headers.get('Content-Length', 0))
        if content_length > 0:
            post_data = self.rfile.read(content_length)
            print(f"📝 Body: {post_data.decode('utf-8')}")  # Assuming UTF-8 encoded body

        # Send a simple response
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b"POST received")

            
# Start the server on port 8080
def run_server(port=8082):
    server_address = ("0.0.0.0", port)
    httpd = HTTPServer(server_address, RequestLoggerHandler)
    print(f"🚀 Server running on port {port}...")
    httpd.serve_forever()

if __name__ == "__main__":
    run_server()
