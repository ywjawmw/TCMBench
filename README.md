## TCMBench: Benchmarking Large Language Models in Traditional Chinese Medicine from Knowledge to Clinical Reasoning
Repo for TCMBench (“ShuzhiQihuang” LLMs series，The first comprehensive benchmark for evaluating LLMs in TCM)

[**English**](./README.md) | [**中文**](./README_Chinese.md)

<p align="center">
    <br>
    <img src="./image/TCMBench_logo.png" width="355"/>
    <br>
</p>
<p align="center">
    <img alt="GitHub" src="https://img.shields.io/github/license/ymcui/Chinese-LLaMA-Alpaca.svg?color=blue&style=flat-square">
    <img alt="GitHub top language" src="https://img.shields.io/github/languages/top/ymcui/Chinese-LLaMA-Alpaca">
</p>

## Updates

💥 TCMBench V2.0 is here! In this version, we added test questions that reflect the multi-standard and multi-factor characteristics of dynamic clinical reasoning in TCM. We also generated new questions with reasoning perturbations, forming three levels of evaluation tasks and 13 sub-tasks in total.

🚀 The initial version of the paper has been released. Citations are welcome. ❗ All forms of plagiarism are strictly rejected (smile.jpg).

## ⚡ Introduction

To further evaluate the performance of large language models (LLMs) in Traditional Chinese Medicine (TCM) more effectively and accurately, we established a standardized and comprehensive benchmark framework: TCMBench. This benchmark fully considers the complexity and domain-specific nature of TCM, covering multiple aspects to ensure the practical usability and applicability of LLMs in real-world TCM scenarios.

📚 Dataset: TCMEval

We first constructed the TCMEval dataset, the first benchmark dataset in TCM. To objectively and accurately reflect the knowledge system and clinical reasoning characteristics of TCM, TCMEval is built using high-quality simulated questions from the TCM Licensing Examination as the data source.

The dataset contains 6,482 question–answer pairs, of which 1,300 pairs are accompanied by official standard explanations for evaluating the generation quality of LLMs. All data avoids personal information and focuses on TCM knowledge and clinical content.

Under the guidance of TCM experts, the original questions were filtered and confirmed. From each subject and question type, no more than 100 samples were randomly selected while ensuring an even distribution of answer options to avoid data bias. Two graduate students in TCM further verified the questions, ensuring full coverage of all exam subjects and question types. Through this collection, organization, and annotation process, TCMEval provides a comprehensive, accurate, and representative TCM benchmark to support the evaluation and improvement of LLM applications in TCM.

**🔎 Task Types**:
- 🚀 **Fundamental Knowledge Cognition Tasks**:The lowest complexity level includes 5,473 Q&A pairs. This task set is based on standard question types in the TCMLE exam and subdivided into three representative tasks, each reflecting different dimensions of knowledge cognition:
	- Fundamental Knowledge Understanding (FKU)
	- Knowledge Horizontal Correlation (KHC)
	- Clinical Vertical Reasoning (CVR)
    Data available at [./data/first_level](./data/first_level).
- 🚀 **Comprehensive Dynamic Clinical Analysis Tasks**:Built on top of the fundamental knowledge cognition tasks and designed with input from TCM experts, this set includes six types of tasks featuring multi-standard diagnosis and treatment (e.g., syndrome differentiation and treatment, one disease with different treatments, different diseases with the same treatment) and multi-factor reasoning (e.g., social environment, classical literature interpretation, and philosophical understanding).
This set contains 883 Q&A pairs, with at least 50 samples per task to ensure stable evaluation.
Data available at [./data/second_level](./data/second_level)l.
- 🚀 **Complex Clinical Decision-Making Tasks**:To further evaluate the comprehensive reasoning ability and stability of LLMs in multi-standard TCM clinical environments, we designed four types of complex decision-making tasks based on the dynamic clinical analysis tasks. By restructuring original reasoning samples, introducing semantic perturbations, and converting task formats (e.g., perturbations in syndrome differentiation and treatment, one disease with different treatments, different diseases with the same treatment, as well as Chinese medicine prescription tasks), we generated 1,009 new Q&A pairs.This task set systematically examines model consistency in high-complexity reasoning, robustness in inference, and stability in decision-making.
Data available at [./data/third_level](./data/third_level).

## 👨‍⚕️ Data Processing

### Example: Fundamental Knowledge Cognition Tasks

We converted the test questions into structured evaluation data. The data format is as follows:

Fundamental Knowledge Understanding Task
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
Clinical Vertical Reasoning Task：
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
Knowledge Horizontal Correlation Task：
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

## 🧐 Evaluation Details

We designed task-adaptive prompts that require LLMs to answer questions and provide explanations. The evaluation framework consists of the following components:

| 文件名                     | 说明           |
| -------------------------- | -------------- |
| [./pipline/choice_bench.py](./pipline/choice_bench.py)     | Set up different tasks and guide LLMs to generate answers and explanations|
| [./pipline/bench_function.py](./pipline/bench_function.py)   | Functions for testing   |
| [./pipline/Acc.py](./pipline/Acc.py) | Compute accuracy   |
| [./pipline/Model_API.py](./pipline/Model_API.py)| Call model APIs (OpenAI as an example), adjustable for different models |
| [./TCMBench_code/explain_evaluation.py](./TCMBench_code/explain_evaluation.py)| Evaluate explanation quality using ROUGE-1, ROUGE-L, SARI, BERTScore, BartScore, and our proposed SKScore |
|[./HumanTrue.json](./HumanTrue.json)| HumanTrue Dataset|


First, run [/pipline/choice_bench.py](./pipline/choice_bench.py) to test models and obtain their generated answers and explanations:
```
# (Optional) If needed, set your proxy:
os.environ['HTTPS_PROXY']="your proxy"

# If using closed-source models, enter your API key; otherwise leave blank:
api_key = "your key"

# Specify --data_path and --sys_prompt for different tasks, and --model_name to call different models.
# Example: run the FKU task on gpt-4-0613
python choice_bench.py --data_path ../data/first_level --sys_prompt FKU.json --model_name gpt-4-0613
```

Use [./pipline/Acc.py](./pipline/Acc.py) to compute accuracy scores for different models on different tasks by setting --data_path, --queation_type, and --model_name:
 ```
python Acc.py --data_path ../data/first_level --queation_type FKU --model_name gpt-4-0613
 ```

Use [./TCMBench_code/explain_evaluation.py](./TCMBench_code/explain_evaluation.py) to compute explanation scores across six metrics by specifying --model_name:
 ```
python explain_evaluation.py --model_name gpt-4-0613
 ```
The models used for these metrics can be found at [code link](https://huggingface.co/WJing123/TCMBench_code)


👨‍⚕️ In addition, this work also introduces our previously developed TCM LLMs, ShenNong. We welcome everyone to follow our open-source TCM large language model project ShenNong-TCM-LLM: **ShenNong-TCM-LLM**：

- 🚀 [ShenNong-TCM](https://github.com/ywjawmw/ShenNong-TCM-LLM) : To promote the development and real-world application of LLMs in Traditional Chinese Medicine, we released ShenNong, a large-scale TCM language model designed to improve knowledge coverage and enhance its ability to answer medical consultations in TCM. It is built upon the [TCM instruction dataset SN-QA](https://huggingface.co/datasets/michaelwzhu/ShenNong_TCM_Dataset)。

We also introduce our other open-source healthcare LLM projects:
- 🚀 [Intelligent TCM Inheritance and Innovation Platform](https://github.com/ywjawmw/AI4TCM-Platform) : As part of the Shuzhi Qihuang series, this platform addresses two main challenges: 1.	The inability of existing TCM platforms to cover multimodal data by constructing a more comprehensive knowledge graph integrating TCM and Western medicine. 2.	The inefficiency in TCM experience inheritance by proposing interpretable prescription analysis technology that automatically analyzes the holistic diagnostic process from symptoms to prescriptions and provides scientific reasoning. It also provides a fair platform to help young doctors and TCM students quickly master advanced knowledge and inherit medical expertise.
- 🚀 [ChatMed-Consult](https://huggingface.co/michaelwzhu/ChatMed-Consult) : Built from the [ChatMed_Consult_Dataset](https://huggingface.co/datasets/michaelwzhu/ChatMed_Consult_Dataset) with over 500k online medical consultations paired with ChatGPT responses. The model backbone is [LlaMA-7b](https://github.com/facebookresearch/llama), combined with LoRA weights from [Chinese-LlaMA-Alpaca](https://github.com/ymcui/Chinese-LLaMA-Alpaca) and extended Chinese vocabulary, followed by efficient parameter tuning using LoRA. All codes are publicly released.
  
- 🚀 [PromptCBLUE中文医疗大模型评测基准](https://github.com/michael-wzhu/PromptCBLUE): A prompt-based adaptation of the [CBLUE](https://tianchi.aliyun.com/dataset/95414) benchmark, designed to evaluate Chinese medical knowledge and text-processing abilities of LLMs. PromptCBLUE enables a single generative LLM to handle a variety of medical NLP tasks such as medical record structuring, consultation, and clinical documentation writing.

## Acknowledgements

This project was developed based on APIs of large language models and inspired by evaluation tasks on Gaokao examination questions. We thank the related projects and developers for their contributions:

- [ChatGPT](https://openai.com/blog/chatgpt)
- [ChatGLM](https://github.com/THUDM/ChatGLM-6B)
- [GaoKao-Bench](https://github.com/OpenLMLab/GAOKAO-Bench)


## Citation

If you use the data or code from this project, please cite:

```bash
@misc{yue2023 TCMBench,
      title={TCMBench: Benchmarking Large Language Models in Traditional Chinese Medicine from Knowledge to Clinical Reasoning}, 
      author={Wenjing Yue, Xiaoling Wang, Ming guan, Wei Zhu, Honglin li},
      year={2023},
      publisher = {GitHub},
      journal = {GitHub repository},
      howpublished = {\url{https://github.com/ywjawmw/TCMBench}},
}

```

## Team

This project was completed under the guidance of **Prof. Xiaoling Wang** from the School of Computer Science and Technology, East China Normal University.





