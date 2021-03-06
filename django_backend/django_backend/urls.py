"""django_backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from backend_app import views
from django.conf.urls import include, url

urlpatterns = [
    # path('backend_app/', include('urls')),
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('question_selection/', views.question_selection, name='question_selection'),
    path('qas/', views.qas, name='qas'),
    path('lda/', views.lda, name='lda'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('user_specific_doc_meta/', views.user_specific_doc_meta, name='user_specific_doc_meta'),
    path('update_user_specific_doc_meta/', views.update_user_specific_doc_meta, name='update_user_specific_doc_meta'),
    # url('', include('django_prometheus.urls'))
]
