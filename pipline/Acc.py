#!/usr/bin/env python
# !/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2025/9/28 21:55
# @Author  : Wenjing
# @File    : Acc.py
# @Desc    : 计算各个任务的准确率


import json
import os
from bench_function import test_correction_score_A12, test_correction_score_A34
import matplotlib.pyplot as plt
import numpy as np
import argparse


def parse_args():
    parser = argparse.ArgumentParser(description="parameter of LLMs")
    parser.add_argument(
        "--data_path",
        type=str,
        default='../data/first_level',   # 注意按照三个不同的级别进行选择不同的测试任务
        help="测试数据",
    )
    parser.add_argument(
        "--model_name",
        type=str,
        default='gpt-4-0613',
        help="The LLM name.",
    )
    parser.add_argument(
        "--question_type",
        type=str,
        default='FKU',
        help="选择不同测试题类型.",
    )
    parser.add_argument(
        "--start_num",
        type=int,
        default=0,
        help="保存文档的起始id",
    )
    args = parser.parse_args()
    return args

def the_first_task(data_FKU, data_CVR, data_KHC):
    score_A12, false_dict_A12, A12_kp_dict, score_num_A12, all_num_A12, correct_dict_A12 = test_correction_score_A12(data_FKU)
    score_A34, false_dict_A34, A34_kp_dict, score_num_A34, all_num_A34 = test_correction_score_A34(data_CVR)
    score_B1, false_dict_B1, B1_kp_dict, score_num_B1, all_num_B1 = test_correction_score_A34(data_KHC)

    print("基础知识认知任务测试结果")
    print("A1-A2题目正确率：%f \nA3-A4题目正确率：%f \nB1题目正确率：%f \n" % (score_A12, score_A34, score_B1))
    print("A3-A4-k题目正确率：%f" % score_A34)
    # print("A3-A4-k-shot题目正确率：%f" % (score_A34_k))
    print("总的准确率：%f",
          (score_num_A12 + score_num_A34 + score_num_B1) / (all_num_A12 + all_num_A34 + all_num_B1))

    # 创建一个字典来保存相同Key的合并后的值
    merged_values = {}

    A1_num, A3_num, B1_num = 0, 0, 0
    for k, v in A12_kp_dict.items():
        A1_num += v[1]

    for k, v in A34_kp_dict.items():
        A3_num += v[1]

    for k, v in B1_kp_dict.items():
        B1_num += v[1]

    print(A1_num, A3_num, B1_num)

    # 遍历所有相同的Key，并将它们的值合并成一个列表
    num = 0
    kp_num = 0

    A12_res_kp, A34_res_kp, B1_res_kp = dict(), dict(), dict()
    res_kp = dict()

    print("A12各个知识点的准确率：", "*" * 100)
    for key, value in A12_kp_dict.items():
        print(key, "\t", value[0] / value[1])
        A12_res_kp[key] = value[0] / value[1]

    print("A34各个知识点的准确率：", "*" * 100)
    for key, value in A34_kp_dict.items():
        print(key, "\t", value[0] / value[1])
        A34_res_kp[key] = value[0] / value[1]

    print("B1各个知识点的准确率：", "*" * 100)
    for key, value in B1_kp_dict.items():
        print(key, "\t", value[0] / value[1])
        B1_res_kp[key] = value[0] / value[1]

    print("总的知识点准确率：", "*" * 100)
    for key in A12_kp_dict.keys():
        # 从每个字典中获取Key对应的值的列表
        values1 = A12_kp_dict.get(key, [])
        values2 = A34_kp_dict.get(key, [])
        values3 = B1_kp_dict.get(key, [])
        if len(values1) == 0:
            values1 = [0, 0]
        if len(values2) == 0:
            values2 = [0, 0]
        if len(values3) == 0:
            values3 = [0, 0]

        # 将三个字典中相同Key的值合并成一个列表
        merged_values[key] = [0, 0, 0.0]
        merged_values[key][0] = values1[0] + values2[0] + values3[0]
        merged_values[key][1] = values1[1] + values2[1] + values3[1]
        merged_values[key][2] = merged_values[key][0] / merged_values[key][1]
        # print(key, ":  ",  merged_values[key][0]/merged_values[key][1])
        print(key, "\t", merged_values[key][0] / merged_values[key][1])
        res_kp[key] = merged_values[key][0] / merged_values[key][1]
        num += merged_values[key][1]
    print(A12_res_kp)
    print(A34_res_kp)
    print(B1_res_kp)
    print(res_kp)

def A12_type_task(data_dict):
    score = 0
    all_num = 0
    for data in data_dict['example']:
        all_num += 1
        true_answer = data['standard_answer']
        model_answer = data['model_answer']
        if true_answer == model_answer:
            score += 1
    print(score / all_num)

def A34_type_task(data_dict):
    score = 0
    all_num = 0
    for data in data_dict['example']:
        question = data["question"]
        for sub_question in question:
            all_num += 1
            standard_answer = sub_question['standard_answer']
            model_answer = sub_question['model_answer']
            if standard_answer == model_answer:
                score += 1
    print(score / all_num)

# 如果两个元素的sym_set列表的交集为sym_set的长度，那么我们将这些元素分为一组，添加到一个新的列表中
def new_test_gt(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)["example"]
    new_data = {}
    visited = set()
    count = 0
    for i, d1 in enumerate(data):
        if i in visited:
            continue
        sym_set1 = set(d1['sym_set'])
        sym_set_key = "-".join(sorted(sym_set1))
        new_data[sym_set_key] = [d1["herb_set"]]
        visited.add(i)
        count += 1
        for j in range(i+1, len(data)):
            if j in visited:
                continue
            d2 = data[j]
            # 求d1和d2的sym_set的交集
            sym_set2 = set(d2['sym_set'])
            if len(sym_set1) == len(sym_set2):
                if len(sym_set1 & sym_set2) == len(sym_set1):
                        new_data[sym_set_key].append(d2["herb_set"])
                        count += 1
                        visited.add(j)
    # print(count)
    return new_data



def test_metric(gt_data, test_data):
    test_group_list = test_data["example"]
    Ks = [20]
    result = {'precision': np.zeros(len(Ks)), 'recall': np.zeros(len(Ks)),
              'ndcg': np.zeros(len(Ks)), 'rmrr': np.zeros(len(Ks))}

    precision_n = np.zeros(len(Ks))
    recall_n = np.zeros(len(Ks))
    ndcg_n = np.zeros(len(Ks))
    rmrr_n = np.zeros(len(Ks))
    topN = Ks

    for index in range(len(test_group_list)):
        entry = test_group_list[index]
        sym_set = sorted(set(entry["sym_set"]))
        if "-".join(sym_set) not in gt_data.keys():
            print(test_group_list[index])
            break
        v_list = gt_data["-".join(sym_set)]  # sym-index's true herb set list
        rating = entry["model_output"]  # sym-index's predicted herb set list
        K_max = topN[len(topN) - 1]
        for ii in range(len(topN)):  # topN: [5, 10, 15, 20]
            top_recall, top_precision, top_ndcg, top_rmrr, top_iou = 0., 0., 0., 0., 0.
            for v in v_list:  # v:对应的ground truth
                r = []
                for i in rating[:K_max]:
                    herb = i.replace("\"", "")
                    if herb in v:
                        r.append(1)
                    else:
                        r.append(0)
                number = 0
                all_list_number = 0
                herb_results = []  # 推荐列表中herb 集合
                for i in rating[:topN[ii]]:
                    herb = i.replace("\"", "")
                    herb_results.append(herb)
                    if herb in v:
                        number += 1
                herb_v = set(herb_results + v)
                all_list_number = len(herb_v)
                # todo: modified MRR to Rank-MRR
                mrr_score = 0.
                for a_rank in range(len(v)):  # herb 在grand truth中的位置a_rank
                    if v[a_rank] in herb_results:
                        a_refer = herb_results.index(v[a_rank])  # herb 在推荐列表中的位置a_refer
                        mrr_score += 1.0 / (abs(a_refer - a_rank) + 1)
                if float(number / topN[ii]) > top_precision:  # 使用precision选择GT
                    top_precision = float(number / topN[ii])
                    top_recall = float(number / len(v))
                    top_ndcg = ndcg_at_k(r, topN[ii])
                    top_rmrr = mrr_score / len(v)
            precision_n[ii] = precision_n[ii] + top_precision  # [ii]所有测试数据top k的precision之和
            recall_n[ii] = recall_n[ii] + top_recall
            ndcg_n[ii] = ndcg_n[ii] + top_ndcg
            rmrr_n[ii] = rmrr_n[ii] + top_rmrr
    for ii in range(len(topN)):
        result['precision'][ii] = precision_n[ii] / len(test_group_list)
        result['recall'][ii] = recall_n[ii] / len(test_group_list)
        result['ndcg'][ii] = ndcg_n[ii] / len(test_group_list)
        result['rmrr'][ii] = rmrr_n[ii] / len(test_group_list)
    return result

def dcg_at_k(r, k, method=1):
    """Score is discounted cumulative gain (dcg)
    Relevance is positive real values.  Can use binary
    as the previous methods.
    Returns:
        Discounted cumulative gain
    """
    r = np.asfarray(r)[:k]
    if r.size:
        if method == 0:
            return r[0] + np.sum(r[1:] / np.log2(np.arange(2, r.size + 1)))
        elif method == 1:
            return np.sum(r / np.log2(np.arange(2, r.size + 2)))
        else:
            raise ValueError('method must be 0 or 1.')
    return 0.


def ndcg_at_k(r, k, method=1):
    """Score is normalized discounted cumulative gain (ndcg)
    Relevance is positive real values.  Can use binary
    as the previous methods.
    Returns:
        Normalized discounted cumulative gain
    """
    # dcg_max = dcg_at_k(np.ones_like(r), k, method)
    dcg_max = dcg_at_k(sorted(r, reverse=True), k, method)
    if not dcg_max:
        return 0.
    return dcg_at_k(r, k, method) / dcg_max

def herb_rec_test(gt_data, data):
    result = test_metric(gt_data, data)
    res_score = ""
    for key, value in result.items():
        res = [str(round(v, 4)) for v in value]
        print(key + ":" + ", ".join(res))


if __name__ == "__main__":
    args = parse_args()
    # 第一级三个任务一起计算，因为需要计算一个总分
    if "first_level" in args.data_path:
        question_type = "FKU"
        with open(f"{args.data_path}/{args.model_name}_{question_type}.json", "r", encoding="utf-8") as f:
            data_FKU = json.load(f)
        f.close()

        question_type = "CVR"
        with open(f"{args.data_path}/{args.model_name}_{question_type}.json", "r", encoding="utf-8") as f:
            data_CVR = json.load(f)
        f.close()

        question_type = "KHC"
        with open(f"{args.data_path}/{args.model_name}_{question_type}.json", "r", encoding="utf-8") as f:
            data_KHC = json.load(f)
        f.close()

        the_first_task(data_FKU, data_CVR, data_KHC)

    # 利用args.question_type 来分别计算其他任务的ACC
    question_type = args.question_type
    with open(f"{args.data_path}/{args.model_name}_{question_type}/seperate_0-1.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    f.close()
    if question_type in ["CBF", "SCF", "PF", "SDDT", "DDST", "SDDT_hard", "DDST_hard"]:
        A12_type_task(data)
    elif question_type in ["SDT", 'SDT_reverse', "SDT_shuffle"]:
        A34_type_task(data)
    elif question_type in ["herb_predict"]:
        gt_file_path = f"{args.data_path}/{question_type}.json"
        gt_data = new_test_gt(gt_file_path)
        herb_rec_test(gt_data, data)








