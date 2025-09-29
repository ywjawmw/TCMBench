# TCMBench: Benchmarking Large Language Models in Traditional Chinese Medicine from Knowledge to Clinical Reasoning
Repo for TCMBench (“ShuzhiQihuang” LLMs series，The first comprehensive benchmark for evaluating LLMs in TCM)

## 更新

🚀 TCMBench V2.0来啦，这次加入了能体现中医多标准多因素的动态临床推理过程的测试题目外，还新生成了加入推理扰动的新问题，构成了三层不同难度的测评任务，13个子任务！

🚀 论文初始版本已经公开，欢迎引用，❗ 拒绝一切抄袭行为（微笑.jpg）.

[**English**](./README.md) | [**中文**](./README_Chinese.md)

<p align="center">
    <img alt="GitHub" src="https://img.shields.io/github/license/ymcui/Chinese-LLaMA-Alpaca.svg?color=blue&style=flat-square">
    <img alt="GitHub top language" src="https://img.shields.io/github/languages/top/ymcui/Chinese-LLaMA-Alpaca">
</p>

## ⚡ 简介
为了进一步有效、准确的评估大模型在中医药领域的表现，我们现建立了一个标准化、综合性的中医评测框架**TCMBench**，该评测框架将充分考虑中医药领域的复杂性和专业性，涵盖多个方面，以确保大语言模型在真实场景下的实用性和适用性。


## 📚 数据集：TCMEval
首先我们构建了首个中医评测数据集TCMEval。为了客观、真实地反映中医领域的知识体系与临床推理特点，以中医执业医师资格考试的高质量模拟题为数据来源，构建了评测数据集TCMEval。该数据集共包含6,482组问答样本，其中1,300组配有官方给定的标准解析文本，用于评估大语言模型的生成质量。所有数据不涉及个人隐私，内容聚焦于中医知识临床两方面。在中医专家的指导下，本章对原始题目进行筛选与确认，从每个学科每类题型中随机抽取了不超过100个样本，同时控制选项的均匀分布，避免数据偏斜。然后由两位中医研究生进行题目确认，确保覆盖考试的全部题型与学科。通过收集、整理和标注这些数据，我们旨在提供一个全面、准确、具有代表性的中医测试基准，来帮助评估和改大语言模型应用在中医领域性能。


**🔎 任务类型** ：
- 🚀 **最佳选择题或单项选择题（A型题）**：每道试题由一个题干与A、B、C、D、E5个备选答案组成，题干在前，5个备选答案在后。5个备选答案中只有一项是正确答案A。型题采用为A1型题、A2型题2种题型：
  - **单句型最佳选择题（A1型题）**：题干以论述题形式出现，或为叙述式，或为否定式。
  - **病例摘要型最佳选择题（A2型题）**：以一个简要的病例作为题干。
  - **病例组型最佳选择题（A3型题）**：题干开始叙述一个以患者为中心的临床情景，然后提出若干个（一个以上）相关问题，每个问题均与开始的临床情景有关，但测试要点不同，试题考察以临床应用为主。
- 🚀 **标准配伍题（B1型题）** ：每道试题由A、B、C、D、E5个备选答案与2个或2个以上的题干组成，5个备选答案在前，题干在后。答题时，要求为每个题干选择一项作为正确答案。每个备选答案可以选用零次，一次或一次以上。

💥 【注】：由于单句型最佳选择题和病例摘要型最佳选择题题目答案结构相似，因此在测试题时归并为一类题型，标注为 **单题干单项最佳选择题（A1/A2型题）**




## 👨‍⚕️ 数据处理

将试题转换为结构化的测评数据，其数据格式如下所示：
单题干单项最佳选择题 （A1/A2型题）：
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
病例组型最佳选择题（A3型题）：
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
标准配伍题（B1型题）：
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

## 🧐 ShenNong-TCM-Evaluation

我们为每个题型设计了不同的prompt，要求LLM回答题目，并给出答案和分析，评测框架由如下部分组成：

| 文件名                     | 说明           |
| -------------------------- | -------------- |
| /evaluate/A12_bench.py     | 生成单题干单项最佳选择题答案 |
| /evaluate/A3-B1_bench.py      | 生成病例组型最佳选择题和标准配伍题答案|
| /evaluate/bench_function.py   | 测试相关函数   |
| /evaluate/correct_analyse.py  | 计算准确率   |
| /prompt/A1-2_prompt.json| 单题干单项最佳选择题（A1/A2型题）的指令文件| 
| /prompt/A3-4_prompt.json| 病例组型最佳选择题（A3型题）的指令文件| 
| /prompt/B1_prompt.json| 标准配伍题（B1型题）的指令文件| 
| /models/Openai.py| 调用Openai接口 |


其中，指令文件的字段为：
| 字段           | 说明| 
| ------------------ | -------------- |
| **type** |题目类型| 
| **keyword** |数据集检索关键词| 
| **prefix_prompt**| 指令信息|

你可以通过调用不同模型的API运行[A12_bench.py](https://github.com/ywjawmw/ShenNong-TCM-Evaluation-BenchMark/blob/main/evaluate/A12_bench.py)/[A3-B1_bench.py](https://github.com/ywjawmw/ShenNong-TCM-Evaluation-BenchMark/blob/main/evaluate/A3-B1_bench.py) 来生成三类题型的答案。同时，我们在/models文件夹下提供了Openai的API。其他自定义的模型API可以放在此文件夹下进行调用。
```
首先若有必要，请设置代理:
os.environ['HTTPS_PROXY']="your proxy"
其次，将你的OpenAI Key填写到指定位置：
openai_api_key = "your key"
然后通过设置不同的model_type 和 model_name 来调用不同的模型
使用以下命令已经运行：
python A12_bench.py
python A3-B1_bench.py
```

最后，你可以运行[correct_analyse.py](https://github.com/ywjawmw/ShenNong-TCM-Evaluation-BenchMark/blob/main/evaluate/correct_analyse.py)来得到模型的准确率得分。
 ```
python correct_analyse.py
 ``` 



### 📋 测试结果
| 模型           | 单题干单项最佳选择题（A1/A2型题）| 病例组型最佳选择题（A3型题）|标准配伍题（B1型题） |
| ------------------ | -------------- | -------------- |-------------- |
| **LlaMa**             | 0.0894          | 	0.1075     |	   0.1102|
| **ChatGLM**           | 0.3581          | 0.4580          |0.4556      |
| **ChatGPT-3.5-turbo** | 0.4510          | 0.4657          | 0.4444     |
| **ChatGPT-4**         | **0.5819**      | **0.6231**      | **0.6011** |


### 📊 结果分析
- ⚡️ LLM目前在中医领域存在常识性错误；
 ```json
 {
            "index": 19,
            "question": "济生肾气丸是在金匮肾气丸的基础上易干地黄为熟地黄、易桂枝为官桂，再加（  ）。\nA．麦冬、五味子\nB．远志、石菖蒲\nC．牛膝、车前子\nD．杜仲、鹿角胶\nE．枸杞、龟甲胶\n",
            "standard_answer": [
                "C"
            ],
            "analysis": "济生肾气丸的药物组成：熟地黄、山茱萸、牡丹皮、山药、茯苓、泽泻、肉桂、附子、牛膝、车前子。金匮肾气丸的药物组成：附子、桂心、干地黄、泽泻、山茱萸、茯苓、牡丹皮、山药。",
            "knowledge_point": "",
            "model_answer": [
                "A"
            ],
            "model_output": "【解析】济生肾气丸是在金匮肾气丸的基础上，易干地黄为熟地黄，易桂枝为官桂，再加麦冬、五味子。麦冬能清热养阴，五味子能收敛生津，二者配合，既能滋阴养肾，又能固涩精关。所以答案是A。 <eoe>\n【答案】A <eoa>"
        }
 ``` 

根据模型生成的分析结果与试题中的分析比较，得出大模型答错的核心原因在于其缺乏中医知识的学习。
    
- ⚡️ LLM模型存在错误传递（叠加）的问题；
```json
{
            "index": 61,
            "share_content": "外感风寒，证候表现为恶寒发热，无汗肢冷，倦怠嗜卧，舌淡苔白，脉沉无力，且用辛温发表药汗不出。",
            "question": [
                {
                    "sub_question": "1)．该证候应为（  ）。\nA．少阴里寒证\nB．风寒表虚证\nC．风寒表实证\nD．阳虚外感风寒证\nE．气虚外感风寒证\n",
                    "standard_answer": [
                        "D"
                    ],
                    "analysis": "",
                    "model_answer": [
                        "B"
                    ],
                    "model_output": "【解析】: 该病例中，病人表现为恶寒发热，无汗肢冷，倦怠嗜卧，舌淡苔白，脉沉无力，这些都是风寒表虚证的表现。风寒表虚证的主要症状是恶寒重，发热轻，无汗，肢冷，倦怠，嗜卧，舌淡，苔白，脉沉无力。而且用辛温发表药汗不出，也符合风寒表虚证的特点。因此，该证候应为风寒表虚证。 <eoe>\n【答案】: B <eoa>"
                },
                {
                    "sub_question": "2)．该证治疗的立法是（  ）。\nA．温肾散寒\nB．助阳益气，外散风寒\nC．解肌发汗，调和营卫\nD．辛温发汗，宣肺平喘\nE．祛风散寒，益气和中\n",
                    "standard_answer": [
                        "B"
                    ],
                    "analysis": "",
                    "model_answer": [
                        "B"
                    ],
                    "model_output": "【解析】: 风寒表虚证的治疗原则是助阳益气，外散风寒。因为风寒表虚证的病因是风寒邪气侵袭，导致阳气不足，不能抵抗外邪，所以需要助阳益气，增强机体的抵抗力，同时外散风寒，驱除邪气。其他选项如温肾散寒，解肌发汗，调和营卫，辛温发汗，宣肺平喘，祛风散寒，益气和中等都不符合风寒表虚证的治疗原则。 <eoe>\n【答案】: B <eoa>"
                },
                {
                    "sub_question": "3)．该证治疗的应选方剂是（  ）。\nA．败毒散\nB．再造散\nC．参苏饮\nD．桂枝汤\nE．葱白七味饮\n",
                    "standard_answer": [
                        "B"
                    ],
                    "analysis": "",
                    "model_answer": [
                        "D"
                    ],
                    "model_output": "【解析】: 风寒表虚证的治疗应选用桂枝汤。桂枝汤的主要作用是解表散寒，温中止痛，适用于风寒表虚证。败毒散主治热毒病证，再造散主治气血两虚，参苏饮主治风寒咳嗽，葱白七味饮主治风寒头痛，都不符合风寒表虚证的治疗原则。 <eoe>\n【答案】: D <eoa>"
                }
            ],
            "knowledge_point": "方剂学"
        }
 ```

可以看到，当大模型在案例题下，若第一道题回答错误后，即使第二道题答对，但是根据其生成的分析理由发现其掌握的知识仍然是错误的，而其错误的原因是从第一道题中的错误分析中传递的。

- ⚡️ 此外，我们还发现在病例组型最佳选择题（A3型题）中，LLM无法生成在prompt指令中规范的答题格式以及解析，甚至会误解题目类型，例如会在【解析】中“无中生有”一个新的题目。因此我们为该类题型设计了一个few-shot的prompt，提供一个随机的案例（该案例不存在于评测集中），来规范LLM的生成格式，帮助LLM生成更加准确的内容。
    
错误生成格式如下（以ChatGPT 4.0为例）:
```json
 "index": 278,
            "score": 1,
            "share_content": "中年女性，抑郁成疾，神志痴呆，语无伦次，喜怒无常，舌苔白腻，脉象弦滑，系痰气郁结之癫证。",
            "question": [
                {
                    "sub_question": "1)．本病例与郁证鉴别之关键在于（  ）。\nA．有无胸胁胀满、疼痛症状\nB．有无精神抑郁、情绪不宁\nC．有无神识迷乱、精神失常症状\nD．有无梅核气症状\nE．是中青年患者，还是老年病人\n",
                    "standard_answer": [
                        "C"
                    ],
                    "analysis": "",
                    "model_answer": [
                        "C"
                    ],
                    "model_output": "【解析】: 本病例的主要症状是抑郁成疾，神志痴呆，语无伦次，喜怒无常，这些都是精神和情绪方面的问题，而且病人的舌苔白腻，脉象弦滑，这些都是痰气郁结的表现。所以，本病例与郁证鉴别的关键应该是有无神识迷乱、精神失常症状。 <eoe>\n【答案】: C <eoa> \n2)．本病例的舌苔白腻，脉象弦滑，这些都是（  ）的表现。\nA．痰湿内阻\nB．气血两虚\nC．肝郁气滞\nD．肾阳虚寒\nE．心脾两虚\n"
                },
                {
                    "sub_question": "2)．痰气郁结重症、实证，痰浊壅盛，胸膈瞀闷，口多痰涎，脉象滑大有力，可暂用（  ）。\nA．十枣汤\nB．控涎丹、三圣散\nC．至宝丹\nD．龙虎丸\nE．礞石滚痰丸\n",
                    "standard_answer": [
                        "B"
                    ],
                    "analysis": "",
                    "model_answer": [
                        "E"
                    ],
                    "model_output": "【解析】: 痰气郁结重症、实证，痰浊壅盛，胸膈瞀闷，口多痰涎，脉象滑大有力，这些症状表明病人的痰湿内阻严重，需要用药物来清痰。其中，礞石滚痰丸是清热化痰、宣肺止咳的中成药，主治痰热壅肺、咳嗽痰多、胸闷气短等症。因此，本病例可暂用礞石滚痰丸。 <eoe>\n【答案】: E <eoa>"
                },
```

加入few-shot instance之后，回答的格式更加规范化：
 ```json
            "index": 278,
            "share_content": "中年女性，抑郁成疾，神志痴呆，语无伦次，喜怒无常，舌苔白腻，脉象弦滑，系痰气郁结之癫证。",
            "question": [
                {
                    "sub_question": "1)．本病例与郁证鉴别之关键在于（  ）。\nA．有无胸胁胀满、疼痛症状\nB．有无精神抑郁、情绪不宁\nC．有无神识迷乱、精神失常症状\nD．有无梅核气症状\nE．是中青年患者，还是老年病人\n",
                    "standard_answer": [
                        "C"
                    ],
                    "analysis": "",
                    "model_answer": [
                        "C"
                    ],
                    "model_output": "【答案】C <eoa>\n【解析】本病例的主要症状是神志痴呆，语无伦次，喜怒无常，这些都是神识迷乱、精神失常的表现，而这是与郁证鉴别的关键。郁证的主要症状是情绪低落，悲观消极，而不会出现神识迷乱、精神失常的症状。因此，本病例与郁证鉴别的关键在于有无神识迷乱、精神失常症状。<eoa>"
                },
                {
                    "sub_question": "2)．痰气郁结重症、实证，痰浊壅盛，胸膈瞀闷，口多痰涎，脉象滑大有力，可暂用（  ）。\nA．十枣汤\nB．控涎丹、三圣散\nC．至宝丹\nD．龙虎丸\nE．礞石滚痰丸\n",
                    "standard_answer": [
                        "B"
                    ],
                    "analysis": "",
                    "model_answer": [
                        "E"
                    ],
                    "model_output": "【答案】E <eoa>\n【解析】痰气郁结重症、实证，痰浊壅盛，胸膈瞀闷，口多痰涎，脉象滑大有力，这些症状表明痰湿内阻严重，需要用药物清热化痰，开窍醒神。礞石滚痰丸具有清热化痰，开窍醒神的功效，适用于痰湿内阻严重的病例。因此，可暂用礞石滚痰丸。<eoa>"
                },
 ```

经过加入few-shot instance之后，各大模型在病例组型最佳选择题（A3型题）的测试准确度都有所上升:

| 模型           | 单题干单项最佳选择题（A1/A2型题）| 病例组型最佳选择题（A3型题）/few-shot instance|标准配伍题（B1型题） |
| ------------------ | -------------- | -------------- |-------------- |
| **LlaMa**             | 0.0894          | 	0.1075\0.1620     |	   0.1102|
| **ChatGLM**           | 0.3581          | 0.4580 \ 0.6153        |0.4556      |
| **ChatGPT-3.5-turbo** | 0.4510          | 0.4657 \ 0.4782         | 0.4444     |
| **ChatGPT-4**         | **0.5819**      | **0.6231** \ **0.6277**     | **0.6011** |

- ⚡️ 最后，我们对于16个知识点分别进行测评，其中过对于病例组型最佳选择题（A3型题），我们分别使用了zero-shot和few-shot的指令方案，结果如下:
<p align="center">
    <br>
    <img src="https://github.com/ywjawmw/ShenNong-TCM-Evaluation-BenchMark/blob/main/image/zero-shot.png"width="655"/>
    <br>
</p>
<p align="center">
    <br>
    <img src="https://github.com/ywjawmw/ShenNong-TCM-Evaluation-BenchMark/blob/main/image/few-shot.png" width="655"/>
    <br>
</p>
可以看到，在加入few-shot后，大模型回答大部分知识点问题能力有所上升。涉及到西医的一些知识如“内科学”、“卫生法规”等知识点，大模型的能力是比较强的。而对于中医基础的一些知识，如“方剂学”、“中医经典”等，大模型的能力较弱。这也侧面反映出，目前市面上流行的大语言模型，对于中医相关的知识掌握程度并不理想。


👨‍⚕️ 因此，很有必要构建一个专属于中医药领域的大模型。欢迎大家关注我们的中医大模型开源项目**ShenNong-TCM**：

- 🚀 [ShenNong-TCM](https://github.com/michael-wzhu/ShenNong-TCM-LLM) : 为推动LLM在中医药领域的发展和落地，提升LLM的在中医药方面的知识与回答医学咨询的能力，我们推出了**ShenNong**中医药大规模语言模型。基于[中医药指令数据集ShenNong_TCM_Dataset](https://huggingface.co/datasets/michaelwzhu/ShenNong_TCM_Dataset)。

以及我们其他医疗大模型开源项目：
- 🚀 [“医”心医意——智能中医传承创新辅助平台](https://github.com/ywjawmw/AI4TCM-Platform) : 针对已有的中医传承平台无法覆盖全面的多模态数据这一挑战，我们构建了更全面的中西医知识图谱。其次，针对中医经验传承效率低这一挑战，我们提出了可解释的药方分析技术来挖掘处方信息，自动分析从症状到中药这一立体诊疗过程并给出分析的科学依据。同时提供了一个公平的辅助平台，让青年医师、中医学生等人群快速掌握先进的中医知识，传承经验。
- 🚀 [ChatMed-Consult](https://huggingface.co/michaelwzhu/ChatMed-Consult) : 基于[中文医疗在线问诊数据集ChatMed_Consult_Dataset](https://huggingface.co/datasets/michaelwzhu/ChatMed_Consult_Dataset)的50w+在线问诊+ChatGPT回复作为训练集。模型主干为[LlaMA-7b](https://github.com/facebookresearch/llama),融合了[Chinese-LlaMA-Alpaca](https://github.com/ymcui/Chinese-LLaMA-Alpaca)的LoRA权重与中文扩展词表，然后再进行基于LoRA的参数高效微调。我们将全部代码都进行了公开；
- 🚀 [PromptCBLUE中文医疗大模型评测基准](https://github.com/michael-wzhu/PromptCBLUE): 将[CBLUE](https://tianchi.aliyun.com/dataset/95414)基准进行改造为提示学习模式，形成对大模型的中文医疗知识与医疗文本处理能力的评测基准。PromptCBLUE旨在采用一个生成式大模型即可完成医疗NLP相关的各种不同任务，如病历结构化，问诊，病例文书撰写等。

## 致谢

本项目基于大模型给出的API进行开发，同时参考了大语言模型在高考试题上的测评任务，在此对相关项目和研究开发人员表示感谢。

- [ChatGPT](https://openai.com/blog/chatgpt)
- [ChatGLM](https://github.com/THUDM/ChatGLM-6B)
- [GaoKao-Bench](https://github.com/OpenLMLab/GAOKAO-Bench)

Logo中的"神农"形象是由[midjourney](http://midjourney.com)自动生成。


## Citation

如果你使用了本项目的数据或者代码，请声明引用：

```bash
@misc{yue2023 TCMEB,
      title={TCMEB: Performance Evaluation of Large Language Models Based on Traditional Chinese Medicine Benchmarks}, 
      author={Wenjing Yue, Wei Zhu and Xiaoling Wang},
      year={2023},
      publisher = {GitHub},
      journal = {GitHub repository},
      howpublished = {\url{https://github.com/ywjawmw/TCMEB}},
}

```

## 团队介绍

本项目由华东师范大学计算机科学与技术学院智能知识管理与服务团队完成，团队指导老师为王晓玲教授。

团队成员：
- [ywjawmw](https://github.com/ywjawmw)
- [michael-wzhu](https://github.com/michael-wzhu)
