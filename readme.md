# TikTok爬虫程序

## 基本需求
获取指定账号在指定时间段内的全部视频信息，并导出为Excel格式的文件

支持获取的视频信息字段：

- 播放量 playCount
- 点赞数 diggCount
- 评论数 commentCount
- 标签标题 title
- 发布日期 createTime
- 视频时长 duration
- 标签组 tags

## 使用文档
1. 使用 requirements.txt 安装依赖
   ```shell
   # 进入当前项目根目录，输入以下代码
    pip install -r requirements.txt
    ```
2. 修改默认配置：`config.py`文件包含了项目的配置信息：
   - `UserName` [必选字段]指定用户的用户名，如`https://www.tiktok.com/@wholepotato` 的用户名为`wholepotato`
   - `StartTime` [可选字段]指定待获取视频的起始时间
   - `EndTime` [可选字段]指定待获取视频的结束时间
3. 运行代码，最终将该用户的视频信息保存至 `username-videos.xlsx`文件中
