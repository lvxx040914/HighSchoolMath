# HighSchoolMath｜高中数学系统讲义与题库

> **V1.3：单调性专题 · 40 条独立题目记录 · 四种 PDF 产品 · 可复现组卷**。
> 课程知识目录仍是规划架构，不代表全高中已完稿；全部题目仍为 `draft`，待独立数学人工审核。

本项目遵守 **知识点—解题方法—典型题型—独立题库—出版组合** 的可维护模式。同一道题可被讲义、习题册和按条件组卷重用，且使用不可变 ID 与来源字段。

## 快速开始

需求：Python ≥ 3.10、PyYAML、XeLaTeX、latexmk。PDF 内容检查需要 `pdftotext`（Mac 可用 `brew install poppler`）。中文排版优先使用 Noto，Mac 使用 Songti / PingFang，缺失时可使用 Fandol 回退。

```bash
python3 -m pip install -r requirements.txt
make check
make build
make pdfcheck
```

默认生成四种 PDF（`dist/`）：

| 产品 | 文件名 | 内容 |
|---|---|---|
| 讲义版 | `monotonicity_lecture.pdf` | 理论、目录、10 道带完整解答的示范例题、30 道训练题；不含训练题解答 |
| 专项习题册 | `monotonicity_workbook.pdf` | 独立题干，提供解题书写空间 |
| 教师解析版 | `monotonicity_teacher.pdf` | 讲义正文、10 道示范例题和 30 道训练题的详细解答 |
| 答案速查册 | `monotonicity_answer_key.pdf` | 与习题册题号一致，提供简明结论 |

兼容旧脚本时仍保留 `monotonicity_student.pdf`（讲义版副本）以及 `make student`。

## 按条件自动组卷

示例：从单调性知识点中抽取 6 道、难度 2–4、题型为解答题的练习，固定随机种子保证下次运行相同题单。

```bash
python3 tools/compose.py --topic K-FUN-MONO --min-difficulty 2 --max-difficulty 4 --type solution --count 6 --seed 2026 --slug monotonicity_practice --out config/monotonicity_practice.yml
python3 tools/build.py --config config/monotonicity_practice.yml --edition workbook
python3 tools/build.py --config config/monotonicity_practice.yml --edition answer_key
```

输出 `dist/monotonicity_practice_workbook.pdf` 与 `dist/monotonicity_practice_answer_key.pdf`。可加 `--method M-DERIV-SIGN`、`--archetype A-FUN-04`、`--level intermediate`，或 `--include-worked` 将示范题放入可选池。若匹配数量不足，程序明确报错，不自动放宽条件。详细命令见 [出版与组卷说明](docs/PUBLICATION_GUIDE.md)。

**当前边界：** 自动组卷只针对已录入的单调性专题题池。自定义 YAML 仅能构建独立习题册和答案速查册；讲义与教师版目前包含专门编写的单调性正文，不会把不同知识领域误配到正文里。运行自定义构建后会恢复默认生成索引，不污染已提交的题单文件。

## 内容与技术规范

- [项目规范](docs/PROJECT_SPEC.md) · [数学编写规范](docs/EDITORIAL_STANDARD_V1_1.md)
- [知识目录](docs/KNOWLEDGE_ATLAS.md) · [解题方法与题型目录](docs/METHOD_AND_ARCHETYPE_ATLAS.md)
- [题目字段规范](docs/QUESTION_SCHEMA.md) · [组卷与四版本出版说明](docs/PUBLICATION_GUIDE.md)
- [V1.3 更新记录](docs/V1_3_RELEASE_NOTES.md) · [后续路线](docs/ROADMAP.md)

## 内容质量边界

V1.3 将以前嵌在 `monotonicity.tex` 内的六道示范例题迁入 `questions/HSM-FUN-0035` 至 `HSM-FUN-0040`。这是**结构迁移，不是新增六道原创数学题**。题库累计 40 条，10 道示范、30 道训练，尚未完成独立人工复核。自动编译、元数据测试和 PDF 隔离测试不是数学正确性证书。公开转载外部真题前须核查许可。
