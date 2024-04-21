from http.server import HTTPServer, SimpleHTTPRequestHandler


class CORSRequestHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET')
        self.send_header(
            'Cache-Control', 'no-store, no-cache, must-revalidate')
        return super(CORSRequestHandler, self).end_headers()


host = "localhost"
port = 8003
httpd = HTTPServer((host, port), CORSRequestHandler)
print(f"Server started at http://{host}:{port}")
httpd.serve_forever()
