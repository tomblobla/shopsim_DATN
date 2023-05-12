from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import CartItem


class CartItemSerializer(ModelSerializer):
    sim_id = serializers.IntegerField(source='sim.id')
    sim_img = serializers.ImageField(source='sim.image')
    sim_slug = serializers.CharField(source='sim.slug')
    sim_phone_number = serializers.CharField(source='sim.phone_number')
    
    network_name = serializers.CharField(source='sim.network.name')
    network_slug = serializers.CharField(source='sim.network.slug')
    network_image_logo = serializers.ImageField(source='sim.network.image_logo')
    network_image_simcard = serializers.ImageField(source='sim.network.image_simcard')

    class Meta:
        model = CartItem
        fields = ["id", 
                  'sim_id',
                  'sim_img',
                  'sim_slug',
                  'sim_phone_number',
                  'get_phone_number',
                  'get_network_name',
                  'get_original_price_str',
                  'get_discount',
                  'get_sale_price_str',
                  'get_total_price',
                  "network_name", 
                  "network_image_logo", 
                  "network_image_simcard", 
                  "network_slug"]

