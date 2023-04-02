'''
Author: twjohnsontsai twjohnsontsai@icloud.com
Date: 2023-03-31 14:53:05
LastEditors: twjohnsontsai twjohnsontsai@icloud.com
LastEditTime: 2023-04-02 09:31:32
FilePath: /photo/photo.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
import os
import shutil
from datetime import datetime

# 源文件夹路径
source_folder = r'/Volumes/home/Photos/MobileBackup/photo'
# 目标文件夹路径
target_folder = r'/Volumes/home/Photos/MobileBackup/photo1'
# 错误文件夹路径
error_folder = r'/Volumes/home/Photos/MobileBackup/error'

# 支持的文件扩展名
valid_extensions = ('.png', '.jpg', '.jpeg', '.svg', '.bmp',
                    '.dng', '.gif', '.psd', '.3gp', '.mp4', '.mov', '.heic')

# 分类文件夹路径
folders = {
    'png': os.path.join(target_folder, 'png'),
    'jpg': os.path.join(target_folder, 'jpg'),
    'jpeg': os.path.join(target_folder, 'jpeg'),
    'svg': os.path.join(target_folder, 'svg'),
    'bmp': os.path.join(target_folder, 'bmp'),
    'dng': os.path.join(target_folder, 'dng'),
    'gif': os.path.join(target_folder, 'gif'),
    'psd': os.path.join(target_folder, 'psd'),
    '3gp': os.path.join(target_folder, '3gp'),
    'mp4': os.path.join(target_folder, 'mp4'),
    'mov': os.path.join(target_folder, 'mov'),
    'heic': os.path.join(target_folder, 'heic')
}

# 遍历源文件夹下的所有文件和文件夹
for root, dirs, files in os.walk(source_folder):
    for filename in files:
        # 判断文件扩展名是否为支持的文件扩展名
        if filename.lower().endswith(valid_extensions):
            # 拼接文件路径
            filepath = os.path.join(root, filename)
            try:
                # 读取文件创建时间
                file_created_time = datetime.fromtimestamp(
                    os.path.getctime(filepath))
                # 获取文件类型
                file_type = filename.split('.')[-1].lower()
                # 如果文件类型未被分类，则将文件移动到错误文件夹
                if file_type not in folders:
                    error_filepath = os.path.join(error_folder, filename)
                    shutil.move(filepath, error_filepath)
                else:
                    # 根据文件类型和创建时间创建目标文件夹路径
                    folder_path = os.path.join(
                        folders[file_type], f'{file_created_time:%Y%m%d}')
                    # 如果目标文件夹不存在，则创建目标文件夹
                    if not os.path.exists(folder_path):
                        os.makedirs(folder_path)
                    # 拼接目标文件夹路径和文件名
                    target_filepath = os.path.join(
                        folder_path, f'{file_created_time:%Y%m%d_%H%M%S}_{filename}')
                    # 移动文件到目标文件夹
                    shutil.move(filepath, target_filepath)
            except Exception as e:
                # 如果无法处理文件，则将其移动到错误文件夹
                error_filepath = os.path.join(error_folder, filename)
                shutil.move(filepath, error_filepath)
                print(f'无法处理文件{filename}，已移动到错误文件夹。错误信息：{str(e)}')


# 输出脚本执行完毕的信息
print(f'脚本执行完毕！完成时间：{datetime.now()}')
