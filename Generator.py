import g4f
import json


class Generator:
    def __init__(self, provider=g4f.Provider.Aichat, model="gpt-3.5-turbo"):
        self.model = model
        self.provider = provider

    @staticmethod
    def __read_instruction(task_type):
        with open("json/instructions.json") as file:
            return json.load(file)[task_type]

    def __get_completion_from_messages(self, messages):
        response = g4f.ChatCompletion.create(
            provider=self.provider,
            model=self.model,
            messages=messages,
            temperature=0.1,  # this is the degree of randomness of the model's output
        )
        return response

    def __get_response_from_list(self, instruction, outline):
        messages = [
            {"role": "system", "content": instruction},
        ]
        for text in outline:
            messages.append({"role": "user", "content": text})
        return self.__get_completion_from_messages(messages)

    def generate_outline(self, teaching_material: list):
        instruction = self.__read_instruction("generate outline")
        list_concat = ["Here is the input text:"] + teaching_material
        return self.__get_response_from_list(instruction, teaching_material)

    def generate_content(self, teaching_material: list, outline: list):
        instruction = self.__read_instruction("generate content")
        list_concat = ["Here is the input text:"] + teaching_material + ["Here is the outline:"] + outline
        return self.__get_response_from_list(instruction, list_concat)
