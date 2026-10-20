# HighSchoolMath V1.1｜内容标准与知识目录

**发布日期**：2026-10-20。**性质**：V1.0 基础上的兼容式升级，非全部高中数学正文完工。

## 已交付

- 11 个知识领域、93 个知识主题的结构化目录（`catalog/knowledge_map.yml`）。
- 42 种解题方法，每种都记录适用条件、易错或失效情况（`catalog/methods.yml`）。
- 50 类典型题型，记录知识关联、方法关联、两条变式轴及典型失误（`catalog/archetypes.yml`）。
- 自动生成的完整浏览目录（`docs/KNOWLEDGE_ATLAS.md`、`docs/METHOD_AND_ARCHETYPE_ATLAS.md`）。
- 正式编写审核标准、内容模板、课标定位说明与 AI 协作规范。
- 保留 V1.0 的 10 道题，增加题型 ID 关联，所有题仍为 `draft`。
- 对目录循环依赖、错误引用、旧实体别名和题型关联的校验；包含负向测试。
- 保持两套样章 PDF 的现有生成机制，未冒称完成四套模板。

## 已完成的本地验证

- `python tools/validate.py`：通过；10 道题引用和来源字段完整。
- `python tools/validate_catalog.py`：通过；11/93/42/50，关联 10 道现存题。
- `python tools/render_catalog.py --check`：通过；目录产物与 YAML 一致。
- `python -m unittest discover -s tests -v`：5 项测试通过，含 3 项错误样例的拒绝测试。
- 清空中间文件后 `python tools/build.py --edition all`：成功；学生 PDF 5 页，教师 PDF 7 页。

## 不应误读为已完成的工作

- 93 个知识主题、42 种方法与 50 种题型都是**规划分类**，不是逐个成文与数学审稿完成。
- 原有 10 道题保留 `draft`；自动检测无法保证解答正确。
- 课标归属为编辑候选分类，尚未逐条对应课程标准与地区考试范围。
- GitHub 远程仓库**尚未由此次升级自动更新**；请依照升级补丁操作上传。

## 将 V1.1 升级到既有仓库

1. 确认 `git status` 干净。如有自己未提交的改动，先自行提交或暂存，避免覆盖。
2. 下载 `HighSchoolMath_V1.1_升级补丁.patch` 到电脑 `~/Downloads`。
3. 在终端依次运行：

```bash
cd ~/Desktop/HighSchoolMath
git switch -c feature/v1.1-content-standards
git apply --check ~/Downloads/HighSchoolMath_V1.1_升级补丁.patch
git apply ~/Downloads/HighSchoolMath_V1.1_升级补丁.patch
python3 -m pip install -r requirements.txt
python3 tools/validate.py
python3 tools/validate_catalog.py
python3 tools/render_catalog.py --check
python3 -m unittest discover -s tests -v
python3 tools/build.py --edition all
git add .
git commit -m "feat: add V1.1 curriculum and editorial taxonomy"
git push -u origin feature/v1.1-content-standards
```

4. 在 GitHub 页面新建从 `feature/v1.1-content-standards` 到 `main` 的 Pull Request，核验 CI 与数学内容后合并。

**Mac 环境提醒**：如缺少 XeLaTeX / latexmk，先安装 MacTeX 或 BasicTeX（并安装相应字体）再编译 PDF；目录、验证与单元测试可先执行，但不能把未运行的 PDF 编译宣称为通过。
