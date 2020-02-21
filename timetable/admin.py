
from django.contrib import admin
from .models import Faculty, Cathedra, Korpus, \
    Group_info, Group, DaysWeek, \
    LessonTime, Room, Lessons, \
    TypeLesson, Lessons_for_group, \
    Teacher, Time_table, TeacherCathedra


# Register your models here.

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ['number', 'korpus']

@admin.register(Lessons_for_group)
class Lessons_for_groupAdmin(admin.ModelAdmin):
    list_display = ['group_info', 'lesson']

@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    list_display = ['name', 'abbr']


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ['last_name', 'first_name', 'patronymic', 'cathedra']

@admin.register(Cathedra)
class CathedraAdmin(admin.ModelAdmin):
    list_display = ['name', 'abbr', 'faculty']


@admin.register(Korpus)
class KorpusAdmin(admin.ModelAdmin):
    list_display = ['letter']


@admin.register(Group_info)
class Group_infoAdmin(admin.ModelAdmin):
    list_display = ['group_name', 'semester']

    def group_name(self, obj):
        return obj.abbr + " - " + str(obj.course) + str(obj.code)

@admin.register(Lessons)
class LessonsAdmin(admin.ModelAdmin):
    list_display = ['name', 'cathedra']
    search_fields = ['name']


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ['_group_info', 'subgroup', 'user_create', 'added_to_bot']
    list_filter = ['subgroup', 'user_create', 'added_to_bot']
    search_fields = ['subgroup']

    def _group_info(self, obj):
        return obj.group_info.abbr + \
               " - " + str(obj.group_info.course) + \
               str(obj.group_info.code) + \
               " / " + str(obj.group_info.semester)


@admin.register(TeacherCathedra)
class TeacherCathedraAdmin(admin.ModelAdmin):
    list_display = ['_teacher', '_cathedra', '_cathedra_name']
    search_fields = ['teacher__last_name', 'cathedra__abbr', 'cathedra__name']

    def _teacher(self, obj):
        return f"{obj.teacher.last_name} {obj.teacher.first_name[0]}. {obj.teacher.patronymic[0]}."

    def _cathedra(self, obj):
        return obj.cathedra.abbr

    def _cathedra_name(self, obj):
        return obj.cathedra.name

@admin.register(Time_table)
class Time_tableAdmin(admin.ModelAdmin):
    list_display = ["_group_id", '_group', '_day', 'number_week', '_lesson_time',
                    '_lesson', '_teacher', '_room', '_type_lessons']


    def _group_id(self, obj):
        return obj.group.id

    def _room(self, obj):
        return obj.korpus.letter + " - " + str(obj.room.number)

    def _day(self, obj):
        return obj.day.name

    def _lesson_time(self, obj):
        return obj.lesson_time.number_lesson

    def _lesson(self, obj):
        return obj.lesson.name

    def _teacher(self, obj):
        return obj.teacher.last_name

    def _type_lessons(self, obj):
        return obj.type_lessons.name

    def _group(self, obj):
        return obj.group.group_info.abbr + \
               " - " + str(obj.group.group_info.course) + \
               str(obj.group.group_info.code) + \
               " / " + str(obj.group.group_info.semester)


