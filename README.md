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
  
<table class="MsoTableGrid" border="1" cellspacing="0" style="border-collapse:collapse;border:none;mso-border-left-alt:0.5000pt solid windowtext;
mso-border-top-alt:0.5000pt solid windowtext;mso-border-right-alt:0.5000pt solid windowtext;mso-border-bottom-alt:0.5000pt solid windowtext;
mso-border-insideh:0.5000pt solid windowtext;mso-border-insidev:0.5000pt solid windowtext;mso-padding-alt:0.0000pt 5.4000pt 0.0000pt 5.4000pt ;"><tbody><tr><td width="142" valign="center" style="width:106.5000pt;padding:0.0000pt 5.4000pt 0.0000pt 5.4000pt ;border-left:1.0000pt solid rgb(219,238,219);
mso-border-left-alt:0.5000pt solid rgb(219,238,219);border-right:1.0000pt dotted windowtext;mso-border-right-alt:0.5000pt dotted windowtext;
border-top:1.0000pt solid rgb(118,190,118);mso-border-top-alt:0.5000pt solid rgb(118,190,118);border-bottom:1.0000pt solid rgb(118,190,118);
mso-border-bottom-alt:0.5000pt solid rgb(118,190,118);background:rgb(219,238,219);"><p class="MsoNormal" align="center" style="text-align:center;"><span style="font-family:宋体;mso-ascii-font-family:Calibri;mso-hansi-font-family:Calibri;
mso-bidi-font-family:'Times New Roman';color:rgb(0,0,0);font-size:14.0000pt;
mso-font-kerning:1.0000pt;"><font face="宋体">题型</font></span><span style="font-family:宋体;mso-ascii-font-family:Calibri;mso-hansi-font-family:Calibri;
mso-bidi-font-family:'Times New Roman';color:rgb(0,0,0);font-size:14.0000pt;
mso-font-kerning:1.0000pt;"><o:p></o:p></span></p></td><td width="142" valign="center" style="width:106.5000pt;padding:0.0000pt 5.4000pt 0.0000pt 5.4000pt ;border-left:none;
mso-border-left-alt:none;border-right:1.0000pt dotted windowtext;mso-border-right-alt:0.5000pt dotted windowtext;
border-top:1.0000pt solid rgb(118,190,118);mso-border-top-alt:0.5000pt solid rgb(118,190,118);border-bottom:1.0000pt solid rgb(118,190,118);
mso-border-bottom-alt:0.5000pt solid rgb(118,190,118);background:rgb(219,238,219);"><p class="MsoNormal" align="center" style="text-align:center;"><span style="font-family:宋体;mso-ascii-font-family:Calibri;mso-hansi-font-family:Calibri;
mso-bidi-font-family:'Times New Roman';color:rgb(0,0,0);font-size:14.0000pt;
mso-font-kerning:1.0000pt;"><font face="Calibri">A1/A2</font></span><span style="font-family:Calibri;mso-fareast-font-family:宋体;mso-bidi-font-family:'Times New Roman';
color:rgb(0,0,0);font-size:14.0000pt;mso-font-kerning:1.0000pt;"><o:p></o:p></span></p></td><td width="142" valign="center" style="width:106.5500pt;padding:0.0000pt 5.4000pt 0.0000pt 5.4000pt ;border-left:none;
mso-border-left-alt:none;border-right:1.0000pt dotted windowtext;mso-border-right-alt:0.5000pt dotted windowtext;
border-top:1.0000pt solid rgb(118,190,118);mso-border-top-alt:0.5000pt solid rgb(118,190,118);border-bottom:1.0000pt solid rgb(118,190,118);
mso-border-bottom-alt:0.5000pt solid rgb(118,190,118);background:rgb(219,238,219);"><p class="MsoNormal" align="center" style="text-align:center;"><span style="font-family:宋体;mso-ascii-font-family:Calibri;mso-hansi-font-family:Calibri;
mso-bidi-font-family:'Times New Roman';color:rgb(0,0,0);font-size:14.0000pt;
mso-font-kerning:1.0000pt;"><font face="Calibri">A3/A4</font></span><span style="font-family:Calibri;mso-fareast-font-family:宋体;mso-bidi-font-family:'Times New Roman';
color:rgb(0,0,0);font-size:14.0000pt;mso-font-kerning:1.0000pt;"><o:p></o:p></span></p></td><td width="142" valign="center" style="width:106.5500pt;padding:0.0000pt 5.4000pt 0.0000pt 5.4000pt ;border-left:none;
mso-border-left-alt:none;border-right:1.0000pt solid rgb(219,238,219);mso-border-right-alt:0.5000pt solid rgb(219,238,219);
border-top:1.0000pt solid rgb(118,190,118);mso-border-top-alt:0.5000pt solid rgb(118,190,118);border-bottom:1.0000pt solid rgb(118,190,118);
mso-border-bottom-alt:0.5000pt solid rgb(118,190,118);background:rgb(219,238,219);"><p class="MsoNormal" align="center" style="text-align:center;"><span style="font-family:宋体;mso-ascii-font-family:Calibri;mso-hansi-font-family:Calibri;
mso-bidi-font-family:'Times New Roman';color:rgb(0,0,0);font-size:14.0000pt;
mso-font-kerning:1.0000pt;"><font face="Calibri">B1</font></span><span style="font-family:Calibri;mso-fareast-font-family:宋体;mso-bidi-font-family:'Times New Roman';
color:rgb(0,0,0);font-size:14.0000pt;mso-font-kerning:1.0000pt;"><o:p></o:p></span></p></td></tr><tr><td width="142" valign="center" style="width:106.5000pt;padding:0.0000pt 5.4000pt 0.0000pt 5.4000pt ;border-left:1.0000pt solid rgb(219,238,219);
mso-border-left-alt:0.5000pt solid rgb(219,238,219);border-right:1.0000pt dotted windowtext;mso-border-right-alt:0.5000pt dotted windowtext;
border-top:none;mso-border-top-alt:0.5000pt solid rgb(118,190,118);border-bottom:1.0000pt dotted windowtext;
mso-border-bottom-alt:0.5000pt dotted windowtext;background:rgb(255,255,255);"><p class="MsoNormal" align="center" style="text-align:center;"><span style="font-family:宋体;mso-ascii-font-family:Calibri;mso-hansi-font-family:Calibri;
mso-bidi-font-family:'Times New Roman';color:rgb(0,0,0);font-size:14.0000pt;
mso-font-kerning:1.0000pt;"><font face="宋体">问题（道）</font></span><span style="font-family:Calibri;mso-fareast-font-family:宋体;mso-bidi-font-family:'Times New Roman';
color:rgb(0,0,0);font-size:14.0000pt;mso-font-kerning:1.0000pt;"><o:p></o:p></span></p></td><td width="142" valign="center" style="width:106.5000pt;padding:0.0000pt 5.4000pt 0.0000pt 5.4000pt ;border-left:none;
mso-border-left-alt:none;border-right:1.0000pt dotted windowtext;mso-border-right-alt:0.5000pt dotted windowtext;
border-top:none;mso-border-top-alt:0.5000pt solid rgb(118,190,118);border-bottom:1.0000pt dotted windowtext;
mso-border-bottom-alt:0.5000pt dotted windowtext;background:rgb(255,255,255);"><p class="MsoNormal" align="center" style="text-align:center;"><span style="font-family:宋体;mso-ascii-font-family:Calibri;mso-hansi-font-family:Calibri;
mso-bidi-font-family:'Times New Roman';color:rgb(0,0,0);font-size:14.0000pt;
mso-font-kerning:1.0000pt;"><font face="Calibri">1600</font></span><span style="font-family:Calibri;mso-fareast-font-family:宋体;mso-bidi-font-family:'Times New Roman';
color:rgb(0,0,0);font-size:14.0000pt;mso-font-kerning:1.0000pt;"><o:p></o:p></span></p></td><td width="142" valign="center" style="width:106.5500pt;padding:0.0000pt 5.4000pt 0.0000pt 5.4000pt ;border-left:none;
mso-border-left-alt:none;border-right:1.0000pt dotted windowtext;mso-border-right-alt:0.5000pt dotted windowtext;
border-top:none;mso-border-top-alt:0.5000pt solid rgb(118,190,118);border-bottom:1.0000pt dotted windowtext;
mso-border-bottom-alt:0.5000pt dotted windowtext;background:rgb(255,255,255);"><p class="MsoNormal" align="center" style="text-align:center;"><span style="font-family:宋体;mso-ascii-font-family:Calibri;mso-hansi-font-family:Calibri;
mso-bidi-font-family:'Times New Roman';color:rgb(0,0,0);font-size:14.0000pt;
mso-font-kerning:1.0000pt;"><font face="Calibri">198</font></span><span style="font-family:Calibri;mso-fareast-font-family:宋体;mso-bidi-font-family:'Times New Roman';
color:rgb(0,0,0);font-size:14.0000pt;mso-font-kerning:1.0000pt;"><o:p></o:p></span></p></td><td width="142" valign="center" style="width:106.5500pt;padding:0.0000pt 5.4000pt 0.0000pt 5.4000pt ;border-left:none;
mso-border-left-alt:none;border-right:1.0000pt solid rgb(219,238,219);mso-border-right-alt:0.5000pt solid rgb(219,238,219);
border-top:none;mso-border-top-alt:0.5000pt solid rgb(118,190,118);border-bottom:1.0000pt dotted windowtext;
mso-border-bottom-alt:0.5000pt dotted windowtext;background:rgb(255,255,255);"><p class="MsoNormal" align="center" style="text-align:center;"><span style="font-family:宋体;mso-ascii-font-family:Calibri;mso-hansi-font-family:Calibri;
mso-bidi-font-family:'Times New Roman';color:rgb(0,0,0);font-size:14.0000pt;
mso-font-kerning:1.0000pt;"><font face="Calibri">1481</font></span><span style="font-family:Calibri;mso-fareast-font-family:宋体;mso-bidi-font-family:'Times New Roman';
color:rgb(0,0,0);font-size:14.0000pt;mso-font-kerning:1.0000pt;"><o:p></o:p></span></p></td></tr><tr><td width="142" valign="center" style="width:106.5000pt;padding:0.0000pt 5.4000pt 0.0000pt 5.4000pt ;border-left:1.0000pt solid rgb(219,238,219);
mso-border-left-alt:0.5000pt solid rgb(219,238,219);border-right:1.0000pt dotted windowtext;mso-border-right-alt:0.5000pt dotted windowtext;
border-top:none;mso-border-top-alt:0.5000pt dotted windowtext;border-bottom:1.0000pt solid rgb(118,190,118);
mso-border-bottom-alt:0.5000pt solid rgb(118,190,118);background:rgb(242,249,242);"><p class="MsoNormal" align="center" style="text-align:center;"><span style="font-family:宋体;mso-ascii-font-family:Calibri;mso-hansi-font-family:Calibri;
mso-bidi-font-family:'Times New Roman';color:rgb(0,0,0);font-size:14.0000pt;
mso-font-kerning:1.0000pt;"><font face="宋体">子问题</font></span><span style="font-family:Calibri;mso-fareast-font-family:宋体;mso-bidi-font-family:'Times New Roman';
color:rgb(0,0,0);font-size:14.0000pt;mso-font-kerning:1.0000pt;"><o:p></o:p></span></p></td><td width="142" valign="center" style="width:106.5000pt;padding:0.0000pt 5.4000pt 0.0000pt 5.4000pt ;border-left:none;
mso-border-left-alt:none;border-right:1.0000pt dotted windowtext;mso-border-right-alt:0.5000pt dotted windowtext;
border-top:none;mso-border-top-alt:0.5000pt dotted windowtext;border-bottom:1.0000pt solid rgb(118,190,118);
mso-border-bottom-alt:0.5000pt solid rgb(118,190,118);background:rgb(242,249,242);"><p class="MsoNormal" align="center" style="text-align:center;"><span style="font-family:宋体;mso-ascii-font-family:Calibri;mso-hansi-font-family:Calibri;
mso-bidi-font-family:'Times New Roman';color:rgb(0,0,0);font-size:14.0000pt;
mso-font-kerning:1.0000pt;"><font face="Calibri">\</font></span><span style="font-family:Calibri;mso-fareast-font-family:宋体;mso-bidi-font-family:'Times New Roman';
color:rgb(0,0,0);font-size:14.0000pt;mso-font-kerning:1.0000pt;"><o:p></o:p></span></p></td><td width="142" valign="center" style="width:106.5500pt;padding:0.0000pt 5.4000pt 0.0000pt 5.4000pt ;border-left:none;
mso-border-left-alt:none;border-right:1.0000pt dotted windowtext;mso-border-right-alt:0.5000pt dotted windowtext;
border-top:none;mso-border-top-alt:0.5000pt dotted windowtext;border-bottom:1.0000pt solid rgb(118,190,118);
mso-border-bottom-alt:0.5000pt solid rgb(118,190,118);background:rgb(242,249,242);"><p class="MsoNormal" align="center" style="text-align:center;"><span style="font-family:宋体;mso-ascii-font-family:Calibri;mso-hansi-font-family:Calibri;
mso-bidi-font-family:'Times New Roman';color:rgb(0,0,0);font-size:14.0000pt;
mso-font-kerning:1.0000pt;"><font face="Calibri">642</font></span><span style="font-family:宋体;mso-ascii-font-family:Calibri;mso-hansi-font-family:Calibri;
mso-bidi-font-family:'Times New Roman';color:rgb(0,0,0);font-size:14.0000pt;
mso-font-kerning:1.0000pt;"><o:p></o:p></span></p></td><td width="142" valign="center" style="width:106.5500pt;padding:0.0000pt 5.4000pt 0.0000pt 5.4000pt ;border-left:none;
mso-border-left-alt:none;border-right:1.0000pt solid rgb(219,238,219);mso-border-right-alt:0.5000pt solid rgb(219,238,219);
border-top:none;mso-border-top-alt:0.5000pt dotted windowtext;border-bottom:1.0000pt solid rgb(118,190,118);
mso-border-bottom-alt:0.5000pt solid rgb(118,190,118);background:rgb(242,249,242);"><p class="MsoNormal" align="center" style="text-align:center;"><span style="font-family:宋体;mso-ascii-font-family:Calibri;mso-hansi-font-family:Calibri;
mso-bidi-font-family:'Times New Roman';color:rgb(0,0,0);font-size:14.0000pt;
mso-font-kerning:1.0000pt;"><font face="Calibri">3231</font></span><span style="font-family:Calibri;mso-fareast-font-family:宋体;mso-bidi-font-family:'Times New Roman';
color:rgb(0,0,0);font-size:14.0000pt;mso-font-kerning:1.0000pt;"><o:p></o:p></span></p></td></tr></tbody></table>
同时，欢迎大家关注我们的中医大模型开源项目**ShenNong-TCM**：
- 🚀 [ShenNong-TCM](https://github.com/michael-wzhu/ShenNong-TCM-LLM) : 为推动LLM在中医药领域的发展和落地，提升LLM的在中医药方面的知识与回答医学咨询的能力，我们推出了**ShenNong**中医药大规模语言模型。基于[中医药指令数据集ShenNong_TCM_Dataset](https://huggingface.co/datasets/michaelwzhu/ShenNong_TCM_Dataset)。

