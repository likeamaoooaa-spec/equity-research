// Curated decision layer for the research workspace.
// Every field below is a research judgment, not live market data. Keep the
// source document and as-of date attached so the website never presents an
// old view as a real-time recommendation.
const RESEARCH_STATE = {
  asOf: "2026-08-09",
  companies: {
    AMAT: {
      name: "Applied Materials",
      sector: "半导体设备",
      stance: "观察 / 持有",
      tone: "watch",
      price: "$539.14",
      value: "Base $520",
      valueRange: "$275 — $735",
      thesis: "AI 正在强化先进逻辑、DRAM 与先进封装需求，但估值已提前计入 2027 年的高增长。",
      debate: "增长持续时间能否支撑 30 倍以上前瞻市盈率。",
      nextMove: "等待财报兑现、估值消化，或价格回到 $400—450 后重估。",
      invalidation: "毛利率跌破 49% 且持续两个季度，或先进封装增长未兑现。",
      updated: "2026-08-09",
      source: "research/AMAT/2026-08-09_buyside-memo.md",
      catalyst: { window: "2026-08-13", event: "FY26 Q3 财报", watch: "Q4 指引、先进封装收入、毛利率", impact: "high" }
    },
    LITE: {
      name: "Lumentum",
      sector: "AI 光互连",
      stance: "Watchlist / Hold",
      tone: "watch",
      price: "$724.50",
      value: "PW $605",
      valueRange: "$300 — $1,000",
      thesis: "InP 激光器与 AI 光互连驱动盈利跃迁，但极高估值与客户集中让风险回报偏向下行。",
      debate: "FY27 盈利翻倍能否兑现，并抵消估值压缩和股本稀释。",
      nextMove: "等待财报确认，或价格进入 $550—650 区间后重估。",
      invalidation: "1.6T 爬坡或利润率改善不及预期，且客户集中风险继续上升。",
      updated: "2026-07-16",
      source: "research/LITE/2026-07-16_buyside-memo.md",
      catalyst: { window: "2026-08-11", event: "FY26 Q4 财报", watch: "收入指引、1.6T 爬坡、营业利润率", impact: "high" }
    },
    PLTR: {
      name: "Palantir",
      sector: "企业 AI 软件",
      stance: "HOLD / 上调警戒",
      tone: "watch",
      price: "$172.01",
      value: "PW $154",
      valueRange: "$80 — $195",
      thesis: "营收增长与美国商业业务继续加速，但 56 倍前瞻 P/S 已要求极高的持续兑现。",
      debate: "增长的超预期能否持续快于费用追赶和估值压缩。",
      nextMove: "保持观察，重点验证商业收入是否超过政府收入，以及利润率是否正常化。",
      invalidation: "增速明显跌破指引路径，或经营利润率持续下滑而费用增长加速。",
      updated: "2026-08-08",
      source: "research/PLTR/2026-08-08_Q2-2026-earnings-update.md",
      catalyst: { window: "2026 Q3", event: "Q3 经营数据", watch: "商业收入占比、美国商业增速、经营利润率", impact: "high" }
    },
    RKLB: {
      name: "Rocket Lab",
      sector: "商业航天",
      stance: "等待 / 小仓位",
      tone: "neutral",
      price: "$81.04",
      value: "Audit: Wait",
      valueRange: "$28 — $109",
      thesis: "公司正在转向国防太空系统平台，但 Neutron 工程门与当前估值仍不匹配。",
      debate: "Neutron 是平台放大器，还是继续吞噬资本并推迟盈利的单点风险。",
      nextMove: "等待 $45—55，或 Neutron 关键工程节点完成后重新承保。",
      invalidation: "Neutron 再次明显延迟、首飞失败，或 2027 收入路径下修。",
      updated: "2026-07-15",
      source: "research/RKLB/2026-07-12_investment-audit.md",
      catalyst: { window: "2026 Q4", event: "Neutron 首飞目标", watch: "一级储箱、Archimedes 热试车、整车测试与许可", impact: "high" }
    },
    SPACEX: {
      name: "SpaceX",
      sector: "太空基础设施",
      stance: "Avoid / Watchlist",
      tone: "avoid",
      price: "$133.11",
      value: "PW $112",
      valueRange: "$37 — $200",
      thesis: "Starlink 是优质利润池，但 AI 资本开支、短期合同与稀释把长期资产和短期风险绑在一起。",
      debate: "Starship V3 与 AI 云变现是否足以支撑接近 $2T 的完全稀释估值。",
      nextMove: "$105 以上不追高；$80—105 仅在里程碑兑现后重估。",
      invalidation: "V3 部署失速、AI 云收入下降或资本开支继续上升而现金流未改善。",
      updated: "2026-08-09",
      source: "research/SPACEX/2026-08-09_buyside-memo.md",
      catalyst: { window: "2026-08", event: "Starship Flight 14", watch: "入轨、V3 部署、重启、回收与复飞周期", impact: "high" }
    },
    WOLF: {
      name: "Wolfspeed",
      sector: "碳化硅",
      stance: "回避 / 重组观察",
      tone: "avoid",
      price: "~$35 未核验",
      value: "资本结构未定",
      valueRange: "暂不适用",
      thesis: "业务仍在恶化，旧股价值被 Chapter 11 重组后的稀释与新资本结构主导。",
      debate: "200mm 降本、CHIPS 补贴与重组能否共同扭转负毛利和收入下滑。",
      nextMove: "等待重组退出和新股本结构，再基于新股重新估值。",
      invalidation: "重组后毛利率仍为负、收入继续下滑，或客户与补贴进度进一步恶化。",
      updated: "2026-07-30",
      source: "research/WOLF/2026-07-30_bayesian-intrinsic-growth-valuation.md",
      catalyst: { window: "待定", event: "Chapter 11 重组退出", watch: "新股数、净负债、毛利率与 CHIPS 补贴", impact: "high" }
    }
  }
};
