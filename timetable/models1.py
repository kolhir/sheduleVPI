from django.db import models

# Create your models here.

class SubGroup(models.Model):
    number = models.IntegerField()
    group = models.ForeignKey("Group")

class Group(models.Model):
    name = models.CharField(max_length = 20)

class DaysWeek(models.Model):
    name = models.CharField(max_length = 20)


class NumberWeek(models.Model):
    number = models.IntegerField()


class LessonTime(models.Model):
    number_lesson = models.IntegerField()
    start = models.TimeField()
    end = models.TimeField()

class Korpus(models.Model):
    letter = models.CharField(max_length = 10)
class Room(models.Model):
    number = models.IntegerField()


class Teacher(models.Model):
    first_name = models.CharField(max_length = 100, null = True)
    last_name = models.CharField(max_length = 100)
    patronymic = models.CharField(max_length = 100, null = True)


class TypeLesson(models.Model):
    type_name = models.CharField(max_length = 50)


class Lessons(models.Model):
    name = models.CharField(max_length = 50)
    full_name = models.CharField(max_length = 100)

class Users(models.Model):
    user_id = models.IntegerField(primary_key=True)
    user_name = models.CharField(max_length = 100, null = True)
    name = models.CharField(max_length = 100, null = True)
    last_name = models.CharField(max_length = 100, null = True)
    subgroup = models.ForeignKey("Group")

class Time_table(models.Model):
    group = models.ForeignKey("Group")
    day = models.ForeignKey("DaysWeek")
    number_week = models.ForeignKey("NumberWeek")
    lesson_time = models.ForeignKey("LessonTime")
    lesson = models.ForeignKey("Lessons")
    teacher = models.ForeignKey("Teacher")
    room = models.ForeignKey("Room")
    type_lessons = models.ForeignKey("TypeLesson")
# def create_tables():
#     with db:
#         db.create_tables([Users, Group, Time_table, DaysWeek, NumberWeek,
#                             LessonTime, Room, Teacher, TypeLesson, Lessons])


import time
def read_file(s):
    f = open(s, "r")
    for line in f:

        l = list(line.split("|"))
        # print(l)
        if len(Group.select().where(Group.name == l[0])) == 0:
            Group.create(name = l[0])
        l0 = Group.select().where(Group.name == l[0]).get()

        l1 = DaysWeek.select().where(DaysWeek.id == int(l[1])).get()

        l2 = NumberWeek.select().where(NumberWeek.number == int(l[2])).get()

        l3 = LessonTime.select().where(LessonTime.number_lesson == int(l[3])).get()

        l4 = Lessons.select().where(Lessons.full_name  == l[4]).get()

        l5 = Teacher.select().where(Teacher.last_name  == l[5]).get()

        l6 = Room.select().where(Room.korpus  == l[6], Room.number == int(l[7])).get()

        l[8] = l[8].replace("\n", "")
        if len(TypeLesson.select().where(TypeLesson.type_name  == l[8])) == 0:
            TypeLesson.create(type_name = l[8])
        l8 = TypeLesson.select().where(TypeLesson.type_name  == l[8]).get()

        # print(l)
        # print(l8.type_name)

        Time_table.create(group = l0, day = l1, number_week = l2,
            lesson_time = l3, lesson = l4, teacher = l5, room = l6, type_lessons = l8)
        # print("done")
