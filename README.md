# ShenNong-TCM-Evaluation-BenchMark
Repo for ShenNong-TCM-Evaluation (“神农”大模型系列，首个中医评测框架和中医评测数据集)

[**中文**](./README.md) | [**English**](./README.md)

<p align="center">
    <br>
    <img src="https://github.com/michael-wzhu/ShenNong-TCM-LLM/blob/main/pics/ShenNong-TCM_banner.png" width="355"/>
    <br>
</p>
<p align="center">
    <img alt="GitHub" src="https://img.shields.io/github/license/ymcui/Chinese-LLaMA-Alpaca.svg?color=blue&style=flat-square">
    <img alt="GitHub top language" src="https://img.shields.io/github/languages/top/ymcui/Chinese-LLaMA-Alpaca">
</p>

为了进一步有效、准确的评估大模型在中医药领域的表现，我们现建立了一个标准化、综合性的中医评测框架**ShenNong-TCM-Evaluation**，该评测框架将充分考虑中医药领域的复杂性和专业性，涵盖多个方面，以确保大语言模型在真实场景下的实用性和适用性。


🚀 **数据集：ShenNong-TCM-EB** ：首先我们构建了首个中医评测数据集ShenNong-TCM-EB。该数据集中的试题基于某中医执业医师资格考试题库，涵盖了中医基础理论、中医诊断学、中药学、方剂学、中医经典、中医内科学、中医外科学、中医妇科学、中医儿科学、针灸学、诊断学基础、内科学、传染病学、医学伦理学、卫生法规、其他等16个知识点，共3类选择题类型，每类题型都包含16个知识点的至多100道题，后续我们会逐步开放更多的测试题并扩充该数据集。通过收集、整理和标注这些数据，我们旨在提供一个全面、准确、具有代表性的中医测试基准，来帮助评估和改大语言模型应用在中医领域性能。

| 题目类型           | A1/A2       | A3/A3       | B1       |
| ------------------ | -------------- | -------------- |-------------- |
| **题目数量**           | 1600           | 198         |1481         |
| **子问题**             | \           | 642          | 3231          |

A1/A2: 每一道考题下面有A、B、C、D、E五个备选答案；

A3/A4: 实际案例题； 每一道考题下提供一个案例，每个案例下设若干道试题，在每一道试题下面有A、B、C、D、E 五个备选答案；

B1:  每一道考题下有若干组考题，每组考题共用在考题前列出的A、B、C、D、E五个备选答案。


🚀 **数据处理** ：

将试题转换为结构化的测评数据，其数据格式如下所示：
A1/A2类试题：
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
A3/A4类试题：
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
B1类试题：
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

🚀 **ShenNong-TCM-Evaluation** ：我们为每个题型设计了不同的prompt，要求LLM回答题目，并给出答案和分析。

🚀 **测试结果** ：
| 大模型           | A1/A2       | A3/A3       | B1       |
| ------------------ | -------------- | -------------- |-------------- |
| **ChatGLM**           | 0.3581          | 0.4611          |0.4513      |
| **ChatGPT-3.5-turbo** | 0.4510          | 0.4689          | 0.4438     |
| **ChatGPT-4**         | **0.5819**      | **0.6231**      | **0.6044** |


🚀 **结果分析** ：
- LLM目前在中医领域存在常识性错误；
  
  ![image](https://github.com/ywjawmw/ShenNong-TCM-Evaluation-BenchMark/assets/38470046/dcdc223f-5c47-4b6a-827f-34ef8c196958)

    根据模型生成的分析结果与试题中的分析比较，得出大模型答错的核心原因在于其缺乏中医知识的学习。
- LLM模型存在错误传递（叠加）的问题；
  ![image](https://github.com/ywjawmw/ShenNong-TCM-Evaluation-BenchMark/assets/38470046/78e56d29-f9a5-4732-90cd-95831612458e)

    可以看到，当大模型在案例题下，若第一道题回答错误后，即使第二道题答对，但是根据其生成的分析理由发现其掌握的知识仍然是错误的，而其错误的原因是从第一道题中的错误分析中传递的。
  
🚀 因此，很有必要构建一个专属于中医药领域的大模型。欢迎大家关注我们的中医大模型开源项目**ShenNong-TCM**：

- 🚀 [ShenNong-TCM](https://github.com/michael-wzhu/ShenNong-TCM-LLM) : 为推动LLM在中医药领域的发展和落地，提升LLM的在中医药方面的知识与回答医学咨询的能力，我们推出了**ShenNong**中医药大规模语言模型。基于[中医药指令数据集ShenNong_TCM_Dataset](https://huggingface.co/datasets/michaelwzhu/ShenNong_TCM_Dataset)。

以及其他医疗大模型开源项目：
- 🚀 [ChatMed-Consult](https://huggingface.co/michaelwzhu/ChatMed-Consult) : 基于[中文医疗在线问诊数据集ChatMed_Consult_Dataset](https://huggingface.co/datasets/michaelwzhu/ChatMed_Consult_Dataset)的50w+在线问诊+ChatGPT回复作为训练集。模型主干为[LlaMA-7b](https://github.com/facebookresearch/llama),融合了[Chinese-LlaMA-Alpaca](https://github.com/ymcui/Chinese-LLaMA-Alpaca)的LoRA权重与中文扩展词表，然后再进行基于LoRA的参数高效微调。我们将全部代码都进行了公开；
- 🚀 [ChatMed-MT](https://huggingface.co/michaelwzhu/ChatMed-MT) : ChatMed-Consult的多轮对话版本，对已有的开源中文问诊数据集进行LLM自动改造，使得医生回复文本更加具有共情性，也更贴心与详细，由此训练的LLM在患者/用户体验上会更好。
- 🚀 [PromptCBLUE中文医疗大模型评测基准](https://github.com/michael-wzhu/PromptCBLUE): 将[CBLUE](https://tianchi.aliyun.com/dataset/95414)基准进行改造为提示学习模式，形成对大模型的中文医疗知识与医疗文本处理能力的评测基准。PromptCBLUE旨在采用一个生成式大模型即可完成医疗NLP相关的各种不同任务，如病历结构化，问诊，病例文书撰写等。

