from django.shortcuts import render
from sim_manager.models import SIM, Network, Tag
from sim_manager.serializers import SIMSerializer, NetworkSerializer, TagSerializer
from customer.models import CartItem

from post.models import Post, Topic
from post.serializers import PostSerializer, TopicSerializer
# Create your views here.

def post(request, topic_slug, post_slug):
    tagSerializer = TagSerializer(
        Tag.objects.all(), many=True)
    
    networkSerializer = NetworkSerializer(
        Network.objects.all(), many=True)
    
    post = Post.objects.get(slug = post_slug)
    
    pinned_posts = Post.objects.filter(is_pinned=True)
    topics = Topic.objects.all()
    c_count = 0
    
    if request.user.is_authenticated:
        c_count = CartItem.objects.filter(customer=request.user).count()
        
    context = {
        "tags": tagSerializer.data,
        "networks": networkSerializer.data,
        "cart_count": c_count,
        "pinned_posts": PostSerializer(pinned_posts, many = True).data,
        "topics": TopicSerializer(topics, many = True).data,
        "post": post,
    }

    return render(request, 'post_detailed.html', context=context)


def topic_post(request, topic_slug):
    tagSerializer = TagSerializer(
        Tag.objects.all(), many=True)
    
    networkSerializer = NetworkSerializer(
        Network.objects.all(), many=True)
    
    posts = Post.objects.filter(topic__slug = topic_slug)
    
    pinned_posts = Post.objects.filter(is_pinned=True)
    topics = Topic.objects.all()
    
    c_count = 0
    
    if request.user.is_authenticated:
        c_count = CartItem.objects.filter(customer=request.user).count()
        
    context = {
        "tags": tagSerializer.data,
        "networks": networkSerializer.data,
        "cart_count": c_count,
        "pinned_posts": PostSerializer(pinned_posts, many = True).data,
        "topics": TopicSerializer(topics, many = True).data,
        "posts": PostSerializer(posts, many = True).data
    }

    return render(request, 'post_list.html', context=context)


def all_post(request):
    tagSerializer = TagSerializer(
        Tag.objects.all(), many=True)
    
    networkSerializer = NetworkSerializer(
        Network.objects.all(), many=True)
    
    posts = Post.objects.all()
    
    pinned_posts = Post.objects.filter(is_pinned=True)
    topics = Topic.objects.all()
    
    c_count = 0
    
    if request.user.is_authenticated:
        c_count = CartItem.objects.filter(customer=request.user).count()
    context = {
        "tags": tagSerializer.data,
        "networks": networkSerializer.data,
        "cart_count": c_count,
        "pinned_posts": PostSerializer(pinned_posts, many = True).data,
        "topics": TopicSerializer(topics, many = True).data,
        "posts": PostSerializer(posts, many = True).data
    }

    return render(request, 'post_list.html', context=context)