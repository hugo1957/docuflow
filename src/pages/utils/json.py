import base64


def json_base64(json_file_path):
    with open(json_file_path, 'rb') as json_file:
        json_data = json_file.read()
        return base64.b64encode(json_data).decode('utf-8')
