#!/usr/bin/python3

from pyzabbix.api import ZabbixAPI
import os
from pathlib import Path

# Create ZabbixAPI class instance
zapi = ZabbixAPI(url='http://localhost/zabbix/', user=os.environ['ZUSER'], password=os.environ['ZPASS'])
result1 = zapi.host.get(monitored_hosts=1, output='extend')

print("=" * 60)
if os.path.isfile('UpdateSummary.txt'):
    print ("UpdateSummary.txt exist")
else:
    print ("UpdateSummary.txt does not exist")
    exit()

print("=" * 55 )

#check if proxylist exits
my_file = Path("RevertbackSummary.txt")
if my_file.is_file():
        os.remove("RevertbackSummary.txt")

f = open("UpdateSummary.txt","r")
fw = open("RevertbackSummary.txt","w")
fw.write("Hostid:Proxyid"+"\n")

count = 0


for line in f:
        if count != 0:
                lst = line.rstrip()
                x = lst.split(":")
                print ("restore host: " + x[0] + " to proxy: " + x[1])
                host_updated = zapi.host.update(hostid=x[0],proxy_hostid=x[1]) #### proxy update for the host ######################
                if host_updated:
                        print ("For Host : " + x[0] + "  Proxy : " + x[1] + " is successfully updated")
                        fw.write(x[0] + ":" + x[1] + "\n")
                else:
                        print("proxy for Hostid : " + x[0] + " couldn\'t be updated")
        count += 1

fw.close()
print("=" * 60)
print("Change Summary")
os.system("cat RevertbackSummary.txt")
print("=" * 60)