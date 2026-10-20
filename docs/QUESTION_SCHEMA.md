# 题目数据结构协议（v1）

题目在 `questions/<id>/` 下存放：

```text
questions/HSM-FUN-0001/
├── metadata.yml    # 来源、标签、题型、审核状态、版权
├── stem.tex        # 题干（不含题号）
└── solution.tex    # 完整规范解答（不含“解：”）
```

核心字段：

| 字段 | 类型 | 约束 |
|---|---|---|
| `id` | string | 正则 `^HSM-[A-Z]{3}-[0-9]{4}$`，全库唯一且与目录一致 |
| `title` | string | 非空；仅辅助检索 |
| `chapter` | string | 知识领域 |
| `topics` | list[str] | 至少一个；引用 `knowledge/` 中存在的知识点 ID |
| `methods` | list[str] | 至少一个；引用 `methods/` 中存在的方法 ID |
| `difficulty` | int | 1–5 |
| `level` | enum | `foundation`, `intermediate`, `advanced`, `competition` |
| `type` | enum | `choice`, `fill`, `proof`, `solution` |
| `review_status` | enum | `draft`, `math_checked`, `typeset_checked`, `published` |
| `source.kind` | enum | `self_written`, `public_domain`, `licensed`, `reference_only` |
| `source.citation` | string | 明确出处或“本项目示例自拟” |
| `source.permission` | string | 例如 `self_authored` 或获得许可的具体说明 |

可选字段：`source.url`、`source.note`、`variant_of`、`prerequisites`、`curriculum_version`、`images`、`reviewed_by`。

`source.kind: reference_only` 的题目不能直接输出原题全文；构建脚本会拒绝。**不能用 `self_written` 洗白来源不明的外部题目。**

`config/monotonicity.yml` 的 `question_ids` 定义题目输出顺序。这一层决定讲义组合，不应复制题干内容。学生版仅显示 `stem.tex`，教师版附 `solution.tex`。

## 兼容与变更

元数据键名稳定，未来增加字段应提供默认值；需要重命名/删字段时，先升 schema_version 再执行迁移脚本；发布题目编号不得重用。
