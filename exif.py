from PIL import Image

with Image.open('/Volumes/home/Photos/MobileBackup/photo1/IMG_6378.HEIC') as img:
    exif_data = img._getexif()
    if exif_data:
        date_str = exif_data.get(36867)
        if date_str:
            print(date_str)
