## 2018-12-28  
####添加使用文档  

* 安装 
  `pip install aios-part-uploader`

* 引入  
  - 数据集分片上传:  
    ```
    from aios_part_uploader.dateset import Uploader  

    file_name = 'c:\\test.txt'
    # 和数据集相关的业务数据
    data = {'name': 'A', ...}
    # 上传/合并参数
    args = {'upload_url': 'http://127.0.0.1:7777/api/xxx',
            'merge_url': 'http://127.0.0.1:7777/api/yyy'}
    
    try:
        res = Uploader(file_name, data, **args).start()
        print('上传结果', res.text)
    except Exception as err:
        return print('上传失败', err)
    ```

  - 文件分片上传到指定文件挂载点:  
    ```
    from aios_part_uploader.nfs import Uploader

    # sub_dir格式 <环境:prod/test/dev>/<模块>/<自定义>
    sub_dir = 'dev/dmp/1/xxx'
    file_name = 'c:\\test.txt'
    args = {'upload_url': current_app.config['FILE_UPLOAD_URL'],
            'merge_url': current_app.config['FILE_MERGE_URL']}

    res = Uploader(sub_dir, file_name, **args).start()

    if not res.ok:
        print('上传失败', res.text)
    else:
        print('上传成功', res.text)
    ```

---------------------------------------------------------------------
* 更新版本发布流程
1. 在setup.py更新版本号
2. 生成最新版本发布包 `python setup.py sdist`
3. 第一次时,安装上传组件 `pip install twine`
4. 上传指定发布包 `twine upload dist/aios_part_uploader-0.0.1.tar.gz`