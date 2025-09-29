
import os
import json

import re

from typing import List

from tqdm import tqdm
from collections import Counter

# args = parse_args()


def get_api_key(filename: str, start_num: int, end_num: int) -> List[str]:
    """
    Retrieves API keys from a file.

    :param filename: Name of the file containing API keys
    :param start_num: Starting line number for reading the file
    :param end_num: Ending line number for reading the file
    :return: List of API keys
    """
    with open(filename, 'r') as file:
        lines = file.readlines()
    
    pattern = re.compile(r'sk-[\s\S]*?(?=\s*\n)')
    api_key_list = []
    
    for i in range(start_num, end_num):
        api_key = pattern.findall(lines[i])
        if len(api_key) != 0:
            api_key_list.append(api_key[0])
    
    return api_key_list


def extract_choice_answer(model_output, question_type, answer_lenth=None):
    """
    Extract choice answer from model output

    Format of model_output that is expected:
    'single_choice': choice answer should be the last Capital Letter of the model_output, e.g.: "...【答案】 A <eoa>"
    'multi_question_choice': "...【答案】A ... 【答案】C ..." or write the choice answers at the beginning of the model_output, e.g. "A C D E F...."
    'multi_choice': "...【答案】 ABD " or write the choice answers at the end of the model_output, e.g. "... ACD"
    'five_out_of_seven': choice answers should be the first five Capital Letters of the model_output, e.g. "A C D F B ...."
    """
    model_answer = []
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

def extract_choice_answer_hard(model_output, question_type, answer_lenth=None):
    model_answer = []
    # DDST
    if question_type == "DDST_hard":
        model_answer = []
        model_output = model_output[0].replace("[", "").replace("]", "").replace("<eoa>", "").replace("</eoa>",
                                                                                                      "").replace(" ",
                                                                                                                  "")
        model_output = ''.join([char for char in model_output if char.isdigit()])
        temp = re.findall(r'[0-9]', model_output)
        if len(temp) != 0:
            model_answer.append(model_output)
    elif question_type == "herb_predict":
        model_answer = []
        model_output = model_output[0].replace("[", "").replace("]", "").replace("<eoa>", "").replace("</eoa>",
                                                                                                      "").replace(" ",
                                                                                                                  "")
        temp = model_output.split(",")
        if len(temp) != 0:
            if len(temp) < 20:
                # 在temp补若干个-1，让其长度为20
                for i in range(20 - len(temp)):
                    temp.append("-1")
            if len(temp) > 20:
                temp = temp[:20]
            model_answer.append(temp)
    return model_answer

def A3_second_check(model_output):
    pattern = r"【答案】"
    temp = re.findall(pattern, model_output)
    check_answer = list()
    if len(temp) > 0:
        model_output = model_output.replace("\n", "")
        pattern = r"答案】.*?([A-Z])"
        temp = re.findall(pattern, model_output)
        if len(temp) > 0:
            answer = temp[-1]
            check_answer.append(answer)
        else:
            check_answer = []
    else:
        pattern = r"答案.*?([A-Z])"
        check_info = re.findall(pattern, model_output)
        if check_info:
            answer = check_info[-1]
            check_answer.append(answer)
        else:
            model_output = model_output[::-1]
            temp = re.findall(r'[A-E]', model_output)
            if len(temp) != 0:
                answer = temp[0]
                check_answer.append(answer)
    return check_answer

def pattern_second_check(ans_list, model_output):
    check_answer = list()
    ans_list = [
        ans.replace("A", "").replace("B", "").replace("C", "").replace("D", "").replace("E", "").replace(
            "．", "").replace(".", "") for ans in ans_list if len(ans) > 0]
    ans_id = -1
    candidate_ans = {}
    for ans in ans_list:
        a_list = re.split(r'[，。；\s]', ans)
        max_count = 0
        for a in a_list:
            if a in model_output:
                ans_id = ans_list.index(ans)
                c = model_output.count(a)
                max_count += c
        if max_count > 0:
            candidate_ans[ans] = max_count
    if len(candidate_ans) > 1:
        # 有多个选项
        # 如果多个选项中，有的选项出现的频率超过了其它选项，那么认为这个选项是正确答案
        max_value = max(candidate_ans.values())
        value_clist = Counter(candidate_ans.values())
        if value_clist[max_value] == 1:
            unique_max_key = [key for key, value in candidate_ans.items() if value == max_value][0]
            ans_id = ans_list.index(unique_max_key)
            check_answer.append(chr(ans_id + 65))
        else:
            print(candidate_ans)
    elif ans_id >= 0:
        check_answer.append(chr(ans_id + 65))
    return check_answer

def herb_second_check(model_output):
    no_answer = 0
    no_standard = 0
    if "-1" in model_output:
        # 统计有多少个-1
        count = model_output.count("-1")
        if 19 <= count <= 20:
            no_answer += 1
        else:
            no_standard += 1
    res_list = []
    if type(model_output[0]) is list:
        model_output = model_output[0]
    for res in model_output:
        if "、" in res:
            res_list += res.split("、")
    if len(res_list) > 5:
        new_res_list = []
        for res in model_output:
            if res != "-1" and "、" not in res:
                new_res_list += res
            else:
                if res == "-1":
                    continue
                new_res_list.extend(res_list)
        if len(new_res_list) < 20:
            # 在temp补若干个-1，让其长度为20
            for i in range(20 - len(new_res_list)):
                new_res_list.append("-1")

        model_output = new_res_list
    if len(set(model_output)) != 20:
        # 找到重复的非-1的元素
        repeat_list = []
        for i, res in enumerate(model_output):
            if res != "-1":
                if res not in repeat_list:
                    repeat_list.append(res)
                else:
                    model_output[i] = "-1"
    return model_output


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
    args = kwargs['args']
   
    model_answer_dict = []
    for i in range(start_num, end_num):
        index = data[i]['index']
        question = data[i]['question'].strip() + '\n'
        score = 1
        standard_answer = data[i]['answer']
        try:
            analysis = data[i]['analysis']
        except:
            analysis = ''
        try:
            knowledge_point = data[i]['knowledge_point']
        except:
            knowledge_point = ''
        model_output = model_api.send_request_turbo(prompt, question)[0]
        model_answer = extract_choice_answer(model_output, question_type, 5)
        if len(model_answer) == 0:
            ans_list = question.split("\n")[1:]
            model_answer = pattern_second_check(ans_list, model_output)
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
        for key, value in dict.items():
            print(key, ":", value)
        # print(dict)
        print("*" * 100, "index-", dict["index"], "*" * 100)
        model_answer_dict.append(dict)

    file_name = f"seperate_{start_num}-{end_num}.json"
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
    args = kwargs['args']

    model_answer_dict = []
    for i in range(start_num, end_num):
        index = data[i]['index']
        question = data[i]['question']    # list() 包含多个小问题和答案
        score = 1
        try:
            knowledge_point = data[i]['knowledge_point']
        except:
            knowledge_point = ''
        share_content = data[i]['share_content']
        model_output = model_api.send_request_chat(prompt, share_content, question)

        question_list = []
        for sub_question, output in zip(question, model_output):
            standard_answer = sub_question['answer']
            try:
                analysis = sub_question['analysis']
            except:
                analysis = ''
            model_answer = extract_choice_answer(output, question_type, 5)
            if question_type in ["CVR", "SDT", 'SDT_reverse', "SDT_shuffle"]:
                model_answer = A3_second_check(output)
            if len(model_answer) == 0:
                if question_type in ["CVR", "SDT", 'SDT_reverse', "SDT_shuffle"]:
                    ans_list = sub_question.split("\n")[1:]
                else:
                    ans_list = share_content.split("\n")[1:]
                model_answer = pattern_second_check(ans_list, output)
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
        model_answer_dict.append(dict)

    file_name = f"seperate_{start_num}-{end_num}.json"
    file_path = os.path.join(save_directory, file_name)
    with open(file_path, 'w', encoding='utf-8') as f:
        output = {
            'keyword': keyword,
            'example': model_answer_dict
        }
        json.dump(output, f, ensure_ascii=False, indent=4)
        f.close()

def choice_test_DDST_hard(**kwargs):
    model_api = kwargs['model_api']
    model_name = kwargs['model_name']
    start_num = kwargs['start_num']
    end_num = kwargs['end_num']
    data = kwargs['data']['example']
    keyword = kwargs['keyword']
    prompt = kwargs['prompt']
    save_directory = kwargs['save_directory']

    model_answer_dict = []
    for i in range(start_num, end_num):
        question = data[i]['question']
        option = data[i]['option']
        standard_answer = data[i]['answer']
        model_output = model_api.send_request_hard(prompt, question, option, int(standard_answer))
        model_answer = extract_choice_answer_hard(model_output, keyword, 0)
        # TODO: which content of temp we expect
        dict = {
            'question': question,
            'option': option,
            'standard_answer': [standard_answer],
            'model_answer': model_answer
        }
        # print("*" * 100, "index-", dict["index"], "*" * 100)
        for key, value in dict.items():
            print(key, ":", value)
        # print(dict)
        model_answer_dict.append(dict)

    file_name = f"seperate_{start_num}-{end_num}.json"
    file_path = os.path.join(save_directory, file_name)
    with open(file_path, 'w', encoding='utf-8') as f:
        output = {
            'keyword': keyword,
            'example': model_answer_dict
        }
        json.dump(output, f, ensure_ascii=False, indent=4)
        f.close()

def choice_test_TCM_Rec(**kwargs):
    model_api = kwargs['model_api']
    model_name = kwargs['model_name']
    start_num = kwargs['start_num']
    end_num = kwargs['end_num']
    data = kwargs['data']['example']
    keyword = kwargs['keyword']
    prompt = kwargs['prompt']
    save_directory = kwargs['save_directory']
    question_type = kwargs['question_type']

    model_answer_dict = []
    for i in range(start_num, end_num):
        question = "、".join(data[i]['sym_set'])
        # option = data[i]['option']
        standard_answer = data[i]['herb_set']
        model_output = model_api.send_request_TCM_Rec(prompt, question)
        model_answer = extract_choice_answer_hard(model_output, keyword, 0)[0]
        model_answer = herb_second_check(model_answer)
        # TODO: which content of temp we expect
        dict = {
            'sym_set': data[i]['sym_set'],
            'model_output': model_answer,
            'herb_set': standard_answer,
        }
        # print("*" * 100, "index-", dict["index"], "*" * 100)
        for key, value in dict.items():
            print(key, ":", value)
        # print(dict)
        model_answer_dict.append(dict)

    file_name = f"seperate_{start_num}-{end_num}.json"
    file_path = os.path.join(save_directory, file_name)
    with open(file_path, 'w', encoding='utf-8') as f:
        output = {
            'keyword': keyword,
            'example': model_answer_dict
        }
        json.dump(output, f, ensure_ascii=False, indent=4)
        f.close()


def export_union_json(directory: str, model_name: str, zero_shot_prompt_text: str or list[str], question_type: str) -> None:
    """
    Merges JSON files containing processed examples in a directory into a single JSON file.

    :param directory: Directory containing the JSON files
    :param model_name: Name of the model used to process the examples
    # :param keyword: Keyword used to identify the JSON files
    :param zero_shot_prompt_text: Prompt text for zero-shot learning
    :param question_type: Type of questions in the JSON files (e.g. single_choice, five_out_of_seven, etc.)
    """
    
    save_directory = os.path.join(directory, f'{model_name}_{question_type}')
    if os.path.exists(save_directory):
        output = {
                        'keywords': question_type,
                        'model_name': model_name,
                        'prompt': zero_shot_prompt_text, 
                        'example': []
                    }
        
        # Iterate through the JSON files with the specified keyword in the directory
        
        print("Start to merge json files")
        files = [file for file in os.listdir(save_directory) if file.endswith('.json')]
        for file in files:
            file_path = os.path.join(save_directory, file)

            # Load and merge the data from the JSON files
            with open(file_path, "r", encoding='utf-8') as f:
                data = json.load(f)
                output['example'] += (data['example'])
        # Save the merged data into a single JSON file
        merge_file = os.path.join(directory, f'{model_name}_{question_type}_predictions.json')
        output['example'] = sorted(output['example'], key=lambda x: x['index'])
        with open(merge_file, 'w', encoding='utf-8') as f:
            json.dump(output, f, ensure_ascii=False, indent=4)

def export_distribute_json(
        model_api,
        model_name: str, 
        directory: str, 
        # keyword: str,
        zero_shot_prompt_text: str or List[str], 
        question_type: str,
        args,
        parallel_num: int = 1
    ) -> None:
    """
    Distributes the task of processing examples in a JSON file across multiple processes.

    :param model_name: Name of the model to use
    :param directory: Directory containing the JSON file

    :param zero_shot_prompt_text: Prompt text for zero-shot learning
    :param question_type: Type of questions in the JSON file (e.g. single_choice, five_out_of_seven, etc.)
    :param parallel_num: Number of parallel processes to use (default: 5)
    
    """
    # Find the JSON file with the specified keyword
    for root, _, files in os.walk(directory):
        for file in files:
            if file == f'{question_type}.json':
                filepath = os.path.join(root, file)
                with open(filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
    
    example_num = len(data['example'])
        
    # Prepare the list of keyword arguments for parallel processing
    kwargs_list = []
    batch_size = example_num // parallel_num
    save_directory = os.path.join(directory, f'{model_name}_{question_type}')
    if not os.path.exists(save_directory):
        os.makedirs(save_directory)
    # os.system(f'mkdir {save_directory}')

    for idx in range(args.start_num, parallel_num):
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
            'keyword': question_type,
            'prompt': zero_shot_prompt_text, 
            'question_type': question_type, 
            'save_directory': save_directory,
            'args': args,
        }
        
        kwargs_list.append(kwargs)
    
    # Run parallel processing based on the question type
    if question_type in ["FKU", "CBF", "SCF", "PF", "SDDT", "DDST", "SDDT_hard"]:
        for kwargs in kwargs_list:
           choice_test_A12(**kwargs)
    elif question_type in ["CVR", "KHC", "SDT", 'SDT_reverse', "SDT_shuffle"]:
        for kwargs in kwargs_list:
           choice_test_A34(**kwargs)
    elif question_type in ["DDST_hard"]:
        for kwargs in kwargs_list:
           choice_test_DDST_hard(**kwargs)
    elif question_type in ["herb_predict"]:
        for kwargs in kwargs_list:
           choice_test_TCM_Rec(**kwargs)



def test_correction_score_A12(data_dict):
    score = 0
    all_num = 0
    model_answer_dict = []
    correct_answer_list = []
    model_kpoint = {}
    for data in data_dict['example']:
        all_num += 1
        true_answer = data['standard_answer']
        model_answer = data['model_answer']
        knowledge_point = data["knowledge_point"]
        if knowledge_point == "":
            knowledge_point = "其他"
        if knowledge_point not in model_kpoint.keys():
            model_kpoint[knowledge_point] = [0, 0]
        model_kpoint[knowledge_point][1] += 1
        dict = {
            'index': data["index"],
            'question': data["question"],
            'standard_answer': true_answer,
            'analysis': data["analysis"],
            'knowledge_point': data["knowledge_point"],
            'model_answer': model_answer,
            'model_output': data["model_output"]
        }
        if true_answer == model_answer:
            score += 1
            model_kpoint[knowledge_point][0] += 1
            correct_answer_list.append(dict)
        else:
            model_answer_dict.append(dict)
    output = {'keyword': data_dict["keyword"],
              'correct_num': score,
              'all_num': all_num}
    if len(model_answer_dict) > 0:
        output['example'] = model_answer_dict
    return score / all_num, output, model_kpoint, score, all_num, correct_answer_list


def test_correction_score_A34(data_dict):
    score = 0
    all_num = 0
    model_answer_dict = []
    model_kpoint = {}
    for data in data_dict['example']:
        correction_flag = True
        question = data["question"]
        knowledge_point = data["knowledge_point"]
        question_list = []
        if knowledge_point == "":
            knowledge_point = "其他"
        if knowledge_point not in model_kpoint.keys():
            model_kpoint[knowledge_point] = [0, 0]
        # all_num += len(question)
        for sub_question in question:
            all_num += 1
            model_kpoint[knowledge_point][1] += 1
            standard_answer = sub_question['standard_answer']
            model_answer = sub_question['model_answer']
            if standard_answer == model_answer:
                score += 1
                model_kpoint[knowledge_point][0] += 1
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
        if correction_flag == False:   # 有一个错就存起来当错题
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

    return score / all_num, output, model_kpoint, score, all_num



