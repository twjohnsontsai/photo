'''
Author: twjohnsontsai twjohnsontsai@icloud.com
Date: 2023-04-02 07:48:20
LastEditors: twjohnsontsai twjohnsontsai@icloud.com
LastEditTime: 2023-04-02 08:02:48
FilePath: /photo/exif.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
from PIL import Image

with Image.open('/Volumes/home/Photos/MobileBackup/photo1/IMG_6378.HEIC') as img:
    exif_data = img._getexif()
    if exif_data:
        date_str = exif_data.get(36867)
        if date_str:
            print(date_str)
