import time

import json
from Generator import Generator
import os
import aspose.pdf as ap


class InputHandler:
    def __init__(self, client_id):
        self.teaching_material_token = 1000
        self.outline_token = 1000
        self.client_json_path = f"json/client/{client_id}.json"
        self.latex_path = f"latex/{client_id}.md"
        self.pdf_path = f"pdf/{client_id}-export.pdf"
        self.generator = Generator()
        self.client_id = client_id
        if not os.path.isfile(self.client_json_path):
            with open(self.client_json_path, "x") as file:
                file.write("{}")

    def __save_to_client(self, dict_to_save):
        with open(self.client_json_path, 'w') as file:
            json.dump(dict_to_save, file)

    def __load_from_client(self):
        with open(self.client_json_path, 'r') as file:
            return json.load(file)

    def __split_str_by_token(self, s):
        out_list = []
        start = 0
        while start < len(s):
            out_list.append(s[start:min(start + self.teaching_material_token, len(s))])
            start += self.teaching_material_token
        return out_list

    def generate_outline(self, teaching_material: str):
        # 将teaching_material 存入 json
        client_dict = self.__load_from_client()
        teaching_material_list = self.__split_str_by_token("".join(teaching_material))
        client_dict['teaching_material'] = teaching_material_list
        self.__save_to_client(client_dict)

        # 调用模型得到输出
        outline = self.generator.generate_outline(teaching_material_list)
        client_dict["outline"] = self.__split_str_by_token(outline)
        self.__save_to_client(client_dict)
        return outline

    def regenerate_outline(self):
        # outline是用户输入的outline，用来生成content的，content就是生成的markdown，最后调生成ppt API来生成ppt的
        client_dict = self.__load_from_client()
        teaching_material_list = client_dict['teaching_material']

        # 调用模型得到输出
        outline = self.generator.generate_outline(teaching_material_list)
        client_dict["outline"] = self.__split_str_by_token(outline)
        self.__save_to_client(client_dict)
        return outline

    def generate_content(self, outline: str):
        # 将outline 存入 json
        client_dict = self.__load_from_client()
        outline_list = self.__split_str_by_token(outline)
        client_dict["outline"] = outline_list
        self.__save_to_client(client_dict)

        #读入teaching_material_list
        teaching_material_list = client_dict['teaching_material']

        # 调用模型得到输出
        content = self.generator.generate_content(teaching_material_list, outline_list)
        content = content[content.find(r"\documentclass"):content.find(r"\end{document}") + len(r"\end{document}")]
        client_dict["content"] = self.__split_str_by_token(content)
        self.__save_to_client(client_dict)
        return content

    def regenerate_content(self):
        with open(self.client_json_path, 'r') as file:
            client_dict = json.load(file)
        outline_list = client_dict["outline"]

        # 读入teaching_material_list
        teaching_material_list = client_dict['teaching_material']

        # 调用模型得到输出
        content = self.generator.generate_content(teaching_material_list, outline_list)
        content = content[content.find(r"\documentclass"):content.find(r"\end{document}") + len(r"\end{document}")]
        client_dict["outline"] = self.__split_str_by_token(content)
        self.__save_to_client(client_dict)
        return content

    def generate_pdf(self):
        # 从json读取content
        client_dict = self.__load_from_client()
        content_list = client_dict['content']
        with open(self.latex_path, "w") as file:
            file.write("".join(content_list))

        # TODO 调用generate PPT API 在这里写 這

        # os.system(fr'cmd /C"cd slidev & pnpm slidev export {self.client_id}.md & cd.."')
        # # os.system("cd..")
        # while True:
        #     try:
        #         return open(self.pdf_path, 'rb'), self.markdown_path, self.pdf_path
        #     except FileNotFoundError:
        #         print("file not found")
        #         time.sleep(2)

        # 创建 TeXLoadOptions 类对象
        options = ap.TeXLoadOptions()

        # 创建文档类对象
        document = ap.Document(self.latex_path, options)

        # 将 Latex 转换为 PDF
        document.save(self.pdf_path)

        return self.latex_path, self.pdf_path

    def upload_content(self, content):
        client_dict = self.__load_from_client()
        client_dict['content'] = self.__split_str_by_token(content)
        self.__save_to_client(client_dict)
