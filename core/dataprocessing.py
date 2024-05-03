from re import search,S
import core,json
def data_replace(receiveData:str) -> str:   
  # 下载网页源代码 
  # with open(f'{core.thisPath}/2.html','w',encoding='utf-8') as f:
  #   f.write(ResQ)
  ResQ=receiveData.replace('\\u0026','&').replace('\\"','"')
  nonce=search('nonce=(\S*?)/>',ResQ,S).group(1)
  script_str=search(f'<script nonce={nonce} >self.__pace_f.push\(\[1,\"c:\[\"\$\",\"\$L12\",null,(.*?)\]\\\\n\"\]\)</script>',ResQ,S).group(1)
  script_str=script_str.replace('\\','')  
  #写入数据json文件
  # with open(f'{core.thisPath}/2.json','w',encoding='utf-8') as f:
  #   f.write(script_str)

  rept={'"[':'[',']"':']','"{':'{','}"':'}'}
  for k,v in rept.items():
      script_str=script_str.replace(k,v)
  return script_str