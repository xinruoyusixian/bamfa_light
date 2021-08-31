
#巴法物联
import time
from simple import MQTTClient
from urequests import get 
DEBUG=0

def log(arg1, *vartuple):
    # timeInfo = time.strftime("%H:%M:%S %Y", time.localtime())
    if DEBUG== False :
        return
    data = str(arg1)
    for var in vartuple:
        data = data + str(var)
    data = '[' + str(millis()) + '] ' + data
    print(data)


os_time_start = time.ticks_ms()
def millis():
    return time.ticks_ms() - os_time_start

    
class  mq:

# key:私钥
#当主题名字后三位是001时为插座设备,002时为灯泡设备,003时为风扇设备,004时为传感器设备,005时为空调设备。
#cb 回调函数 例如 def cb(topic, msg):
#topic:需要带入的topic

  def __init__(self,key,cb,topic,devTpye="light"):
    self.SERVER = "bemfa.com"
    self.CLIENT_ID =  key
    self.port=9501
    self.c=MQTTClient(client_id=self.CLIENT_ID,server=self.SERVER,
    port=self.port)
    self.c.DEBUG = True
    self.c.set_callback(cb)
    self.subtopic=topic
    self.pubtopic=topic
    self.connect_count=0


  #MQQT 连接    
  def connect(self):
    log("connect:准备连接....")
    try:
      if not self.c.connect(clean_session=False):
              self.c.subscribe(self.subtopic)
              self.connect_count+=1
              self.log()
              log("新会话已连接.")
    except:
      log("检查网络或登录信息")
  #mqtt 信息轮询
  def log(self):
    if DEBUG:
      log("连接: ",self.connect_count," 次")
  def check_msg(self):
      try:
        self.c.check_msg()
        self.online=1
      except OSError as e:
        self.connect()
  #mqtt 心跳回复
  def ping(self): 
    try:
        self.c.ping()
        if DEBUG:
          print("Mqtt Ping")
    except OSError as e:
        self.connect()

  #mqtt 发布消息
  def publish(self,dict): 
      try:   
        self.c.publish(self.pubtopic,dict)
        if DEBUG:
            log ("Mqtt发送>>>>",self.pubtopic, dict)        
      except OSError as e:
        if DEBUG:
           log ("publish:",e)
        self.connect()
        
        















