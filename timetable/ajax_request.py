from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from vpitt.dbfunc import  get_lesson_by_name, get_teacher_by_caf, \
                        get_korpus_by_name, get_rooms_by_korpus, print_message, \
                        get_group_by_id
import json
from ast import literal_eval

@login_required
@require_http_methods(["POST"])
def get_teacher(request):
    name = request.POST["name"]
    lesson = get_lesson_by_name(name)
    
    teachers = get_teacher_by_caf(lesson.cathedra)
    teachers_dict = {0:"Выберете преподавателя"}
    for item in enumerate(teachers):
        s = (item[1].last_name) + " " + item[1].first_name[:1] + ". " + item[1].patronymic[:1] + "."
        teachers_dict[item[0]+1] = s
    teachers_dict = json.dumps(teachers_dict, ensure_ascii=False)
    return HttpResponse(teachers_dict)

@login_required
@require_http_methods(["POST"])
def get_room(request):
    name = request.POST["name"]
    korpus = get_korpus_by_name(name)
    rooms = get_rooms_by_korpus(korpus)
    rooms_dict = {0:""}
    for item in enumerate(rooms):
        s = (item[1].number)
        rooms_dict[item[0]+1] = s
    rooms_dict = json.dumps(rooms_dict, ensure_ascii=False)
    return HttpResponse(rooms_dict)

@login_required
@require_http_methods(["POST"])
def save_changes(request):
    var = literal_eval(list(request.POST.keys())[0])
    json_from_user = var["0"]
    group = get_group_by_id(int(json_from_user["id"]))
    group.tt_json = json_from_user
    group.save()
    return HttpResponse(200)
