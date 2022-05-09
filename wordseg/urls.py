from django.contrib import admin
from django.urls import path, include, re_path
from wordseg_app import views
from api import api_edit_project, api_filterfiles_edit, api_filterfiles_version, api_edit_wordseg, api_edit_version

urlpatterns = [
    # admin page (http://127.0.0.1:8000/admin/)
    path('admin/', admin.site.urls),

    # Index page (http://127.0.0.1:8000/)
    path('', views.Homepage, name='homepage'),

    # Segmentation page (http://127.0.0.1:8000/segmentaion)
    path('segmentation/',views.Segmentaionpage, name='segmentation'),
    re_path(r'^segmentation/(?P<slug>.*)/$', views.Segmentaionpage, name='segmentation'),

    # Segmentation page (http://127.0.0.1:8000/segmentaion)
    path('version/', views.Versionpage, name='version'),

    # Function (http://127.0.0.1:8000/{currentpage}/{function})
    path('add/', views.add_project),
    path('loginpage/', views.Loginpage),
    re_path(r'login$', views.login, name='login'),
    re_path(r'logout$', views.logout, name='logout'),
    path('deletepj/', views.delete_project),

    # API (http://127.0.0.1:8000/{Currentpage}/{API})
    # ! index page
    re_path(r'getinfoproject$', api_edit_project.getInfoProject, name='getinfoproject'),
    re_path(r'uploadfiles$', api_edit_project.uploadFiles, name='uploadfiles'),
    re_path(r'deletefiles$', api_edit_project.deleteFiles, name='deletefiles'),

    # ! segmentation page
    path('segmentation/filterfiles', api_filterfiles_edit.fileterFiles),
    path('segmentation/selectfiles', api_filterfiles_edit.selectFiles),
    # re_path(r'saveValues$', api_edit_wordseg.saveValues),
    re_path(r'keepVersion$', api_edit_wordseg.keepVersion),
    re_path(r'merge$', api_edit_wordseg.function_merge),
    re_path(r'split$', api_edit_wordseg.function_split),
    re_path(r'edit$', api_edit_wordseg.function_edit),
    re_path(r'undo$', api_edit_wordseg.reAction_undo),
    re_path(r'redo$', api_edit_wordseg.reAction_redo),

    # ! version page
    path('version/filterfiles', api_filterfiles_version.fileterFiles),
    path('version/selectfiles', api_filterfiles_version.selectFiles),
    re_path(r'export$',api_filterfiles_version.export),
    re_path(r'use_version$', api_edit_version.use_version),
]
