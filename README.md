# Equity Research

这是一个面向买方研究的投资决策工作台，同时通过 GitHub Pages 提供静态阅读界面。网站围绕“判断—证据—催化剂—证伪—复盘”组织，而不只是展示文章目录。

网站：<https://likeamaoooaa-spec.github.io/equity-research/>

## 内容结构

```text
research/[TICKER]/         个股研究报告
research/[TICKER]/data/    SEC 文件、电话会记录和其他原始资料
notes/[sector]/             行业研究笔记
notes/[日报名称]/            美股收盘日报等定期内容
```

`research/` 和 `notes/` 下的 Markdown 文件会自动出现在网站侧边栏。`data/` 目录只保存研究底稿，不进入导航。

网站包含五个核心工作区：

- 决策台：展示覆盖规模、当前判断与最新研究变化
- 覆盖池：统一比较立场、估值锚、核心逻辑和研究日期
- 催化剂：追踪报告中已经定义的验证节点
- 研究库：按决策、更新和背景研究分类浏览
- 标的档案：汇总单家公司论点、行动、证伪条件与历史报告

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

`research-state.js` 是人工维护的决策层。新增覆盖标的或完成关键复核后，需要同步更新其中的立场、报告价格、估值锚、核心争议、下一步动作、证伪条件、催化剂、来源报告和研究日期。它不是实时行情文件，任何数字都必须保留口径与日期。

## 新增报告与更新结论

从 [templates/research-report-template.md](templates/research-report-template.md) 复制报告模板，并按以下规则处理：

1. 报告放入 `research/[TICKER]/YYYY-MM-DD_type.md`，填写完整 front matter。
2. 如果报告改变或重新确认评级、估值锚、行动建议、催化剂或证伪条件，设置 `decision_update: true`；纯背景研究设置为 `false`。
3. 当 `decision_update: true` 时，在同一提交中更新 `research-state.js`：至少同步 `stance`、`price`、`value`、`valueRange`、`thesis`、`debate`、`nextMove`、`invalidation`、`catalyst`、`updated` 和 `source`，并把顶层 `asOf` 更新到最新复核日。
4. 运行 `python3 build_tree.py` 和 `python3 scripts/validate_repo.py`。如果决策报告已经新增但结论层没有同步，校验会失败并指出具体 ticker。
5. 检查网站的标的档案和催化剂页面，再提交并推送。GitHub Pages 会从 `master` 自动发布。

判断层不应机械复制报告摘要。它只保存做决策所需的最小状态；完整证据、模型和来源仍留在报告中。

## 来源纪律

研究报告应区分已披露事实、管理层指引、市场共识和分析师推断，并尽量记录文件类型、发布日期与查阅日期。无法核验的数字标记为“未核验”。

财务数据的期间结束日、申报日期和指标级来源由 `extract_financials.py` 写入；仓库校验会检查来源路径和期间重复。原始 SEC 文件的长期归档边界见 [DATA_ARCHIVE.md](DATA_ARCHIVE.md)。

网站提供全文搜索、覆盖池、催化剂跟踪、标的档案、财务仪表盘和读者批注。Supabase 批注的 RLS 配置模板见 [supabase/rls.sql](supabase/rls.sql)；应用前请按实际表结构复核。

## 免责声明

本仓库内容仅用于研究、记录和教育交流，不构成投资、税务或法律建议。历史数据、估值结果和个人判断均可能存在错误，也不代表任何证券的未来表现。
