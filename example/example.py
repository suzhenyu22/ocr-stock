"""
例子

注意：
    买入卖出因为点击确认买入卖出后，还会弹出提示确认对话框，这一部分还没有处理，在操作日志中会有记录。
    此外，最大化窗口操作中，由于模拟鼠标点击，点击任务栏的图标，程序并没有最大化或最小化，暂时没有解决这个问题。因此，不要让程序最小化，否则我暂时没办法最大化。这个在操作日志中也会记录有。
"""

# 买入股票
from ocrstock.operate.buy_sell import buy
buy('600001',12.01,200)

# 卖出股票
from ocrstock.operate.buy_sell import sell
sell('600001',12.01,200)

# 获取资金
from ocrstock.operate.get_summary import get_mony_summary
get_mony_summary()

# 获取持仓列表
from ocrstock.operate.get_positions import get_position_table
get_position_table()
