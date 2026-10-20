# HighSchoolMath｜高中数学讲义与题库

> V1.0 样章：函数与导数 · 函数的单调性。项目初始工程，尚未发布到 GitHub。

本项目坚持「一份结构化数学内容，多种输出」：**知识点库—方法库—独立题库—讲义编译** 四层解耦，形成便于审核、长期维护的高中数学出版系统。

## 获取内容

- [完整项目规范](docs/PROJECT_SPEC.md)
- [内容与数学写作规范](docs/EDITORIAL_GUIDE.md)
- [题目数据规范](docs/QUESTION_SCHEMA.md)
- [V1.0 实施计划](docs/ROADMAP.md)
- [样章源码](lectures/functions/monotonicity.tex)
- [练习题清单](config/monotonicity.yml)

## 运行（需 XeLaTeX / latexmk / Python ≥ 3.10）

```bash
python -m pip install -r requirements.txt
python tools/validate.py
python tools/build.py --edition all
```

预期生成：`dist/monotonicity_student.pdf`（学生版）、`dist/monotonicity_teacher.pdf`（教师版）。学生版含理论与完整示范例题、专题训练不含答案；教师版在末尾附独立答案详解。输出由同一批题目生成。

若没有 `latexmk`，可在项目根目录直接运行：

```bash
xelatex -interaction=nonstopmode -halt-on-error -output-directory=dist tex/student.tex
xelatex -interaction=nonstopmode -halt-on-error -output-directory=dist tex/student.tex
```

上述手工方式必须先运行一次 `python tools/build.py --generate-only` 以生成索引文件。

## 初始内容

- 1 个样章：严格单调、导数判定、复合函数、参数分类、构造函数和零点个数。
- 带规范 ID 的知识点库与解题方法库。
- 10 道带唯一 ID、YAML 元数据、独立题干和完整解答的试验题目。
- 同一题库生成学生版 / 教师版；自动执行题目完整性及版权字段检查。
- `README`、规范文档、测试、GitHub Actions 构建工作流。

## 当前边界

这是一套**可用的最小出版骨架**，不是声称已完成的高中数学完整题库。样章中的题目均为独立编写的教学示例（数学基本题型不可独占），源数据初始审核状态为 `draft`；上线或出版前仍需人工数学复核和版式复核。

## 建立 GitHub 仓库

当前连接不提供“创建仓库”操作。先在 GitHub 新建空仓库 `HighSchoolMath`（不要勾选自动创建 README），然后在项目根目录执行：

```bash
git init
git add .
git commit -m "chore: initialize HighSchoolMath v1 monotonicity sample"
git branch -M main
git remote add origin https://github.com/<你的用户名>/HighSchoolMath.git
git push -u origin main
```

替换 `<你的用户名>` 后执行。建议先设置为私有仓库，确定内容版权策略后再考虑公开。项目未选择统一开源许可证，详见[项目规范](docs/PROJECT_SPEC.md)。
