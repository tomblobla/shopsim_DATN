from rest_framework import serializers
from .models import Order, OrderItem

class OrderItemSerializer(serializers.ModelSerializer):
    sim_id = serializers.IntegerField(source='sim.id')
    sim_img = serializers.ImageField(source='sim.image')
    sim_slug = serializers.CharField(source='sim.slug')
    sim_phone_number = serializers.CharField(source='sim.phone_number')
    
    network_name = serializers.CharField(source='sim.network.name')
    network_slug = serializers.CharField(source='sim.network.slug')
    network_image_logo = serializers.ImageField(source='sim.network.image_logo')
    network_image_simcard = serializers.ImageField(source='sim.network.image_simcard')

    class Meta:
        model = OrderItem
        fields = ['get_original_price_str', 'get_sale_price_str', 'get_discount',
                  'sim_id',
                  'sim_img',
                  'sim_slug',
                  'sim_phone_number',
                  "network_name", 
                  "network_image_logo", 
                  "network_image_simcard", 
                  "network_slug"]


class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True, read_only=True)
    
    order_date = serializers.DateTimeField(format="%d/%m/%Y - %H:%M:%S")
    
    class Meta:
        model = Order
        fields = ['id',
                  'full_name',
                  'phone_number',
                  'email',
                  'address', 
                  'gender',
                  'order_date',
                  'message',
                  'payment_method',
                  'is_paid',
                  'paid_date',
                  'order_items', 
                  'order_status',
                  'tracking_number',
                  'shipping_provider',
                  'ship_date',
                  'get_customer_username', 
                  'get_gender_display', 
                  'get_order_status_display', 
                  'get_payment_method_display', 
                  'get_paid_state_display', 
                  'get_total_price']