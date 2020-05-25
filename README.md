### django+fastdfs的docker部署实现


免去安装环境的繁琐直接拉取别人安装好了的[docker镜像](https://hub.docker.com/r/ygqygq2/fastdfs-nginx)

写的时候最新版本是V6.06，[不要只使用latest的TAG](https://zhuanlan.zhihu.com/p/73369281)
```
docker pull ygqygq2/fastdfs-nginx:V6.06

# 新建了一个（桥接）网络？，虽然不建也可以，那还是建一下吧(ip可能是172.19.0.2)
docker network create fastdfs-net
# 把tracker跟踪服务器这边的端口暴露出来方便项目的docker容器访问（可以设置访问ip限制）
docker run -dit --network=fastdfs-net --name tracker -p 8070:80 -p 22122:22122 -v /var/fdfs/tracker:/var/fdfs ygqygq2/fastdfs-nginx:V6.06 tracker
docker run -dit --network=fastdfs-net --name storage0 -e TRACKER_SERVER=tracker:22122 -v /var/fdfs/storage0:/var/fdfs ygqygq2/fastdfs-nginx:V6.06 storage
docker run -dit --network=fastdfs-net --name storage1 -e TRACKER_SERVER=tracker:22122 -v /var/fdfs/storage1:/var/fdfs ygqygq2/fastdfs-nginx:V6.06 storage

建好容器后会自动启动Nginx，先把三个Nginx都关了，进入tracker容器，把/nginx_conf/conf.d的复制到nginx默认配置中
cp -r /nginx_conf/conf.d /usr/local/nginx/conf/conf.d
修改其中的tracker.conf的负载均衡配置
upstream fdfs {
    # storage为上面两个storage0，storage1的容器ip（例172.19.0.3）
    server storage:8080;
}
测试nginx -t 运行 nginx
测试上传(图片)：
/usr/bin/fdfs_upload_file /etc/fdfs/client.conf /run/nginx.pid
返回一个路径链接>> group1/M00/00/00/rBkAAV0BEBGAJ4M-AAAeSwu9TgM5076993
再去访问http nginx_host+ 路径 


与Django的结合使用：
---安装---：
进入 项目/utils/fastDFS  (所需文件在这里面，包括client.conf)
pip install fdfs_client-py-master.zip（或者把.zip解压后进入目录执行 python setup.py install）
pip install mutagen
pip install requests
---*---

修改client.conf配置：
tracker_server=运行tracker服务的机器ip:22122

粗略使用方法：（具体实现见 ./utils/fastDFS/fdfs_api.py）
---start---
from fdfs_client.client import Fdfs_client
client = Fdfs_client('./client.conf')
re=client.upload_by_filename(‘文件名’)  或client.upload_by_buffer(文件bytes数据)
>>>re
{'Group name': 'group1', 'Remote file_id': 'group1/M00/00/00/rBMABF7I3e2AKOgfAAD7LBrSuwQ072.png', 'Status': 'Upload successed.', 
'Local file name': '/my_django/awa.png', 'Uploaded size': '62.00KB', 'Storage IP': '172.19.0.4'}
---end---

Django使用自定义Storage类，见./utils/fastDFS/fdfs_storage.py


```

