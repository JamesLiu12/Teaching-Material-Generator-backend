import os
import shutil
import subprocess
import time
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from InputHandler import InputHandler
from ClientId import *
# import shutil


class FakeBackend(BaseHTTPRequestHandler):
    def do_POST(self):
        delete_timeout_clients()

        # read json
        req_data = self.rfile.read(int(self.headers['content-length'])).decode()
        print(req_data)


        # convert json to dict, dict_data['operation'] is how to operate data, dict_data['content'] is the content
        dict_data = json.loads(req_data)

        response = ""

        operation = dict_data['operation']

        if operation == 'check client id':
            response = check_client_id(dict_data['content'])
        else:
            client_id = dict_data['client id']
            update_client_time(client_id)
            input_handler = InputHandler(client_id)
            if operation == 'generate outline':
                response = input_handler.generate_outline(dict_data['content'])
            elif operation == 'regenerate outline':
                response = input_handler.regenerate_outline()
            elif operation == 'generate content':
                response = input_handler.generate_content(dict_data['content'])
            elif operation == 'regenerate content':
                response = input_handler.regenerate_content()
            elif operation == 'generate ppt':
                pdf, md_path, pdf_path = input_handler.generate_ppt()
                self.send_response(200)
                self.send_header('Content-Type', 'application/pdf')
                self.end_headers()
                self.wfile.write(pdf.read())
                pdf.close()
                os.remove(md_path)
                os.remove(pdf_path)
                return
            elif operation == 'upload content':
                response = input_handler.upload_content(dict_data['content'])

        response = json.dumps(response).encode("utf-8")

        self.send_response(200)
        self.send_header("Content-type", "application/json; charset=utf-8")
        self.send_header("Content-length", str(len(response)))
        self.end_headers()

        self.wfile.write(response)


if __name__ == '__main__':
    shutil.rmtree('json/client')
    os.mkdir('json/client')
    # for file_name in os.listdir("slidev"):
    #     if file_name.endswith('.md') or file_name.endswith('.pdf'):
    #         file_path = os.path.join("slidev", file_name)
    #         if os.path.exists(file_path):
    #             os.remove(file_path)
    #         else:
    #             print(f"文件 {file_path} 不存在")

    HTTPServer(("127.0.0.1", 50000), FakeBackend).serve_forever()