#!/usr/bin/env python
#encoding:utf8
#author: linuxhub.org
#根据进程名称获取远程连接的IP地址
#process_link_address.py

import psutil, requests, re

def get_ip_info(ip):
              ''' 根据ip地址查询出IP所在的地理位置 '''
              r = requests.get('http://ip.taobao.com/service/getIpInfo.php?ip=%s' %ip)
              if  r.json()['code'] == 0 :
                            i = r.json()['data']
                            country = i['country']  #国家 
                            area = i['area']        #区域
                            region = i['region']    #地区
                            city = i['city']        #城市
                            isp = i['isp']          #运营商 
                            ip_info = u'%s,%s地区,%s%s,%s' %(country, area, region, city, isp)
                            return ip_info

def get_process_pid(pname):
              ''' 根据进程名称获取进行pid '''
              p = psutil.get_process_list()
              pid_list = []
              for r in p:
                            aa = str(r)
                            f = re.compile(pname,re.I)
                            if f.search(aa):
                                          pid = aa.split('pid=')[1].split(',')[0]
                                          if pid not in pid_list:
                                                        pid_list.append(pid)
              return pid_list



def get_process_ip(pid):
              ''' 根据进程pid获取网络连接的IP地址'''
              p = psutil.Process(pid)
              p_conn = p.connections()
              ip = []
              for conn in p_conn:
                            if conn.status != "NONE": 
                                          raddr = str(conn.raddr).split(',')[0].strip("('")
                                          if raddr not in ip:
                                                        ip.append(raddr)

              return ip



def main(process_name): 
              ''' 根据进程名称取出pid,然后根据pid取出与其连接的远程ip,最后调用淘宝ip库取出位置信息 '''

              pid_list = get_process_pid(process_name)
              print "\n进程名称: %s" % process_name
              for pid in pid_list:
                            print "\n------ pid: %s ----" % pid
                            raddr = get_process_ip(int(pid))
                            for ip in raddr:
                                          ip_info = get_ip_info(ip)
                                          print "%s  \t%s" %(ip, ip_info)              


if __name__ == '__main__':              
              process_name="QQ.exe" #QQ进程
              main(process_name)









