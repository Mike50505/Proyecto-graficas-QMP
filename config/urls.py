from django.urls import path, include
from django.contrib import admin
from audits import views
urlpatterns = [path('admin/',admin.site.urls),path('cuentas/',include('django.contrib.auth.urls')),path('',views.dashboard,name='dashboard'),path('presentacion/',views.dashboard,{'presentation':True},name='presentation'),path('importar/',views.upload,name='upload'),path('datos/',views.data,name='data'),path('exportar/',views.export,name='export'),path('auditoria/<int:pk>/',views.detail,name='detail')]
