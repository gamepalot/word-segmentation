from django.http import JsonResponse, HttpResponse
# from django.db import connection
from datetime import datetime
import pytz
import json
import io

def read_json(filename, mode='r', json_data=None):
    if mode is not 'r' :
        with open(filename, mode, encoding='utf_8') as f:
            f.write(json_data.decode())

    else :
        with open(filename, mode, encoding='utf_8') as f:
            data = json.load(f)
        return data

def read_text(filename, mode='r', text_data=None):
    if mode is not 'r' :
        with io.open(filename, mode, encoding='utf_8') as f:
            f.write(text_data)
        
    else :
        with io.open(filename, mode, encoding='utf_8') as f:
            data = f.read()
        return data

def dateNow():
    return datetime.now(pytz.timezone('Asia/Bangkok')).strftime("%Y-%m-%d %H:%M:%S")