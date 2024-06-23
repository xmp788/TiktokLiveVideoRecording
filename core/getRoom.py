import core,time,json
from core.dataprocessing import data_replace
from core.liveDataProcessing import LiveProcess
from core.getLoca import getIP
from re import findall,search,S
from requests import get
from loguru import logger


def netWork(url,urlparams=False,times=3):
  header={
    'User-Agent':'Mozilla/5.0 (Linux; U; Android 8.1.0; en-US; Nexus 6P Build/OPM7.181205.001) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.108 UCBrowser/12.11.1.1197 Mobile Safari/537.36'
  }
  if urlparams==True:
    resQ=get(url,headers=header,timeout=times)
    return resQ.json()
  else:
    referer='https://live.douyin.com/'
    if url.rsplit('/',1)[0]+'/'==referer:
      cookie='xgplayer_user_id=863729427626; my_rd=2; store-region=cn-sc; store-region-src=uid; LOGIN_STATUS=0; d_ticket=6bedd4c96acb25b2e1fd821601d8550ae5ce1;       odin_tt=b378d2cdff4d61108b94b5c1ed475ae92d37141b590f7d3759e07cccce7eec24715e982ea7114c9e8ba0b1db07f7a4a41193c2380369b2798fd881166957797b; live_use_vvc=%22false%22; ttwid=1%7C23y7oxbheLxknVkj_qkPsZCUhY_iv8imnJAdCYROSLU%7C1711616395%7C66f49b9b1dfae1c47deb49cbbcc192ae6695dd5b36a08f7ca1c1b00f2ee1fc99; FORCE_LOGIN=%7B%22videoConsumedRemainSeconds%22%3A180%7D; bd_ticket_guard_client_web_domain=2; passport_csrf_token=b547843d84d87635cdfc1f521a5369a0; passport_csrf_token_default=b547843d84d87635cdfc1f521a5369a0; bd_ticket_guard_client_data=eyJiZC10aWNrZXQtZ3VhcmQtdmVyc2lvbiI6MiwiYmQtdGlja2V0LWd1YXJkLWl0ZXJhdGlvbi12ZXJzaW9uIjoxLCJiZC10aWNrZXQtZ3VhcmQtcmVlLXB1YmxpYy1rZXkiOiJCQzdBaHhCaFhKclFHMitwQ0ljZngwT0krYWEyZHRqQWR5WTlkWkZCOGlEMTNya0Q4WVZOZ0MzeDB3K1F1Q3Y5cmFmcXN5V0tqNXQ5VHhPS0FVWTM2SEE9IiwiYmQtdGlja2V0LWd1YXJkLXdlYi12ZXJzaW9uIjoxfQ%3D%3D; tt_scid=.khKXzPQsc9TbS5Q7pkNEJcHCCUWej0TbNr2E8Fv1i95hPLNzkpwKw0-2UoBBN-1d390; GlobalGuideTimes=%221712482831%7C1%22; msToken=uLX-Zh9ysdqi9NT--1E5eYrNDcSEon6_96WVJuzcJ1RKwWgW9Rn3gQ1xaHZ0yy14kTC4fM7gieGE2S1o2vxKqQBFID44NevMp1jnipx7fyLwIcwoyec=; __live_version__=%221.1.1.9558%22; download_guide=%223%2F20240411%2F0%22; pwa2=%220%7C0%7C3%7C0%22; __ac_nonce=06617b7cf00fec78e3947; __ac_signature=_02B4Z6wo00f01go4t-AAAIDBN5GtfMUu5WIKGLNAAOSnTW3GyTdhEmi4jC0dcttp42hJg0R0.gkYPL.3510em8SuhrrsmSn5dZory9sZRV.LhCeZP7Rr50y0HukQqac6LvrC3mPCBJHBEDDd7d; xg_device_score=7.45813092351116; has_avx2=null; device_web_cpu_core=12; device_web_memory_size=8; csrf_session_id=67c4b7a3818a975a4dd3ea6e4132fea4; webcast_leading_last_show_time=1712830417459; webcast_leading_total_show_times=1; live_can_add_dy_2_desktop=%221%22; msToken=LVmSUWnUEOROdB1aZglaEuH3nvobbFS3qBS0__VYF3Kb2fe2sESIPIJhjIwVrlONl4P5H5x86qx6Fa1pf0r6gEeYtwNqndqTstEte1MfY9zBsvvb1c-tiySTLmrY; IsDouyinActive=false'
      header['Cookie']=cookie
      header['Referer']=referer
      header['User-Agent']='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
      resQ=get(url,headers=header,timeout=times)
      resQ.encoding='utf-8' 
      return(resQ.text,'Web',resQ.status_code)
    else:
      resQ=get(url,headers=header,timeout=times)
      return(resQ.url,'App',resQ.status_code)

def getRoomInfo(url,notes='未添加备注'):
  try:
    web_html,mark,status_code=netWork(url)
    uData=dict()
    if mark=='Web':
      script_str=data_replace(web_html)      
      # 下载网页源代码 
      # with open(f'{thisFileP}/{notes}.html','w',encoding='utf-8') as f:
      #   f.write(web_html)
      # 写入数据json文件
      # with open(f'{thisFileP}/{notes}.json','w',encoding='utf-8') as f:
      #   f.write(script_str)
      script_info=json.loads(script_str)
      webid=script_info['state']['userStore']['odin']['user_unique_id']
      room_info=script_info['state']['roomStore']['roomInfo']
      uData.update({
        'nickname':room_info['anchor']['nickname'],
        'sec_uid':room_info['anchor']['sec_uid'],
        'status':room_info['room']['status'],# 开播为2 未开播为4
        'roomId':room_info['roomId'],
        'web_rid':room_info['web_rid'],
        'city':'未知',
      })
      # uData['city']=getIP(uData['sec_uid'],webid)
        # '----------------------------------未开播以下报错-----------------------------------------'
      uData.update({
        'flv_rtmp':room_info['room']['stream_url']['flv_pull_url'].get('FULL_HD1'), # 直播流链接
        'web_flv_rtmp':room_info['web_stream_url']['flv_pull_url']['FULL_HD1'], # 直播流链接
        'total_userCount':room_info['room']['stats']['total_user_str'],#总观看人数
        'userCount':room_info['room']['stats']['user_count_str'],# 当前房间人数
        # 'userCount':roomInfo['room']['user_count_str'],# 当前房间人数
        # city:netWork2(sec_uid).split('：')[1]#开播城市
      })      
      if uData['status']==2:
        uData['Living'],uData['msg']=True,'正在直播'
      else:
        uData['Living'],uData['msg'],uData['flv_rtmp']=False,'未开播',""
    else:
      roomId=findall(r'reflow\/(\d+)\?',web_html)[0]
      live_info_url = lambda roomid:f"https://webcast.amemv.com/webcast/room/reflow/info/?type_id=0&live_id=1&room_id={roomid}&app_id=1128" 
      LiveInfoURL=live_info_url(roomId)
      resqJson=netWork(LiveInfoURL,urlparams=True)
      uData.update({
        'status':resqJson['data']['room']['status'],# 开播状态：4未开播，2开播
        # 'start_time':time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(resqJson['data']['room']['start_time'])),
        # 'create_time':time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(resqJson['data']['room']['create_time'])),# 开播时间
        # 'finish_time':time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(resqJson['data']['room']['finish_time'])),# 现在时间
        'display_id':resqJson['data']['room']['owner']['display_id'],
        'sec_uid':resqJson['data']['room']['owner']['sec_uid'],
        'web_rid':resqJson['data']['room']['owner']['web_rid'],# '308601070381'
        'webcast_uid':resqJson['data']['room']['owner']['webcast_uid'],
        'city':resqJson['data']['room']['owner']['city'],
        'location_city':resqJson['data']['room']['owner']['location_city'],
        'nickname':resqJson['data']['room']['owner']['nickname'],#主播
        'signature':resqJson['data']['room']['owner']['signature'],
        'pay_grade':resqJson['data']['room']['owner']['pay_grade'],
        'p_level':resqJson['data']['room']['owner']['pay_grade']['level'],# 财富等级
        'stats':resqJson['data']['room']['stats'],
      })
      resqJson = netWork(live_info_url(resqJson['data']['room']['owner']["own_room"]["room_ids_str"][0]),urlparams=True)        
      uData.update({
        'modify_time':time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(resqJson['data']['room']['owner']['modify_time'])),
        'follower_count':resqJson['data']['room']['owner']['follow_info']['follower_count'],
        # 'follower_count_str':resqJson['data']['room']['owner']['follow_info']['follower_count_str'],

        'is_virtual_anchor':resqJson['data']['room']['extra']['is_virtual_anchor'],
        'flv_rtmp':resqJson['data']['room']['stream_url']['rtmp_pull_url'],
        'uri':resqJson['data']['room']['cover']['uri'], # 'webcast-cover/7351568045158173490'
        'userCount':resqJson['data']['room']['user_count'],# 当前房间人数
        'total_userCount':resqJson['data']['room']['stats']['total_user'],
        # 'total_user_str':resqJson['data']['room']['stats']['total_user_str'],
        'user_count_str':resqJson['data']['room']['stats']['user_count_str'],
        
        'stream_url':resqJson['data']['room']['stream_url'],
        'user_dress_info':resqJson['data']['room']['owner']['user_dress_info'],
        'user':resqJson['data']['user'],
        'u_status':resqJson['data']['user']['status'],
        'flv_rtmp':resqJson['data']['room']['stream_url']['rtmp_pull_url'],
        # 'start_time':resqJson['data']['room']['link_mic']['battle_settings']['start_time'],
        # 'start_time_ms':resqJson['data']['room']['link_mic']['battle_settings']['start_time_ms']
      })
      # print(self_data)
      if uData['status']==4:
        uData['Living'],uData['msg']=True,'正在直播'
      else:
        uData['Living'],uData['msg'],uData['flv_rtmp']=False,'未开播',""

  except KeyError as e:
    uData['Living'],uData['msg']=False,'未开播'
  except TimeoutError as e:
    uData['Living'],uData['msg']=False,f'{type(e)}:{e}'
  except OSError as e:
    # from pathlib import Path
    # thisFileP=Path(__file__).parent.parent
    # import subprocess
    # subprocess.Popen(f'{thisFileP}/ffmpeg/ffplay.exe -nodisp -volume 100 -autoexit -i {thisFileP}/sound/notify_message.mp3')
    # uData['Living'],uData['msg']=False,'未开播'
    logger.error(f'{type(e)}:{e}')
    uData['Living'],uData['msg']=False,f'{type(e)}'
  finally:
    # uData['authorURL']=f'https://www.douyin.com/user/{uData["sec_uid"]}'
    # return uData
    try:
      uData['authorURL']=f'https://www.douyin.com/user/{uData["sec_uid"]}'
    except Exception as e:
      print(e,resqJson,sep='\n')
    finally:
      return (uData)
    
@logger.catch 
def MonitoringLive(notes,url):
  
  roomInfo=getRoomInfo(url,notes)
  # core.Public_v['Obj'][notes]['nickname']=roomInfo['nickname']
  core.Public_v['Obj'][notes].update(roomInfo)
  # 控制台输出状态信息
  # notes='：IP:'.join([notes,(roomInfo['city'].split('：')[1] if roomInfo['city'] else roomInfo['city'])])
  # return
  if roomInfo['Living']:# 判断当前主播是否开播
    print(f'{(notes+","+roomInfo["city"]):{"`"}{"<"}{10}}{roomInfo["msg"]},{roomInfo["userCount"]}/{roomInfo["total_userCount"]},{roomInfo["flv_rtmp"]}')
    # print(f'{notes:{"`"}{"<"}{10}}{roomInfo["msg"]},{roomInfo["userCount"]}/{roomInfo["total_userCount"]},{roomInfo["flv_rtmp"]}')
    # if core.Public_v['Obj'][notes]['isRecord'] or core.Public_v['Obj'][notes]['watch']:# 当前主播是否需要录制 控制程序是否需要执行后面代码
      # if core.Public_v['mode']['RecordVideo']: #判断是否启用录制模式
    info=(notes,roomInfo['nickname'],roomInfo['flv_rtmp'])# 备注，昵称，直播流
    LiveProcess(info)
  else:
    try:
      print(f'{(notes+","+roomInfo["city"]):{"`"}{"<"}{26*2}}{roomInfo["msg"]}')
    except Exception as e:
      print(e,roomInfo,sep='\n')
    # print(f'{notes:{"`"}{"<"}{26*2}}{roomInfo["msg"]}')
  return
