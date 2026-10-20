# V1.3 发布说明：题库引用与多产品出版

**日期**：2026-10-20。**状态**：可编译试验版，全部题目尚未进行独立数学人工复核。

## 实际完成

1. 将原先手写在 `lectures/functions/monotonicity.tex` 的六道示范例题迁入 `HSM-FUN-0035` 至 `HSM-FUN-0040`。保留原文题干和解答，另存 `answer.tex`，现有永久 ID 不变。**总共 40 条题目记录，但仅是从 34 增至 40 个可引用实体，不代表新增 6 道题型。**
2. 10 道示范题 + 30 道训练题，全部采用统一的 `\showworked{ID}` / `\showquestion{ID}` 引用机制，支持展示别名和统一编号。
3. 增设答案速查源 `answer.tex`（40 条），生成讲义（lecture）、独立习题册（workbook）、教师解析（teacher）和答案速查（answer_key）四个 PDF，兼容旧版 `student` PDF 名称。
4. `tools/compose.py` 支持按知识、方法、题型原型、难度上下界、层级和题目类型筛选；使用随机种子保证可复现且拒绝不满足的数量。新增自定义题单仅出版习题册和速查册。
5. XeLaTeX 字体自动回退（Noto/Songti/PingFang/Fandol）、首条错误定位、GitHub CI/PDF 内容隔离测试继续保留。生成讲义目录，独立习题册按难度留白，答案速查册双栏排版。

## 本版不做

- 没有新增 20–40 道数学试题；原题数学审核状态继续 `draft`。
- 不做互联网真题抓取、联网 AI 批改、在线判题或跨专题自动撰写数学讲义。
- 单元测试和 PDF 检查不代表对数学证明正确性作出独立保证。

## 验收命令

```bash
python3 -m pip install -r requirements.txt
make check
make build
make pdfcheck
```

自定义组卷见 `docs/PUBLICATION_GUIDE.md`。文件名一律 ASCII 英文，TeX、MD、YAML 正文可保留 UTF-8 中文。

## 下一阶段建议

V1.4：独立数学复核与质量标注；补齐图题和多解法数据模型；试点第二知识专题，并把组卷索引扩展成跨专题。自动化优先服务审题与复用，不以题量替代质量。
