# B站一键添加到稍后再看
### 自动添加指定日期附近之前的已关注的UP的视频到稍后再看
利用Login.py实现二维码登录B站，以此获取Cookie来读取用户的稍后再看列表和已关注UP主最近发布的视频。\
以页为单位，在自定义天数之前，添加时间段内的视频到稍后再看，并保存未添加到稍后再看的视频列表。
# 使用指南
1. 请pip install所需库（注意cv2需pip install opencv-python，且注意cv2的大小写）
2. 运行main.py
3. 扫码登录B站并**关闭二维码**
4. 按照提示运行
5. 修改Viewed.txt的第一个字符以改变运行模式

# Credits
### Main.py、Core.py
**Credit**: 我自己[Chuan Peng][1]；B站：[加把劲假面骑士][2]
### Login.py
**Credit**: 忘了抄的是哪位大神的了，纯净版[这边请][3]


[1]: https://erichuanp.com
[2]: https://space.bilibili.com/4689754
[3]: https://github.com/CreeberSlime/Bilibili_Cookie_QRCodeLogin
