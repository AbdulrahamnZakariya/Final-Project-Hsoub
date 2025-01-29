from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from main import add_student, delete_student, update_student, show_student

class APIHandler(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()

    def do_POST(self):
        if self.path == "/add_student":
            content_length = int(self.headers['Content-Length'])
            post_data = json.loads(self.rfile.read(content_length))

            student_data = (
                post_data['id'], post_data['first_name'], post_data['last_name'],
                post_data['age'], post_data['grade'], post_data['registration_date']
            )
            lessons = post_data['lessons']
            add_student(student_data, lessons)
            self._set_headers()
            self.wfile.write(json.dumps({"message": "Student added successfully."}).encode())

    def do_DELETE(self):
        if self.path == "/delete_student":
            content_length = int(self.headers['Content-Length'])
            post_data = json.loads(self.rfile.read(content_length))

            delete_student(post_data['id'])
            self._set_headers()
            self.wfile.write(json.dumps({"message": "Student deleted successfully."}).encode())

    def do_GET(self):
        if self.path.startswith("/show_student/"):
            student_id = int(self.path.split('/')[-1])
            student = show_student(student_id)
            self._set_headers()
            self.wfile.write(json.dumps(student).encode())

def run_server():
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, APIHandler)
    print("Server running on port 8000...")
    httpd.serve_forever()

if __name__ == "__main__":
    run_server()
