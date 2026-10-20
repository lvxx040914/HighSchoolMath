# 内容贡献与复核流程

1. 创建新题目录，使用未被占用的不可变 `HSM-XXX-NNNN` ID。
2. 填写来源类型、可再发布许可及题目元数据；未知版权内容只能作索引，不允许全文提交。
3. `stem.tex` 只保存题面，`solution.tex` 独立保存完整、可检验的数学解答；题号自动生成。
4. 如果题目与已有题属于母题/变式关系，请补充 `variant_of`，不重复复制无实质区别的答案。
5. 先运行 `make validate && make test && make build`。
6. 人工检查极值端点、参数临界值、导数判定前提、量词、定义域与等号条件。
7. 在 PR 中列出新增题目的 ID、来源授权、独立复算记录、学生/教师版页面截图；未经人工复核的题保持 `draft`。

单人初期开发时仍要区分「脚本验证通过」与「独立审稿通过」。任何数学内容更新应由独立复算或详细反例测试佐证。

## V1.1 协作流程

先读 `AGENTS.md` 与 `docs/EDITORIAL_STANDARD_V1_1.md`。目录条目只编辑 `catalog/*.yml`，然后执行 `python tools/render_catalog.py` 并提交同步更新的 `docs/*ATLAS.md`。新增题目建议填写 `archetypes`，审稿状态保留 `draft`，人工复核后再升级。每个 PR 应附本次涉及的知识点/方法/题型 ID 及测试命令。

V1.3：示范例题也须独立存入题库并提供 `answer.tex`。提交前运行 `make check && make build && make pdfcheck`。不要将自动构建视为数学人工审核。
