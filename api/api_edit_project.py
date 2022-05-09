from django.http import JsonResponse
from django.db import connection
from django.core.files.storage import FileSystemStorage
from django.shortcuts import redirect
from api.api_general_func import read_json, read_text, dateNow
import requests
import json


cursor = connection.cursor()

def getInfoProject(request) :
    if request.method == 'POST' and request.POST["project_id"]:
        project_id = request.POST["project_id"]
        sql1 = f'SELECT project_name FROM projects WHERE project_id = %s'%project_id
        cursor.execute(sql1)
        prject_name = cursor.fetchall()
        sql2 = f''' SELECT 
                            f.file_id,
                            f.file_name_ori,
                            f.word_now,
                            f.word_upload,
                            f.is_segmented,
                            COUNT(v.version_index),
                            f.create_date
                    FROM 
                            files f,
                            versions v
                    WHERE 
                            f.file_id = v.version_file_id
                        AND
                            f.is_deleted = 0 
                        AND 
                            f.file_project_id = %s 
                        GROUP BY
                            f.file_id,
                            f.file_name_ori,
                            f.word_now,
                            f.word_upload,
                            f.is_segmented,
                            f.create_date
						ORDER BY
                            f.file_id
                '''%(project_id)
        cursor.execute(sql2)
        prject_info = cursor.fetchall()
        arr = [arr_id, arr_name, arr_word, arr_status, arr_version, arr_date] = [], [], [], [], [], []
        for project_details in prject_info:
            arr_val = [ project_details[0],
                        project_details[1][:-5],
                        (str(project_details[2])+'/'+str(project_details[3])), 
                        project_details[4], 
                        project_details[5], 
                        project_details[6]
                        ]
            for list_arr, list_val in zip(arr,arr_val) :
                if list_val == None: list_arr.append("-")
                else: list_arr.append(list_val)
        context = {
            'id':   arr_id,
            'name': arr_name,
            'word': arr_word,
            'date': arr_date,
            'version':  arr_version,
            'status':   arr_status,
            'project_name' : prject_name
        }
    return JsonResponse(context)

def uploadFiles(request) :
    if request.method == 'POST' and request.FILES.getlist('myfile') :
        project_id = request.POST['project_id']
        myfile = request.FILES.getlist('myfile')
        for file_list in myfile:
            path_file = FileSystemStorage().save('./static/upload/original_file/'+file_list.name, file_list)
            file, count_word = wordseg(path_file)
            file_list1 = file_list.name.split('.')[0]+'.json'
            file_type = str(file_list1).split('.')[-1]
            sql1 = f"""  INSERT INTO 
                            files
                                (file_name_ori, 
                                file_name_encrypt, 
                                file_type, 
                                word_upload, 
                                word_now, 
                                versions, 
                                create_date, 
                                file_project_id)
                        VALUES
                            ('%s', 
                            '%s', 
                            '%s', 
                            {count_word}, 
                            {count_word}, 
                            1, 
                            '%s',  
                            {project_id})
                    """
            cursor.execute(sql1 % (file_list1, file, file_type, dateNow()))
            sql2 = f""" INSERT INTO 
                            versions
                                (version_files, 
                                version_index, 
                                version_date, 
                                version_file_id) 
                        VALUES
                            ('%s',
                            1,
                            '%s',
                            (SELECT file_id FROM files WHERE file_name_encrypt = '%s'))
                    """
            cursor.execute(sql2 % (file, dateNow(), file))
            sql3 = f""" INSERT INTO 
                            actions
                                (action_index, 
                                action_date, 
                                action_version_id)
                        VALUES
                            (0, 
                            '%s', 
                            (SELECT version_id FROM versions WHERE version_file_id = (SELECT file_id FROM files WHERE file_name_encrypt = '%s')))
                    """
                        # (1, '{date}', (SELECT version_id FROM versions WHERE version_file_id = (SELECT file_id FROM files WHERE file_name_encrypt = '{file}'))
            cursor.execute(sql3 % (dateNow(), file))
        context = {
            'project_id' : project_id
            }
    return JsonResponse(context)

def wordseg(ori_file) :
    texts = read_text(ori_file, 'r')
    url = "https://lst.nectec.or.th/lst_tools/api/neuswath/v1/tokenize"
    datas = {'text':'{}'.format(texts)}
    headers = {}
    response = requests.request("POST", url, headers=headers, data=datas)
    api_response = response.json()['result']
    for data_response in api_response :
        for index, val in enumerate(data_response.split('|')[:-1]) :
            if index == 0 :
                valu = {index:{"id":index,"val":val,}}
                valu2 = {'action%s'%index:[[],[]]}
                json_dump = json.dumps(valu)
            load = json.loads(json_dump)
            load.update({index:{"id":index,"val":val}})
            json_dump = json.dumps(load, ensure_ascii=False, indent=4).encode('utf-8')
            json_dump2 = json.dumps(valu2, ensure_ascii=False, indent=4).encode('utf-8')
    new_path = ['upload', 'edit', 'action']
    for file in new_path:
        ori_file_save = str(ori_file[30:-4]+'-1.json')
        output_file = './static/upload/segmented_file/'+file+'/'+ori_file_save
        read_json(output_file, 'w', json_dump)
        if file == 'action':
            read_json(output_file, 'w', json_dump2)
    count = count_word(api_response)
    return ori_file_save, count

def count_word(text) :
    count = 1
    for char in text :
        for index in char :
            if index == '|' :
                count+=1
            elif index == ' ' :
                count-=1
    return count

# ! function delete file , get file_id from request.POST
def deleteFiles(request) :
    print(request.POST.getlist('file_id[]'))
    if request.method == 'POST':
        for file_id in request.POST.getlist('file_id[]') :
            print(file_id)
            sql = f""" UPDATE files SET is_deleted = 1 WHERE file_id = {file_id} """
            cursor.execute(sql)
    return JsonResponse({})
