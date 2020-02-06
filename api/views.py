from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from timetable.models import Group_info, Group, LessonTime, Time_table
from accounts.models import BotUser
from .serializers import UserSerializer, GroupInfoListSerializer, LessonTimeSerializer, Time_tableOnDaySerializer
from vpitt.dbfunc import print_message
from django.http import HttpResponse
from vpitt import dbfunc
from datetime import datetime
#NEW VIEWS

@api_view(['POST'])
def add_new_user(request):
    if request.method == 'POST':
        user = dbfunc.add_new_bot_user(request.POST)
    return HttpResponse(200)

@api_view(['GET'])
def get_abbr_groups(request):
    group = Group_info.objects.filter(course=1, semester=1)
    serializer = GroupInfoListSerializer(group, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_group_name_list(request):
    group = Group_info.objects.filter(semester=1)
    serializer = GroupInfoListSerializer(group, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def get_groups_for_abbr(request):
    group = Group_info.objects.filter(abbr=request.POST['abbr'], semester=1)
    serializer = GroupInfoListSerializer(group, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def set_group_for_user(request):
    """
    :param request:
    "user_id"
    "course"
    "semester"
    "abbr"
    "subgroup"
    "code"
    """
    data = request.POST
    group_info = Group_info.objects.filter(abbr=data["abbr"],
                                           course=data["course"],
                                           code=data["code"],
                                           semester=data["semester"]).first()

    if data["subgroup"] == 0:
        pass
    group = Group.objects.filter(group_info=group_info, subgroup=data["subgroup"]).first()
    users = BotUser.objects.filter(user_id=data["user_id"]).first()
    users.group = group
    users.save()
    return HttpResponse(200)

########################################
'''
Методы для DataProcessor
'''
@api_view(['GET'])
def get_time_dict(request):
    times = LessonTime.objects.all()
    serializer = LessonTimeSerializer(times, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_current_day_timetable(request, user_id):
    group = BotUser.objects.filter(user_id=user_id).first().group
    number_week = (datetime.now().isocalendar()[1]%2+1)
    day_number = datetime.now().isocalendar()[2]
    timetable = Time_table.objects.filter(group=group, day=day_number, number_week=number_week)
    return Response(Time_tableOnDaySerializer(timetable,  many=True).data)

@api_view(['GET'])
def get_day_timetable(request, user_id, day_number, number_week):
    group = BotUser.objects.filter(user_id=user_id).first().group
    day_number = day_number
    timetable = Time_table.objects.filter(group=group, day=day_number, number_week=number_week)
    print_message(timetable)
    return Response(Time_tableOnDaySerializer(timetable, many=True).data)

@api_view(['GET'])
def get_teacher_all(request, fam):
    HttpResponse(200)

########################################
@api_view(['GET'])
def get_user(request, user_id):
    if request.method == 'GET':
        try:
            users = BotUser.objects.filter(user_id=user_id)
            if users:
                serializer = UserSerializer(users, many=True)
                return Response(serializer.data)
            else:
                raise Exception("Нет такого пользователя")
        except Exception as e:
            print_message(e)
            return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def reset_user_group(request, user_id):
    user = BotUser.objects.filter(user_id=user_id).first()
    user.group_id = None
    user.save()
    if user:
        return HttpResponse(200)
    else:
        return Response(status=status.HTTP_402_PAYMENT_REQUIRED)

@api_view(['GET'])
def get_user_group(request, user_id):
    group = BotUser.objects.filter(user_id=user_id).first().group
    if group:
        return HttpResponse(200)
    else:
        return Response(status=status.HTTP_402_PAYMENT_REQUIRED)

@api_view(['GET'])
def get_list_groups(request, course, semester):
    if request.method == 'GET':
        group = Group_info.objects.filter(course=course, semester=semester)
        serializer = GroupInfoListSerializer(group, many=True)
        return  Response(serializer.data)


@api_view(['POST'])
def get_subgroup_for_group(request):
    """
    request.POST : QueryDict: {'course': ['1'], 'code': ['01'], 'semester': ['2'], 'abbr': ['ВХТ']} >
    """
    data = request.POST
    group_info = Group_info.objects.filter(abbr=data["abbr"],
                                           course=data["course"],
                                           code=data["code"],
                                           semester=data["semester"]).first()
    groups = Group.objects.filter(group_info=group_info)
    content = {"group": f'{data["abbr"]} - {data["course"]}{data["code"]}',
               'subgroup': len(groups)}
    return Response(content)
