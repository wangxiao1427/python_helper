import os
import json
import random
import string
import requests
from io import BytesIO


class Uploader(object):
    r"""文件存储服务NFS上传接口  
    params:sub_dir 文件在文件系统存放的目录  
    params:file_name 物理文件路径  
    params:args 上传接口 upload_url & 合并接口 merge_url 
    
    文件分片上传阶段异常  
    FileTransError : File transfer failed (1)!  

    分片合并阶段异常  
    FileTransError : File transfer failed (2)!  
    """

    def __init__(self, sub_dir, file_name, **args):
        r"""
        params:sub_dir 文件在文件系统存放的目录  
        params:file_name 物理文件路径  
        params:args 上传接口 upload_url & 合并接口 merge_url 
        """
        if not sub_dir:
            raise Exception('sub_dir is missing or invalidate!')
        if not os.path.exists(file_name):
            raise Exception('File not exist!')

        self._upload_url = args.get('upload_url')
        self._merge_url = args.get('merge_url')

        if not self._upload_url:
            raise Exception('upload_url is required!')
        if not os.path.basename(self._file_name):
            raise Exception('upload_url is invalid format!')
        if not self._merge_url:
            raise Exception('merge_url is required!')

        self._file_name = file_name

    def start(self):
        self._reset_task_id()
        self._push_part_file()
        return self._part_merge()

    def _reset_task_id(self):
        self.task_id = 'wu_{}'.format(
            ''.join(random.sample(string.ascii_letters + string.digits, 28)))

    # slice
    def _push_part_file(self):

        _chunk = 0
        _upload_data = {'task_id': self.task_id, 'sub_dir': self._sub_dir}

        with open(self._file_name, 'rb') as f:
            while True:
                # 每次读取20M
                part_bytes = f.read(20 * 1024 * 1024)
                if not part_bytes:
                    break

                _upload_data['chunk'] = _chunk

                _files = {'file': (file_name, BytesIO(part_bytes), 'application')}
                _res = requests.post(self._upload_url, files=_files, data=_upload_data)
                
                if not _res.ok:
                    raise FileTransError('File transfer failed (1)!')
                _chunk += 1

                _size += len(part_bytes)
    
    # merge
    def _part_merge(self):
        _file_name = os.path.basename(self._file_name)
        _merge_data = {'sub_dir': self._sub_dir, 'task_id': self.task_id, 'filename': _file_name}
        _res = requests.put(self._merge_url, data=data)
        if not _res.ok:
            raise FileTransError('File transfer failed (2)!')
        return _res
