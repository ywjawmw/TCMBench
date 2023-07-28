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

- 🚀 **ShenNong-TCM-EB** ：首先我们构建了首个中医评测数据集ShenNong-TCM-EB。该数据集来自公开的某中医执业医师资格考试题库，涵盖丰富的问题类型，涵盖了中医基础理论、中医诊断学、中药学、方剂学、中医经典、中医内科学、中医外科学、中医妇科学、中医儿科学、针灸学、诊断学基础、内科学、传染病学、医学伦理学、卫生法规、其他等16个知识点，共3类选择题类型，每类题型都包含16个知识点的至多100道题，后续我们会逐步开放更多的测试题完善该数据集。通过收集、整理和标注这些数据，我们旨在提供一个全面、准确、具有代表性的测试基准，来帮助评估和改大语言模型应用在中医领域性能。
  
| 题目类型           | A1/A2       | A3/A3       | B1       |
| ------------------ | -------------- | -------------- |-------------- |
| 题目数量             | 1600           | 198         |1481         |
| 子问题             | \           | 642          | 3231          |

同时，欢迎大家关注我们的中医大模型开源项目**ShenNong-TCM**：

- 🚀 [ShenNong-TCM](https://github.com/michael-wzhu/ShenNong-TCM-LLM) : 为推动LLM在中医药领域的发展和落地，提升LLM的在中医药方面的知识与回答医学咨询的能力，我们推出了**ShenNong**中医药大规模语言模型。基于[中医药指令数据集ShenNong_TCM_Dataset](https://huggingface.co/datasets/michaelwzhu/ShenNong_TCM_Dataset)。

