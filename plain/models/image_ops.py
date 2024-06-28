import os
from PIL import Image
import datetime

def get_image_metadata(image_path):
    # Get file name and path
    file_name = os.path.basename(image_path)
    file_path = os.path.abspath(image_path)

    timestamp_created = os.path.getctime(image_path)
    timestamp_modified = os.path.getmtime(image_path)
 
    file_size = os.path.getsize(image_path)
    image = Image.open(image_path)
    file_format = image.format
    width, height = image.size
    file_path = os.path.basename(file_path) # TODO: implement folder
    metadata = {
        'file_name': file_name,
        'file_path': file_path,
        'timestamp_created': timestamp_created,
        'timestamp_modified': timestamp_modified,
        'file_format': file_format,
        'file_size': file_size,
        'width': width,
        'height': height
    }
    
    return metadata

def read_image_metadata():
    # created_date = datetime.datetime.fromtimestamp(created_timestamp).strftime('%Y-%m-%d %H:%M:%S')
    # modified_date = datetime.datetime.fromtimestamp(modified_timestamp).strftime('%Y-%m-%d %H:%M:%S')
    
    pass