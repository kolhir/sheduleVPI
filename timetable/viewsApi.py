from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.response import Response
from .models import Lessons_for_group, Lessons, Group_info
from .serializers import LessonForGroupSerializer, LessonSerializer
from vpitt.dbfunc import get_group_by_id


class LessonsForGroupView(viewsets.ViewSet):

    def list(self, request, group_id):
        group = get_group_by_id(group_id)
        queryset = Lessons_for_group.objects.filter(group_info=group.group_info).all()
        print(group_id, queryset[0].group_info_id)
        print(queryset)
        serializer = LessonForGroupSerializer(queryset, many=True)
        return Response(serializer.data)

    def update(self, request, group_id):
        lessons = request.data["data"]
        print(lessons)
        group_info_id = get_group_by_id(group_id).group_info_id
        lessons_ids = [item['lesson']['id'] for item in lessons]
        group_info = Group_info.objects.get(id=group_info_id)
        Lessons_for_group.objects.filter(group_info=group_info).exclude(lesson__id__in=lessons_ids).delete()
        for item in lessons:
            lesson = Lessons.objects.get(id=item['lesson']['id'])
            Lessons_for_group.objects.get_or_create(group_info=group_info, lesson=lesson)
        return HttpResponse(200)
# [{'group_info': 24, 'lesson': {'id': 63, 'name': 'Защита информации'}},
#  {'group_info': 24, 'lesson': {'id': 57, 'name': 'Выполнение выпускной работы'}},
#  {'group_info': 24, 'lesson': {'id': 80, 'name': 'Экономика программной инженерии'}},
#  {'group_info': 24, 'lesson': {'id': 65, 'name': 'Компьютерные методы обработки экспериментальных данных'}},
#  {'group_info': 24, 'lesson': {'id': 64, 'name': 'Методы анализа нечеткой информации'}},
#  {'group_info': 24, 'lesson': {'id': 81, 'name': 'Введение в разработку интеллектуальных систем'}}]


class LessonsView(viewsets.ViewSet):

    def list(self, request):
        queryset = Lessons.objects.all()
        serializer = LessonSerializer(queryset, many=True)
        return Response({"count":len(serializer.data), "entries":serializer.data})
