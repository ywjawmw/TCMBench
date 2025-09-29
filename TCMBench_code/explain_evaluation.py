#!/usr/bin/env python
# !/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2025/9/28 23:10
# @Author  : Wenjing
# @File    : explain_evaluation.py
# @Desc    : 评估LLMs生成解析的质量

import argparse
import json
import sys
import json
import math
import os
import time
from typing import List, Dict
from sari import SARIsent
import numpy as np
from BARTScore.bart_score_chinese import BARTScorerChinese
# from BARTScore.bart_score import BARTScorer
import evaluate, torch
import statistics
from rouge_chinese import Rouge
import jieba
from transformers import (
    AutoConfig,
    AutoModelForSequenceClassification,
    AutoTokenizer
)
from sklearn.metrics import roc_auc_score
from sklearn import metrics
from matplotlib import pyplot as plt

jieba.load_userdict("jieba_tcm.txt")    # load进入TCM术语
with open('jieba_tcm.txt', 'r', encoding='utf-8') as f:
  tcm_terms = f.readlines()
  tcm_term_db = [t.strip() for t in tcm_terms]

def parse_args():
    parser = argparse.ArgumentParser(description="parameter of LLMs")
    parser.add_argument(
        "--model_name",
        type=str,
        default='gpt-4-0613',
        help="The LLM name.",
    )
    args = parser.parse_args()
    return args


def get_analysis_A12(data_dict_predict):
    correct_analysis, predict_analysis = [], []
    for data in data_dict_predict['example']:
        if len(data['analysis']) > 0:
            correct_analysis.append(data['analysis'])
            predict_analysis.append(data['model_output'])
    return correct_analysis, predict_analysis


def get_analysis_A34(data_dict_predict):
    correct_analysis, predict_analysis = [], []
    for data in data_dict_predict['example']:
        question = data["question"]
        for sub_question in question:
            if len(sub_question['analysis']) > 0:
                correct_analysis.append(sub_question['analysis'])
                predict_analysis.append(sub_question['model_output'])
    return correct_analysis, predict_analysis


def rouge_score(correct_analysis, predict_analysis):
    # rouge = evaluate.load('rouge')
    # results = rouge.compute(predictions=correct_analysis,
    #                         references=predict_analysis,
    #                         rouge_types=['rouge1', 'rougeL'],
    #                         use_aggregator=False)
    rouge = Rouge()
    empty_num = 0
    correct_analysis_cal, predict_analysis_cal = [], []
    for ca, pa in zip(correct_analysis, predict_analysis):
        if len(pa) == 0:
            empty_num += 1
        else:
            correct_analysis_cal.append(' '.join(jieba.cut(ca)))
            predict_analysis_cal.append(' '.join(jieba.cut(pa)))
    scores = rouge.get_scores(predict_analysis_cal, correct_analysis_cal)
    results_rouge1 = [round(score['rouge-1']['r'],2) for score in scores] + [0.0] * empty_num
    results_rougel = [round(score['rouge-l']['f'], 2) for score in scores] + [0.0] * empty_num
    return np.mean(results_rouge1), np.mean(results_rougel)

def bert_score(correct_analysis, predict_analysis):
    bertscore = evaluate.load('../TCMBench_code/bertscore')
    results = bertscore.compute(predictions=predict_analysis, references=correct_analysis, lang="zh",
                                model_type="bert-base-chinese")
    score = [round(v, 2) for v in results["f1"]]
    return np.mean(score)

def bart_Score(correct_analysis, predict_analysis):
    bart_scorer = BARTScorerChinese(checkpoint='bart-base-chinese')
    bart_scores = bart_scorer.score(correct_analysis, predict_analysis, batch_size=4)
    # print("BART Score", np.mean(bart_scores))
    return np.mean(bart_scores)

def calculate_sari(
        input_lns: List[str], output_lns: List[str], reference_lns: List[str]
) -> Dict:
    a, b, c, d = [], [], [], []
    for input, output, ref in zip(input_lns, output_lns, reference_lns):
        a_, b_, c_, d_ = SARIsent(input, output, [ref])

        a.append(round(a_,2))
    return a


def sari_score(correct_analysis, predict_analysis):
    sariscores = calculate_sari(correct_analysis, predict_analysis, correct_analysis)  # 参考答案根据reference  只看sari_avgkeepscore
    # print(f"SARI score_解析: {sariscores}")
    return np.mean(sariscores)

print("使用 x / sum_x，缩放f1的值")
def softmax(x):
    e_x = x
    sum_x = e_x.sum(axis=0)
    if sum_x == 2 * x.size:  # 标准解析中就没有中医术语，那么解析中的每一句话的f1score都=2
        return [1/x.size] * x.size  # 加和平均
    elif sum_x == 0:
        return [0] * x.size    # 也就是LLMs中没有中医术语，那么这个解析是不好的，给一个特别低的分数
    else:
        return x / sum_x

import re
def split_sentences(text):
    # 利用正则表达式按照句号、感叹号、问号进行划分
    sentences = re.split(r'(?<=[。！？])\s*', text)
    # 去除空字符串和空白符
    sentences = [s.strip() for s in sentences if s.strip()]
    return sentences

from collections import Counter
def tcm_score_f1(analysis_tcm_terms_counter, analysis_terms_counter, doc, tcm_term_db):
    """
    中医术语匹配度
    :param analysis_tcm_terms_counter: 解析中的中医术语以及计数
    :param analysis_terms_counter: 解析
    :param doc:  需要检测的语句
    :param tcm_term_db:  中医术语库
    :return:
    """

    doc_terms_list = list(jieba.cut(doc))
    doc_terms_counter = Counter(doc_terms_list)
    doc_tcm_terms_list = [term for term in doc_terms_list if term in tcm_term_db]
    doc_tcm_terms_counter = Counter(doc_tcm_terms_list)  # 片段中所有的中医术语计数
    if len(analysis_tcm_terms_counter) == 0:
        return 2   # 如果解析中没有中医术语，那么就不需要进行F1score的计算
    elif len(doc_tcm_terms_counter) == 0:
        return 0   # # 如果LLMs中没有中医术语，那么F1score=0, 说明这句话不符合中医诊疗语言，或者没有什么信息量
    comment_term_counter = analysis_tcm_terms_counter & doc_tcm_terms_counter  # 重复的中医术语
    recall_comment_score, precision_comment_score = 0, 0
    for term in comment_term_counter:
        recall_comment_score += comment_term_counter[term] / analysis_tcm_terms_counter[term]
        precision_comment_score += comment_term_counter[term] / doc_tcm_terms_counter[term]
    recall = recall_comment_score / len(analysis_tcm_terms_counter)   # 重复的中医术语个数/解析中的中医术语个数 —— 重叠度
    precision = precision_comment_score / len(doc_tcm_terms_counter)   # 重复的中医术语个数/ 文档的中医术语个数 —— 冗余度
    informational = len(list(set(doc_tcm_terms_list))) / len(list(set(doc_terms_list)))
    # informational = len(doc_tcm_terms_counter) / len(doc_terms_counter) * (sum(doc_terms_counter.values()) / sum(analysis_terms_counter.values()))  # 片段中的中医术语 / 片段中术语个数（不重复） * (片段的术语总个数 / 解析的术语总个数)[长度的惩罚项] —— 信息度
    if precision == 0 or recall == 0:
        return 0
    else:
        f1_score = 3 * (precision * recall * informational) / (precision + recall + informational)
        return f1_score

def calculate_score(sentence, sample, model, tokenizer):
    inputs = tokenizer.batch_encode_plus(
        batch_text_or_text_pairs=[(sentence, sample)],
        add_special_tokens=True, padding="longest",
        truncation=True, return_tensors="pt",
        return_token_type_ids=True, return_attention_mask=True,
        max_length=512
    )

    logits = model(**inputs).logits  # neutral is already removed
    # print(logits)
    probs = torch.argmax(logits, dim=-1)
    prob_label = probs[0].item()  # 类别
    probs1 = torch.softmax(logits, dim=-1)
    prob_1 = probs1[0][0].item()  # prob(相关程度)
    return prob_label, prob_1

def f1_score_tcm_term(analysis_tcm_terms_list, analysis_terms_list, doc, tcm_term_db):
    """
    中医术语匹配度
    :param analysis_tcm_terms_list: 解析中的中医术语
    :param analysis_terms_list: 解析
    :param doc:  需要检测的语句
    :param tcm_term_db:  中医术语库
    :return:
    """

    doc_terms_list = list(jieba.cut(doc))
    doc_tcm_terms_list = [term for term in doc_terms_list if term in tcm_term_db]
    doc_tcm_terms_list = doc_tcm_terms_list  # 片段中所有的中医术语(含有重复元素）
    if len(analysis_tcm_terms_list) == 0:
        return 2   # 如果解析中没有中医术语，那么就不需要进行F1score的计算
    elif len(doc_tcm_terms_list) == 0:
        return 0   # # 如果LLMs中没有中医术语，那么F1score=0, 说明这句话不符合中医诊疗语言，或者没有什么信息量
    comment_term = set(analysis_tcm_terms_list) & set(doc_terms_list)  # 重复的中医术语
    comment_num = 0
    for doc_term in doc_tcm_terms_list:
        if doc_term in comment_term:
            comment_num += 1
    recall = comment_num / len(analysis_tcm_terms_list)   # 重复的中医术语个数/真正对的中医术语个数 —— 重叠度
    precision = comment_num / len(doc_tcm_terms_list)   # 重复的中医术语个数/ 文档的中医术语个数 —— 冗余度
    informational = len(list(set(doc_tcm_terms_list))) / len(list(set(doc_terms_list)))
    if precision == 0 or recall == 0 or informational == 0:
        return 0
    else:
        f1_score = 3 * (precision * recall * informational) / (precision + recall + informational)
        return f1_score


def predict_analysys_response(sentences: List[str], sampled_passages: List[str], model, tokenizer):
    """
    :param sentences: list of 标准解析
    :param sampled_passages: LLMs的解析
    """
    scores1 = list()  # 计算LLMs生成的解析与标准解析之间的分数
    scores1_counter = list()  # _counter
    scores1_nof1 = list()
    scores1_dotf1 = list()
    num = 0
    for sentence, sample in zip(sentences, sampled_passages):  # 解析
        if num == 0:
            print(f"sentence: {sentence}")
            print(f"sample: {sample}")
        num += 1
        # 分句
        response_sentence_list = split_sentences(sample)
        analysis_sentence_list = split_sentences(sentence)
        tcm_score = []
        tcm_score_counter = []
        prob_score_list = []
        tcm_score_dotf1 = []
        for analysis_sentence in analysis_sentence_list:  # 分句
            f1_score, prob_score = [], []
            f1_score_counter = []
            if len(response_sentence_list) > 0:
                for response_sentence in response_sentence_list:  # LLMs分析分句
                    # 统计标准解析中的中医术语
                    analysis_terms = list(jieba.cut(analysis_sentence))
                    analysis_terms_counter = Counter(analysis_terms)
                    analysis_tcm_terms_list = [term for term in analysis_terms if term in tcm_term_db]
                    analysis_tcm_terms_counter = Counter(analysis_tcm_terms_list)  # 解析中的中医术语计数
                    analysis_tcm_terms_list = list(analysis_tcm_terms_counter.keys())  # 解析中的中医术语列表

                    prob_label_A, prob_1_A = calculate_score(analysis_sentence, response_sentence, model, tokenizer)
                    prob_label_reverse_A, prob_1_reserve_A = calculate_score(response_sentence, analysis_sentence,
                                                                             model, tokenizer)
                    prob = (prob_1_A + prob_1_reserve_A) / 2
                    ################## TCM score ####################
                    f1_term_score = f1_score_tcm_term(analysis_tcm_terms_list, analysis_terms, response_sentence, tcm_term_db)
                    f1_term_score_counter = tcm_score_f1(analysis_tcm_terms_counter, analysis_terms_counter, response_sentence, tcm_term_db)
                    f1_score.append(f1_term_score)
                    prob_score.append(prob)
                    f1_score_counter.append(f1_term_score_counter)
                f1_score = np.array(f1_score)

                ####不加f1 score#######
                average_prob_score = statistics.mean(prob_score)
                prob_score_list.append(average_prob_score)

                prob_score = np.array(prob_score)
                f1_score_counter = np.array(f1_score_counter)
                # 对列表进行归一化
                try:
                    normalized_f1_score = softmax(f1_score)
                    normalized_f1_score_counter = softmax(f1_score_counter)
                except:
                    print(response_sentence_list)
                    print(f1_score)
                    sys.exit()

                #####直接与F1 score相乘#####
                analysis_sentence_dotf1 = np.sum(f1_score * prob_score) / prob_score.size
                tcm_score_dotf1.append(analysis_sentence_dotf1)
                ###### 计算相乘并相加的结果，加权平均
                analysis_sentence_score = np.sum(normalized_f1_score * prob_score)
                tcm_score.append(analysis_sentence_score)
                # 用Counter计算的score
                analysis_sentence_score_counter = np.sum(normalized_f1_score_counter * prob_score)
                tcm_score_counter.append(analysis_sentence_score_counter)
            else:
                tcm_score.append(0)
                tcm_score_counter.append(0)
                tcm_score_dotf1.append(0)
                prob_score_list.append(0)
        if len(sample) < len(sentence):
            if len(sample) > 1:
                length_penalty = math.exp(1 - math.log(len(sentence)) / math.log(len(sample)))
            elif len(sample) == 1:
                length_penalty = math.exp(1 - math.log(len(sentence)) / math.log(len(sample) + 1))
            else:
                length_penalty = 0
        else:
            # length_penalty = 1
            length_penalty = math.exp(1 - math.log(len(sample)) / math.log(len(sentence)))
        scores_per_response = statistics.mean(tcm_score) * length_penalty
        scores1.append(scores_per_response)
        # 用Counter计算的score
        scores_per_response_counter = statistics.mean(tcm_score_counter) * length_penalty
        scores1_counter.append(scores_per_response_counter)
        ############不加f1 score
        scores1_nof1.append(statistics.mean(prob_score_list))
        #####直接与F1 score相乘#####
        scores_per_response_dotf1 = statistics.mean(tcm_score_dotf1)
        scores1_dotf1.append(scores_per_response_dotf1)
    scores_per_doc = statistics.mean(scores1)
    scores_per_doc_counter = scores1_counter
    print("解析与回答之间的TCM Score，用Counter计算:", scores_per_doc_counter)
    return scores_per_doc_counter

def nli_score(references, predictions, model, tokenizer):
    n_score = predict_analysys_response(sentences=references,  sampled_passages=predictions, model=model, tokenizer=tokenizer)
    return n_score


if __name__ == "__main__":
    args = parse_args()
    question_type = "FKU"
    with open(f"../data/first_level/{args.model_name}_{question_type}.json", "r", encoding="utf-8") as f:
        data_FKU = json.load(f)
    f.close()

    question_type = "CVR"
    with open(f"../data/first_level/{args.model_name}_{question_type}.json", "r", encoding="utf-8") as f:
        data_CVR = json.load(f)
    f.close()

    question_type = "KHC"
    with open(f"../data/first_level/{args.model_name}_{question_type}.json", "r", encoding="utf-8") as f:
        data_KHC = json.load(f)
    f.close()

    correct_analysis, predict_analysis = [], []
    correct_analysis_A12, predict_analysis_A12 = get_analysis_A12(data_FKU)
    correct_analysis_A3, predict_analysis_A3 = get_analysis_A34(data_CVR)
    correct_analysis_B1, predict_analysis_B1 = get_analysis_A34(data_KHC)
    correct_analysis += correct_analysis_A12 + correct_analysis_A3 + correct_analysis_B1
    predict_analysis += predict_analysis_A12 + predict_analysis_A3 + predict_analysis_B1

    rouge1, rouge_L = rouge_score(correct_analysis, predict_analysis)
    print("ROUGE-1：", rouge1)
    print("ROUGE-L:", rouge_L)
    sari_scores = sari_score(correct_analysis, predict_analysis)
    print("SARI:", sari_scores)
    bert_scores = bert_score(correct_analysis, predict_analysis)
    print("BERTScore:", bert_scores)
    bart_scores = bart_Score(correct_analysis, predict_analysis)
    print("BARTScore:", bart_scores)

    # SKScore
    model_name_or_path = "../TCMBench_code/Deberta-V3-base-tmnli-QAC"
    print(model_name_or_path)
    config = AutoConfig.from_pretrained(
        model_name_or_path,
        num_labels=3,
        finetuning_task="mnli",
        trust_remote_code=False
    )
    tokenizer = AutoTokenizer.from_pretrained(
        model_name_or_path, use_fast=not False, trust_remote_code=False
    )
    # print(tokenizer)
    model = AutoModelForSequenceClassification.from_pretrained(
        f"{model_name_or_path}",
        from_tf=bool(".ckpt" in model_name_or_path),
        config=config,
        ignore_mismatched_sizes=False,
    )
    sk_score = nli_score(correct_analysis, predict_analysis, model, tokenizer)
    SKScore = np.mean(sk_score)
    print("SKScore:", SKScore)


