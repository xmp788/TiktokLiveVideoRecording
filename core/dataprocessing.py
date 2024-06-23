from re import search,findall,S
# import core,json
import json
def data_replace(receiveData:str) -> str:
  # 下载网页源代码 
  # with open(f'{core.thisPath}/2.html','w',encoding='utf-8') as f:
  #   f.write(receiveData)
  nonce=search('nonce=(\S*?)/>',receiveData,S).group(1)
  scriData=findall(f'<script nonce={nonce} >self.__pace_f.push\((.*?)\)</script>',receiveData,S)
  for i in range(1,len(scriData)):
    script_str=json.loads(scriData[len(scriData)-i])
    script_str=script_str[1].split(':',1)[1]
    if script_str[0]!='[':
      continue
    else:
      break
  # 以下三行，调试代码用  
  script_str=json.loads(script_str)
  script_str=json.dumps(script_str[3])# 下载数据  
  return script_str
if __name__=='__main__':
  from pathlib import Path
  with open(f'{Path(__file__).parent.parent}/11.网工培训.html','r',encoding='utf-8') as f:
      data=f.read()
  
  print(data_replace(data))