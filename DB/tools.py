import os

def get_path (file_name):
    current_file_path = os.path.realpath(__file__)
    current_dir_path = os.path.dirname(current_file_path)
    file_path = os.path.join(current_dir_path, file_name)
    return file_path