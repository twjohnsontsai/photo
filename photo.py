'''
Author: twjohnsontsai twjohnsontsai@icloud.com
Date: 2023-03-31 14:53:05
LastEditors: twjohnsontsai twjohnsontsai@icloud.com
LastEditTime: 2023-04-02 08:47:57
FilePath: /photo/photo.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
import os
import shutil
import hashlib
from datetime import datetime
import logging

# 设置日志文件
logging.basicConfig(filename='photo_organizer.log', level=logging.INFO)

# 源文件夹路径
src_folder = 'downloads'

# 目标文件夹路径
dst_folder = 'photos'

# 错误文件夹路径
error_folder = 'error'

# 支持的图片格式
img_extensions = ('.png', '.jpg', '.jpeg', '.svg', '.bmp',
                  '.dng', '.gif', '.psd', '.3gp', '.mp4', '.mov', '.heic')

# 遍历文件夹中的文件
for root, dirs, files in os.walk(src_folder):
    for filename in files:
        # 获取文件完整路径
        file_path = os.path.join(root, filename)

        # 如果是文件夹则跳过
        if os.path.isdir(file_path):
            continue

        # 如果文件不是图片格式则跳过
        if not filename.lower().endswith(img_extensions):
            continue

        # 计算文件哈希值，用于去重
        with open(file_path, 'rb') as f:
            file_hash = hashlib.md5(f.read()).hexdigest()

        # 根据文件哈希值判断是否是重复文件
        if os.path.exists(os.path.join(dst_folder, file_hash)):
            logging.info(f'文件 "{filename}" 是重复文件，已跳过')
            continue

        try:
            # 读取文件创建时间
            file_created_time = datetime.fromtimestamp(
                os.path.getctime(file_path))

            # 拼接目标文件夹路径和文件名
            new_filename = f'{file_created_time:%Y-%m-%d_%H-%M-%S}_{filename}'
            target_filepath = os.path.join(dst_folder, file_hash, new_filename)

            # 移动文件到目标文件夹
            shutil.move(file_path, target_filepath)

            # 输出日志信息
            logging.info(f'文件 "{filename}" 已移动到目标文件夹')
        except Exception as e:
            # 如果无法处理文件，则将其移动到错误文件夹
            error_filepath = os.path.join(error_folder, filename)
            shutil.move(file_path, error_filepath)

            # 输出错误日志信息
            logging.error(f'移动文件 "{filename}" 时发生错误: {e}')

# 输出脚本执行完毕的信息
print(f'脚本执行完毕！完成时间：{datetime.now()}')
