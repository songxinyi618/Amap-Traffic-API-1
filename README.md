# Amap-Traffic-API-1
一句话介绍：给定矩形区域顶点的经纬度，帮董家渡项目用高德地图(Amap）和百度地图API爬取了工作日与周末道路实时路况，保存为CSV格式并绘图。

baidu api:
百度地图API调用脚本。

baidu_figure:
用百度API爬取的数据画折线图，横轴表示时间，纵轴表示路段拥堵评价（畅通、缓行、拥堵、严重拥堵）。

gaode api:
高德地图(也叫Amap)的API调用脚本。

gaode_concat:
由于网络不稳定，高德地图的抓取进程经常会断，因此需要将分段的数据合并。

gaode_figures:
将高德的数据按每个数据点绘制折线图。

gaode_figures_15:
将高德的数据按每3个点（大约15分钟）取最小值，绘制折线图。

gaode_little_table:
因为抓取到的一些路段超出了研究范围，因此需手动删选，在删选之前先统计一个含有各路段组合的小表格。

gaode_figures_all:
将高德的数据用subplot合并绘制在一个大图中。

gaode_modify:
中华路的方向需要从四向改成双向。
