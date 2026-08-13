# 数据归档边界

`research/*/data/` 是研究底稿区，不参与网站导航。它包含 SEC 原始 HTML、PDF、电话会记录和下载后的文本材料。

当前仓库仍保留这些文件，以保证历史报告可以离线复核；后续新增的大型原始文件建议存放到独立的归档仓库或对象存储，研究报告只保留：

- 官方来源 URL、文件类型、发布日期和查阅日期；
- 提取后的结构化数据；
- 能支撑投资判断的必要摘录。

归档迁移前不要直接删除现有 `data/` 文件，也不要重写公开 Git 历史。迁移时应先建立校验和清单，再更新报告中的相对链接和 `financial-data.js` 来源路径。

## 建议的清单字段

`ticker`、`form`、`period_end`、`filing_date`、`source_url`、`local_path`、`sha256`、`accessed_at`。

当前已通过 `python3 scripts/build_data_manifest.py` 生成 [data-manifest.json](data-manifest.json)，其中记录仓库内已跟踪底稿的大小和 SHA-256。迁移归档时应先用这份清单做完整性核对。
