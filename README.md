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


🚀 **ShenNong-TCM-EB** ：首先我们构建了首个中医评测数据集ShenNong-TCM-EB。该数据集来自某中医执业医师资格考试题库，涵盖丰富的问题类型，涵盖了中医基础理论、中医诊断学、中药学、方剂学、中医经典、中医内科学、中医外科学、中医妇科学、中医儿科学、针灸学、诊断学基础、内科学、传染病学、医学伦理学、卫生法规、其他等16个知识点，共3类选择题类型，每类题型都包含16个知识点的至多100道题，后续我们会逐步开放更多的测试题完善该数据集。通过收集、整理和标注这些数据，我们旨在提供一个全面、准确、具有代表性的测试基准，来帮助评估和改大语言模型应用在中医领域性能。

| 题目类型           | A1/A2       | A3/A3       | B1       |
| ------------------ | -------------- | -------------- |-------------- |
| **题目数量**           | 1600           | 198         |1481         |
| **子问题**             | \           | 642          | 3231          |


🚀 **ShenNong-TCM-Evaluation** ：我们为每个题型设计了不同的prompt，让LLM回答题目，并给出答案和分析。


同时，欢迎大家关注我们的中医大模型开源项目**ShenNong-TCM**：

- 🚀 [ShenNong-TCM](https://github.com/michael-wzhu/ShenNong-TCM-LLM) : 为推动LLM在中医药领域的发展和落地，提升LLM的在中医药方面的知识与回答医学咨询的能力，我们推出了**ShenNong**中医药大规模语言模型。基于[中医药指令数据集ShenNong_TCM_Dataset](https://huggingface.co/datasets/michaelwzhu/ShenNong_TCM_Dataset)。

以及其他医疗大模型开源项目：
- 🚀 [ChatMed-Consult](https://huggingface.co/michaelwzhu/ChatMed-Consult) : 基于[中文医疗在线问诊数据集ChatMed_Consult_Dataset](https://huggingface.co/datasets/michaelwzhu/ChatMed_Consult_Dataset)的50w+在线问诊+ChatGPT回复作为训练集。模型主干为[LlaMA-7b](https://github.com/facebookresearch/llama),融合了[Chinese-LlaMA-Alpaca](https://github.com/ymcui/Chinese-LLaMA-Alpaca)的LoRA权重与中文扩展词表，然后再进行基于LoRA的参数高效微调。我们将全部代码都进行了公开；
- 🚀 [ChatMed-MT](https://huggingface.co/michaelwzhu/ChatMed-MT) : ChatMed-Consult的多轮对话版本，对已有的开源中文问诊数据集进行LLM自动改造，使得医生回复文本更加具有共情性，也更贴心与详细，由此训练的LLM在患者/用户体验上会更好。
- 🚀 [PromptCBLUE中文医疗大模型评测基准](https://github.com/michael-wzhu/PromptCBLUE): 将[CBLUE](https://tianchi.aliyun.com/dataset/95414)基准进行改造为提示学习模式，形成对大模型的中文医疗知识与医疗文本处理能力的评测基准。PromptCBLUE旨在采用一个生成式大模型即可完成医疗NLP相关的各种不同任务，如病历结构化，问诊，病例文书撰写等。

