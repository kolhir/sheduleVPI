from django.urls import path, include
from .views import get_user, \
	add_new_user, \
	get_list_groups, \
	set_group_for_user, \
	get_subgroup_for_group, \
	get_abbr_groups, \
	get_groups_for_abbr, \
	get_group_name_list, \
	get_time_dict, \
	get_user_group, \
	reset_user_group, \
	get_current_day_timetable, \
	get_day_timetable,\
	get_teacher_all


urlpatterns = [

	path('get_user/<int:user_id>/', get_user),
	path('add_new_user/', add_new_user),
	path('get_user_group/<int:user_id>/', get_user_group),
	path('get_list_groups/<int:course>/<int:semester>/', get_list_groups),
	path('set_group_for_user/', set_group_for_user),
	path('get_subgroup_for_group/', get_subgroup_for_group),
	path('get_abbr_groups/', get_abbr_groups),
	path('get_group_name_list/', get_group_name_list),
	path('get_groups_for_abbr/', get_groups_for_abbr),
	path('get_time_dict/', get_time_dict),
	path('reset_user_group/<int:user_id>/', reset_user_group),
	path('get_current_day_timetable/<int:user_id>/', get_current_day_timetable),
	path('get_day_timetable/<int:user_id>/<int:day_number>/<int:number_week>/', get_day_timetable),
	path('get_teacher_all/<str:fam>/', get_teacher_all)
]