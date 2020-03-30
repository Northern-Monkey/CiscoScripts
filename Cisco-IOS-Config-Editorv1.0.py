import sys
import time
import paramiko 
import os
import cmd
import datetime

now = datetime.datetime.now()
user = 'PUT USERNAME HERE'
password = 'PUT PASSWORD HERE'
enable_password = '\n'
port=22
f0 = open('devices.txt')
for ip in f0.readlines():
       ip = ip.strip()
       filename_prefix ='CUSTOMER NAME' + ip + 'RunningCfg' 
       ssh = paramiko.SSHClient()
       ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
       ssh.connect(ip,port, user, password, look_for_keys=False)
       chan = ssh.invoke_shell()
       time.sleep(2)
       chan.send('enable\n')
       chan.send(enable_password +'\n')
       time.sleep(1)
       chan.send('term len 0\n')
       time.sleep(1)
       chan.send('conf t\n')
       chan.send('snmp-server host 10.35.2.219 traps ver 3 priv LMS1\n')
       time.sleep(1)
       chan.send('logging host 10.35.2.220\n')
       time.sleep(1)
       chan.send('logging trap notifications\n')
       time.sleep(1)
       chan.send('exit\n')
       chan.send('sh run\n')
       time.sleep(5)
       output = chan.recv(999999)
       filename = "%s %.2i% 2i% i" % (ip,now.day,now.month,now.year)
       f1 = open(filename, 'a')
       f1.write(output.decode("utf-8") )
       f1.close()
       ssh.close() 
       f0.close()