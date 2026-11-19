# hzxs-scifigmak-skill · 科研制图完整版

面向论文数据图、组图和可编辑方法图的 Codex Skill。把科学问题、真实参考、版式选择、Python/R 或 draw.io/SVG 实现和成图审核放进同一流程。常规任务可直接使用包内规范和脚本。

## 安装和调用

克隆本仓库，将整个 `research-figure-studio/` 目录复制到项目的 `.agents/skills/`，或复制到用户目录的 `~/.agents/skills/` 供各项目使用。已经安装同名 Skill 时，先决定采用哪个版本，避免重复安装。目录结构和发现规则见 [OpenAI 安装说明](https://developers.openai.com/api/reference/cli)。

在 Codex 会话中显式调用 `$research-figure-studio`，也可以说「使用科研制图完整版」。提供可读取的数据或摘要、绘图脚本、稿件相关段落或已有图，再说明目标格式及版面要求。

> 使用 $research-figure-studio，根据项目中的数据与正文设计一张组图。请在一次回复里给出三种方案、推荐方案及会改变布局的取舍，我选定后再制作。交付矢量 PDF、绘图源码和简短图注。

新图会把证据与参考图共同用于三案设计。可以回复 `A`、`B`、`C`，合并不同方案的面板，或在请求中直接指定方案。只改已有图的图例、编号或留白时，直接说明要改的对象和范围即可。

## 运行环境

| 任务 | 所需环境 |
| --- | --- |
| 图库检索、draw.io 文件生成和结构检查、SVG 尺寸检查 | Python 3.10+。在线检索需访问公开图库索引，已有 JSON 索引可离线使用 |
| PDF 字体、碰撞和对齐审核 | Python 和 PyMuPDF。多面板 PDF 还需从最终绘图布局测得的几何记录 |
| Python 或 R 数据图 | Python 路线通常使用 Matplotlib。R 路线按原图选包，patchwork 对齐助手需要 patchwork、jsonlite 和可用的 Python |
| 可编辑方法图导出 | `.drawio` 可在 draw.io 中编辑。桌面批量导出使用 draw.io Desktop，原生 SVG 可用支持 SVG 的矢量编辑器查看和修改 |

安装 Skill 仅复制工作流与工具。绘图库、字体和导出应用按上表准备。

## 目录结构

```text
research-figure-studio/
├── SKILL.md                # 入口、流程及分支
├── agents/openai.yaml      # Codex 界面名称与调用示例
├── references/             # 选案、统计口径与偏好、数据图、方法图、审核、图注
├── scripts/                # 图库检索、PDF/SVG 审核、绘图源码检查及 draw.io 工具
├── licenses/               # 第三方许可文本
└── origin_manifest.json    # 文件级来源、版本和改动
```

可从[三案设计与问答](research-figure-studio/references/design-and-choice.md)、[数据图实现](research-figure-studio/references/data-figures.md)或[方法图实现](research-figure-studio/references/method-figures.md)查看相应命令和图件约定。

## 个性化修改

- **一次集中选型。** 三案共用同一组读图问题、统计口径和系列风格。第一轮同时给出方案、推荐理由和少数确实影响构图的偏好问题。选定后沿用已确认决定，直接制作和校验。
- **保留关键证据。** 总体分布、效应幅度、比例和逐对象配对分别表达。每案说明读者从哪里读出答案，以及取舍会丢掉哪些信息。投稿尺寸下先用成图和图注试读，再回源表核值。
- **把常见返修变成制图习惯。** 沿用同系列已采纳的字号层级与颜色含义。关键值就近标，图例和色标靠近所属面板，子图连续编号。方法图用简洁的框和文字，箭头接到真实目标。
- **使用一个主源和一次合并审核。** 复用同一个绘图源迭代，将数据、版式和视觉检查对准同一次导出，局部返修只重查受影响处。

## 上游来源与致谢

| 项目 | 在本包中的用途 |
| --- | --- |
| [Yuan1z0825/nature-skills · nature-figure](https://github.com/Yuan1z0825/nature-skills/tree/14ca69710cae192325395a380e9cdd4ae5d9d0c8/skills/nature-figure) | 科学证据与统计表达规范，PDF、面板对齐、源码和 SVG 审核脚本。R 助手改为显式传入本包 Python 检查器路径 |
| [Chutj/sci-figure-gallery](https://github.com/Chutj/sci-figure-gallery) | 图库与公开索引。包内的检索脚本来自本地整合工作，读取公开元数据供选图和核对来源 |
| [plbbl/academic-diagram-skill](https://github.com/plbbl/academic-diagram-skill) | 方法图构图、图形语义和连线规范的参考 |
| [bahayonghang/drawio-skills](https://github.com/bahayonghang/drawio-skills) | 学术标签、公式、投稿物理尺寸与可编辑矢量导出的参考 |
| [kayla9928/scientific-drawio-flowchart](https://github.com/kayla9928/scientific-drawio-flowchart/tree/9a18c05aeaeee4f877e6d96c126f323d9be08f13) | draw.io 构建、验证与 SVG 尺寸工具。流程规范调整为沿用会话已经确认的关系和制作决定 |
| `research-figure-workflow` 和 `research-writing-skill` 的本地版本 | 三案选择、合并审核、PDF 审核入口和精简图注，结合历次制图反馈整合 |

发布包包含公开工作流、通用偏好和工具。第三方文件许可按来源适用，具体范围和整合改动见[来源与许可](research-figure-studio/references/provenance.md)。参考论文的图片仍遵循各自的授权条款。
