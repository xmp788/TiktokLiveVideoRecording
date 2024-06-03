require('./douyin.js');

pr = 'device_platform=webapp&aid=6383&channel=channel_pc_web&publish_video_strategy_type=2&source=channel_pc_web&sec_user_id=MS4wLjABAAAAfaAILjgxb3bfpSKseKSTQ1_SLv8MmOcqLrrI8keR8eLaL5unRuVNh1ODtDVz9aZ4&personal_center_strategy=1&pc_client_type=1&version_code=170400&version_name=17.4.0&cookie_enabled=true&screen_width=1920&screen_height=1080&browser_language=zh-CN&browser_platform=Win32&browser_name=Chrome&browser_version=124.0.0.0&browser_online=true&engine_name=Blink&engine_version=124.0.0.0&os_name=Windows&os_version=10&cpu_core_num=12&device_memory=8&platform=PC&downlink=10&effective_type=4g&round_trip_time=50&webid=7351336382603920896';
let ab = maping.get_a_bogus(pr);
console.log((new Date()).getSeconds(),'a_bogus:::',ab.length,ab);