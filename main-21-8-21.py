from machine import Pin, UART,Timer,reset

import bfMqtt,lib,os,time,network
from httpServer import http

def setFile(s=0):
      print("[Restart]:counter is running",type(s)      )
      file="setWifi.py"
      try:
        f=open(file,"r")
        num=int(f.read())
      except:
        f=open(file,"w")
        f.write("1")
        f.flush()
        f.close()        
        return 1
      del f
      if s=="read":
        return num
      f=open(file,"w")
      int_1= str(0) if type(s).__name__=="Timer"  else (str(1+int(num)))
      f.write(int_1)
      f.flush()
      f.close()
      print("[Restart] counter set: ",int_1)
      return int(int_1)


def wifi_setup(url):

        if url =="/":
          serv.sendall('<form action="wifi">SSD:<br><input type="text" name="ssd" value=""><br>PASSWORD<br><input type="text" name="pwd" value=""><br<br><input type="submit" value="Submit"></form> ')
          serv.sendall('<hr/>')
          ap_list=lib.wifi()[0].scan()

          for i in ap_list:
            #conn.sendall("<tr><td>%s</td><td>%d</td><tr/>"%(i[0].decode(),i[3]))
            serv.sendall("%s ,%d<br/>"%(i[0].decode(),i[3]))
          #conn.sendall(html)
        if url.find("/wifi")!=-1:
            d=(serv.get_Args(url))
            print(d)
            if d.get("ssd") !=None and d.get("pwd")!=None:
              conf="ssd='%s'\r\npwd='%s'"%(d.get("ssd"),d.get("pwd"))
              wc=open("wifi_info.py","wb")
              wc.write(conf)
              wc.flush()
              wc.close()
              serv.send("\r\n") 
              serv.send("设置成功，即将重启。")
              time.sleep(3)
              reset()
        else:
         serv.send("666 \r\n")




print("重启次数：",setFile("read"))

tim=Timer(-1)     
tim.init(period=5000, mode=Timer.ONE_SHOT, callback=setFile)

if setFile("read") >=3:
    lib.ap("My_Light")
    setFile(tim)
    lib.pin(12,1)
    lib.pin(13,1)
    lib.pin(15,1)
    serv=http("192.168.4.1",80)
    while 1:
      serv.http(wifi_setup)    



setFile()
 
try:
  import wifi_info
  ssd=wifi_info.ssd
  pwd=wifi_info.pwd
except:
  ssd=''
  pwd=''

lib.pin(12,0)
lib.pin(13,1)
lib.pin(15,0)
wifi=lib.wifi(ssd,pwd)[0]


def p_data(x,y):
  print(x,y)



  

bfMqtt.DEBUG=1
c=bfMqtt.mq("d023980739a4c6d611f59b9e351b791c",p_data,"light002")
c.connect()

light=bfMqtt.mq("d023980739a4c6d611f59b9e351b791c",p_data,"ac005")
light.connect()
uart = UART(0)
lib.pin(13,0)


_time1=0
while 1:  
  if  not wifi.isconnected():
      if (time.ticks_ms()-_time1)>150:
        lib.pin(15)
        _time1=time.ticks_ms()
      continue
    
  if (time.ticks_ms()-_time1)>500:
    lib.pin(13)
    _time1=time.ticks_ms()
  if c.online:
    dely_time=40
    lib.pin(15,0)
    lib.pin(12,1)
  else:
    dely_time=2
    lib.pin(12,0)
    lib.pin(15,1)
  if time.time()%dely_time==0:
    c.ping()
    time.sleep(1)
  c.check_msg()
  light.check_msg()
  if uart.any():
      a=uart.read()
      print(a)   










