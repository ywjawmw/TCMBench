import sys
import os
parent_path = os.path.dirname(sys.path[0])
if parent_path not in sys.path:
    sys.path.append(parent_path)

from models.Openai import OpenaiAPI
# from ChatGLM import ChatGLMAPI
from bench_function import get_api_key, export_distribute_json, export_union_json
import json
from moss import MossAPI
import time

if __name__ == "__main__":
    # Load the FBQ_prompt.json file
    os.environ['HTTPS_PROXY'] = "your proxy"
    with open("prompt/A3-4_prompt.json", "r", encoding="utf-8") as f:
        data = json.load(f)['examples']
    f.close()


    # Iterate through the examples in the data
    for i in range(len(data)):
        directory = "data"
        # get the api_key_list
        openai_api_key = "your key"
        # openai_api_key_list = get_api_key(, start_num=0, end_num=1)
        # moss_api_key_list = [""]
        model_type = "ChatGLM"
        # get the model_name and instantiate model_api
        if model_type == "OpenAI":
            model_name = 'gpt-3.5-turbo'
            # model_name = 'gpt-4'
            model_api = OpenaiAPI(openai_api_key, model_name=model_name)
        elif model_type == "ChatGLM":
            model_name = 'chatglm'
            model_api = ChatGLMAPI()
        elif model_type == 'Moss':
            model_name = 'moss'
            # model_api = MossAPI(moss_api_key_list)
        keyword = data[i]['keyword']
        question_type = data[i]['type']
        zero_shot_prompt_text = data[i]['prefix_prompt']
        print(keyword)
        print(model_name)
        print(question_type)

        export_distribute_json(
            model_api,
            model_name,
            directory,
            keyword,
            zero_shot_prompt_text,
            question_type,
            [],
            parallel_num=50,
        )

        export_union_json(
            directory,
            model_name,
            keyword,
            zero_shot_prompt_text,
            question_type
        )
