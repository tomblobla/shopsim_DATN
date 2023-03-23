from django.shortcuts import render, get_object_or_404, redirect
from sim_manager.models import SIM, Tag, Network 
from sim_manager.serializers import SIMSerializer, TagSerializer, NetworkSerializer


def home(request):
    tagSerializer = TagSerializer(
        Tag.objects.all(), many=True)
    
    networkSerializer = NetworkSerializer(
        Network.objects.all(), many=True)
    
    sale_sims = SIM.objects.all(is_available=True, discount__gt=0).first(20)
    

    context = {
        "tags": tagSerializer.data,
        "networks": networkSerializer.data,
    }

    return render(request, 'home.html', context)


def shop(request):
    tagSerializer = TagSerializer(
        Tag.objects.all(), many=True)
    
    networkSerializer = NetworkSerializer(
        Network.objects.all(), many=True)

    context = {
        "tags": tagSerializer.data,
        "networks": networkSerializer.data,
    }

    return render(request, 'shop.html', context)

