# --*-- conding:utf-8 --*--
# @Time : 2024/1/11 17:21
# @Author : YWJ
# @Email : 52215901025@stu.ecnu.edu.cn
# @File : Model_API.py
# @Software : PyCharm
# @Description :  各个模型的API接口
import os
import openai
import requests
import urllib
import json
import time
import sys
from http import HTTPStatus
import dashscope
import random
# from vllm import LLM, SamplingParams
# from transformers import AutoModelForCausalLM, AutoTokenizer
from dashscope import Generation
from dashscope.api_entities.dashscope_response import Role

class API():
    def __init__(self, api_key_list: str, model_name: str = "gpt-3.5-turbo", temperature: float = 0.0,
                 max_tokens: int = 1024):
        self.api_key_list = api_key_list
        self.model_name = model_name  # 新的model, 支持1w+
        self.temperature = temperature
        self.max_tokens = max_tokens
        # if self.api_key_list == "":
        #     self.llm = LLM("/data/xxx", tokenizer_mode='auto',  # local model
        #           trust_remote_code=True,
        #           enforce_eager=True,
        #           enable_prefix_caching=True)
        #     self.sampling_params = SamplingParams(temperature=0.85, top_p=0.8, max_tokens=512)
        #     self.tokenizer = AutoTokenizer.from_pretrained("/data/xxx", trust_remote_code=True)

    # GPT系列
    def send_request_turbo(self, prompt, question):
        """
        """
        zero_shot_prompt_message = {'role': 'system', 'content': prompt}

        messages = [zero_shot_prompt_message]
        question = sensitive(question)
        message = {"role": "user", "content": question}
        print(f"LLM的Prompt是{'*' * 100}\n{zero_shot_prompt_message['content']}\n{message['content']}")
        messages.append(message)

        output = {}
        while True:
            try:
                # os.environ['HTTPS_PROXY'] = "http://127.0.0.1:10809"
                openai.api_base = "https://xiaoai.plus/v1"
                openai.api_key = self.api_key_list
                output = openai.ChatCompletion.create(
                    model=self.model_name,
                    messages=messages,
                    temperature=self.temperature
                )
                answer = revers_sensitive(output['choices'][0]['message']['content'])
                print(answer)
                return [answer]
            except Exception as e:
                print('Exception:', e)
                print("原始Prompt：")
                sys.exit()

        return [output]

    # 多轮会话
    def send_request_chat(self, prompt, share_content, question):
        """
        """
        zero_shot_prompt_message = {'role': 'system', 'content': prompt}

        messages = [zero_shot_prompt_message]
        share_content = sensitive(share_content)
        message = {"role": "user", "content": share_content}
        messages.append(message)
        output_chat = []
        i = 0
        error_num = 0
        while i < len(question):
            sub_question = question[i]
            sub_question['sub_question'] = sensitive(sub_question['sub_question'])
            message = {"role": "user", "content": sub_question['sub_question']}
            messages.append(message)
            # os.environ['HTTPS_PROXY'] = "http://127.0.0.1:33210"
            # os.environ['HTTPS_PROXY'] = "http://127.0.0.1:10809"
            # os.environ['OPENAI_API_KEY'] = self.api_key_list
            # os.environ["OPENAI_BASE_URL"] = "https://api.xiaoai.plus/v1"
            openai.api_base = "https://xiaoai.plus/v1"
            openai.api_key = self.api_key_list
            try:
                output = openai.ChatCompletion.create(
                    model=self.model_name,
                    messages=messages,
                    temperature=self.temperature
                )
                answer = revers_sensitive(output['choices'][0]['message']['content'])
                answer = sensitive(answer)
                messages.append({"role": "assistant", "content": answer})
                output_chat.append(answer)
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
                if "max" in e.args[0]:  # 说明到了最大的token, 将上面存储的靠前的子问题删除几个
                    time.sleep(5)
                    if error_num == 0:
                        if len(messages) < 13:
                            star_index = -1 * len(messages) + 2
                        else:
                            star_index = -11  # 前5个
                    else:
                        star_index += 2  # 如果还超长，那么就不断的逐个删除子问题
                    if star_index >= -1:
                        print("无法处理该问题")
                        output_chat.append("")
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

        time.sleep(2)

        return output_chat

    # DDST hard
    def send_request_hard(self, prompt, option, question, option_num):
        """
        """
        prompt = prompt.replace("<answer>", option).replace("<option_num>", str(option_num))
        zero_shot_prompt_message = {'role': 'system', 'content': prompt}

        messages = [zero_shot_prompt_message]
        question = sensitive(question)
        message = {"role": "user", "content": question}
        print(f"LLM的Prompt是{'*' * 100}\n{message['content']}")
        messages.append(message)

        output = {}
        while True:
            try:
                # os.environ['HTTPS_PROXY'] = "http://127.0.0.1:10809"
                openai.api_base = "https://xiaoai.plus/v1"
                openai.api_key = self.api_key_list
                output = openai.ChatCompletion.create(
                    model=self.model_name,
                    messages=messages,
                    temperature=self.temperature
                )
                answer = revers_sensitive(output['choices'][0]['message']['content'])
                print(answer)
                return [answer]
            except Exception as e:
                print('Exception:', e)
                print("原始Prompt：")
                sys.exit()
    # herb_predict
    def send_request_TCM_Rec(self, prompt, question):
        """
        """
        zero_shot_prompt_message = {'role': 'system', 'content': "你是一个中药推荐系统，你需要根据症状信息推荐20个中药。"}

        messages = [zero_shot_prompt_message]
        question = sensitive(question)
        question = f"{prompt}\n症状信息为：{question}。\n"
        message = {"role": "user", "content": question}
        print(f"LLM的Prompt是{'*' * 100}\n{zero_shot_prompt_message['content']}\n{message['content']}")
        messages.append(message)

        output = {}
        while True:
            try:
                # os.environ['HTTPS_PROXY'] = "http://127.0.0.1:10809"
                openai.api_base = "https://xiaoai.plus/v1"
                openai.api_key = self.api_key_list
                output = openai.ChatCompletion.create(
                    model=self.model_name,
                    messages=messages,
                    temperature=self.temperature
                )
                answer = revers_sensitive(output['choices'][0]['message']['content'])
                print(answer)
                return [answer]
            except Exception as e:
                print('Exception:', e)
                print("原始Prompt：")
                sys.exit()

def sensitive(sentence):
    sentence = sentence.replace("阴道", "term-YD")
    sentence = sentence.replace("射精", "term-SJ")
    return sentence

def revers_sensitive(sentence):
    sentence = sentence.replace("term-YD", "阴道")
    sentence = sentence.replace("term-SJ", "射精")
    return sentence