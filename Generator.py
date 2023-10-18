import g4f
import json
import openai

openai.api_base = "https://api.aiohub.org/v1"
openai.api_key = 'e8d20ad67ba241228469ae8c37877f41'


class Generator:
    # def __init__(self, provider=g4f.Provider.Aichat, model="gpt-3.5-turbo"):
    #     self.model = model
    #     self.provider = provider

    def __init__(self, model="gpt-3.5-turbo"):
        self.model = model

    @staticmethod
    def __read_instruction(task_type):
        with open("json/instructions.json") as file:
            return json.load(file)[task_type]

    def __get_completion_from_messages(self, messages):
        # response = g4f.ChatCompletion.create(
        response = openai.ChatCompletion.create(
            # provider=self.provider,
            model=self.model,
            messages=messages,
            temperature=0.1,  # this is the degree of randomness of the model's output
            request_timeout=100,
        )
        return response.choices[0]['message']['content']

    def __get_response_from_list(self, instruction, text_input):
        messages = [
            {"role": "system", "content": instruction},
            {"role": "user", "content": text_input}
        ]
        print(instruction)
        print(text_input)
        # for text in text_input:
        #     messages.append({"role": "user", "content": text})
        return self.__get_completion_from_messages(messages)

    def generate_outline(self, teaching_material: list):
        instruction = self.__read_instruction("generate outline")
        text_concat = "Here is the input text:" + "\n" + "".join(teaching_material)
        return self.__get_response_from_list(instruction, text_concat)

    def generate_content(self, teaching_material: list, outline: list):
        instruction = self.__read_instruction("generate content")
        # text_concat = "Here is the outline:\n" + "".join(outline) + "Please specify each step in the outline."
        text_concat = "Here is the input text:\n" + "".join(teaching_material)
        return self.__get_response_from_list(instruction, text_concat)
