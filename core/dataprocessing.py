from re import search,findall,S
import core,json
def data_replace(receiveData:str) -> str:
  # 下载网页源代码 
  # with open(f'{core.thisPath}/2.html','w',encoding='utf-8') as f:
  #   f.write(receiveData)
  nonce=search('nonce=(\S*?)/>',receiveData,S).group(1)
  scriData=findall(f'<script nonce={nonce} >self.__pace_f.push\((.*?)\)</script>',receiveData,S)
  script_str=json.loads(scriData[len(scriData)-1])
  script_str=json.loads(script_str[1].split(':',1)[1])
  script_str=json.dumps(script_str[3])

  return script_str