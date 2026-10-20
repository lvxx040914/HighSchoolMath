# HighSchoolMath 协作与 AI 编辑约束（V1.1）

这是面向数学讲义与题库的长期内容工程，而非一次性 PDF 项目。所有人类和 AI 编辑均遵守如下规则。

1. **先读** `docs/EDITORIAL_STANDARD_V1_1.md`、`docs/QUESTION_SCHEMA.md`、`docs/CURRICULUM_ALIGNMENT.md`，以及本次涉及的 `catalog/*.yml`。数学范围和课程版本不能根据印象标注为官方已核验。
2. **维护单一事实源**：知识编辑目录在 `catalog/knowledge_map.yml`，方法在 `catalog/methods.yml`，题型在 `catalog/archetypes.yml`；`docs/KNOWLEDGE_ATLAS.md` 和 `docs/METHOD_AND_ARCHETYPE_ATLAS.md` 只能由 `tools/render_catalog.py` 生成，不得手工改。
3. **兼容既有 V1.0**：不得随意重命名 `K-*`、`M-*` 或 `HSM-*` ID；任何迁移必须附映射与测试。题目 `stem.tex` 和 `solution.tex` 分离，讲义调用题库而非粘贴复制。
4. **严谨考试数学**：公式为主，定理条件明确；参数、端点、不可导点、零分母、等价变形、充要性、极值与最值须逐项核查；结论尽量 `\boxed{}`。不得用“显然”跳过关键论证。
5. **不批量洗稿**：来源未经确认时不可标记原创或可转载。竞赛拓展单列，未审草稿不得公开标为“精选题”。
6. **审核保守**：AI 或测试不得单方面将 `draft` 升为 `math_checked` 或 `published`；维护可追溯审稿人及时间。
7. **每次改动必须检查**：
   ```bash
   python tools/validate.py
   python tools/validate_catalog.py
   python tools/render_catalog.py --check
   python -m unittest discover -s tests -v
   python tools/build.py --edition all
   ```
8. **提交说明**应明确新增与修改的知识 / 方法 / 题型 / 题目 ID、数学审核状态、编译验证结果。若没有本地 TeX 工具，必须说明 PDF 未验证，不能宣称编译通过。
9. **变更方式**：优先特性分支与 PR；合并前检查生成文档和源目录一致。不要为了通过测试而降级校验规则。

版本定位：V1.1 为内容目录和审核标准版本；尚未完成 93 个知识主题的正文、42 种方法讲解或 50 类题型母题，明确区分目录规划与实际审核产物。

## V1.2 补充

- 函数单调性讲义新母题统一通过 `\showworked{HSM-*}` 读取题库，禁止再为同一母题复制另一份解答。
- 修改 `config/monotonicity.yml` 时，训练题与示范母题集合必须互斥。
- 每次 PDF 编译后运行 `python tools/verify_pdf.py`；所有题目仍标记 `draft`，不因自动化通过而升级审稿等级。


## V1.3 附加约束

- 讲义正文只编写知识、证明和方法解释；完整例题用独立 `questions/<ID>/` 引用（包括 `stem.tex` / `solution.tex` / `answer.tex`），禁止把整套示范例题直接重新写进正文。
- 构建四种输出，学生用习题册和速查答案绝不可包含教师版完整解答；修改后应运行 `make check && make build && make pdfcheck`。
- macOS / Linux XeLaTeX 必须使用字体回退，补丁和压缩包必须使用 ASCII 英文文件名。
- 自动组卷应有固定随机种子、明确数量及缺题报错，题库数不足不得重复或假造题目。
- 不要自动更改 `draft` 审核等级；新增题目要记录来源授权和课程范围。
