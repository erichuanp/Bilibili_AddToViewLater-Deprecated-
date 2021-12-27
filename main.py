import json
import os
import time
import re
import requests
import Login


def scan(filena):
    dirs = os.listdir('.')
    for dir in dirs:
        if not dir.find(filena) == -1:
            return dir
    return 'None'


def list_maker():
    bvlist = []
    url = 'https://api.vc.bilibili.com/dynamic_svr/v1/dynamic_svr/dynamic_new?uid=' + UID + '&type_list=8&from=&platform=web'
    response = session.get(
        url=url,
        cookies=cookies,
        data={
            'uid': UID,
        })
    historyOffset = response.text[response.text.find('history_offset') + 16:response.text.find(',"_gt_":0}}')]
    for bv in extract_bvs(response.text):
        bvlist.append(bv)
    timestamps = []
    page = 1

    print('第' + str(page) + '页，翻页中...')

    keep = True
    while keep and int(
            response.text[response.text.rfind('timestamp') + 11:response.text.rfind('timestamp') + 21]) > endDate:
        url = 'https://api.vc.bilibili.com/dynamic_svr/v1/dynamic_svr/dynamic_history?uid=' + UID + '&offset_dynamic_id=' + historyOffset + '&type=8&from=&platform=web'
        response = session.get(
            url=url,
            cookies=cookies,
            data={
                'uid': UID,
                'offset_dynamic_id': historyOffset
            })
        page = page + 1
        print('第' + str(page) + '页，翻页中...')
        historyOffset = response.text[response.text.find('next_offset') + 13:response.text.find(',"_gt_":0}}')]
        res = response.text
        for bv in extract_bvs(res):
            bvlist.append(bv)
        while not res.find('timestamp') == -1:
            stampLoc = res.find('timestamp') + 11
            timestamps.append(res[stampLoc:stampLoc + 10])
            res = res[stampLoc:]
        for timestamp in timestamps:
            if int(timestamp) < endDate:
                keep = False

    bvlist = sorted(set(bvlist), key=bvlist.index)
    return bvlist


def extract_bvs(txt):
    bvs = []
    while not txt.find('bvid') == -1:
        bvidLoc = txt.find('bvid') + 7
        bvs.append(txt[bvidLoc:bvidLoc + 12])
        txt = txt[bvidLoc:]
    return bvs


def time_check(into):
    if not into.find('d') == -1:
        before = int(into[0:into.find('d')]) * 86400
        return before
    elif not into.find('h') == -1:
        before = int(into[0:into.find('h')]) * 3600
        return before
    elif not into.find('m') == -1:
        before = int(into[0:into.find('m')]) * 60
        return before
    elif not into.find('s') == -1:
        before = int(into[0:into.find('s')])
        return before
    elif into.isdigit():
        before = int(into)
        return before
    return -1


readytxt = open('Viewed.txt', 'a')
readytxt.close()

while scan('json') == 'None':
    Login.login_code()
filename = scan('json')

into = input('需要将多久以前的视频添加到列表？: ')

while time_check(into) == -1:
    print('请重新输入时间(纯数字或者数字+d/h/m/s)', end=': ')
    into = input()

endDate = int(time.time()) - time_check(into)

print('以页数为单位，在' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(endDate)) + '左右前的视频有: ')

session = requests.session()
with open(filename, 'r', encoding='UTF-8') as f:
    cookies = json.load(f)
UID = cookies['DedeUserID']

bvs = list_maker()


# bvs =   # 手动添加列表


def augment_list(Lis):
    count = 0
    for i in range(0, len(Lis)):
        if not i == len(Lis) - 1:
            print(Lis[i], end=", ")
            count = count + 1
        else:
            print(Lis[i] + '. \n')
        if count == 5:
            print('')
            count = 0


augment_list(bvs)

vieweles = session.get(
    url='https://api.bilibili.com/x/v2/history/toview',
    cookies=cookies
)


def make_newbvs():
    newlist = []
    for y in range(100 - numview, len(bvs)):
        newlist.append(bvs[y])
    print('\n')

    viewlist = []
    viewtext = vieweles.text
    while not viewtext.find('b23.tv/') == -1:
        viewlist.append(viewtext[viewtext.find('b23.tv/') + 7:viewtext.find('b23.tv/') + 19])
        viewtext = viewtext[viewtext.find('b23.tv/') + 7:]
    for viewing in viewlist:
        if viewing in newlist:
            newlist.remove(viewing)

    print(newlist)
    print('\n去掉重复视频之后，以上是未添加到稍后再看的包含' + str(len(newlist)) + '个视频的列表，请按需复制')
    print('稍后再看列表已满')
    return newlist


alreadyview = []
for eachline in open('Viewed.txt', 'r').readlines():
    alreadyview.append(eachline)
for vvdd in alreadyview:
    vvdd = vvdd.replace('\n', '')
    if vvdd in bvs:
        bvs.remove(vvdd)

numview = len(re.findall('b23.tv', vieweles.text))
print('去掉已观看的视频，在此期间一共有' + str(len(bvs)) + '个视频')
print('您的稍后再看列表内有' + str(numview) + '个视频')

if numview < 100:
    if input('是否要添加' + str(100 - numview) + '个视频到稍后再看(y/n)：') == 'y':
        if len(bvs) <= 100 - numview:
            for bv in bvs:
                response = session.post(
                    url='http://api.bilibili.com/x/v2/history/toview/add',
                    cookies=cookies,
                    data={
                        'bvid': bv,
                        'csrf': cookies['bili_jct']})
        else:
            for x in range(0, 100 - numview):
                response = session.post(
                    url='http://api.bilibili.com/x/v2/history/toview/add',
                    cookies=cookies,
                    data={
                        'bvid': bvs[x],
                        'csrf': cookies['bili_jct']})
            newbvs = make_newbvs()

        code = response.headers['Bili-Status-Code']
        if code == '0':
            print('成功添加到稍后再看')
        elif code == '-101':
            print('账号未登录')
        elif code == '-111':
            print('csrf校验失败')
        elif code == '-400':
            print('请求错误')
        elif code == '90001':
            print('列表已满')
        elif code == '90003':
            print('稿件已被删除')
        else:
            print('未知错误 错误代码: ' + code)
else:
    newbvs = make_newbvs()

vieweles = session.get(
    url='https://api.bilibili.com/x/v2/history/toview',
    cookies=cookies
)
viewedlist_for_CVd = []
viewtext_for_CVd = vieweles.text
while not viewtext_for_CVd.find('b23.tv/') == -1:
    viewedlist_for_CVd.append(
        viewtext_for_CVd[viewtext_for_CVd.find('b23.tv/') + 7:viewtext_for_CVd.find('b23.tv/') + 19])
    viewtext_for_CVd = viewtext_for_CVd[viewtext_for_CVd.find('b23.tv/') + 7:]

checklist = []
getinto = open('Viewed.txt', 'a')
if not len(open('Viewed.txt', 'r').readlines()) == 0:
    for line in open('Viewed.txt', 'r').readlines():
        checklist.append(line)
for check in checklist:
    check = check.replace('\n', '')
    if check in viewedlist_for_CVd:
        viewedlist_for_CVd.remove(check)
for viewed in viewedlist_for_CVd:
    getinto.write(viewed + '\n')
getinto.close()

print('请保管好Viewed.txt文件')
print('程序已结束')
