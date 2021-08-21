




## IR MODE
from machine import UART
import   time,os
class IR:
 
  def __init__(self,rx,tx):
    self.uart = UART(1, baudrate=115200, rx=rx,tx=tx,timeout=10)
    self._write_flag=0
    self.dir="ir_Data"
    self.ac_state=0
  def exsit_dir(self):
    try:
      os.chdir(self.dir)
      os.chdir("../")
    except:
      os.mkdir(self.dir)  
      
  def uartSend(self,t):
    self.uart.write(t)
    
  def write(self,name,str):
    self.exsit_dir()
    f=open(name,"wb")
    f.write(str)
    f.close()
    
  def read(self,name):
    self.exsit_dir()
    f=open(name,"rb")
    data=f.read()
    f.close()
    return data

  def main(self):
      if self.uart.any():
          a=self.uart.read()
          print(a)
          if a!=b'\xfe\xfc\xcf':
            if self._write_flag:
              file_name=self.dir+"/Ac_"+ self._write_flag
              self.write(file_name,a)
              print (self._write_flag,":已写入。")
              self._write_flag=0
            return a
 





