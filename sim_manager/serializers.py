from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import Network, SIM, Tag


class NetworkSerializer(ModelSerializer):
    class Meta:
        model = Network
        fields = ["id", "image_logo", "image_simcard", "name",
                  "description", "sims", 'slug']


class SIMSerializer(ModelSerializer):
    network_id = serializers.IntegerField(source='network.id')
    network_name = serializers.CharField(source='network.name')
    network_slug = serializers.CharField(source='network.slug')
    network_image_logo = serializers.ImageField(source='network.image_logo')
    network_image_simcard = serializers.ImageField(source='network.image_simcard')

    class Meta:
        model = SIM
        fields = ["id", "phone_number", "description", "image",
                  "price", 'get_saleprice', "discount", "tags", 'slug',
                  "network_name", "network_id", "network_image_logo", "network_image_simcard", "network_slug"]


class TagSerializer(ModelSerializer):
    class Meta:
        model = Tag
        fields = ["id", "name", 'sims']
