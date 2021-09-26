


import uos, machine,gc
gc.enable()
try:
  import lib
except:
  pass

device="Light"
power=lib.flashLed(0)#开关控制引脚
led=lib.flashLed(2)
_cfg="cfg.py"
_Stat="stat"
power.sw( 1 if lib.file(_Stat)=="1" else 0 )

def setFile(s=1):
      file="isRset.py"
      num=lib.file(file)
      if type(s).__name__=="Timer" or s==1 or s=='r':
        if num:
          if s=='r':
            return int(num)
          num=int(num)
          lib.file(file,str(num+1))
          return num+1
        else:
          if s=='r':
            return False         
          lib.file(file,"0")
      if s==0:
        lib.file(file,"0")
        return 1
      if s==4:
        lib.file(file,"4")
        return 4 
def _reset(s=1):
    lib.file("isRset.py","4")
    machine.reset()
led.flash(50)
print("\n========:",lib.file("isRset.py"))
machine.Timer(-1).init(period=5000, mode=machine.Timer.ONE_SHOT, callback=lambda t:print(setFile(0))) #1次
if int(lib.file("isRset.py")) >=3:
      import webrepl,time
      webrepl.start()
      led.flash(1000)
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
                    machine.sleep(3000)
                    machine.reset()
              else:
               serv.send("666 \r\n")    
      lib.ap(device)
      serv=http("0.0.0.0",80)
      while 1:
          if time.ticks_ms()==180000:
            machine.reset()
          serv.http(wifi_setup)    
      raise

try:
  import cfg
  ssd=cfg.ssd
  pwd=cfg.pwd
  key=cfg.key
except Exception as e:
  print(e)
  #_reset()
wifi=lib.wifi(ssd,pwd,device)[0]
led.stop()
led.sw(1)
print("=======boot.py========")
del  setFile
gc.collect()