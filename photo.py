import os
import shutil
import hashlib
from datetime import datetime
from PIL import Image


# 指定源目录和目标目录
src_folder = '/Volumes/photo'
dst_folder = '/Volumes/home/Photos/MobileBackup/photo'

# 创建目标目录
os.makedirs(dst_folder, exist_ok=True)

# 遍历源目录中的所有文件和照片
for root, dirs, files in os.walk(src_folder):
    for filename in files:
        # 获取文件路径
        file_path = os.path.join(root, filename)

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
                        dst_folder_year_month = os.path.join(
                            dst_folder, str(date.year), f'{date.month:02d}')
                        os.makedirs(dst_folder_year_month, exist_ok=True)
                        # 判断目标文件夹中是否已经存在相同文件名的图片
                        dst_file_path = os.path.join(
                            dst_folder_year_month, filename)
                        if not os.path.exists(dst_file_path):
                            # 移动文件到目标文件夹
                            shutil.move(file_path, dst_file_path)
        except:
            # 如果文件不是图片，则直接移动到目标目录
            try:
                with open(file_path, 'rb') as f:
                    if not f.readable():
                        continue
            except IOError as e:
                print(f'Error: {e}')
                continue
            dst_file_path = os.path.join(dst_folder, filename)
            if not os.path.exists(dst_file_path):
                shutil.move(file_path, dst_file_path)
            else:
                # 如果目标目录中已经存在相同的文件，则进行比较哈希值
                src_file_hash = hashlib.md5(
                    open(file_path, 'rb').read()).hexdigest()
                dst_file_hash = hashlib.md5(
                    open(dst_file_path, 'rb').read()).hexdigest()
                if src_file_hash != dst_file_hash:
                    # 如果哈希值不相同，则在文件名前加上当前时间戳，并移动到目标目录
                    timestamp = int(datetime.now().timestamp())
                    new_filename = f'{timestamp}_{filename}'
                    new_file_path = os.path.join(dst_folder, new_filename)
                    shutil.move(file_path, new_file_path)

print('脚本执行完毕！')
