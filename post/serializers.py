from rest_framework import serializers
from .models import Topic, Post


class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = ['id', 'name', 'slug', 'desc']


class PostSerializer(serializers.ModelSerializer):
    topic = TopicSerializer()

    class Meta:
        model = Post
        fields = ['id', 'title', 'short_desc', 'thumbnail', 'topic', 'slug', 'content', 'is_pinned']
