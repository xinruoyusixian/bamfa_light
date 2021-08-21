
from machine import Pin,UART
from urequests import get
import   time ,lib,_thread,machine,ujson,os



from IR_Model import IR
_ir= IR(23,5)
send=_ir.uartSend
read=_ir.read
def ir():
  while 1:
    d=_ir.main()

    if d!= None :
      print(d)
_thread.start_new_thread(ir, ())


class btn:
  def __init__(self,cb):

    self.debug=0


    #cb:需要触发的函数



    self.start=0

    self.cb=cb

    

  def click(self,_0=4):

    #按键消抖

    #_0:为无效参数，防止出错

    t=time.ticks_ms()-self.start

    if t<100:

      return

    if self.debug:
      print("Click",time.ticks_ms(),t)
    self.start=time.ticks_ms()
    self.cb()
    
    
 
 
class acTurn:
  
  

  def __init__(self):

    self.state=0
    self.dir="ir_Data"
    try:

      self.list=os.listdir(self.dir)

    except:

      print ("遥控错误")

      return

  

  def run(self):

    list_len=len(self.list)
    print(self.list[self.state])
    send(read(self.dir+self.list[self.state]))
    if self.state>=(list_len-1):
      self.state=0
    self.state=self.state+1

  
  def off(self):
    print("click")
    if self.list[self.state]!='Ac_btn-off':
      self.state=self.list.index("Ac_btn-off")
      send(read(self.dir+"/Ac_btn-off"))
    else:
      
      self.state=0
      send(read(self.dir+"/"+self.list[self.state]))
      
      
  
  
ac=  acTurn()

#按键循环切换
#_26=btn(ac.run)  
#_26_btn=Pin(26,Pin.IN)
#_26_btn.irq(handler=_26.click,trigger=(Pin.IRQ_FALLING))
#按键控制开关
_25=btn(ac.off)  
_25_btn=Pin(32,Pin.IN)
_25_btn.irq(handler=_25.click,trigger=(Pin.IRQ_FALLING))


uart = UART(2, baudrate=115200, rx=26,tx=33,timeout=10)


def resp(topic,msg):
        
          try:
            if topic=="light002":
                if msg=="on":
                   lib.pin(16,1)
                   print("lighton")
                   return
                if msg=="off":
                   print("lightoff")
                   lib.pin(16,0)
                   return
                return
            if topic=="ac005":
              msg_ac=msg.split("#")
              print(msg_ac )
              if msg_ac[0]=="on":
                send(read(ac.dir+"/Ac_btn-"+msg_ac[2]))
                print(ac.dir+"/Ac_btn-"+msg_ac[2])
              if msg_ac[0]=="off":
                send(read(ac.dir+"/Ac_btn-off"))
                print(ac.dir+"/Ac_btn-off")
              return
            
            
          except :
            
            print("err")



def loop(): 
 while 1 :
      if uart.any():
          a=uart.read()
          try: 
            res=a[2:2-5].decode().replace("b'",'').replace("'",'').split(" ")
            print(res)
            if len(res)==2:
              resp(res[0],res[1])
          except:
            print("解析失败")



_thread.start_new_thread(loop, ())





