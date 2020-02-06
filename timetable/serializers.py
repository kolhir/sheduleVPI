
from rest_framework import serializers
from .models import Group, Group_info, LessonTime, Time_table, Lessons_for_group, Lessons


class LessonSerializer(serializers.ModelSerializer):
	class Meta:
		model = Lessons
		fields = ("id", "name")


class LessonForGroupSerializer(serializers.ModelSerializer):
	lesson = LessonSerializer()

	class Meta:
		model = Lessons_for_group
		fields = ("group_info", "lesson")
