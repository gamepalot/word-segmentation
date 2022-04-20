from django.http import JsonResponse, HttpResponse
from django.db import connection

cursor = connection.cursor()

def use_version(request):
    if request.method == 'POST':
        sql = f"""  UPDATE 
                        files
                    SET
                        versions = {request.POST['version']}
                    WHERE
                        is_deleted = 0
                        AND
                        file_name_encrypt = '{request.POST['file_encrypt']}'
                """
        cursor.execute(sql)
    return JsonResponse({'version': '1.0.0'})