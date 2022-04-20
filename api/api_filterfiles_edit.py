from django.http import JsonResponse
from django.db import connection
from api.api_general_func import read_json, read_text, dateNow

cursor = connection.cursor()

def getIndex(source, sequence):
    return source.index(sequence[0]), source.index(sequence[-1])+1

def replace_list(source, sequence, replace):
    start, end = getIndex(source, replace) #! Function
    source[start:end] = []
    start, end = getIndex(source, sequence) #! Function
    source[start:end] = replace
    return source

def fileterFiles(request):
    if request.method == "POST":
        project_id = request.POST['project_id']
        sql = f"""  SELECT
                        f.file_name_ori,
                        f.file_id,
                        v.version_files 
                    FROM 
                        files f, 
                        versions v 
                    WHERE 
                        v.version_index = f.versions 
                        AND 
                        f.file_id = v.version_file_id 
                        AND
                        f.is_deleted = 0
                        AND 
                        file_project_id = {project_id}
                        """
        cursor.execute(sql)
        data = cursor.fetchall()
        arr = [arr_file_id, arr_file_name, arr_file_name_encrypt] = [], [], []
        for val_list in data:
            arr_val = [val_list[1], val_list[0], val_list[2]]
            for list_arr, list_val in zip(arr,arr_val) :
                list_arr.append(list_val)
        context = {
            "id": arr_file_id,
            "name": arr_file_name,
            "name_encrypt": arr_file_name_encrypt
        }
    return JsonResponse(context)

def selectFiles(request):
    if request.method == "POST":
        context = {}
        arr, arr_data_seg, arr_id_seg = [], [] ,[]
        filename = request.POST['file_encrypt']
        path_file = './static/upload/segmented_file/'
        sql = f"""  SELECT 
                        ac.action_index 
                    FROM 
                        versions v,
                        actions ac 
                    WHERE 
                        v.version_id = ac.action_version_id
                        AND
                        v.version_files = '{filename}';
                """
        cursor.execute(sql)
        action_index = cursor.fetchone()
        action_index = action_index[0]
        original_data = read_json(path_file+'upload/'+filename) #! Function
        original_data = [original_data[data]['val'] for data in original_data.keys()]
        context['original_file'] = original_data
        raw_data = read_json(path_file + 'edit/' + filename) #! Function
        action_data = read_json(path_file + 'action/' + filename) #! Function
        
        for actions_count, actions in enumerate(action_data.keys()) :
            if actions == 'action0' :
                if action_index == 0 :
                    upload_data = read_json(path_file + 'upload/' + filename) #! Function
                    arr = [int(index) for index in upload_data.keys()]
                    break
                else:
                    arr = [int(index) for index in raw_data.keys()]
                    if len(action_data) != action_index+1 : 
                        if len(action_data) > action_index+1 : 
                            # arr = arr[:-(len(action_data)-(action_index))]
                            arr = arr[:arr.index(action_data['action%s'%action_index][1][-1]+1)]
                        # else: arr = arr[:-((action_index)-len(action_data))]
            else :
                default_val = action_data[actions][0]
                replace_val = action_data[actions][1]
                arr = replace_list(arr, default_val, replace_val) #! Function
                if actions_count == action_index : break
        for arr_list in arr:
            arr_id_seg.append(raw_data[str(arr_list)]['id'])  
            arr_data_seg.append(raw_data[str(arr_list)]['val'])  
        version = getVersion(filename) #! Function
        context['version'] = version
        context['id'] = arr_id_seg
        context['segmented_file'] = arr_data_seg
        context['action_index'] = action_index
        context['action_count'] = len(action_data.keys())-1
    return JsonResponse(context)

def getVersion(filename):
    sql = """   SELECT
                    f.file_id, 
                    f.versions
                FROM
                    files f,
                    versions v
                WHERE
                    v.version_file_id = f.file_id
                    AND 
                    v.version_files = '%s'
            """
    cursor.execute(sql%filename)
    data1 = cursor.fetchone()
    sql = """  SELECT
                    COUNT(version_index)
                FROM
                    versions
                WHERE
                    version_file_id = %s
    """
    cursor.execute(sql % data1[0])
    data2 = cursor.fetchone()
    if data1[1] == data2[0]:
        # print('if :',(data1[1],data2[0]))
        return data2[0]
    else:
        # print('else :',(data1[1],data2[0]))
        return data2[0]+1