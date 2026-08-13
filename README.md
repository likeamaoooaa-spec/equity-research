# Equity Research

这是一个面向买方研究的个人投研知识库，同时通过 GitHub Pages 提供静态阅读界面。

网站：<https://likeamaoooaa-spec.github.io/equity-research/>

## 内容结构

```text
research/[TICKER]/         个股研究报告
research/[TICKER]/data/    SEC 文件、电话会记录和其他原始资料
notes/[sector]/             行业研究笔记
notes/[日报名称]/            美股收盘日报等定期内容
```

`research/` 和 `notes/` 下的 Markdown 文件会自动出现在网站侧边栏。`data/` 目录只保存研究底稿，不进入导航。

## 本地维护

生成侧边栏索引：

```bash
python3 build_tree.py
```

从 SEC XBRL 文件提取财务数据：

```bash
python3 extract_financials.py
```

运行仓库完整校验：

```bash
python3 scripts/validate_repo.py
```

安装财务数据提取依赖：

```bash
python3 -m venv .venv
. .venv/bin/activate
python3 -m pip install -r requirements.txt
```

如果使用本地 Git hook，先执行：

```bash
git config core.hooksPath .githooks
```

## 文件命名

- 个股研究：`YYYY-MM-DD_type.md`
- 行业笔记：`YYYY-MM-DD_topic-slug.md`
- 日报：`名称_YYYY-MM-DD.md`

日期由文件名承载，股票代码由父目录承载，避免重复命名。

每篇公开 Markdown 还应包含 YAML front matter：`schema_version`、`title`、`date`、`type`；个股研究额外填写 `ticker`。侧边栏和全文搜索均从这些字段生成。

`search-data.js`、`tree-data.js` 和 `financial-data.js` 都是生成文件，不要手工编辑。

## 来源纪律

研究报告应区分已披露事实、管理层指引、市场共识和分析师推断，并尽量记录文件类型、发布日期与查阅日期。无法核验的数字标记为“未核验”。

财务数据的期间结束日、申报日期和指标级来源由 `extract_financials.py` 写入；仓库校验会检查来源路径和期间重复。原始 SEC 文件的长期归档边界见 [DATA_ARCHIVE.md](DATA_ARCHIVE.md)。

网站提供全文搜索、研究总览、财务仪表盘和读者批注。Supabase 批注的 RLS 配置模板见 [supabase/rls.sql](supabase/rls.sql)；应用前请按实际表结构复核。

## 免责声明

本仓库内容仅用于研究、记录和教育交流，不构成投资、税务或法律建议。历史数据、估值结果和个人判断均可能存在错误，也不代表任何证券的未来表现。
