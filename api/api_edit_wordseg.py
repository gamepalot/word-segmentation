from django.http import JsonResponse
from django.db import connection
from django.shortcuts import redirect
from api.api_general_func import read_json
from api.api_filterfiles_edit import replace_list
from api.api_filterfiles_edit import selectFiles
from api.api_general_func import read_json, dateNow
import json
import re

cursor = connection.cursor()

def updateActions(filename, action=None):
    if action == None :
        sql = """   UPDATE 
                        actions
                    SET
                        action_index = action_index + 1,
                        action_date = '%s'
                    WHERE
                        action_version_id = (
                                                SELECT 
                                                    v.version_id 
                                                FROM 
                                                    versions v, 
                                                    files f 
                                                WHERE 
                                                    v.version_file_id = f.file_id 
                                                    AND 
                                                    v.version_files = '%s'
                                            )
            """
    else :
        sql = """   UPDATE 
                        actions
                    SET
                        action_index = action_index - 1,
                        action_date = '%s'
                    WHERE
                        action_version_id = (
                                                SELECT 
                                                    v.version_id 
                                                FROM 
                                                    versions v
                                                WHERE 
                                                    v.version_files = '%s'
                                            )
            """
    cursor.execute(sql % (dateNow(), filename))

def replaceActions(filename,action):
    sql = """   UPDATE 
                    actions
                SET
                    action_index = %s,
                    action_date = '%s'
                WHERE
                    action_version_id = (
                                            SELECT 
                                                v.version_id 
                                            FROM 
                                                versions v
                                            WHERE 
                                                v.version_files = '%s'
                                        )
            """
    cursor.execute(sql % (action, dateNow(), filename))

def getDataClients(request):
    filename = request.POST['file_encrypt']
    id = request.POST.getlist('id[]')
    val_text = request.POST.getlist('text[]')
    filename_edit = "./static/upload/segmented_file/edit/"+filename
    filename_action = "./static/upload/segmented_file/action/"+filename
    action_index = request.POST['action']
    return filename, id, val_text, filename_edit, filename_action, action_index

def function_merge(request):
    if request.method == 'POST':
        filename, id, val_text, filename_edit, filename_action, action_index = getDataClients(request) #! Function
        data_value = read_json(filename_edit) #! Function
        data_action = read_json(filename_action) #! Function
        if int(action_index) != len(data_action.keys())-1:
            data_value, data_action = remove_action(request,int(action_index),data_value,data_action) #! Function
        new_keys = int(list(set([int(x) for x in data_value.keys()]))[-1])+1
        data_value[new_keys] = {'id':new_keys, 'val':''.join(val_text)}
        json_dump = json.dumps(data_value, ensure_ascii=False, indent=4).encode('utf-8')
        read_json(filename_edit, 'w', json_dump) #! Function
        action_count = len(data_action.keys())
        arr_id = [int(id_list) for id_list in id]
        data_action['action%s'%action_count] = [arr_id,[new_keys]]
        json_dump2 = json.dumps(data_action, ensure_ascii=False, indent=4).encode('utf-8')
        read_json(filename_action, 'w', json_dump2) #! Function
        updateActions(filename) #! Function
    return selectFiles(request) #! Function

def function_edit(request) :
    if request.method == 'POST':
        filename, id, val_text, filename_edit, filename_action, action_index = getDataClients(request) #! Function
        data_value = read_json(filename_edit) #! Function
        data_action = read_json(filename_action) #! Function
        if int(action_index) != len(data_action.keys())-1:
            data_value, data_action = remove_action(request,int(action_index),data_value,data_action) #! Function
        new_keys = int(list(set([int(x) for x in data_value.keys()]))[-1])+1
        data_value[new_keys] = {'id':new_keys, 'val':''.join(val_text)}
        json_dump = json.dumps(data_value, ensure_ascii=False, indent=4).encode('utf-8')
        read_json(filename_edit, 'w', json_dump) #! Function
        action_count = len(data_action.keys())
        data_action['action%s'%action_count] = [[int(id[0])],[new_keys]]
        json_dump2 = json.dumps(data_action, ensure_ascii=False, indent=4).encode('utf-8')
        read_json(filename_action, 'w', json_dump2) #! Function
        updateActions(filename) #! Function
    return selectFiles(request) #! Function

def function_split(request) : 
    if request.method == 'POST':
        filename, id, val_text, filename_edit, filename_action, action_index = getDataClients(request) #! Function
        val_text = ''.join(val_text[:]).split('|')
        arr_split = []
        data_value = read_json(filename_edit)
        data_action = read_json(filename_action)
        if int(action_index) != len(data_action.keys())-1:
            data_value, data_action = remove_action(request,int(action_index),data_value,data_action) #! Function
        new_keys = int(list(set([int(x) for x in data_value.keys()]))[-1])+1
        for val_str in range(len(val_text)) :
            arr_split.append(new_keys+val_str)
            data_value[new_keys+val_str] = {'id': new_keys+val_str, 'val': val_text[val_str]}
        json_dump = json.dumps(data_value, ensure_ascii=False, indent=4).encode('utf-8')
        read_json(filename_edit, 'w', json_dump) #! Function
        action_count = len(data_action.keys())
        data_action['action%s'%action_count] = [[int(id[0])], arr_split]
        json_dump2 = json.dumps(data_action, ensure_ascii=False, indent=4).encode('utf-8')
        read_json(filename_action, 'w', json_dump2) #! Function
        updateActions(filename) #! Function
    return selectFiles(request) #! Function

def reAction_undo(request):
    if request.method == 'POST':
        filename = request.POST['file_encrypt']
        updateActions(filename, 'delete') #! Function
        return selectFiles(request) #! Function

def reAction_redo(request):
    if request.method == 'POST':
        filename = request.POST['file_encrypt']
        updateActions(filename) #! Function
        return selectFiles(request) #! Function

def remove_action(request, action_index, data_value, data_action):
    if request.method == 'POST':
        for key_action in range(action_index, len(data_action.keys())):
            if key_action != action_index and key_action >= action_index:
                for key_val in data_action['action%s'%key_action][1]:
                    del data_value[str(key_val)]
                # del data_value[str(data_action['action%s'%key_action][1][0])]
                del data_action['action%s'%key_action]
        replaceActions(request.POST['file_encrypt'], action_index) #! Function
        return data_value, data_action
    
def keepVersion(request):
    if request.method == "POST" :
        filename = request.POST['filename']
        # ! Query sql 1
        sql1 = """   SELECT 
                        MAX(v.version_index) 
                    FROM 
                        versions v,
                        files f 
                    WHERE
                        v.version_file_id = f.file_id 
                        AND
                        v.version_files = '{0}';"""
        cursor.execute(sql1.format(filename))
        version_index_now = cursor.fetchone()[0]+1
        
        # ! Query sql 2
        sql2 = """  INSERT INTO versions
                        (   
                            version_files, 
                            version_index, 
                            version_date, 
                            version_file_id
                        )
                    VALUES 
                        (   
                            '{2}', 
                            (
                                SELECT 
                                    MAX(v.version_index)+1
                                FROM 
                                    versions v,
                                    files f
                                WHERE
                                    v.version_file_id = f.file_id 
                                    AND 
                                    v.version_files = '{0}'
                            ), 
                            '{1}', 
                            (
                                SELECT 
                                    file_id 
                                FROM 
                                    files f,
                                    versions v
                                WHERE 
                                    v.version_file_id = f.file_id 
                                    AND 
                                    v.version_files = '{0}'
                                    LIMIT 1
                            )
                        );
                        """
        cursor.execute(sql2.format(filename, 
                                    dateNow(), 
                                    re.sub( r'-\d.json', '-'+str(version_index_now)+'.json', filename)))
        
        # ! 
        sql3 = """  UPDATE 
                        files
                    SET 
                        versions = {1}
                    WHERE 
                        file_id = (
                                    SELECT 
                                        f.file_id 
                                    FROM 
                                        files f, 
                                        versions v 
                                    WHERE 
                                        f.file_id = v.version_file_id 
                                        AND 
                                        v.version_files = '{0}'
                                        LIMIT 1
                                    );
                """
        cursor.execute(sql3.format( filename, 
                                    version_index_now))
        
        # ! query sql 4
        sql4 = """INSERT INTO actions
                    (
                        action_index,
                        action_date,
                        action_version_id
                    )
                    VALUES
                    (
                        0,
                        '{1}',
                        (
                            SELECT
                                MAX(v.version_id)
                            FROM
                                versions v,
                                files f
                            WHERE
                                v.version_file_id = (
                                    SELECT 
                                        f.file_id
                                    FROM
                                        files f,
                                        versions v
                                    WHERE
                                        f.file_id = v.version_file_id
                                        AND 
                                        v.version_files = '{0}'
                                        LIMIT 1
                                    )
                        )
                    )"""
        cursor.execute(sql4.format(filename, dateNow()))
        cutVersion(filename, version_index_now) #! Function
    return JsonResponse({})

def cutVersion(filename, version_index_now):
    path_file = './static/upload/segmented_file/'
    raw_data = read_json(path_file + 'edit/' + filename) #! Function
    action_data = read_json(path_file + 'action/' + filename) #! Function
    arr_list = []
    json_format = {}
    for actions_count, actions in enumerate(action_data.keys()) :
        if actions == 'action0' :
            arr = [int(index) for index in raw_data.keys()]
        else :
            default_val = action_data[actions][0]
            replace_val = action_data[actions][1]
            arr = replace_list(arr, default_val, replace_val) #! Function
            # arr_list.append(arr)
    for arr_list in arr:
            # arr_id_seg.append(raw_data[str(arr_list)]['id'])  
            # arr_data_seg.append(raw_data[str(arr_list)]['val'])
            json_format[raw_data[str(arr_list)]['id']] = raw_data[str(arr_list)]
    new_filename = re.sub(r'-\d.json','-'+str(version_index_now)+'.json', filename)
    json_dump = json.dumps(json_format, indent=4, ensure_ascii=False).encode('utf-8')
    read_json(path_file + 'edit/' + new_filename,'w', json_dump ) #! Function
    read_json(path_file + 'upload/' + new_filename,'w', json_dump ) #! Function
    json_dump2 = json.dumps({'action0':[[],[]]} ,indent=4, ensure_ascii=False).encode('utf-8')
    read_json(path_file + 'action/' + new_filename,'w', json_dump2) #! Function
