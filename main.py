import time
import Core
import webbrowser
from os import system


# region 初始化
Core.init()
mode = open('Viewed.txt', 'r').readline(1)
# endregion

# region 询问并计算时间
time_input = 3
if mode != 'a':
    time_input = input('需要添加多少天以前的视频(默认为3)：')
    if not time_input.isdigit():
        print('输入了非数字，默认解析前三天的视频。')
        time_input = 3

print('一般需要解析(2*天数+1)页视频...')
end_time = int(time.time()) - int(time_input) * 86400  # 获取 time_input 天前的时间戳
# endregion

# region 添加BV号到稍后再看
BVs = Core.get_BVs(end_time)
msg = ''
print('在此期间，有' + str(len(BVs)) + '个视频未看。\n')
if mode != 'a':
    if input('是否要移除已看的视频(y)：') == 'y':
        msg += Core.del_to_view()
    if input('是否要添加到稍后再看(y)：') == 'y':
        msg += Core.add_BV()
else:
    msg += Core.del_to_view()
    msg += Core.add_BV()
# endregion

# region 结束
if mode != 'a':
    if input('是否要查看运行日志(y):') == 'y':
        print(msg)
else:
    log = open('Log.txt', 'w')
    log.write(msg)
    log.close()
    print(msg)
Core.update_viewed()
webbrowser.open('https://www.bilibili.com/watchlater/#/list')
print('程序已结束\n')
if mode != 'a':
    system('pause')
# endregion
