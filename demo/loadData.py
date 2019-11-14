import os
import django
import yaml

import time, statistics

from django.utils import timezone

from myWX_l_ningmo import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myWX_l_ningmo.settings')
django.setup()

def init_app_data():
    data_file = os.path.join(settings.BASE_DIR, 'app.yaml')
    with open(data_file, 'r', encoding='utf-8') as f:
        apps = yaml.load(f, Loader=yaml.FullLoader)
        return apps

if __name__ == '__main__':
    init_app_data()