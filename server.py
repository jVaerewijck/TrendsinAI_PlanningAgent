from http.server import HTTPServer, SimpleHTTPRequestHandler
import os

class CalendarHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-Type', 'text/calendar')
        self.end_headers()
        with open('my_calendar.ics', 'rb') as f:
            self.wfile.write(f.read())

def run_server(port=8000):
    server_address = ('', port)
    httpd = HTTPServer(server_address, CalendarHandler)
    print(f'Server running on port {port}')
    httpd.serve_forever()

if __name__ == '__main__':
    run_server()
