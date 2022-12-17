import json
import time
from bs4 import BeautifulSoup
from const import headers, url
from utils.sessions import Sessions
from utils.times import is_between, stamp2time
from config import configs
from openpyxl import Workbook


# 初始化session
def init(Session):
    session = Session()
    session.headers['User-Agent'] = headers.UserAgent
    session.headers['Cookie'] = headers.Cookies
    return session


# 获取用户信息
def grab_user_id(session):
    print("Start grabbing user info....")
    user_name = configs['UserName']
    print('Username : ' + user_name)
    link = url.HomePage + user_name + '?lang=en'
    soup = BeautifulSoup(session.get(link).content, 'html.parser')
    info = json.loads(soup.find('script', id="SIGI_STATE").text)
    user_info = info['UserModule']['users'][user_name]
    id = user_info['id']
    print('User ID : ' + id)
    print("Grabbing user info finished")
    return id


# 获取当前用户的所有视频
def grab_video_list(session, max_cursor, uid):
    params = {
        'count': '50',
        'maxCursor': max_cursor,
        'minCursor': '0',
        'sourceType': '8',
        'id': uid
    }
    response = session.get(url.VideosAPI, params=params).json()
    is_has_more = response['hasMore']
    max_cursor = response['maxCursor']
    videos = response['items']
    videos_data = []
    for video in videos:
        desc = video['desc']
        stats = video['stats']
        timeStamp = video['createTime']
        duration = video['video']['duration']
        # 根据需求过滤部分视频
        if filter_video(timeStamp):
            item = {'desc': desc, 'stats': stats, 'timeStamp': timeStamp, 'duration': duration}
            print("Successfully grabbing video ", item)
            videos_data.append(item)
    if is_has_more:
        # 暂停执行5秒，以免被后台检测到是爬虫程序
        time.sleep(5)
        videos_data.extend(grab_video_list(session, max_cursor, uid))
    return videos_data


# 根据需求来过滤当前爬取的视频信息,如视频数据、创建时间、视频时长、tags等
# 当前仅根据时间进行过滤
def filter_video(stamp):
    begin_time = configs['StartTime']
    end_time = configs['EndTime']
    return is_between(begin_time, end_time, stamp)


# 将爬取的源信息转换为目标格式
# 播放量 点赞数 评论数 发布日期 视频时长 标签
def format_video_info(info):
    playCount = info['stats']['playCount']
    diggCount = info['stats']['diggCount']
    commentCount = info['stats']['commentCount']
    createTime = stamp2time(info['timeStamp'])
    duration = info['duration']
    descArr = info['desc'].split("#")
    title = descArr[0]
    res = [title.strip(), playCount, diggCount, commentCount, createTime, duration]
    tags = descArr[1:]
    for i in range(0, len(tags)):
        res.append(tags[i].strip())
    return res


def gen_output(videos):
    user_name = configs['UserName']
    workbook = Workbook()
    worksheet = workbook.active
    worksheet.title = user_name
    worksheet.append(['名称', '播放量', '点赞数', '评论数', '发布时间', '视频时长', '标签组'])
    for v in videos:
        worksheet.append(format_video_info(v))
    file_name = user_name + '-videos.xlsx'
    workbook.save(file_name)
    print("Success! Save as " + file_name)


if __name__ == "__main__":
    session = init(Sessions)
    # 获取用户信息
    user_id = grab_user_id(session)
    time.sleep(5)
    print("Start grabbing user video....")
    # 获取视频信息列表
    videos = grab_video_list(session, 0, user_id)
    print("Grabbing user video finished")
    # 写入文件系统
    print("Write video info to excel file...")
    gen_output(videos)
    pass
