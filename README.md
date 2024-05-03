# 抖音直播录制

### 文件说明：0.0.3协程gevent_joinall.py  程序运行入口
        config.ini视频录制保存位置配置文件，如需要可以自行更改
        douyin_log.log 程序运行时记录的日志
### FFmgeg使用
        考虑到github文件下载缓慢，导致下载不成功，故已删除ffmepg.exe，ffplay.exe文件，运行文件时需要自行下载这两个对应两个对应文件并手动放到ffmpeg文件夹中，否则无法录制视频和实时观看直播
        FFmpeg官网下载地址：https://ffmpeg.org/download.html
基于python的抖音录制
说明：
1.  手机直播共享地址，如  王涛：https://v.douyin.com/2EQRjy2/
    电脑地址:https://live.douyin.com/47142496403
    粘贴到MonitoringAddress.json里，注意：每行只能添加一个地址，地址前需要添加备注名,并以:分隔,如下：
    XX:https://live.douyin.com/12346
    不需要监控的地址:前面以// 以注释
    程序在运动时，MonitoringAddress.jsonm内容支持动态更改，无需重新运行程序
    不要问我会为什么要用.json命名，问就是为VScode快捷键方便注释掉不需要监控的地址，这种存放监控地址方式只在暂时使用，后期随着程序的完善会被遗弃！
2.  只录制指定的主播,指定方式详请查看入口文件0.0.3协程gevent_joinall.py 第67行代码
    只观看不录制，请注释掉core/getRoom.py文件 第192行


安装包 pip install subprocess loguru requests
gevent subprocess 
观看实时直播需要安装 pip install screeninfo 用于获取你屏幕尺寸，计算出直播窗口所在位置
如安装库缓慢：可以先下载‘自动添加阿里镜像站.py’,运行将会为你自动阿里镜像地址，再次运行将会删除阿里镜像地址

