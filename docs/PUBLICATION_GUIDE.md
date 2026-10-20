# V1.3 四版本出版与自动组卷操作说明

## 1. 内容数据职责

- `questions/HSM-FUN-XXXX/metadata.yml`：来源、审核状态、知识点、方法、题型、难度。
- `stem.tex`：不含题号的题干；`solution.tex`：严谨完整解答；`answer.tex`：用于速查册的结论，不能代替推理。
- `config/monotonicity.yml`：默认 10 道示范题与 30 道训练题，题号由引用顺序生成。
- `lectures/functions/monotonicity.tex`：只编写理论、方法、例题引用与图；所有例题题干和解答必须存入题库。
- `tex/preamble.tex`：统一风格与版面；`tools/build.py`：索引生成及四份 PDF 的编译入口。

## 2. 四种产品

运行 `make build`，生成 lecture / workbook / teacher / answer_key 四种产品：

- **lecture**：理论、目录、讲授用母题完整解析和训练题题干。
- **workbook**：只含当前选定题单，随难度提供不同的答题空白。
- **teacher**：lecture 加训练题完整解析，训练题题号与 workbook 一致。
- **answer_key**：当前题单的独立速查结论，不包含教师解析。

另生成旧版名称 `monotonicity_student.pdf` 供旧流程使用。可执行 `make lecture`、`make workbook` 等单独构建。

## 3. 筛选与组卷

```bash
python3 tools/compose.py --topic K-FUN-MONO --min-difficulty 2 --max-difficulty 4 --count 8 --seed 42 --slug week1 --out config/week1.yml
python3 tools/build.py --config config/week1.yml --edition workbook
python3 tools/build.py --config config/week1.yml --edition answer_key
```

可组合 `--method`、`--archetype`、`--type`、`--level`、`--include-worked`。使用 `--seed` 保证结果可复现，随机种子对**同一个版本的题库和元数据**有效，题库变化后建议固化生成的 YAML 题单。未满足题目数量时直接报错，不凑数。自定义构建会恢复既有默认 TeX 索引。

本版只支持已入库单调性题池；尚不支持跨多个专题自动生成讲义正文、不支持解析题自动判分和统计难度标定。

## 4. 新题入库规范

1. 为题目分配永久 ID，不得复用；将题干、完整解析、简明答案分别写为 `stem.tex`、`solution.tex`、`answer.tex`。
2. 填写合法来源、课程知识、方法、题型、难度、审核状态。所有引用必须指向目录中的有效 ID。
3. 用 `config/*.yml` 引用题目，不复制粘贴 TeX 内容到讲义里。
4. 运行 `make check && make build && make pdfcheck` 并人工检查每页公式、分页和字号。
5. 不得把自动校验通过的题目直接标记为 `math_checked`，数学结论必须独立重解；来源不明的外部题只保留索引。

## 5. 常见问题

- macOS 报 `fontspec`：见字体自动回退逻辑；先确认 `xelatex`、`latexmk` 可用，再查看 `dist/monotonicity_lecture.log` 首个 `!` 错误。
- PDF 目录页码不稳定：`latexmk` 会自动运行必要轮次；不要只运行一次 `xelatex` 就判断交叉引用已完成。
- 自定义组卷导致 `make check` 失败：检查是否曾手动运行 `--generate-only` 搭配自定义配置；重新执行 `make generate` 恢复默认生成索引。
- 发布前审查：须保留原始题源、版本及改题记录；版权或数学审核不足时继续保持 `draft`。
