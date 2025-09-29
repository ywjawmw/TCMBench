
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

## 更新

💥 **TCMBench V2.0**来啦，这次加入了能体现中医多标准多因素的动态临床推理过程的测试题目外，还新生成了加入推理扰动的新问题，构成了三层不同难度的测评任务，13个子任务！

🚀 论文初始版本已经公开，欢迎引用，❗ 拒绝一切抄袭行为（微笑.jpg）.

## ⚡ 简介
为了进一步有效、准确的评估大模型在中医药领域的表现，我们现建立了一个标准化、综合性的中医评测框架**TCMBench**，该评测框架将充分考虑中医药领域的复杂性和专业性，涵盖多个方面，以确保大语言模型在真实场景下的实用性和适用性。


## 📚 数据集：TCMEval
首先我们构建了首个中医评测数据集TCMEval。为了客观、真实地反映中医领域的知识体系与临床推理特点，以中医执业医师资格考试的高质量模拟题为数据来源，构建了评测数据集TCMEval。该数据集共包含6,482组问答样本，其中1,300组配有官方给定的标准解析文本，用于评估大语言模型的生成质量。所有数据不涉及个人隐私，内容聚焦于中医知识临床两方面。在中医专家的指导下，本章对原始题目进行筛选与确认，从每个学科每类题型中随机抽取了不超过100个样本，同时控制选项的均匀分布，避免数据偏斜。然后由两位中医研究生进行题目确认，确保覆盖考试的全部题型与学科。通过收集、整理和标注这些数据，我们旨在提供一个全面、准确、具有代表性的中医测试基准，来帮助评估和改大语言模型应用在中医领域性能。


**🔎 任务类型** ：
- 🚀 **基础知识认知任务**：最低复杂度的任务为基础知识认知任务集，共包含5,473组问答样本。该任务集依据TCMLE考试中的标准题型，细分为三类代表性任务，分别对应不同维度的知识认知能力。涵盖基础知识理解任务（FKU）、知识点横向关联任务（KHC）以及临床逻辑纵向推理任务（CVR），数据见[./data/first_level](./data/first_level)。
- 🚀 **综合动态临床分析任务** ：在基础知识认知任务之上，结合中医专家建议进一步构建了六类具备多标准诊疗（包括辨证论治、同病异治、异病同治任务）与环境耦合多因素特征（包括社会环境、古籍经典理解以及哲学思想掌握任务）的临床推理任务集，用于评估大语言模型在真实中医临床情境下的知识融合、逻辑建模与复杂推理能力，共883组问答样本。其中每个任务均包含不少于50个样本，以支持稳定评估，数据见[./data/second_level](./data/second_level)。
-  🚀 **复杂临床决策任务** ：为进一步评估大语言模型在多标准中医临床环境中的综合推理能力和稳定性，在综合动态临床分析任务的基础上设计了四类复杂临床决策任务。该任务集通过对原始推理样本进行结构重构、语义扰动和任务形式转换（包括在辨证论治、同病异治以及异病同治任务上的扰动，以及中药推荐任务），生成了1,009组全新的问答样本。该任务集系统考察了模型在高复杂度推理中的一致性建模能力、推理鲁棒性与决策稳定性。数据见[./data/third_level](./data/third_level)。

## 👨‍⚕️ 数据处理

### 以基础知识认知任务为例
将试题转换为结构化的测评数据，其数据格式如下所示：
基础知识理解任务：
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
临床逻辑纵向推理任务：
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
知识点横向关联任务：
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

## 🧐 测评细节

我们设计了任务自适应的prompt，要求LLM回答题目，并给出答案和分析，评测框架由如下部分组成：

| 文件名                     | 说明           |
| -------------------------- | -------------- |
| [./pipline/choice_bench.py](./pipline/choice_bench.py)     | 设置不同的任务，引导LLMs生成答案与解析 |
| [./pipline/bench_function.py](./pipline/bench_function.py)   | 测试相关函数   |
| [./pipline/Acc.py](./pipline/Acc.py) | 计算准确率   |
| [./pipline/Model_API.py](./pipline/Model_API.py)| 调用模型接口，以openai为例，可根据测评模型进行调整 |
| [./TCMBench_code/explain_evaluation.py](./TCMBench_code/explain_evaluation.py)| 采用ROUGE-1，ROUGE-L, SARI，BerScore, BartScore, 以及我们提出的SKScore评估模型解析质量 |
|[./HumanTrue.json](./HumanTrue.json)| HumanTrue数据集|


首先采用[/pipline/choice_bench.py](./pipline/choice_bench.py),测试模型，得到模型生成的答案与解析
```
首先若有必要，请设置代理:
os.environ['HTTPS_PROXY']="your proxy"
其次，若采用闭源模型则将你的Key填写到指定位置，否则置空：
api_key = "your key"
然后通过设置不同的--data_path 和 --sys_prompt进行不同任务测试，设置--model_name 来调用不同的模型
使用以下命令在FKU任务对gpt-4-0613进行测试：
python choice_bench.py --data_path ../data/first_level --sys_prompt FKU.json --model_name gpt-4-0613
```

通过[./pipline/Acc.py](./pipline/Acc.py)，设置--data_path、--queation_type、--model_name，得到不同模型在不同任务上的准确率得分。
 ```
python Acc.py --data_path ../data/first_level --queation_type FKU --model_name gpt-4-0613
 ```

通过[./TCMBench_code/explain_evaluation.py](./TCMBench_code/explain_evaluation.py)，设置--model_name，得到不同模型在6个指标上的解析得分。
 ```
python explain_evaluation.py --model_name gpt-4-0613
 ```
其中指标加载的模型见[code](https://huggingface.co/WJing123/TCMBench_code)


👨‍⚕️ 此外，该工作中也介绍了我们之前构建中医LLMs，ShenNong，欢迎大家关注我们的中医大模型开源项目**ShenNong-TCM-LLM**：

- 🚀 [ShenNong-TCM](https://github.com/ywjawmw/ShenNong-TCM-LLM) : 为推动LLM在中医药领域的发展和落地，提升LLM的在中医药方面的知识与回答医学咨询的能力，我们推出了**ShenNong**中医药大规模语言模型。基于[中医药指令数据集SN-QA](https://huggingface.co/datasets/michaelwzhu/ShenNong_TCM_Dataset)。

以及我们其他医疗大模型开源项目：
- 🚀 [“医”心医意——智能中医传承创新辅助平台](https://github.com/ywjawmw/AI4TCM-Platform) : 数智岐黄系列平台，针对已有的中医传承平台无法覆盖全面的多模态数据这一挑战，我们构建了更全面的中西医知识图谱。其次，针对中医经验传承效率低这一挑战，我们提出了可解释的药方分析技术来挖掘处方信息，自动分析从症状到中药这一立体诊疗过程并给出分析的科学依据。同时提供了一个公平的辅助平台，让青年医师、中医学生等人群快速掌握先进的中医知识，传承经验。
- 🚀 [ChatMed-Consult](https://huggingface.co/michaelwzhu/ChatMed-Consult) : 基于[中文医疗在线问诊数据集ChatMed_Consult_Dataset](https://huggingface.co/datasets/michaelwzhu/ChatMed_Consult_Dataset)的50w+在线问诊+ChatGPT回复作为训练集。模型主干为[LlaMA-7b](https://github.com/facebookresearch/llama),融合了[Chinese-LlaMA-Alpaca](https://github.com/ymcui/Chinese-LLaMA-Alpaca)的LoRA权重与中文扩展词表，然后再进行基于LoRA的参数高效微调。我们将全部代码都进行了公开；
- 🚀 [PromptCBLUE中文医疗大模型评测基准](https://github.com/michael-wzhu/PromptCBLUE): 将[CBLUE](https://tianchi.aliyun.com/dataset/95414)基准进行改造为提示学习模式，形成对大模型的中文医疗知识与医疗文本处理能力的评测基准。PromptCBLUE旨在采用一个生成式大模型即可完成医疗NLP相关的各种不同任务，如病历结构化，问诊，病例文书撰写等。

## 致谢

本项目基于大模型给出的API进行开发，同时参考了大语言模型在高考试题上的测评任务，在此对相关项目和研究开发人员表示感谢。

- [ChatGPT](https://openai.com/blog/chatgpt)
- [ChatGLM](https://github.com/THUDM/ChatGLM-6B](https://github.com/THUDM/GLM)
- [GaoKao-Bench](https://github.com/OpenLMLab/GAOKAO-Bench)


## 引用

如果你使用了本项目的数据或者代码，请声明引用：

```bash
@misc{yue2023 TCMBench,
      title={TCMBench: Benchmarking Large Language Models in Traditional Chinese Medicine from Knowledge to Clinical Reasoning}, 
      author={Wenjing Yue, Ming guan, Wei Zhu, Xiaoling Wang, Saisai Tian and Weidong Zhang},
      year={2023},
      publisher = {GitHub},
      journal = {GitHub repository},
      howpublished = {\url{https://github.com/ywjawmw/TCMBench}},
}

```

## 团队介绍

本项目在华东师范大学计算机科学与技术学院智能知识管理与服务团队王晓玲教授、海军军医大学天然药物化学教研室张卫东教授、田赛赛研究员指导下完成。



