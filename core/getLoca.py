import json,requests,execjs,urllib.parse,time
from pathlib import Path

import requests.cookies
thisPath=Path(__file__).parent
# print(str(thisPath))

cookies = {
  'bd_ticket_guard_client_web_domain':'2',
  'passport_assist_user':'Cjxh6CMxuKu-cG8lXSwLqNdq37RJeG4gRfHZYevHLLtXdC_3anQ9U3SAZLEHxgwStsfg_eBShAR5panHcIcaSgo8HDpXS39YFISWgNgDGZan-E1BY3j9AXnICrmirRzohmEDgjOFzGRUd2wB0LOS82WrUWtN_H09LJZcQDp2EMSayg0Yia_WVCABIgEDAJoCnA%3D%3D',
  'n_mh':'21rDZZlxi9dPTf-KRNadD5AbiDmnAmDVeN9YX4lfhds',
  'sso_uid_tt':'8f9c10b24ef57d3d33a42d1a85d0b64a',
  'sso_uid_tt_ss':'8f9c10b24ef57d3d33a42d1a85d0b64a',
  'toutiao_sso_user':'c8b6f6ce3494433d5f46cd8369906417',
  'toutiao_sso_user_ss':'c8b6f6ce3494433d5f46cd8369906417',
  'uid_tt':'3dd5e8ed5bc29eb9370e63a484cd2ff1',
  'uid_tt_ss':'3dd5e8ed5bc29eb9370e63a484cd2ff1',
  'sid_tt':'715a9dedec61766fb52b54e646f7ad17',
  'sessionid':'715a9dedec61766fb52b54e646f7ad17',
  'sessionid_ss':'715a9dedec61766fb52b54e646f7ad17',
  'LOGIN_STATUS':'1',
  'store-region':'cn-sc',
  'store-region-src':'uid',
  '_bd_ticket_crypt_cookie':'7d8d0ea76b669abc151ec6e11b2c8ba6',
  'my_rd':'2',
  'live_use_vvc':'%22false%22',
  'xgplayer_device_id':'4926664672',
  'xgplayer_user_id':'33185018430',
  'SEARCH_RESULT_LIST_TYPE':'%22single%22',
  'ttwid':'1%7CZhMQ8frEtQd8Is3QGpf47m3YmukCIkbOhVc3uml_edA%7C1713163799%7C8c77f7ed9454d7de50ce61ec0143181e7c1c12f9ebdfbc62d3754dd241555560',
  'sid_ucp_sso_v1':'1.0.0-KDU3YjI5MjVlZjY4YmYzNzQyZGRjNTZiZmU3NjUxZGI4OTgwOTNiYWQKHQjbgPTG9AEQlKmcsgYY7zEgDDCzoKvMBTgGQPQHGgJsZiIgYzhiNmY2Y2UzNDk0NDMzZDVmNDZjZDgzNjk5MDY0MTc',
  'ssid_ucp_sso_v1':'1.0.0-KDU3YjI5MjVlZjY4YmYzNzQyZGRjNTZiZmU3NjUxZGI4OTgwOTNiYWQKHQjbgPTG9AEQlKmcsgYY7zEgDDCzoKvMBTgGQPQHGgJsZiIgYzhiNmY2Y2UzNDk0NDMzZDVmNDZjZDgzNjk5MDY0MTc',
  'sid_guard':'715a9dedec61766fb52b54e646f7ad17%7C1715934356%7C5184000%7CTue%2C+16-Jul-2024+08%3A25%3A56+GMT',
  'sid_ucp_v1':'1.0.0-KDRhNGZlMTAzZWU2ZGRhNjRkMzgzNzBlZDI3MDI5MDJkYjBiYjk1NjEKGQjbgPTG9AEQlKmcsgYY7zEgDDgGQPQHSAQaAmhsIiA3MTVhOWRlZGVjNjE3NjZmYjUyYjU0ZTY0NmY3YWQxNw',
  'ssid_ucp_v1':'1.0.0-KDRhNGZlMTAzZWU2ZGRhNjRkMzgzNzBlZDI3MDI5MDJkYjBiYjk1NjEKGQjbgPTG9AEQlKmcsgYY7zEgDDgGQPQHSAQaAmhsIiA3MTVhOWRlZGVjNjE3NjZmYjUyYjU0ZTY0NmY3YWQxNw',
  'dy_swidth':'1920',
  'dy_sheight':'1080',
  'passport_csrf_token':'8d148cba65e6ac6a1c449fa4cd41c040',
  'passport_csrf_token_default':'8d148cba65e6ac6a1c449fa4cd41c040',
  's_v_web_id':'verify_lwhjxx53_aIQ5qylc_Att1_4Ajq_AWDF_ilNEUuN0fEQl',
  '__live_version__':'%221.1.2.363%22',
  'publish_badge_show_info':'%220%2C0%2C0%2C1716617232836%22',
  'stream_player_status_params':'%22%7B%5C%22is_auto_play%5C%22%3A0%2C%5C%22is_full_screen%5C%22%3A0%2C%5C%22is_full_webscreen%5C%22%3A0%2C%5C%22is_mute%5C%22%3A0%2C%5C%22is_speed%5C%22%3A2%2C%5C%22is_visible%5C%22%3A0%7D%22',
  'pwa2':'%220%7C0%7C1%7C1%22',
  'live_can_add_dy_2_desktop':'%221%22',
  # '__ac_nonce':'06659806800e383929dd',
  # '__ac_signature':'_02B4Z6wo00f01lCFKfwAAIDBbSwzYOPiCsZQpS1AAPKHG0Zouw5bT0sHmUlSKx728kGwte5cgNvErMWyguJgnbWgHY5TGaeVuoGqhnSSw7WNWXXfhRDqNSO.eotxgF6CuTmkMil8Z9-hrlS6d8',
  'csrf_session_id':'7e208183356eef6c131aa236de5528a1',
  'strategyABtestKey':'%221717141610.705%22',
  'FOLLOW_LIVE_POINT_INFO':'%22MS4wLjABAAAAPsBt-ZfP-HxTq4vm8EheI1xRNPeRK85VeDc3E_fm_IM%2F1717171200000%2F0%2F0%2F1717142372884%22',
  'FOLLOW_NUMBER_YELLOW_POINT_INFO':'%22MS4wLjABAAAAPsBt-ZfP-HxTq4vm8EheI1xRNPeRK85VeDc3E_fm_IM%2F1717171200000%2F0%2F1717141772885%2F0%22',
  'WallpaperGuide':'%7B%22showTime%22%3A0%2C%22closeTime%22%3A0%2C%22showCount%22%3A0%2C%22cursor1%22%3A7%2C%22cursor2%22%3A0%7D',
  # 'msToken':'e065ZTk-w05_Ep-LFA46o98g-YQ8LAx6YucToB8IwoH92ycfiF9obibVjkiBzYHf0gn0iJs_wdzTCvSjjvv8hoSqNdr92mhqH5p6TT5vO7on6mk8_hSksHrXZi0=',
  'bd_ticket_guard_client_data':'eyJiZC10aWNrZXQtZ3VhcmQtdmVyc2lvbiI6MiwiYmQtdGlja2V0LWd1YXJkLWl0ZXJhdGlvbi12ZXJzaW9uIjoxLCJiZC10aWNrZXQtZ3VhcmQtcmVlLXB1YmxpYy1rZXkiOiJCS0kvUlNQcmd0aEI0VHpQN0JaTTF5R2oxZlRndEs5TFVpTXNvaGZaRm1SRzhkcXJsYkdiMnd6YjJJWnJnSG1sdXFOMDhQYTNwVXcxRDNUQWoxZ2dIbGs9IiwiYmQtdGlja2V0LWd1YXJkLXdlYi12ZXJzaW9uIjoxfQ%3D%3D',
  'passport_fe_beating_status':'true',
  'odin_tt':'b564ba5dfb76e75a7cd37d69f9b58bdb2e53ed396065cb1b9d234556d22683f6cb660b586ab35dedacb3bad3db1cbeaf',
  'IsDouyinActive':'true',
  'home_can_add_dy_2_desktop':'%220%22',
  'stream_recommend_feed_params':'%22%7B%5C%22cookie_enabled%5C%22%3Atrue%2C%5C%22screen_width%5C%22%3A1920%2C%5C%22screen_height%5C%22%3A1080%2C%5C%22browser_online%5C%22%3Atrue%2C%5C%22cpu_core_num%5C%22%3A12%2C%5C%22device_memory%5C%22%3A8%2C%5C%22downlink%5C%22%3A10%2C%5C%22effective_type%5C%22%3A%5C%224g%5C%22%2C%5C%22round_trip_time%5C%22%3A50%7D%22',
}

headers = {
  'authority':'www.douyin.com',
  'accept':'application/json, text/plain, */*',
  'accept-language':'zh-CN,zh;q=0.9',
  'cache-control':'no-cache',
  'pragma':'no-cache',
  'referer':'',
  'sec-ch-ua':'"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
  'sec-ch-ua-mobile':'?0',
  'sec-ch-ua-platform':'"Windows"',
  'sec-fetch-dest':'empty',
  'sec-fetch-mode':'cors',
  'sec-fetch-site':'same-origin',
  'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.6261.95 Safari/537.36',
}

params = {
  'device_platform':'webapp',
  'aid':'6383',
  'channel':'channel_pc_web',
  'sec_user_id':'',
  'max_cursor':'0',
  'locate_query':'false',
  'show_live_replay_strategy':'1',
  'need_time_list':'1',
  'time_list_query':'0',
  'whale_cut_token':'',
  'cut_version':'1',
  'count':'18',
  'publish_video_strategy_type':'2',
  'update_version_code':'170400',
  'pc_client_type':'1',
  'version_code':'290100',
  'version_name':'29.1.0',
  'cookie_enabled':'true',
  'screen_width':'1920',
  'screen_height':'1080',
  'browser_language':'zh-CN',
  'browser_platform':'Win32',
  'browser_name':'Chrome',
  'browser_version':'122.0.6261.95',
  'browser_online':'true',
  'engine_name':'Blink',
  'engine_version':'122.0.6261.95',
  'os_name':'Windows',
  'os_version':'10',
  'cpu_core_num':'12',
  'device_memory':'8',
  'platform':'PC',
  'downlink':'10',
  'effective_type':'4g',
  'round_trip_time':'50',
  'webid':'7317544860285077002',
  # 'webid':'7351336382603920896',
  'msToken':'cDSIK2Rb3k7Bm7Q6ZpaX06vARgWDFbtwKN4DCh6id_QNY4trWVOefokRxkQNVzJ5klLMlxZkHYwDLCgg0u1xQaisz7d2na3scyW1CzXibzTFfs1f_DriGUaQDuw=',
  'a_bogus':'',
}

def getIP(sec_user_id,webid='7351336382603920896'):

  URL={
    'url':'https://www.douyin.com',
    # 'interface':'/aweme/v1/web/user/profile/other/',
    'interface':'/aweme/v1/web/aweme/post/'
  }

  headers['referer']=f'https://www.douyin.com/user/{sec_user_id}'
  params['sec_user_id']=sec_user_id
  # cookie.update({
  #   '__ac_nonce':ac_nonce,
  #   '__ac_signature':''
  #   'msToken': c_msToken,
  # })
  # param.update({'webid': webid})
  temp=params.copy()
  del temp['a_bogus']
  params_str=urllib.parse.urlencode(temp)
  del temp
  with open(f'{thisPath}/cd_crypt/douyin.js','r',encoding='utf-8') as f:
    jsCode=f.read()
  cJS=execjs.compile(jsCode)
  a_bogus=cJS.call('maping.get_a_bogus',params_str,str(thisPath),headers['user-agent'])
  # print('a_bogus:::',len(a_bogus),a_bogus)
  # return
  params['a_bogus']=a_bogus

  try:
    res=requests.get(url=''.join(URL.values()),params=params,cookies=cookies,headers=headers,timeout=(1.01,3.05))
  except requests.exceptions.ReadTimeout:
    print("读取超时")
  except requests.exceptions.ConnectionError:
    print("连接出错")
  dic_js={}
  try:
    js=res.json()
    dic_js.update({
      'unique_id':js['user']['unique_id'],# 抖音号
      'nickname':js['user']['nickname'],
      'room_id':js['user']['room_id']
    })
    dic_js.update({
      'ip_location':js['user']['ip_location'],
    })
  except Exception as er:
    dic_js['ip_location']='未知'
  return dic_js['ip_location']
  print(dic_js)
if __name__=='__main__':  
  secID=[
        'MS4wLjABAAAAwmjUqpKJzLGaIkqH7AMto2F2tuAjr3uQrNsHglixehKj7i5Nys8UYieBdkp3kTFH',
        'MS4wLjABAAAAwAoxqI2jLgowIx636DPxKnufLktI0miAKYeAnmoQeq_jslDqxrHL7ByUcOd16HZE',
        'MS4wLjABAAAAfaAILjgxb3bfpSKseKSTQ1_SLv8MmOcqLrrI8keR8eLaL5unRuVNh1ODtDVz9aZ4'
        ]
  for i in range(len(secID)):
    print(getIP(secID[i]))
    # pass