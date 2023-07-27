#!/usr/bin/python3

from pyzabbix.api import ZabbixAPI
import os
from pathlib import Path

#check if proxylist exits
my_file = Path("proxylist.txt")
if my_file.is_file():
        os.remove("proxylist.txt")


#check if proxylistmac exits
my_file = Path("proxylistmac.txt")
if my_file.is_file():
        os.remove("proxylistmac.txt")

#check if ListofHosts.txt exits
my_file = Path("ListofHosts.txt")
if my_file.is_file():
        os.remove("ListofHosts.txt")

#check if ListofHostsMac.txt exits
my_file = Path("ListofHostsMac.txt")
if my_file.is_file():
        os.remove("ListofHostsMac.txt")

#check if UpdateSummary exits
my_file = Path("UpdateSummary.txt")
if my_file.is_file():
        os.remove("UpdateSummary.txt")

#check if DescUpdateSummary.txt exits
my_file = Path("DescUpdateSummary.txt")
if my_file.is_file():
        os.remove("DescUpdateSummary.txt")

os.system('clear')
os.system('clear')

    # Create ZabbixAPI class instance
zapi = ZabbixAPI(url='http://localhost/zabbix/', user=os.environ['ZUSER'], password=os.environ['ZPASS'])
result1 = zapi.host.get(monitored_hosts=1, output='extend')

#listing the Existing proxies
proxy_list = zapi.proxy.get(output="extend", selectGroups="extend")
#print (proxy_list)
f = open ("proxylist.txt","w+")
fh = open ("proxylistmac.txt","w+")

if proxy_list:
        count=0
        for proxy in proxy_list:
                count=count+1
                f.write(str(count) + ". "+ proxy["host"]+"\n")
                fh.write(str(count) + ":" + proxy["host"] + "\n")
else:
        print("No Proxy Exist")
        exit()

#close proxy file
f.close()
fh.close()

f = open("proxylist.txt","r")
###print list of proxies ##########################
if f.mode == 'r':
        contents = f.read()
        print("LIST OF EXISTING PROXIES")
        print('=' * 40)
        print(contents)
        print('=' * 40)
else:
        print("Couldn't find Any Existing Proxies\n")
        exit()

f.close()

####### Source proxy, list the hosts attached to it ##########################
source_proxy_numeric = 0
try:
        source_proxy_numeric = int(input("Enter the Source proxy name in numeric : "))
except ValueError:
        print("Invalid Entry, Exiting........................")
        exit()


def proxy_name_check( source_proxy_numeric):
        fh = open("proxylistmac.txt","r")
        flag = 1
        for line in fh:
                lst = line.rstrip()
                x = lst.split(":")
                if int(source_proxy_numeric) == int(x[0]):
                        source_proxy_name = x[1]
                        flag = 0
                        break


        if flag == 1:
                print("Invalid input " + str(source_proxy_numeric) + " Exiting..........")
                exit()
        return source_proxy_name



source_proxy_name = proxy_name_check(source_proxy_numeric)
print ("You have entered Source proxy name : " + format(source_proxy_name))
source_proxy = zapi.proxy.get(output="extend", selectGroups="extend",filter={"host":source_proxy_name})
print('=' * 40)

if source_proxy:
        print("Source Proxy:  "+source_proxy_name +"  found :)")
        ############# Find list of servers attached to this proxy ###########################
        #print (source_proxy)
        proxyid = source_proxy[0]["proxyid"]
        result1 = zapi.host.get(monitored_hosts=1, output='extend',filter={"proxy_hostid":proxyid})
        if len(result1) > 0:
                print("Hosts are aligned to the source Proxy: " + source_proxy_name + "\n")
                f = open ("ListofHosts.txt","w")
                fh = open ("ListofHostsMac.txt","w")
                count = 0
                for h in result1:
                        count = count + 1
                        f.write(str(count) + ". " + h["host"] + "\n")
                        fh.write(str(count) + ":" + h["hostid"] + ":" + h["host"] +  "\n")###### File contains hostid and hostname ########################
                print (str(count) + " Hosts are aligned to Source proxy: " + source_proxy_name )
                print ('=' * 40)
                print ("List of HostIDs aligned with PROXY:  " + source_proxy_name)
                f.close()
                print ('=' * 40)
                os.system('cat ListofHosts.txt')
                #print ('=' * 40)
        else:
                print ("No Hosts are aligned to Source Proxy: " + source_proxy_name + ",  Exiting.....")
                exit()
else:
        print ("Source Proxy: " + source_proxy_name + " doesn't exit, Exiting.......................")
        exit()

f.close()
fh.close()


########################### Get the List of Valid Hosts ###########################################
def get_valid_host():
        global host_start_num,host_end_num,host_start_id,host_end_id ### Global Variables ###################

        host_start_num = 0
        try:
                host_start_num = int(input("Enter the host number ( like 1 2 3...) you want hostlist to start: "))
        except ValueError:
                print("Invalid Entry, Exiting........................")
                exit()


        host_end_num = 0
        try:
                host_end_num = int(input("Enter the host number ( like 1 2 3...) you want hostlist to END: "))
        except ValueError:
                print("Invalid Entry, Exiting........................")
                exit()


        if ( host_start_num > host_end_num ):
                print('=' * 65 )
                print ("Host End number can't be less than Host Start number, Exiting..................")
                exit()

######################## Check if the host Number is valid ###################################

        f = open("ListofHostsMac.txt","r")
        flag = 1
        for line in f:
                lst = line.rstrip()
                x = lst.split(":")
                if int(host_start_num) == int(x[0]):
                        host_start_id = x[1]
                        print('=' * 55)
                        print ("Valid Host start Number,  :) ")
                        flag = 0
                        break

        if flag == 1:
                print("Invalid Host start Number, Exiting.........................")
                exit()

        flag = 1
        f.close()
        f = open ("ListofHostsMac.txt","r")

        for line in f:
                lst = line.rstrip()
                x = lst.split(":")
                if int(host_end_num) == int(x[0]):
                        host_end_id = x[1]
                        print ('=' * 55)
                        print ("Valid Host End Number,  :) ")
                        flag = 0
                        break

        if flag == 1:
                print ("Invalid Host End Number, Exiting........................................")
                exit()
        f.close()


############################### Get the list of hosts within the valid range #############################
def listofvalidhosts():
        f = open ("ListofHostsMac.txt","r")
        hosts_app = list()
        hosts_app_name = list()
        flag = 1
        for line in f:
                lst = line.rstrip()
                x = lst.split(":")

                if ( host_start_id == host_end_id ) and int(host_start_id) == int(x[1]): ##### if only one host is choosen then break from loop ################
                        hosts_app.append(int(x[1]))
                        hosts_app_name.append(x[2])
                        break

                if int(host_start_id) == int(x[1]):
                        hosts_app.append(int(x[1]))
                        hosts_app_name.append(x[2])
                        flag = 0
                        #print ("prob start " + x[2])
                elif int(host_end_id) == int(x[1]):
                        hosts_app.append(int(x[1]))
                        hosts_app_name.append(x[2])
                        #print ("prob end " + x[2])
                        flag = 1
                elif flag == 0:
                        hosts_app.append(int(x[1]))
                        hosts_app_name.append(x[2])
                        #print ("prob flag is zero  " + x[2])


        print ("list of hosts choosen for change of proxy")
        print (hosts_app_name)
        return hosts_app



get_valid_host()
hosts_app = listofvalidhosts()

#print (hosts_app)

########### Destination proxy ################################
print ('=' * 40)

dest_proxy_numeric = 0
try:
        dest_proxy_numeric = int(input("Enter the Destination proxy name in numeric : "))
except ValueError:
        print("Invalid Entry, Exiting........................")
        exit()


dest_proxy_name = proxy_name_check(dest_proxy_numeric)
print ("You have entered Destination proxy name : " + format(dest_proxy_name))
dest_proxy = zapi.proxy.get(output="extend", selectGroups="extend",filter={"host":dest_proxy_name})
print('=' * 40)

if dest_proxy:
        print ("Destination Proxy: " + dest_proxy_name + "  Found :)")
        dest_proxyid = dest_proxy[0]["proxyid"]
        #print("Destination Proxy")
        #print(dest_proxyid)

else:
        print ("Destination Proxy: " + dest_proxy_name + "  Not Found, Exiting....................")
        exit()


########################### Module to update proxy ID  ###########################################

#print ("Length of hosts_app : " + format(len(hosts_app)))
print ("+" * 55)

f = open ("DescUpdateSummary.txt","w")
fh = open("UpdateSummary.txt","w")
fh.write("Hostid:Source_Proxyid:Destination_Proxyid" + "\n")
count = 0

if len(hosts_app) > 0: ###### check if array of hosts whose proxy is to be updated has at least one entry #########
        for h in hosts_app:
                #print("host name whose proxy should be changed")
                #print (h)
                result_host =  zapi.host.get(monitored_hosts=1, output='extend',filter={"hostid":h})
                #print ("+" * 55)
                #print ("host whose proxy is now changed")
                #print (result_host)
                #print ("+" * 55)
                existing_proxy_id = int(result_host[0]["proxy_hostid"])
                #print("Existing proxy id " + format(existing_proxy_id))
                existing_proxy = zapi.proxy.get(output="extend", proxyids=existing_proxy_id) ##### Important step, Taken cue from zabbix-gnome, hurrah #######
                host_updated = zapi.host.update(hostid=h,proxy_hostid=dest_proxyid)
                #print ("count no of times hosts are updated")
                if host_updated:
                        count = count + 1
                        #print(existing_proxy)
                        #print('=' * 55)
                        #print ("host_updated")
                        #print(host_updated["hostids"])
                        #print('=' * 55)
                        #print(existing_proxy)
                        #print ('+' *  69)
                        host_result = zapi.host.get(monitored_hosts=1, output='extend', hostids=h) ###### Important step, filter keyword didn't work ###########################
                        #print (host_result)
                        #print ('+' * 69)
                        f.write("Host: " + format(host_result[0]["host"]) + " had  the proxy: " + existing_proxy[0]["host"] + "\n")
                        f.write("Host: " + format(host_result[0]["host"]) + " now successfully updated with New Proxy: " + dest_proxy_name + "\n\n")
                        fh.write(str(h) + ":" + format(existing_proxy_id) + ":" + format(dest_proxyid) + "\n")
                else:
                        print (format(h) + " couldn't be updated")
                        break
                #print ("hostid " + format(h["hostid"]))

f.close()
fh.close()
print ("Number of monitored hosts " + format(len(result1)))
print ("Number of hosts updated " + format(count))
print('=' * 40)


f = open("DescUpdateSummary.txt","r")

#print hosts updated with new proxy
if f.mode == 'r':
        contents = f.read()
        print("LIST OF Hosts whose  PROXY has been updated")
        print('=' * 40)
        print(contents)
        print('=' * 40)
else:
        print("Couldn't find Any Host whose  Proxy has been updated\n")
        exit()


print("Output in Plain Format")
print('=' * 40)
os.system('cat UpdateSummary.txt')
print('=' * 40)
