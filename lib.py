
import  urequests
import network
from machine import Pin, PWM ,RTC,Timer
import time,dht,machine,ujson,ntptime,sys




#测温度
def dhts(pin,dh=11):
  if dh==11:
    d=dht.DHT11(machine.Pin(pin))
  if dh==22:
    d=dht.DHT22(machine.Pin(pin))
  a=[]
  try:
      d.measure() 
      time.sleep(0.5)
      #print ("---------------------")
      #print ("温度", d.temperature() )
      #print ("湿度" ,d.humidity())
      a=[d.temperature(),d.humidity()]
    #except OSError as e:
  except Exception as e:
       #print ("出错")
       a=['err','err']
       pass
  return a




def ap(ssd,pwd=''):
    AP= network.WLAN(network.AP_IF)
    if ssd=='':
      AP.active(0)
      return (AP,True)
    try:
      AP.active(1)
      AP.config(essid=ssd, authmode=network.AUTH_WPA_WPA2_PSK, password=pwd) if pwd != '' else AP.config(essid=ssd, authmode=network.AUTH_OPEN)
      return (AP,True)
    except Exception as e:
      print (e)
      return (AP,False)
      
def file(file,c=''):
    if c=='':
      try:
        f=open(file,"r")
        return f.read()
      except Exception as e:
        print(e,"文件不存在")
        return False
    else:
      f=open(file,"w")
      f.write(c)
      f.flush()
      f.close()
      
class flashLed:
    def __init__(self,pin):
      self.pin=Pin(pin,Pin.OUT)
      self.delay=250
      self._time1=time.ticks_ms()
      self.period=1
      self.freq=100
      self.max=1022
      self.duty=self.max      
    def sw(self,s=2,delay=250):
      if type(s).__name__=="Timer" or s==2:
        if (time.ticks_ms()- self._time1)>self.delay:
          self.delay= self.delay if delay==250  else delay
          self.pin.value(0) if self.pin.value() else self.pin.value(1)
          self._time1=time.ticks_ms()
      if s==1:
        self.pin.value(1)
        return
      if s==0:
        self.pin.value(0)
        return
      if s=="":
        return self.pin.value()        
      
    def flash(self,delay=250):
        self.delay=delay
        self.timer(self.sw)
        return
    def stop(self):
        try:
          self.tim.deinit()
          del self.tim
        except:
          pass
        try:
          time.sleep_ms(50)
          self.pwm.deinit()
        except:
          pass 
        self.pin.init(Pin.OUT)

        return
    def timer(self,cb):
        self.tim=Timer(-1)  
        self.tim.init(period=self.period, mode=Timer.PERIODIC, callback=cb)
    def bre(self,loop=1,step=1):
        self.step=step
        if loop==1:
          self.stop()
          self.timer(self.repat)
        if loop==0:
          self.repat()
        return  
    def repat(self,s=1):
        self.pwm = PWM(self.pin)
        self.duty=self.duty-self.step
        if self.duty< -self.max:
           self.duty=self.max
        self.pwm.init(freq=self.freq, duty=abs(self.duty))
        return




def update_time():

      ntptime.host='ntp1.aliyun.com'
      try:
        ntptime.settime()
      except:
        print("TIME UPGRADE FAILED")
        return
      list=time.localtime(time.time()+8*60*60)
      rtc = RTC()
      rtc.datetime((list[0], list[1], list[2] ,None,list[3], list[4], list[5] ,0)) 
      print (rtc.datetime())

def wifi(ssd='',pwd='',hostname="MicroPython"):
      wifi0 = network.WLAN(network.STA_IF)
      wifi0.active(1)  
      if ssd=='':
        return (wifi0,'')
      wifi0.active(True) #激活WIFI
      # 启用mdns
      wifi0.config(dhcp_hostname=hostname,mac=wifi0.config('mac'))
      wifi0.disconnect()
      _s_time=time.time()
      if not wifi0.isconnected(): #判断WIFI连接状态

          print('[WIFI]:Connect to',ssd)

          wifi0.connect(ssd, pwd) #essid为WIFI名称,password为WIFI密码

          while not wifi0.isconnected():

            if (time.time()- _s_time)>5:

              print('[WIFI]:Connect Faied')
              return (wifi0,False)
    
      print('[WIFI]:', wifi0.ifconfig())
      return (wifi0,True)

class btn:
  
  def __init__(self,p):
    self.time_ms=time.ticks_ms
    self.time=0
    self._btn=Pin(p,Pin.IN)
    self.diff_time=0
    self.timer=-999
    self.press_time=400 #长按最小时间
    self.click_time=80 #单击最小时间
    self._btn.irq(handler=self.FALLING,trigger=(Pin.IRQ_FALLING))
    tim=Timer(self.timer)     
    tim.init(period=1, mode=Timer.PERIODIC, callback=self.check)     
    self.cb_press=None
    self.cb_click=None
    self.isNotRising=1
    

  def FALLING(self,_e=0):
      self.isNotRising=1
      self.time=self.time_ms()
      self._btn.irq(handler=self.RISING,trigger=(Pin.IRQ_RISING))
      

  def RISING(self,_e=0):
      self.isNotRising=0
      tmp=self.time_ms()-self.time
      if tmp<self.click_time:
        return
      self.diff_time=tmp
      self._btn.irq(handler=self.FALLING,trigger=(Pin.IRQ_FALLING))
  
  def press(self,cb,s=0):
      self.cb_press=cb
      self.press_time= self.press_time if s==0 else s
      
  def click(self,cb):
      self.cb_click=cb
  def check(self,_e=0):
      if self.time==0:
        return
      realTime=self.time_ms()
      if realTime-self.time>self.press_time and self.isNotRising==1:
          print("press")
          if self.cb_press.__class__.__name__ != 'NoneType':
            self.cb_press()
          self.time=0
          return

      if self.diff_time >self.click_time and self.isNotRising==0:
        print("click")
        if self.cb_click.__class__.__name__ != 'NoneType':
          self.cb_click()
        self.time=0
        return  
        


















