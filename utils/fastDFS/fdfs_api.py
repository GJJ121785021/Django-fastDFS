import os

from fdfs_client.client import Fdfs_client

from my_django.settings import FDFS_CLIENT_CONF, BASE_DIR

def upload_fdfs():
    # 指定client.conf的位置
    client = Fdfs_client(FDFS_CLIENT_CONF)

    filename = os.path.join(BASE_DIR, 'test_image.png')
    result_1 = client.upload_by_filename(filename)
    # {'Group name': 'group1', 'Remote file_id': 'group1/M00/00/00/rBMABF7I3e2AKOgfAAD7LBrSuwQ072.png',
    # 'Status': 'Upload successed.', 'Local file name': '/my_django/awa.png', 'Uploaded size': '62.00KB',
    # 'Storage IP': '172.19.0.4'}
    url_path = '/' + result_1.get('Remote file_id')
    print(url_path)

    # 2 -->
    with open(filename, 'rb') as f:
        result_2 = client.upload_by_buffer(f.read())
    url_path2 = '/' + result_2.get('Remote file_id')
    print(url_path2)


if __name__ == '__main__':
    upload_fdfs()
