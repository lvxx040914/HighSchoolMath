# HighSchoolMath｜高中数学讲义与题库

> V1.2：单调性高质量专题（阶段性草稿）；继承 V1.1 知识、方法与题型目录。

本项目坚持「一份结构化数学内容，多种输出」：**知识点库—方法库—独立题库—讲义编译** 四层解耦，形成便于审核、长期维护的高中数学出版系统。

## 获取内容

- [完整项目规范](docs/PROJECT_SPEC.md)
- [V1.1 数学内容编写与审核标准](docs/EDITORIAL_STANDARD_V1_1.md)
- [高中数学知识地图（11 领域、93 主题）](docs/KNOWLEDGE_ATLAS.md)
- [解题方法与典型题型图谱（42 方法、50 题型）](docs/METHOD_AND_ARCHETYPE_ATLAS.md)
- [课程标准对齐说明](docs/CURRICULUM_ALIGNMENT.md)
- [内容模板与审稿清单](docs/REVIEW_AND_CONTENT_TEMPLATES.md)
- [协作与 AI 编辑约束](AGENTS.md)
- [V1.2 发布说明与验收状态](docs/V1_2_RELEASE_NOTES.md)
- [V1.1 更新说明](docs/V1_1_RELEASE_NOTES.md)
- [内容与数学写作规范](docs/EDITORIAL_GUIDE.md)
- [题目数据规范](docs/QUESTION_SCHEMA.md)
- [分期实施与验收](docs/ROADMAP.md)
- [样章源码](lectures/functions/monotonicity.tex)
- [练习题清单](config/monotonicity.yml)

## 运行（需 XeLaTeX / latexmk / Python ≥ 3.10）

```bash
python -m pip install -r requirements.txt
python tools/validate.py
python tools/validate_catalog.py
python tools/render_catalog.py --check
python -m unittest discover -s tests -v
python tools/build.py --edition all
```

预期生成：`dist/monotonicity_student.pdf`（学生版）、`dist/monotonicity_teacher.pdf`（教师版）。学生版含理论与完整示范例题、专题训练不含答案；教师版在末尾附独立答案详解。输出由同一批题目生成。

若没有 `latexmk`，可在项目根目录直接运行：

```bash
xelatex -interaction=nonstopmode -halt-on-error -output-directory=dist tex/student.tex
xelatex -interaction=nonstopmode -halt-on-error -output-directory=dist tex/student.tex
```

上述手工方式必须先运行一次 `python tools/build.py --generate-only` 以生成索引文件。

## V1.1 的新增内容

- 结构化编辑目录：`catalog/knowledge_map.yml`、`catalog/methods.yml`、`catalog/archetypes.yml`，覆盖 11 个领域、93 个待建设主题、42 种方法、50 类题型。所有条目均是 **规划**，不代表已有同数量的完整讲义、解答或复核。
- 自动导出的浏览目录：`docs/KNOWLEDGE_ATLAS.md`、`docs/METHOD_AND_ARCHETYPE_ATLAS.md`；修改 YAML 后运行 `python tools/render_catalog.py` 重建。
- 10 道 V1.0 练习题增加 `archetypes` 关联，保留原 `K-*`、`M-*`、题目 ID 与审核状态。
- 增加跨目录完整性、引用、依赖环、旧实体别名校验及负向单元测试。
- 后续重点：独立数学审稿、完善讲义正文与真题许可核验。

## V1.2 专题产出

- 1 篇扩展样章：单调性逻辑关系与完整证明、反例、分段跨点判定、典型母题、导数与参数充要性、根数问题，以及自制 PGFPlots 函数图。
- 题库共 **34 道独立题**：原有 10 道 + 新增 24 道（其中 4 道以 `\showworked` 在正文中展示，20 道进入训练）。
- 当前训练题单 30 道，全部来自独立题库，学生版隐藏训练答案，教师版附完整解析。
- 同一题库生成学生版 / 教师版；自动执行题目完整性及版权字段检查。
- `README`、规范文档、测试、GitHub Actions 构建工作流。

## 当前边界

这是一套**可用的最小出版骨架**，不是声称已完成的高中数学完整题库。题目以项目示例自拟或既有示例为来源，题目版权字段不等于独立数学审稿。所有 34 道题仍处于 `draft`；上线、公开宣传为高质量精选或出版前，需完成独立数学审核、版权和逐页排版复核。

## GitHub 仓库

项目地址：<https://github.com/lvxx040914/HighSchoolMath>。V1.1 已合并到 `main`。V1.2 必须先在单独分支验证后才可合并；本地升级包不意味着远程仓库已同步。项目目前未选择统一开源许可证，详见[项目规范](docs/PROJECT_SPEC.md)。
