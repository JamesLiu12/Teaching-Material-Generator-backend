from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from InputHandler import InputHandler


class FakeBackend(BaseHTTPRequestHandler):
    def do_POST(self):
        # response = self.path.encode("utf8")

        # read json
        req_data = self.rfile.read(int(self.headers['content-length'])).decode()
        print(req_data)

        # convert json to dict, dict_data['operation'] is how to operate data, dict_data['content'] is the content
        dict_data = json.loads(req_data)

        response = ""

        operation = dict_data['operation']

        input_handler = InputHandler()
        if operation == 'generate outline':
            response = input_handler.generate_outline(dict_data['content'])
        elif operation == 'regenerate outline':
            response = input_handler.regenerate_outline()
        elif operation == 'generate content':
            response = input_handler.generate_content(dict_data['content'])
        elif operation == 'regenerate content':
            response = input_handler.regenerate_content()
        elif operation == 'generate ppt':
            response = input_handler.generate_ppt()
        elif operation == 'upload content':
            response = input_handler.upload_content(dict_data['content'])

        response = json.dumps(response).encode("utf-8")

        self.send_response(200)
        self.send_header("Content-type", "application/json; charset=utf-8")
        self.send_header("Content-length", str(len(response)))
        self.end_headers()

        self.wfile.write(response)

    # def do_PUT(self):
    #     # read json
    #     req_data = self.rfile.read(int(self.headers['content-length'])).decode()
    #     print(req_data)
    #
    #     # convert json to dict, dict_data['operation'] is how to operate data, dict_data['content'] is the content
    #     dict_data = json.loads(req_data)
    #
    #     operation = dict_data['operation']
    #
    #     if operation == "upload content":
    #         pass
    #         # TODO


if __name__ == '__main__':
    HTTPServer(("127.0.0.1", 50000), FakeBackend).serve_forever()
