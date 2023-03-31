'''
Author: twjohnsontsai twjohnsontsai@icloud.com
Date: 2023-03-31 14:53:05
LastEditors: twjohnsontsai twjohnsontsai@icloud.com
LastEditTime: 2023-03-31 23:29:09
FilePath: /test/photo/photo.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
import os
import shutil
from datetime import datetime
from PIL import Image

# 设置源文件夹路径
src_folder = '/Volumes/Mac/照片'

# 设置目标文件夹路径
dst_folder = '/Volumes/home/Photos/MobileBackup/photo'

# 检查目标文件夹是否已经存在，如果已经存在，则认为脚本已经执行过，不再执行
if os.path.exists(dst_folder):
    print('目标文件夹已经存在，脚本已经执行过！')
else:
    # 遍历源文件夹中的所有文件
    for filename in os.listdir(src_folder):
        file_path = os.path.join(src_folder, filename)

        # 判断文件是否为图片
        try:
            with Image.open(file_path) as img:
                exif_data = img._getexif()
                if exif_data:
                    # 获取图片拍摄日期
                    date_str = exif_data.get(36867)
                    if date_str:
                        # 将拍摄日期转换为datetime类型
                        date = datetime.strptime(date_str, '%Y:%m:%d %H:%M:%S')
                        # 根据年份和月份创建目标文件夹
                        dst_folder = os.path.join(dst_folder, str(date.year), f'{date.month:02d}')
                        os.makedirs(dst_folder, exist_ok=True)
                        # 移动文件到目标文件夹
                        shutil.move(file_path, os.path.join(dst_folder, filename))
        except:
            pass

    print('脚本执行完毕！')
