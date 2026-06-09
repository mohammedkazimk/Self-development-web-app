"""
URL configuration for Lets_Progress project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
"""
URL configuration for Lets_Progress project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from django.urls import path
from app.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('namaz/', namaz, name='namaz'),
    path('new-namaz-entry/', new_namaz_entry, name='new_namaz_entry'),
    path('quran/daily/', quran_daily, name='quran_daily'),
    path('quran/daily/entry/', quran_daily_entry, name='quran_daily_entry'),
    path('sleep-tracking/',sleep_track_home, name="sleep_track"),
    path('sleep-tracking/entry/', sleep_track_entry, name="sleep_track_entry"),
    path('college-studies/',college_studies_home,name="college_studies"),
    path('college-studies/entry/',college_studies_entry,name="college_studies_entry"),
    path('college-studies/notes/',notes,name='notes'),
    path('report/', generate_pdf, name='generate_pdf'),
    path('login/', login_function, name='login'),
    path('logout/', logout_function, name='logout'),
]
