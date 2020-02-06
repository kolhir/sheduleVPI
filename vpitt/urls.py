"""vpitt URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import path, include
from timetable import views as tt_views
from timetable import ajax_request 
from django.conf.urls.static import static
from django.conf import settings

def trigger_error(request):
    division_by_zero = 1 / 0
    
urlpatterns = [
    path('sentry-debug/', trigger_error),
    path('admin/', admin.site.urls),

    path('api/', include('api.urls')),
    path('edit-schedule/<int:group_id>/', tt_views.edit_schedule),
    path('schedule_list/', tt_views.schedule_list_view),
    path('timetable/done/<int:group_id>/',  tt_views.timetable_done),
    path('add-new-schedules/post/',  tt_views.add_new_schedules_post),
    path('add-new-schedules/',  tt_views.add_new_schedules),
    path('edit_sub_for_group/<int:group_id>/',  tt_views.edit_sub_for_group),
    # path('timetable/', tt_views.table_view),
    path('', tt_views.base_view),
    path('api/tt/', include('timetable.urls')),
    path("save_changes", ajax_request.save_changes),
    path('get_room',  ajax_request.get_room),
    path('get_teacher',  ajax_request.get_teacher),


    path('accounts/', include('accounts.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
