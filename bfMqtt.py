#巴法物联
import time
from simple import MQTTClient
from urequests import get 
class  bfmq:

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
    self.online=0


  #MQQT 连接    
  def connect(self):
    try:
      if not self.c.connect(clean_session=False):
              self.c.subscribe(self.subtopic)
              self.online=1
    except:
      self.online=0
  #mqtt 信息轮询

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
        print("Ping")
    except OSError as e:
        print(e)
        self.connect()

  #mqtt 发布消息
  def publish(self,dict): 
      try:   
        self.c.publish(self.pubtopic,dict)
      except OSError as e:
        print(e)


















