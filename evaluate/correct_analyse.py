# -*- coding: utf-8 -*-
# @Time    : 2023/7/7 10:42
# @Author  : Ywj
# @File    : correct_analyse.py
# @Description :  统计正确的题目个数，同时输出错误的题目和模型分析，以便医生或人工进行分析

import json
import os
from bench_function import test_correction_score_A12, test_correction_score_A34
model = 'chatglm'
# file_A12 = 'D:\Ywj\Python project\TCM_GPT\TCM_book\测试题\笔记(1)\不包含真题\%s_题库@100-A1+A2_CQ-知识点标注换行.json' % (model)
file_A34 = 'D:\Ywj\Python project\TCM_GPT\TCM_book\测试题\笔记(1)\不包含真题\k_shot\%s_题库@100-A3+A4_CQ-知识点标注换行.json' % (model)
# file_B1 = 'D:\Ywj\Python project\TCM_GPT\TCM_book\测试题\笔记(1)\不包含真题\%s_题库@100-B1_CQ-知识点标注换行.json' % (model)
false_file = "D:\Ywj\Python project\TCM_GPT\TCM_book\测试题\笔记(1)\不包含真题\k_shot\错题集"

def read_file(file):
    with open(file, 'r', encoding='utf-8') as f:
        data = json.load(f)
        f.close()
    return data

# data_A12 = read_file(file_A12)
data_A34 = read_file(file_A34)
# data_B1 = read_file(file_B1)

# score_A12, false_dict_A12 = test_correction_score_A12(data_A12)
score_A34, false_dict_A34 = test_correction_score_A34(data_A34)
# score_B1, false_dict_B1 = test_correction_score_A34(data_B1)

print("测试结果")
print("A1-A2题目正确率：%f \nA3-A4题目正确率：%f \nB1题目正确率：%f \n" % (0, score_A34, 0))
# with open(os.path.join(false_file, model + "_" + data_A12['keyword'] + '_错题集.json'), 'w', encoding='utf-8') as f:
#     json.dump(false_dict_A12, f, ensure_ascii=False, indent=4)
# f.close()

with open(os.path.join(false_file, model + "_" + data_A34['keyword'] + '_错题集.json'), 'w', encoding='utf-8') as f:
    json.dump(false_dict_A34, f, ensure_ascii=False, indent=4)
f.close()
#
# with open(os.path.join(false_file, model + "_" + data_B1['keyword'] + '_错题集.json'), 'w', encoding='utf-8') as f:
#     json.dump(false_dict_B1, f, ensure_ascii=False, indent=4)
# f.close()




