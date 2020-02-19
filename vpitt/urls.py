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
    path('done-schedules/',  tt_views.get_done_shedule_list),
    # path('timetable/', tt_views.table_view),
    path('', tt_views.base_view),
    path('api/tt/', include('timetable.urls')),
    path("save_changes", ajax_request.save_changes),
    path('get_room',  ajax_request.get_room),
    path('get_teacher',  ajax_request.get_teacher),


    path('accounts/', include('accounts.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
