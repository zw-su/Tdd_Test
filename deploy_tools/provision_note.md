# 配置新网站
====================

## 需要的包

* nginx
* python3.6
* virtualenv + pip
* Git
* mariadb

# 以centos7为例：
mkdir -p /server/tools
cd /server/tools
wget  https://www.python.org/ftp/python/3.6.5/Python-3.6.5.tgz(用的是源码，参考网站：https://blog.51cto.com/13777759/2400192?source=dra)
# 安装nginx,配置文件参考nginx.template.conf
# 安装mariadb10.4.6,参考：https://www.cnblogs.com/keepee/p/10819265.html
# 创建 虚拟环境 
python3.6 -m venv /**/**
# 安装selenium
# 安装chrome和chrome.driver，更改一些配置，参考：https://blog.csdn.net/weixin_40074627/article/details/88933685
# 安装pymysql,运行后报错：
django.core.exceptions.ImproperlyConfigured: mysqlclient 1.3.3 or newer is required; you have 0.7.11.None
在django\db\backends\mysql\base.py下面注释
if version < (1, 3, 3):
     raise ImproperlyConfigured("mysqlclient 1.3.3 or newer is required; you have %s" % Database.__version__) 
在lib\site-packages\django\db\backends\mysql\operations.py里面
把其中的 query = query.decode(errors='replace')修改为query = query.encode(errors='replace')，虚拟环境中，django安装在python3.6/site-pages
# 虚拟环境安装Django和gunicorn
* 把SITENAME替换成所需的域名
# systemd下面gunicorn服务
* service参考gunicorn-upstart.template.serveice
* socket参考gunicorn-upstart.template.socket
运行gunicorn和gunicorn.socket