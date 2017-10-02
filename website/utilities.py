'''

  Utitlities function


'''
import os,errno

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def handle_uploaded_file(file,name):
    destination = open(os.path.join(BASE_DIR,'static/images/'+name), 'wb+')
    for chunk in file.chunks():
        destination.write(chunk)
    destination.close()
    os.chmod(os.path.join(BASE_DIR,'static/images/'+name), 0o777)


def create_folder(path):
    try:
        os.makedirs(path)
    except OSError as exception:
        if(exception.errno != errno.EEXIST):
            raise