from django.shortcuts import render, redirect
from django.urls import reverse
from django.db import connection
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from .models import *
from datetime import datetime
import os

cursor = connection.cursor()
now = datetime.now().date()


def Loginpage(request):
    return render(request, 'login/login.html')


def login(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(username=username, password=password)
    if user is not None:
        auth_login(request, user)
        return redirect('/')
    else:
        return redirect('/loginpage')

@login_required(login_url='/loginpage')
def Homepage(request) :
    sql = """   SELECT 
                    pj.*
                FROM 
                    projects pj, 
                    users us 
                WHERE 
                    pj.project_user_id = us.user_id
                    AND
                    pj.is_deleted = 0 
                    AND 
                    us.user_id = {} ; """
    cursor.execute(sql.format(request.user.user_id))
    data = cursor.fetchall()
    list_project = []
    for i in data:
        sql2 = """  SELECT 
                        COUNT(*),
                        (
                            SELECT 
                                COUNT(*)
                            FROM 
                                files
                            WHERE
                                file_project_id = {0}
                        )
                    FROM 
                        files f
                    WHERE
                        f.is_segmented = 1
                        AND 
                        f.is_deleted = 0
                        AND
                        f.file_project_id = {0} ; """
        cursor.execute(sql2.format(i[0]))
        data2 = cursor.fetchone()
        list_project.append(i+data2)
    context = {}
    context['data'] = list_project
    return render(request, 'index.html' , context)

@login_required(login_url='/loginpage')
def Segmentaionpage(request, **kwargs):
    project_id = request.GET.get('project_id')
    file_id = request.GET.get('file_id')
    sql = f"SELECT project_name, project_id FROM projects WHERE is_deleted = 0 AND project_user_id = {request.user.user_id}"
    cursor.execute(sql)
    data = cursor.fetchall()
    context = {}
    if not file_id and not project_id:
        context['project_name'] = data
    else:
        context['project_name'] = data
        context['project_id'] = int(project_id)
        context['file_id'] = file_id
    return render(request, 'segmentaion.html', context)

@login_required(login_url='/loginpage')
def Versionpage(request):
    project_id = request.GET.get('project_id')
    file_id = request.GET.get('file_id')
    sql = f"SELECT project_name, project_id FROM projects WHERE is_deleted = 0 AND project_user_id = {request.user.user_id}"
    cursor.execute(sql)
    data = cursor.fetchall()
    context = {}
    if not file_id and not project_id:
        print('no file_id')
        context['project_name'] = data
    else:
        print('file_id')
        context['project_name'] = data
        context['project_id'] = int(project_id)
        context['file_id'] = file_id
    return render(request, 'version.html', context)


def logout(request):
    auth_logout(request)
    return redirect('/loginpage')

@login_required(login_url='/loginpage')
def add_project(request) :
    project_name = request.GET['project_name']
    sql = f"INSERT INTO projects (project_user_id, project_name, project_create_date) values({request.user.user_id}, '{project_name}', '{now}')"
    cursor.execute(sql)
    return redirect('/')

@login_required(login_url='/loginpage')
def delete_project(request):
    project_id = request.GET['project_id']
    sql = f"UPDATE files SET is_deleted = 1 WHERE file_project_id = {project_id}; UPDATE projects SET is_deleted = 1 WHERE project_id = {project_id}"
    cursor.execute(sql)
    return redirect('/')
