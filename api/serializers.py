
from rest_framework import serializers
from timetable.models import Group, Group_info, LessonTime, Time_table
from accounts.models import BotUser

class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = BotUser
		fields = ("user_id", "user_name", "name", "last_name", "group")

class GroupInfoListSerializer(serializers.ModelSerializer):
	class Meta:
		model = Group_info
		fields = ("specialty", "abbr", "code", "course", "semester", "cathedra")

class LessonTimeSerializer(serializers.ModelSerializer):
	class Meta:
		model = LessonTime
		fields = ("number_lesson", "start", "end")

class Time_tableOnDaySerializer(serializers.ModelSerializer):
	# day = serializers.StringRelatedField(read_only=True)

	class Meta:
		model = Time_table
		depth = 1
		fields = ("number_week", "day", 'lesson', 'lesson_time', 'room', 'teacher', 'type_lessons', 'korpus')