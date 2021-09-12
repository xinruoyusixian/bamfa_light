


import uos, machine,time,lib
import gc
import webrepl
webrepl.start()
gc.collect()
#响应按键开关
device="MPY_Light"
power=lib.flashLed(5)#开关控制引脚
p4=lib.flashLed(4)
p12=lib.flashLed(12)
btn=lib.btn(14)#按键
_cfg="cfg.py"
def led(c):
  if c=="red":
    p4.sw(0);p12.sw(1)
  if c=="blue":
    p4.sw(1);p12.sw(0)
  if c=="off":
    p4.sw(0);p12.sw(0)
led("blue")
def sw():
    power.sw()
    led("red") if power.sw('') else led("blue")
btn.click(sw)
#响应按键开关
def _reset(s=1):
    lib.file("isRset.py","4")
    machine.reset()
    
btn.press(_reset,5000)
try:
  if int(lib.file("isRset.py")) >=3:
      from httpServer import http
      def wifi_setup(url):
              if url =="/":
                serv.sendall('<form action="wifi">SSD:<br><input type="text" name="ssd" value=""><br>PASSWORD<br><input type="text" name="pwd" value=""><hr>KEY<br><input type="text" name="key" value=""><input type="submit" value="Submit"></form> ')
                serv.sendall('<hr/>')
                ap_list=lib.wifi()[0].scan()
                for i in ap_list:
                  serv.sendall("%s ,%d<br/>"%(i[0].decode(),i[3]))
              if url.find("/wifi")!=-1:
                  d=(serv.get_Args(url))
                  print(d)
                  if d.get("ssd") !=None and d.get("pwd")!=None:
                    conf="ssd='%s'\r\npwd='%s' \r\nkey='%s'"%(d.get("ssd"),d.get("pwd"),d.get("key"))
                    lib.file(_cfg,conf)
                    serv.send("\r\n") 
                    serv.send("设置成功，即将重启。")
                    time.sleep(3)
                    machine.reset()
              else:
               serv.send("666 \r\n")    
      p4.flash(100)
      p12.flash(50)
      lib.ap(device)
      lib.file("isRset.py","0")
      serv=http("0.0.0.0",80)
      while 1:
        serv.http(wifi_setup)    
  
except:
  #print("无法写入")
  pass
try:
  import cfg
  ssd=cfg.ssd
  pwd=cfg.pwd
  key=cfg.key
except:
  _reset()
wifi=lib.wifi(ssd,pwd,device)[0]


