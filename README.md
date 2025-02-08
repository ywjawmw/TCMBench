# TCMBench: A Comprehensive Benchmark for Evaluating Large Language Models in Traditional Chinese Medicine
Repo for TCMBench (The first comprehensive benchmark for evaluating LLMs in TCM)

The [paper](https://arxiv.org/abs/2406.01126) has been submitted to XXX.

[**English**](./README.md) | [**中文**](./README_Chinese.md)

<p align="center">
    <img alt="GitHub" src="https://img.shields.io/github/license/ymcui/Chinese-LLaMA-Alpaca.svg?color=blue&style=flat-square">
    <img alt="GitHub top language" src="https://img.shields.io/github/languages/top/ymcui/Chinese-LLaMA-Alpaca">
</p>

## ⚡ 简介
Large Language Models (LLMs) excel in various natural language processing tasks but lack dedicated benchmarks for traditional Chinese medicine (TCM). To fill this gap, we introduce **TCMBench**, a comprehensive benchmark for evaluating LLMs in TCM. 


## 📚 Dataset：TCM-ED
The TCMLE assesses whether applicants possess the necessary professional knowledge and skills to practice as TCM physicians. Therefore, we collect 5,473 representative practice questions. Among them, the data we collect does not contain personal information but focuses on selecting data instances that can fully reflect and represent theoretical knowledge and practical skills in TCM. The multiple-choice questions in TCMLE. are divided into three categories: A1/A2, A3, and B1. A1/A2 questions consist of one question with five options. A3 questions include multiple sub-questions that share a typical clinical case, simulating actual clinical scenarios. B1 questions also contain multiple sub-questions but share the same five options. Consequently, A3 and B1 questions establish a logical correlation in clinical and knowledge, respectively. For detailed descriptions and examples of three types of questions, please refer to section A of appendix files.

**🔎 题目类型** ：
- 🚀 **The single-sentence best-choice questions(A1) and the case summary best-choice questions(A2) type**: It consists of a question stem and five options with correct one.
- 🚀 **The best choice questions for case group(A3) type**: The stem presents a patient-centered case, followed by multiple sub-questions, each offering five options with one correct answer. It primarily centers on clinical applications.
- 🚀 **The standard compatibility questions(B1) type**: Multiple sub-questions share the same five options, where each option may be chosen zero, one, or multiple times. There is one correct answer among the five options for each sub-question.


TCM-ED：

| Question type           | A1/A2 type| A3 type|B1 type|
| ------------------ | -------------- | -------------- |-------------- |
| **Number of questions**           | 1600           | 198         |1481         |
| **Number of sub-questions**             | \           | 642          | 3231          |



## 👨‍⚕️ Data Processing

A1/A2 type：
```json
 {
      "question": "《素问·咳论》：“五脏六腑皆令人咳”，但关系最密切的是（  ）。\nA．心肺\nB．肺肾\nC．肺脾\nD．肺胃\nE．肺大肠",
      "answer": [
        "D"
      ],
      "analysis": "根据《素问·咳论》“此皆聚于胃，关于肺，使人多涕唾而面浮肿气逆也”可知与五脏六腑皆令人咳关系最密切的脏腑为肺胃。手太阴肺经起于中焦，还循胃口，上膈属肺。寒凉饮食入胃，导致中焦寒，寒气循手太阴肺经上入于肺中，导致肺寒，肺为娇脏，不耐寒热，外内寒邪并聚于肺，则肺失宣降，肺气上逆发生咳嗽。因此答案选D。",
      "knowledge_point": "中医经典",
      "index": 8196,
      "score": 1
    }
```
A3 type：
```json
    {
      "share_content": "刘×，男，46岁，刻下眩晕而见头重如蒙。胸闷恶心，食少多寐，苔白腻，脉濡滑。",
      "question": [
        {
          "sub_question": "1)．证属（  ）。\nA．肝阳上亢\nB．气血亏虚\nC．肾精不足\nD．痰浊中阻\nE．以上都不是\n",
          "answer": [
            "D"
          ],
          "analysis": ""
        },
        {
          "sub_question": "2)．治法宜选（  ）。\nA．燥湿祛痰，健脾和胃\nB．补肾滋阴\nC．补肾助阳\nD．补养气血，健运脾胃\nE．平肝潜阳，滋养肝肾\n",
          "answer": [
            "A"
          ],
          "analysis": ""
        },
        {
          "sub_question": "3)．方药宜选（  ）。\nA．右归丸\nB．左归丸\nC．半夏白术天麻汤\nD．归脾汤\nE．天麻钩藤饮\n",
          "answer": [
            "C"
          ],
          "analysis": ""
        }
      ],
      "knowledge_point": "中医内科学",
      "index": 334,
      "score": 1
    }
```
B1 type：
```json
  {
      "share_content": "（共用备选答案）\nA.化痰息风，健脾祛湿\nB.清肺化痰，散结排脓\nC.疏风宣肺，化痰止咳\nD.清热化痰，平肝息风\nE.润肺清热，理气化痰\n",
      "question": [
        {
          "sub_question": "1)．贝母瓜蒌散的功用是（  ）。",
          "answer": [
            "E"
          ],
          "analysis": ""
        },
        {
          "sub_question": "2)．半夏白术天麻汤的功用是（  ）。",
          "answer": [
            "A"
          ],
          "analysis": ""
        }
      ],
      "knowledge_point": "方剂学",
      "index": 1938,
      "score": 1
    }
```

## 🧐 Evaluation Pipeline


| File Name                     | Description           |
| -------------------------- | -------------- |
| /evaluate/A12_bench.py     | Generating answers for A1/A2 type of quesions |
| /evaluate/A3-B1_bench.py      | Generating answers for A3/B1 type of quesions|
| /evaluate/bench_function.py   | Test   |
| /evaluate/correct_analyse.py  | Accuracy Metric   |
| /prompt/A1-2_prompt.json| Prompt of A1/A2 type of quesions| 
| /prompt/A3-4_prompt.json| Prompt of A3 type of quesions| 
| /prompt/B1_prompt.json| Prompt of B1 type of quesions| 
| /models/Openai.py| Model API(eg. openai) |




You can run with API[A12_bench.py](https://github.com/ywjawmw/ShenNong-TCM-Evaluation-BenchMark/blob/main/evaluate/A12_bench.py)/[A3-B1_bench.py](https://github.com/ywjawmw/ShenNong-TCM-Evaluation-BenchMark/blob/main/evaluate/A3-B1_bench.py).
```
First set the proxy:
os.environ['HTTPS_PROXY']="your proxy"
Next，fill your OpenAI Key：
openai_api_key = "your key"
Run with：
python A12_bench.py
python A3-B1_bench.py
```

Finally，You can run with [correct_analyse.py](https://github.com/ywjawmw/ShenNong-TCM-Evaluation-BenchMark/blob/main/evaluate/correct_analyse.py) to get the accrucy。
 ```
python correct_analyse.py
 ``` 


👨‍⚕️ Welcome everyone to follow our open source project for TCM LLM **ShenNong-TCM**, this is the first version：

- 🚀 [ShenNong-TCM](https://github.com/michael-wzhu/ShenNong-TCM-LLM) : To promote the development and implementation of LLM in the field of TCM, enhance LLM's knowledge and ability to answer medical consultations in the field of traditional Chinese medicine, we have launched the **ShenNong** Large scale Language Model for Traditional Chinese Medicine. Based on the [TCM prompt dataset: ShenNong_TCM_Dataset](https://huggingface.co/datasets/michaelwzhu/ShenNong_TCM_Dataset)。

And our other open source projects for medical LLMs：
- 🚀 [Intelligent TCM Inheritance and Innovation Assistance Platform](https://github.com/ywjawmw/AI4TCM-Platform) ;
- 🚀 [ChatMed-Consult](https://huggingface.co/michaelwzhu/ChatMed-Consult) ；
- 🚀 [PromptCBLUE](https://github.com/michael-wzhu/PromptCBLUE);

## Acknowledge

- [ChatGPT](https://openai.com/blog/chatgpt)
- [ChatGLM](https://github.com/THUDM/ChatGLM-6B)
- [GaoKao-Bench](https://github.com/OpenLMLab/GAOKAO-Bench)


## Citation

Please cite：


## Team Introduction

This project was completed by the Intelligent Knowledge Management and Service Team of the School of Computer Science and Technology, East China Normal University, under the guidance of Professor Xiaoling Wang .

Project members：
- [ywjawmw](https://github.com/ywjawmw)
- [michael-wzhu](https://github.com/michael-wzhu)
