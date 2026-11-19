# 整合来源与许可

本包以 2026-11-17 整合快照和随后两轮制图返修为基础。它包含统一工作流、整合后的制图规范和包内工具。上游发布新版本时，按实际需要核对和合并相关文件。

## 第三方组件

| 来源与版本 | 内容与改动 | 适用许可 |
| --- | --- | --- |
| [Yuan1z0825/nature-skills · nature-figure](https://github.com/Yuan1z0825/nature-skills/tree/14ca69710cae192325395a380e9cdd4ae5d9d0c8/skills/nature-figure) | `audit_pdf_text.py`、`audit_figure_collisions.py`、`audit_panel_alignment.py`、`validate_figure.py`、`audit_svg_schematic.py` 与上游文件一致。修改了 `panel_alignment.R`，使调用者显式传入本包的 Python 审核脚本路径。科学证据组织和统计规范经整合改写 | [Apache-2.0](../licenses/nature-skills.txt)，以该版本仓库根目录 `LICENSE` 为准 |
| [kayla9928/scientific-drawio-flowchart](https://github.com/kayla9928/scientific-drawio-flowchart/tree/9a18c05aeaeee4f877e6d96c126f323d9be08f13) | draw.io 生成器、校验器、SVG 尺寸工具及 `scripts/lib/`。改写了 [流程图规范](flowchart-spec.md) 的流程链接与授权字段使用说明 | [MIT](../licenses/scientific-drawio-flowchart.txt) |
| [plbbl/academic-diagram-skill](https://github.com/plbbl/academic-diagram-skill) | 借鉴方法图构图、图形语义、图文比例和连线规范 | [原始说明的 MIT 许可与适用范围](../licenses/academic-diagram.txt) |
| [bahayonghang/drawio-skills](https://github.com/bahayonghang/drawio-skills) | 借鉴学术标签、公式、物理尺寸和可编辑矢量导出原则 | [MIT](../licenses/drawio-academic-skills.txt) |
| [Chutj/sci-figure-gallery](https://github.com/Chutj/sci-figure-gallery) | 公开图库及检索索引。包内 `search_gallery.py` 是本地工具，从公开 JSON 检索候选并链接回图库。参考图片的许可逐图核对 | 索引与论文图的权利说明见 [图库 LICENSES.md](https://github.com/Chutj/sci-figure-gallery/blob/main/LICENSES.md) |

本地 `research-figure-workflow` 提供三案问答、统一审核和局部返修约定。其 PDF 审核入口改为从包内同级目录调用检查器。本地 `research-writing-skill` 提供经反复修订的简明图注规范。整合后的规则也包含维护者在多轮制图返修中确认的统计与版式偏好。

[文件级来源清单](../origin_manifest.json)记录整合时的来源标识、复制与改写情况，以及原文件和发布文件的 SHA-256。许可范围按文件及上表所列来源确定。论文样图与论文数据由各自的权利人和资料来源管理。
