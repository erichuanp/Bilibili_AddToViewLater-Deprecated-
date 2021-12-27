# B站一键添加到稍后再看
### 自动添加指定日期附近之前的已关注的UP的视频到稍后再看
利用Login.py实现二维码登录B站，以此获取Cookie来读取用户的稍后再看列表和已关注UP主最近发布的视频。\
以页为单位，在自定义时间之前，添加时间段内的视频到稍后再看，并保存未添加到稍后再看的视频列表。
#使用指南
1. 请pip install所需库（注意cv2需pip install opencv-python，且注意cv2的大小写）
2. 运行main.py
3. 扫码登录B站并关闭二维码
4. 输入所需的多久之前（时间格式：数字+d/h/m/s、时间戳：纯数字）
5. 确认是否需要添加到稍后再看
6. 按需复制未添加到稍后再看视频的列表

Tip1: 请保管好Viewed.txt文件，下次使用不会将存在于Viewed.txt里面的视频BV号添加到稍后再看\
Tip2: 删除第二行开头的 # 可以手动添加列表
````Python
bvs = list_maker()
# bvs =   # 手动添加列表
````
请修改成：
````Python
# bvs = list_maker()
bvs = ['BV号1', 'BV号2', 'BV号3', ...]
````
# 所有文件
### Main.py
**Credit**： 我自己[Chuan Peng][1]；B站：[加把劲假面骑士][2]
### Login.py
**Credit**： 忘了抄的是哪位大神的了，纯净版[这边请][3]
### B站UID_cookies.json
json类型的用户cookies
### Viewed.txt
已观看视频的列表，注意保存，下次使用将参考该文件的内容来添加视频。


[1]: https://erichuanp.com
[2]: https://space.bilibili.com/4689754
[3]: https://github.com/CreeberSlime/Bilibili_Cookie_QRCodeLogin
