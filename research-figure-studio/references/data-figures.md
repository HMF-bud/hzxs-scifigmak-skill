# 数据图与混合组图的制作

## 后端和数据契约

复用用户明确选择、已有Python/R源或同一任务已确认的后端。无既有约定时选可运行且能交付目标格式的后端。只有后端会改变用户需要的编辑方式或交付物时，才并入选案问答。只读数据与设计不必等后端。确定后同一图用一个主绘图后端；缺运行环境时说明具体缺项，保留可运行源，不用另一语言偷偷替换成图。包内Python PDF检查器只读R的最终文件，不改绘图语义。

从真实源表建立显示映射，保留全部指定组合和顺序。数值核对表至少含图/面板、变量/组、实际值、单位、样本/分母及来源字段。只记录实际绘图值，不创造另一套正式统计表。差值、区间和类别已冻结时直接读取；比例/展示单位转换记录换算，不重新估计。

图型实现规则：

- 分布图需要原始对象值或明确分位数；箱须规则、离群点和样本单位写清。
- 中位数及区间图直接映射中心、上下端；不对称误差线分别为median−low和high−median。不要把区间当箱体或恢复率。
- 热图所有可比列共享norm，零中心差值用发散色标；颜色和数值指向同一统计量。
- 比例条/符号矩阵的几何按未舍入比例，数字可舍入；尺寸若用面积编码应明说面积。
- CDF用真实对象值排序后的经验比例，不平滑成不存在的分布；显示窗截断需保留尾部含义，不能把界外值移到边界。
- 配对关系使用对应对象的两个量或联合分类，不能从独立摘要倒推。

## Python实现与导出

以matplotlib为基础，已有代码最小修改。选定后检查环境、字体；中文使用本机存在的CJK字体。保持SVG文字可编辑、PDF嵌入字体。以下为导出片段，不生成示例科学值：

```python
from pathlib import Path
import sys
import matplotlib as mpl
import matplotlib.pyplot as plt

skill_dir = Path(skill_dir)  # 本包实际绝对目录，由本次任务定位
sys.path.insert(0, str(skill_dir / 'scripts'))
from audit_panel_alignment import require_matplotlib_panel_alignment

mpl.rcParams.update({'svg.fonttype': 'none', 'pdf.fonttype': 42,
                     'font.size': 8, 'axes.linewidth': 0.7,
                     'legend.frameon': False})
# fig由本任务真实数据代码创建；物理宽高在创建时设置。
fig.canvas.draw()
require_matplotlib_panel_alignment(
    fig, json_out=str(output_stem) + '.alignment.json',
    tolerance_pt=1.5, gutter_tolerance_pt=1.5, strict=True)
for extension in ('pdf', 'svg', 'png'):
    fig.savefig(str(output_stem) + '.' + extension, dpi=600)
```

先把布局放进最终画布再测量和导出；不要在测量之后用`bbox_inches='tight'`改变PDF尺寸却沿用旧manifest。非等大布局/嵌图/色标需声明实际可比组和必要例外，不能人为填写一套整齐几何。`matplotlib_layout_manifest`可接收axes、panel_ids、row_groups、column_groups、exclude_axes和exemptions，使用前按本包函数签名传入。

## R实现与导出

使用已有ggplot2/patchwork或ComplexHeatmap代码，保持字号、坐标和图例统一。`svglite`导出可编辑SVG、`cairo_pdf`导出矢量PDF、`ragg`按任务分辨率导出PNG。只输出用户要求的格式，不因旧模板默认额外输出TIFF。

```r
source(file.path(skill_dir, 'scripts', 'panel_alignment.R'))
# p为用真实数据构建的patchwork对象；宽高用本次任务的实际值。
require_patchwork_panel_alignment(
  p, manifest_path=paste0(stem, '.layout.json'),
  report_path=paste0(stem, '.alignment.json'),
  width_in=width_mm/25.4, height_in=height_mm/25.4,
  audit_script=file.path(skill_dir, 'scripts', 'audit_panel_alignment.py'),
  python=python_path, strict=TRUE)
ggplot2::ggsave(paste0(stem, '.pdf'), p, device=grDevices::cairo_pdf,
               width=width_mm, height=height_mm, units='mm')
ggplot2::ggsave(paste0(stem, '.svg'), p, device=svglite::svglite,
               width=width_mm, height=height_mm, units='mm')
ggplot2::ggsave(paste0(stem, '.png'), p, device=ragg::agg_png,
               width=width_mm, height=height_mm, units='mm', dpi=600)
```

R助手测量patchwork的实际面板；其他框架须从最终grob/viewport提取真实几何，不能把不支持的布局宣称已通过。依赖缺失时不自动安装或切换绘图语言。当前包保留R接口，是否已实测取决于本机检查记录。

## 地图和混合图

沿用已有地理边界、坐标、投影、流域/站点关系和有效样本定义，不为美化新增底图下载、空间分析、插值或平滑。九宫格等可比地图共用范围、投影和色标；端色裁剪只影响显示，不影响统计。无观测符号的移除按用户要求执行，科学样本说明留在图注。

混合方法/数据图保留各原生对象与实际合成链，一套面板编号和整体尺寸；先确定证据层次，再分配面积。共享图例/色标紧邻所属子图，不能隔着另一张图。导出后按[qa-and-delivery.md](qa-and-delivery.md)检查同一个最终文件。
