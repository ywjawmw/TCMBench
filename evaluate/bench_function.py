
import os
import json
import time
import re
# from random import choice
# import requests
from typing import List, Union, Dict
# from joblib import Parallel, delayed

from tqdm import  tqdm


def extract_choice_answer(model_output, question_type, answer_lenth=None):
    """
    Extract choice answer from model output

    Format of model_output that is expected:
    choice answer should be the last Capital Letter of the model_output, e.g.: "...【答案】 A <eoa>"
    """
    if question_type == 'A1+A2' or question_type == 'A3+A4' or question_type == 'B1':
        model_answer = []
        # temp = re.findall(r'[A-E]', model_output[::-1])
        # if len(temp) != 0:
        #     model_answer.append(temp[0])
        model_output = model_output[::-1]
        pattern = r"([A-Z]).*?案答"
        check_info = re.search(pattern, model_output)
        if check_info:
            pattern = r"\．[A-Z]"
            temp = re.findall(pattern, model_output)
            if len(temp) > 0:
                # answer = temp[0]
                answer = check_info.group(1)
                model_answer.append(answer)
            else:
                temp = re.findall(r'[A-E]', model_output)
                if len(temp) != 0:
                    answer = temp[0]
                    model_answer.append(answer)
        else:
            temp = re.findall(r'[A-E]', model_output)
            if len(temp) != 0:
                answer = temp[0]
                model_answer.append(answer)
    return model_answer

def choice_test_A12(**kwargs):
    model_api = kwargs['model_api']
    model_name = kwargs['model_name']
    start_num = kwargs['start_num']
    end_num = kwargs['end_num']
    data = kwargs['data']['example']
    keyword = kwargs['keyword']
    prompt = kwargs['prompt']
    question_type = kwargs['question_type']
    save_directory = kwargs['save_directory']
   
    model_answer_dict = []
    for i in range(start_num, end_num):

        index = data[i]['index']
        question = data[i]['question'].strip() + '\n'
        # year = data[i]['year']
        # category = data[i]['year']
        score = data[i]['score']
        standard_answer = data[i]['answer']
        answer_lenth = len(standard_answer)
        analysis = data[i]['analysis']
        knowledge_point = data[i]['knowledge_point']
        model_output = model_api(prompt, question, "", question_type, None)[0]   # list()
        model_answer = extract_choice_answer(model_output, question_type, answer_lenth)
        # TODO: which content of temp we expect
        dict = {
            'index': index, 
            # 'year': year,
            # 'category': category,
            'score': score,
            'question': question, 
            'standard_answer': standard_answer,
            'analysis': analysis,
            'knowledge_point': knowledge_point,
            'model_answer': model_answer,
            'model_output': model_output
        }
        print("*" * 100, "index-", dict["index"], "*" * 100)
        for key, value in dict.items():
            print(key, ":", value)
        # print(dict)
        model_answer_dict.append(dict)

    file_name = model_name+"_seperate_"+keyword+f"_{start_num}-{end_num-1}.json"
    file_path = os.path.join(save_directory, file_name)
    with open(file_path, 'w', encoding='utf-8') as f:
        output = {
            'keyword': keyword, 
            'example': model_answer_dict
            }
        json.dump(output, f, ensure_ascii=False, indent=4)
        f.close()


def choice_test_A34(**kwargs):
    model_api = kwargs['model_api']
    model_name = kwargs['model_name']
    start_num = kwargs['start_num']
    end_num = kwargs['end_num']
    data = kwargs['data']['example']
    keyword = kwargs['keyword']
    prompt = kwargs['prompt']
    question_type = kwargs['question_type']
    save_directory = kwargs['save_directory']
    examples = kwargs['examples']

    model_answer_dict = []
    for i in range(start_num, end_num):

        index = data[i]['index']
        question = data[i]['question']    # list() 包含多个小问题和答案
        score = data[i]['score']
        knowledge_point = data[i]['knowledge_point']
        share_content = data[i]['share_content']
        model_output = model_api(prompt, question, share_content, question_type, examples)
        question_list = []
        for sub_question, output in zip(question, model_output):
            standard_answer = sub_question['answer']
            answer_lenth = len(standard_answer)
            analysis = sub_question['analysis']
            model_answer = extract_choice_answer(output, question_type, answer_lenth)
            sub_question_dict = {
                'sub_question': sub_question['sub_question'],
                'standard_answer': standard_answer,
                'analysis': analysis,
                'model_answer': model_answer,
                'model_output': output
            }
            question_list.append(sub_question_dict)
        # TODO: which content of temp we expect

        dict = {
            'index': index,
            'score': score,
            'share_content': share_content,
            'question': question_list,
            'knowledge_point': knowledge_point,
        }
        # print("*" * 100, "index-", dict["index"], "*" * 100)
        # for key, value in dict.items():
        #     print(key, ":", value)
        # print(dict)
        model_answer_dict.append(dict)

    file_name = "k_shot" + model_name + "_seperate_" + keyword + f"_{start_num}-{end_num - 1}.json"
    file_path = os.path.join(save_directory, file_name)
    with open(file_path, 'w', encoding='utf-8') as f:
        output = {
            'keyword': keyword,
            'example': model_answer_dict
        }
        json.dump(output, f, ensure_ascii=False, indent=4)
        f.close()

def export_union_json(directory: str, model_name: str, keyword: str, zero_shot_prompt_text: str or list[str], question_type: str) -> None:
    """
    Merges JSON files containing processed examples in a directory into a single JSON file.

    :param directory: Directory containing the JSON files
    :param model_name: Name of the model used to process the examples
    :param keyword: Keyword used to identify the JSON files
    :param zero_shot_prompt_text: Prompt text for zero-shot learning
    :param question_type: Type of questions in the JSON files (e.g. single_choice, five_out_of_seven, etc.)
    """
    
    save_directory = os.path.join(directory, f'{model_name}_{keyword}')
    if os.path.exists(save_directory):
        output = {
                        'keyword': keyword, 
                        'model_name': model_name,
                        'prompt': zero_shot_prompt_text, 
                        'example': []
                    }
        
        # Iterate through the JSON files with the specified keyword in the directory
        
        print("Start to merge json files")
        files = [file for file in os.listdir(save_directory) if file.endswith('.json') and keyword in file]
        for file in files:
            file_path = os.path.join(save_directory, file)

            # Load and merge the data from the JSON files
            with open(file_path, "r", encoding='utf-8') as f:
                data = json.load(f)
                output['example'] += (data['example'])
        
        # Save the merged data into a single JSON file
        merge_file = os.path.join(directory, f'{model_name}_{keyword}.json')
        output['example'] = sorted(output['example'], key=lambda x: x['index'])
        with open(merge_file, 'w', encoding='utf-8') as f:
            json.dump(output, f, ensure_ascii=False, indent=4)

def export_distribute_json(
        model_api,
        model_name: str, 
        directory: str, 
        keyword: str, 
        zero_shot_prompt_text: str or List[str], 
        question_type: str,
        examples: list,
        parallel_num: int = 1
    ) -> None:
    """
    Distributes the task of processing examples in a JSON file across multiple processes.

    :param model_name: Name of the model to use
    :param directory: Directory containing the JSON file
    :param keyword: Keyword used to identify the JSON file
    :param zero_shot_prompt_text: Prompt text for zero-shot learning
    :param question_type: Type of questions in the JSON file (e.g. single_choice, five_out_of_seven, etc.)
    :param examples: Examples of questions-answer-analyse in the JSON file
    :param parallel_num: Number of parallel processes to use (default: 5)
    
    """
    # Find the JSON file with the specified keyword
    for root, _, files in os.walk(directory):
        for file in files:
            if file == f'{keyword}.json':
                filepath = os.path.join(root, file)
                with open(filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
    
    example_num = len(data['example'])
        
    # Prepare the list of keyword arguments for parallel processing
    kwargs_list = []
    batch_size = example_num // parallel_num + 1
    save_directory = os.path.join(directory, f'{model_name}_{keyword}')
    if not os.path.exists(save_directory):
        os.makedirs(save_directory)
    # os.system(f'mkdir {save_directory}')

    for idx in range(0, parallel_num):
        start_num = idx * batch_size
        end_num = min(start_num + batch_size, example_num)
        if start_num >= example_num:
            break

        kwargs = {
            'model_api': model_api,
            'start_num': start_num,
            'end_num': end_num,
            'model_name': model_name, 
            'data': data, 
            'keyword': keyword, 
            'prompt': zero_shot_prompt_text, 
            'question_type': question_type, 
            'save_directory': save_directory,
            'examples': examples
        }
        kwargs_list.append(kwargs)
    
    # Run parallel processing based on the question type
    if question_type in ["A1+A2"]:
        for kwargs in kwargs_list:
           choice_test_A12(**kwargs)
    elif question_type in ["A3+A4", "B1"]:
        for kwargs in kwargs_list:
           choice_test_A34(**kwargs)
        # Parallel(n_jobs=parallel_num)(delayed(choice_test_A12)(**kwargs) for kwargs in kwargs_list)

def test_correction_score_A12(data_dict):
    score = 0
    all_num = 0
    model_answer_dict = []
    for data in data_dict['example']:
        all_num += 1
        true_answer = data['standard_answer']
        model_answer = data['model_answer']
        if true_answer == model_answer:
            score += 1
        else:
            dict = {
                'index': data["index"],
                'question': data["question"],
                'standard_answer': true_answer,
                'analysis': data["analysis"],
                'knowledge_point': data["knowledge_point"],
                'model_answer': model_answer,
                'model_output': data["model_output"]
            }
            model_answer_dict.append(dict)
    output = {'keyword': data_dict["keyword"],
              'correct_num': score,
              'all_num': all_num}
    if len(model_answer_dict) > 0:
        output['example'] = model_answer_dict
    return score / all_num, output


def test_correction_score_A34(data_dict):
    score = 0
    all_num = 0
    model_answer_dict = []
    for data in data_dict['example']:
        correction_flag = True
        question = data["question"]
        question_list = []
        # all_num += len(question)
        for sub_question in question:
            all_num += 1
            standard_answer = sub_question['standard_answer']
            model_answer = sub_question['model_answer']
            if standard_answer == model_answer:
                score += 1
            else:
                correction_flag = False
            sub_question_dict = {
                'sub_question': sub_question['sub_question'],
                'standard_answer': standard_answer,
                'analysis': sub_question['analysis'],
                'model_answer': model_answer,
                'model_output': sub_question['model_output']
            }
            question_list.append(sub_question_dict)
        if correction_flag == False:
            dict = {
                'index': data["index"],
                'share_content': data["share_content"],
                'question': question_list,
                'knowledge_point': data["knowledge_point"],
            }
            model_answer_dict.append(dict)
    output = {'keyword': data_dict["keyword"],
              'correct_num': score,
              'all_num': all_num}
    if len(model_answer_dict) > 0:
        output['example'] = model_answer_dict
    return score / all_num, output
