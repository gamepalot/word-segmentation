from django.http import JsonResponse, HttpResponse
from django.db import connection
# from django.views.decorators.csrf import csrf_protect
from api.api_general_func import read_json, read_text
from api.api_filterfiles_edit import replace_list
from django.core.files.storage import FileSystemStorage

cursor = connection.cursor()

def fileterFiles(request):
    if request.method == "POST":
        project_id = request.POST['project_id']
        sql = f"""  SELECT
                        f.file_name_ori,
                        f.file_id,
                        f.file_name_encrypt
                    FROM 
                        files f
                    WHERE  
                        f.is_deleted = 0
                        AND
                        f.file_project_id = {project_id}"""
        cursor.execute(sql)
        data = cursor.fetchall()
        arr = [arr_val_id, arr_val_name, arr_val_name_encrypt] = [], [], []
        for i in data:
            arr_val = [i[1], i[0], i[2]]
            for list_arr, list_val in zip(arr,arr_val) :
                list_arr.append(list_val)
        context = {
            "id": arr_val_id,
            "name": arr_val_name,
            "name_encrypt": arr_val_name_encrypt
        }
    return JsonResponse(context)

def selectFiles(request):
    if request.method == "POST":
        filename = request.POST['file_encrypt']
        sql = f"""   SELECT 
                        v.version_files, f.versions
                    FROM
                        versions v,
                        files f
                    WHERE
                        f.file_id = v.version_file_id
                        AND
                        f.file_name_encrypt = '{filename}';"""
        cursor.execute(sql)
        file_list = cursor.fetchall()
        path_file = './static/upload/segmented_file/'
        context = {}
        replace1 = []
        context_list = {}
        for filename in file_list:
            list_arr = []
            filename = filename[0]
            raw_data = read_json(path_file + 'edit/' + filename) #! Function
            action_data = read_json(path_file + 'action/' + filename) #! Function
            
            # arr_id_seg = []
            # arr_data_seg = []
            
            for actions_count, actions in enumerate(action_data.keys()) :
                if actions == 'action0' :
                    arr = [int(index) for index in raw_data.keys()]
                else :
                    default_val = action_data[actions][0]
                    replace_val = action_data[actions][1]
                    arr = replace_list(arr, default_val, replace_val) #! Function
                    replace1.extend(replace_val)
            for arr_list in arr:
                if arr_list in replace1:
                    list_arr.append('<span class="bg-danger mx-1 text-black rounded">%s</span>'%(raw_data[str(arr_list)]['val']))
                else:
                    list_arr.append(raw_data[str(arr_list)]['val'])
            context_list[filename] = list_arr
        context['segmented_file'] = context_list
        context['current'] = file_list[0][1]
        return JsonResponse(context)

def export(request):
    filename = request.POST['file_encrypt']
    path_file = './static/upload/segmented_file/'
    raw_data = read_json(path_file + 'edit/' + filename) #! Function
    action_data = read_json(path_file + 'action/' + filename) #! Function
    list_arr = []
    arr_id_seg = []
    arr_data_seg = []
    context = {}
    for actions_count, actions in enumerate(action_data.keys()) :
        if actions == 'action0' :
            arr = [int(index) for index in raw_data.keys()]
        else :
            default_val = action_data[actions][0]
            replace_val = action_data[actions][1]
            arr = replace_list(arr, default_val, replace_val) #! Function
            # arr_list.append(arr)
    txt = ''
    for arr_list in arr:
        txt += raw_data[str(arr_list)]['val']+'|'
    export_file = './static/export/'+filename.split('.')[0]+'.txt'
    read_text(export_file, 'w', txt) #! Function
    context['filename'] = filename.split('.')[0]+'.txt'
    return JsonResponse(context)