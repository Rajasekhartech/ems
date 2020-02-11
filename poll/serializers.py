from rest_framework import serializers
from poll.models import Question

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = [
            "title",
            "status",
            "created_by"

        ]