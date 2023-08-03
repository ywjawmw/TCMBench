import random

import requests
import time
import openai
import os
from random import choice


class  OpenaiAPI:
    def __init__(self, api_key_list:str, model_name:str="gpt-3.5-turbo", temperature:float=0.0, max_tokens: int=1024):
        self.api_key_list = api_key_list
        self.model_name = model_name    # 新的model, 支持1w+
        self.temperature = temperature
        self.max_tokens = max_tokens   # 不设置

    def send_request_davinci(self, request_text:str)->str:
        """
        """
        output = {}

        while True:
            try:
                # openai.proxy = "http://127.0.0.1:33210"
                # openai.proxy = "http://127.0.0.1:10809"
                os.environ['HTTPS_PROXY'] = "http://127.0.0.1:33210"
                openai.api_key = self.api_key_list
                output = openai.Completion.create(
                        model=self.model_name,
                        prompt=request_text,
                        temperature=self.temperature,
                        # max_tokens = self.max_tokens
                    )
                break
            except Exception as e:
                print('Exception:', e)
                time.sleep(1)
                
        time.sleep(1)
        return output
    
    def send_request_turbo(self, prompt, question):
        """
        """
        zero_shot_prompt_message = {'role': 'system', 'content': prompt}
            
        messages = [zero_shot_prompt_message]
        message = {"role":"user", "content":question}
        messages.append(message)

        output = {}
        while True:
            try:
                os.environ['HTTPS_PROXY'] = "http://127.0.0.1:33210"
                # os.environ['HTTPS_PROXY'] = "http://127.0.0.1:10809"
                openai.api_key = self.api_key_list
                output = openai.ChatCompletion.create(
                    model=self.model_name,
                    messages=messages,
                    temperature=self.temperature
                )
                # print(output)
                break
            except Exception as e:
                print('Exception:', e)
                print("原始Prompt：")
                for m in messages:
                    print(m)
                print("—" * 100)
                # if "overloaded" or "Bad" in e:
                if "max" in e.args[0]:  # 说明到了最大的token, 将上面存储的靠前的子问题删除几个
                    time.sleep(5)
                    messages = messages[:2] + messages[-11: -1]
                    print("最大token, 保留历史前五个问题")
                    for m in messages:
                        print(m)
                    print("*" * 100)
                else:
                    time.sleep(5)  # 递归调用自身进行重试 不进行break
                    print("重复提问")
                    for m in messages:
                        print(m)
                    print("*" * 100)
        time.sleep(1)

        return [output]

    def send_request_turbo_chat(self, prompt, share_content, question):
        """
        """
        zero_shot_prompt_message = {'role': 'system', 'content': prompt}

        messages = [zero_shot_prompt_message]
        message = {"role": "user", "content": share_content}
        messages.append(message)
        output_chat = []
        i = 0
        error_num = 0
        while i < len(question):
            sub_question = question[i]
            message = {"role": "user", "content": sub_question['sub_question']}
            messages.append(message)
            # os.environ['HTTPS_PROXY'] = "http://127.0.0.1:33210"
            os.environ['HTTPS_PROXY'] = "http://127.0.0.1:10809"
            openai.api_key = self.api_key_list
            try:
                output = openai.ChatCompletion.create(
                    model=self.model_name,
                    messages=messages,
                    temperature=self.temperature
                )
                answer = output.choices[0].message.content
                messages.append({"role": "assistant", "content": answer})
                output_chat.append(output)
                i += 1
                print(i, ":", "success!")
                # print(output)
            except Exception as e:
                print('Exception:', e)
                print("原始Prompt：")
                for m in messages:
                    print(m)
                print("—" * 100)
                # if "overloaded" or "Bad" in e:
                if "max" in e.args[0]:   # 说明到了最大的token, 将上面存储的靠前的子问题删除几个
                    time.sleep(5)
                    if error_num == 0:
                        if len(messages) < 13:
                            star_index = -1 * len(messages) + 2
                        else:
                            star_index = -11   # 前5个
                    else:
                        star_index += 2    # 如果还超长，那么就不断的逐个删除子问题
                    if star_index >= -1:
                        print("无法处理该问题")
                        output_chat.append({})
                        error_num = 0
                        i += 1
                        print("#" * 100)
                    messages = messages[:2] + messages[star_index: -1]
                    print("最大token, 保留历史前几个问题")
                    error_num = 1
                    for m in messages:
                        print(m)
                    print("*" * 100)
                else:
                    time.sleep(5)  # 递归调用自身进行重试(i不变)
                    print("重复提问")
                    messages = messages[:-1]
                    for m in messages:
                        print(m)
                    print("*" * 100)
                    error_num = 0
                    # output_chat.append({})
                    # i += 1
                    # print("失败，默认回答不出内容！")
                time.sleep(5)

        time.sleep(5)

        return output_chat

    def send_request_turbo_chat_k_shot(self, prompt, share_content, question, k_shot_example):
        """
        k_shot_example: list
        """
        example = random.sample(k_shot_example, 1)
        prompt = prompt.replace('<示例>', example[0])
        zero_shot_prompt_message = {'role': 'system', 'content': prompt}

        messages = [zero_shot_prompt_message]
        message = {"role": "user", "content": "案例：" + share_content}
        messages.append(message)
        output_chat = []
        i = 0
        error_num = 0
        while i < len(question):
            sub_question = question[i]
            message = {"role": "user", "content": "问题" + sub_question['sub_question']}
            messages.append(message)
            os.environ['HTTPS_PROXY'] = "http://127.0.0.1:33210"
            # os.environ['HTTPS_PROXY'] = "http://127.0.0.1:10809"
            openai.api_key = self.api_key_list
            try:
                output = openai.ChatCompletion.create(
                    model=self.model_name,
                    messages=messages,
                    temperature=self.temperature
                )
                answer = output.choices[0].message.content
                messages.append({"role": "assistant", "content": answer})
                output_chat.append(output)
                i += 1
                print(i, ":", "success!")
                # print(output)
            except Exception as e:
                print('Exception:', e)
                print("原始Prompt：")
                for m in messages:
                    print(m)
                print("—" * 100)
                # if "overloaded" or "Bad" in e:
                if "max" in e.args[0]:   # 说明到了最大的token, 将上面存储的靠前的子问题删除几个
                    time.sleep(5)
                    if error_num == 0:
                        if len(messages) < 13:
                            star_index = -1 * len(messages) + 2
                        else:
                            star_index = -11   # 前5个
                    else:
                        star_index += 2    # 如果还超长，那么就不断的逐个删除子问题
                    if star_index >= -1:
                        print("无法处理该问题")
                        output_chat.append({})
                        error_num = 0
                        i += 1
                        print("#" * 100)
                    messages = messages[:2] + messages[star_index: -1]
                    print("最大token, 保留历史前几个问题")
                    error_num = 1
                    for m in messages:
                        print(m)
                    print("*" * 100)
                else:
                    time.sleep(5)  # 递归调用自身进行重试(i不变)
                    print("重复提问")
                    messages = messages[:-1]
                    for m in messages:
                        print(m)
                    print("*" * 100)
                    error_num = 0
                    # output_chat.append({})
                    # i += 1
                    # print("失败，默认回答不出内容！")
                time.sleep(5)

        time.sleep(5)

        return output_chat

    def forward(self, prompt, question, share_content='', key_word='A1+A2', examples=None)->list:
        """
        """
        output = []
        if "gpt" in self.model_name:
            if key_word == 'A1+A2':
                output = self.send_request_turbo(prompt, question)
            else:
                # output = self.send_request_turbo_chat(prompt, share_content, question)
                output = self.send_request_turbo_chat_k_shot(prompt, share_content, question, examples)
        elif self.model_name == "text-davinci-003":
            output = self.send_request_davinci(prompt+question)
            output = [output]
        # print(output)
        model_output = list()
        for o in output:
            model_o = self.postprocess(o)
            model_output.append(model_o)
        return model_output
    
    def postprocess(self, output):
        """
        """
        model_output = None
        try:

            if "gpt" in self.model_name:
                model_output = output['choices'][0]['message']['content']

            elif self.model_name == 'text-davinci-003':
                model_output = output['choices'][0]['text']

            if not model_output:
                print("Warning: Empty Output ")
        except Exception as e:
            print('Exception:', e)
            model_output = '【解析】\n<eoe>\n【答案】'
            print("Warning error: Empty Output ")
        return model_output

    def __call__(self, prompt:str, question:str, share_content:str, key_word:str, examples:list):
        return self.forward(prompt, question, share_content, key_word, examples)


def test(model, prompt:str, question:str):


    response = model(prompt, question)

    return response

    
