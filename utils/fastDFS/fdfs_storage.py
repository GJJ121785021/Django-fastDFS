import time

from django.conf import settings
from django.core.files.storage import Storage, FileSystemStorage
from fdfs_client.client import Fdfs_client


class FDFSStorage(Storage):
    """
    自定义文件图片储存系统为FDFS,
    仅针对django的后台管理,前端上传要重新写,原理还是这个
    """
    def __init__(self):
        """
        初始化参数
        :param settings.BASE_URL: 图片储存的基类路径
        :param settings.FDFS_CLIENT_CONF:客户端的配置文件的路径
        """
        self.base_url = settings.BASE_URL
        self.client = Fdfs_client(settings.FDFS_CLIENT_CONF)

    def _open(self, name, mode):
        # 前端传过来的已经是二进制文件了,因此可以直接pass不写
        pass

    def _save(self, name, content):
        """重写_save方法为FDFS上传"""
        # 创建客户端连接对象

        for i in range(3):
            # 调用连接对象的二进制上传文件方法
            result = self.client.upload_by_buffer(content.read())
            # 判断上传图片是否成功,失败主动报错
            if result['Status'] == 'Upload successed.':
                break
        else:
            raise Exception('fdfs客户端连接对象上传图片失败')
        # 成功则返回文件id
        self.result = result
        return self.result['Remote file_id']

    def url(self, name):
        """返回图片的fdfs完整路径"""
        return self.base_url + name

    def exists(self, name):
        """让django认为每次上传的文件都是新文件"""
        return False

    def size(self, name):
        """返回图片大小"""
        return self.result.get('Uploaded size')

    def delete(self, name):
        """删除文件, 这个name，就是image字段存在数据库里的值"""
        assert name, "The name argument is not allowed to be empty."
        self.client.delete_file(name)

    def listdir(self, path):
        pass

    def path(self, name):
        return self.url(name)

    def get_accessed_time(self, name):
        return time.time()

    def get_created_time(self, name):
        return time.time()

    def get_modified_time(self, name):
        return time.time()
