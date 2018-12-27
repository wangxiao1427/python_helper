import os
import json
import random
import string
import requests
from io import BytesIO


class Uploader(object):
    r"""
    params:file_name 物理文件路径  
    params:data 合并文件接口附带的参数,数据集相关参数  
    params:args 上传接口upload_url & 合并接口merge_url 
    """
    def __init__(self, file_name, data, **args):
        r"""
        params:file_name 物理文件路径  
        params:data 合并文件接口附带的参数,数据集相关参数  
        params:args 上传接口upload_url & 合并接口merge_url 
        """
        if not os.path.exists(file_name):
            raise Exception('File not exist!')

        self._upload_url = args.get('upload_url')
        self._merge_url = args.get('merge_url')

        if not self._upload_url:
            raise Exception('upload_url is required')
        if not self._merge_url:
            raise Exception('merge_url is required')

        self._file_name = file_name
        self._data = data

    def start(self):
        self._reset_task_id()
        self._push_part_file()
        self._part_merge()
        return True

    def _reset_task_id(self):
        self.task_id = 'wu_{}'.format(
            ''.join(random.sample(string.ascii_letters + string.digits, 28)))

    # slice
    def _push_part_file(self):
        with open(self._file_name, 'rb') as f:
            _chunk = 0
            _data = {}
            while True:
                part_bytes = f.read(20 * 1024 * 1024)
                if not part_bytes:
                    break
                files = {'file': (self.task_id, BytesIO(part_bytes), 'application')}
                _data['task_id'] = self.task_id
                _data['chunk'] = _chunk
                res1 = requests.post(self._upload_url, files=files, data=_data)
                if not res1.ok:
                    raise Exception('Encountered an error in pushing a slice')
                _chunk += 1
    # merge
    def _part_merge(self):
        self._data['task_id'] = self.task_id
        _res = requests.put(self._merge_url, data=json.dumps(self._data))
        if not _res.ok:
            raise Exception('Encountered an error in merge all slices')
        return _res.text