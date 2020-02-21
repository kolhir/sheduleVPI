from django.shortcuts import render,redirect

from django.views.generic import View
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from vpitt.dbfunc import get_user, get_user_profile, \
                        get_faculty, get_list_groups_info, \
                        create_profile, create_group, \
                        set_timetable_to_db, get_lessons, \
                        get_korpus, get_groups_name, get_users_schedules,\
                        get_group_by_id
from .models import Lessons_for_group, Cathedra, Teacher, TeacherCathedra
from . import models
import json


@login_required
def base_view(request):
    set_teachers()
    return render(request, "welcome.html")


@login_required
@require_http_methods(["GET"])
def schedule_list_view(request):
    schedule_list = get_users_schedules(request.user)
    context = {"schedules":schedule_list}
    return render(request, "timetable/schedules_list.html", context)


@login_required
@require_http_methods(["GET"])
def add_new_schedules(request):
    groups = get_list_groups_info()
    c = {"groups": groups}
    return render(request, "timetable/add_new_sch.html", c)


@login_required
@require_http_methods(["POST"])
def add_new_schedules_post(request):
    group = get_group_info(request.POST["name-group"], request.POST["name-kurs"], request.POST["name-semester"])
    group = models.Group.objects.filter(group_info=group)
    if group:
        return redirect("/add-new-schedules")
    if int(request.POST["name-subgroup"]) in [1, 2]:
        group = create_group(request.POST["name-group"],
                             request.POST["name-kurs"],
                             request.POST["name-semester"],
                             1,
                             request.user)
        group = create_group(request.POST["name-group"],
                             request.POST["name-kurs"],
                             request.POST["name-semester"],
                             2,
                             request.user)
    else:
        group = create_group(request.POST["name-group"],
                             request.POST["name-kurs"],
                             request.POST["name-semester"],
                             0,
                             request.user)
    return redirect(f"/edit_sub_for_group/{group.id}")


@require_http_methods(["GET"])
def get_done_shedule_list(request):
    groups = models.Group.objects.filter(group_info__semester=2, added_to_bot=True)
    groups_info = models.Group_info.objects.filter(semester=2)
    done_groups = [item.group_info for item in groups]
    c = {"groups": groups, "groups_info": groups_info, "done_groups": done_groups}
    return render(request, "timetable/shedule_done_list.html", c)


@login_required
@require_http_methods(["GET"])
def edit_sub_for_group(request, group_id):
    method_decorator(csrf_protect)
    group = get_group_by_id(group_id)
    subs = Lessons_for_group.objects.filter(group_info=group.group_info).all()
    c = {"group": group,  "lessons": subs}
    return render(request, "timetable/edit_sub_for_group.html", c)


@login_required
@require_http_methods(["GET"])
def edit_schedule(request, group_id):
    method_decorator(csrf_protect)
    group = get_group_by_id(group_id)
    if group and (group.user_create == request.user):
        context = {"tt_json": "", "lessons": generate_lessons_list(group), "korpus": generate_korpus_list(), "group": group}

        if group.tt_json:
            context["tt_json"] = group.tt_json

        return render(request, "timetable/timediv.html", context)


@login_required
@require_http_methods(["GET"])
def timetable_done(request, group_id):
    set_timetable_to_db(group_id)
    return render(request, "timetable/timetable_done.html")


def set_teachers():
    if len(TeacherCathedra.objects.all()) == 0:
        teachers = Teacher.objects.all()
        TeacherCathedra.objects.all().delete()
        for teacher in teachers:
            maybe_not_one = Teacher.objects.filter(
                first_name=teacher.first_name,
                last_name=teacher.last_name,
                patronymic=teacher.patronymic
            )
            if len(maybe_not_one) > 1:
                for item in maybe_not_one:
                    if len(TeacherCathedra.objects.filter(
                            teacher__first_name=item.first_name,
                            teacher__last_name=item.last_name,
                            teacher__patronymic=item.patronymic,
                            cathedra__name=item.cathedra.name
                            ).all()) == 0:
                        TeacherCathedra.objects.get_or_create(teacher=teacher, cathedra=item.cathedra)
            else:
                TeacherCathedra.objects.get_or_create(teacher=teacher, cathedra=teacher.cathedra)



def generate_lessons_list(group):
    lessons = get_lessons(group)

    lesson_list = {0:"Выберете предмет"}
    for item in enumerate(lessons):
        lesson_list[item[0]+1] = item[1].lesson.name
    lesson_list = json.dumps(lesson_list, ensure_ascii=False)
    return lesson_list


def generate_korpus_list():
    korpus = get_korpus()
    korpus_list = {0: ""}
    for item in enumerate(korpus):
        korpus_list[item[0]+1] = item[1].letter
    korpus_list = json.dumps(korpus_list, ensure_ascii=False)
    return korpus_list

#####################################################################################
#####################################################################################
group = models.Group_info()
def get_caf_list(s):
    l  = []
    if "и" in s:
        l.append(s.replace(" ",""))
    else:
        l.append(s)
    return l

def get_group_info(abbr, course, semester):
    return models.Group_info.objects.filter(abbr=abbr, course=course, semester=semester).get()

def get_lesson_by_name(name):
    from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
    try:
        q = models.Lessons.objects.filter(name=name).get()
        return(q)
    except ObjectDoesNotExist:
        return(False)
    except MultipleObjectsReturned:
        return(False)


lessons = models.Lessons()
def pars_lessons_file():
    number_arr = ["первый", "второй", "третий", "четвертый","пятый", "шестой", "седьмой", "восьмой"]
    name = "data/dekan_data/{}.csv"
    namelist = [
    "ввт",
    "вип",
    "вхт",
    "вэ",
    "вэм"
    ]
    f_dict = {}
    kurs = int()
    group_abbr = str()
    sem = int()
    group_info = int()
    for n in namelist:
        file = open(name.format(n), 'r')

        for line in file:
            line = line.replace("\n","")
            elem = line.split(";")

            if elem[0].lower() == "курс":
                ku = elem[1]
                l = elem[2].split(" ")
                gr = l[len(l)-1].split("-")[0]
                continue

            if elem[0].lower() in number_arr:
                sem = number_arr.index(line.lower())+1
                sem = 1 if sem % 2 != 0 else 2
                group_info = get_group_info(abbr = gr, course = ku, semester = sem)
                continue

            if elem[0] == "" and len(elem) == 1:
                continue

            if elem[1].isdigit():

                caf_lis = get_caf_list(elem[3])
                for n in caf_lis:
                    caf = models.Cathedra.objects.filter(abbr = n).get()
                    lesson = get_lesson_by_name(elem[2])
                    if not(lesson):
                        lesson = models.Lessons(name=elem[2], cathedra=caf)
                    lesson.save()
                    lfg = models.Lessons_for_group(group_info=group_info, lesson= lesson)
                    lfg.save()
            print(gr, ku, sem, "||||DONE|||||")


def get_fam_lesson_dict():
    name = "data/dekanfam.xls"

    def RepresentsInt(s):
        try:
            return int(s)
        except ValueError:
            return False

    import re
    import xlrd
    rb = xlrd.open_workbook(name,
                            formatting_info=True)
    cafedra_list = []
    sub_dict = {}
    for i in range(33):
        sheet = rb.sheet_by_index(i)
        group_name = ""
        for item in sheet.row_values(0):
            group_name_re = re.search(r'[А-Я]{2}[-А-Я]{1}[-0-9]{1}[0-9]{2,3}', item)
            if group_name_re:
                group_name = group_name_re.group(0)
                sub_dict.update({group_name: {}})
        if group_name:
            counter = 0
            semester = 0
            for item in range(4, sheet.nrows - 3):
                if RepresentsInt(sheet.row_values(item)[1]) == 1:
                    counter = 1
                    semester += 1
                    sub_dict[group_name].update({semester: {}})
                if (RepresentsInt(sheet.row_values(item)[1])):
                    cafedra = sheet.row_values(item)[12]
                    if cafedra == 'ВАЭ':
                        cafedra = 'ВАЭиВТ'
                    sub_dict[group_name][semester].update({counter: (sheet.row_values(item)[2],
                                                                     cafedra.replace(' ', ''))})
                    cafedra_list.append(cafedra.replace(' ', ''))
                    counter += 1
    import pprint
    pprint.pprint(sub_dict)
    return sub_dict


def pars_fam_lessons():
    # 'СТ-15-1-2': {1: {1: ('Правоведение (Основы законодательства в строительстве)',
    #                       'ВСГ'),
    #                   2: ('Техническая механика', 'ВСТПМ'),
    #                   3: ('Социология', 'ВСГ'),
    #                   4: ('Конструкции городских сооружений и зданий', 'ВСТПМ'),
    #                   5: ('Основания и фундаменты', 'ВСТПМ'),
    #
    #               2: {1: ('Теплогазовентиляция', 'ВСТПМ'),
    #                   2: ('Водоотведение и водоснабжение', 'ВСТПМ'),
    #                   3: ('Физическая культура', 'ВКФ'),
    #                   4: ('Политология', 'ВСГ'),
    #
    #                        'ВСТПМ')}},

    sub_dict = get_fam_lesson_dict()
    sub_dict.pop('НТС-15', None)
    for group in sub_dict:
        for semester in sub_dict[group]:
            group_info = models.Group_info.objects.filter(abbr=group.split('-')[0], course=group.split('-')[1][:1], semester=semester).get()
            for lesson in sub_dict[group][semester]:
                current_val = sub_dict[group][semester][lesson]
                cafedra = models.Cathedra.objects.filter(abbr=current_val[1]).get()
                lesson_from_db = get_lesson_by_name(current_val[0])
                if not (lesson_from_db):
                    lesson_from_db = models.Lessons(name=current_val[0], cathedra=cafedra)
                lesson_from_db.save()
                lfg = models.Lessons_for_group(group_info=group_info, lesson=lesson_from_db)
                lfg.save()
            print(group, semester, group_info, "__________DONE__________")

# if len(models.Lessons.objects.filter()) == 0:
#     pars_lessons_file()
# elif len(models.Lessons.objects.filter()) > 0 :
#     lessons_for_del = models.Lessons.objects.filter()
#     group_lessons = models.Lessons_for_group.objects.filter()
#     for item1 in lessons_for_del:
#         item1.delete()
#     for item2 in  group_lessons:
#         item2.delete()
#     pars_lessons_file()
#     pars_fam_lessons()
