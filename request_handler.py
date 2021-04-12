import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from animals import (get_all_animals,
                    get_single_animal,
                    create_animal,
                    delete_animal,
                    update_animal)

class HandleRequests(BaseHTTPRequestHandler):
    def parse_url(self, path):
        path_params = path.split('/')
        resource = path_params[1]
        id = None

        try:
            id = int(path_params[2])
        except IndexError as e:
            pass
        except ValueError as e:
            pass
            
        return (resource, id)

    def _set_headers(self, status):
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE')
        self.send_header('Access-Control-Allow-Headers', 'X-Requested-With, Content-Type, Accept')
        self.end_headers()

    def do_GET(self):
        self._set_headers(200)

        print(self.path)
        
        (resource, id) = self.parse_url(self.path)

        if resource == 'animals':
            if id is not None:
                response = get_single_animal(id)
            else:
                response = get_all_animals()

        self.wfile.write(json.dumps(response).encode())

    def do_POST(self):
        self._set_headers(201)

        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)
        post_body = json.loads(post_body)

        (resource, id) = self.parse_url(self.path)

        new_object = None

        if resource == 'animals':
            new_object = create_animal(post_body)

        self.wfile.write(json.dumps(new_object).encode())

    def do_PUT(self):
        self._set_headers(201)
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)
        post_body = json.loads(post_body)

        (resource, id) = self.parse_url(self.path)

        if resource == 'animals':
            update_animal(post_body)

    
    def do_DELETE(self):
        self._set_headers(204)
        (resource, id) = self.parse_url(self.path)

        if resource == 'animals':
            delete_animal(id)

        self.wfile.write("".encode())

def main():
    host = ''
    port = 8088
    HTTPServer((host, port), HandleRequests).serve_forever()


if __name__ == "__main__":
    main()



