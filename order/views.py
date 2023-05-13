from django.shortcuts import render, redirect
from .forms import PlaceOrderForm
from sim_manager.models import SIM, Tag, Network
from sim_manager.serializers import SIMSerializer, TagSerializer, NetworkSerializer
from customer.models import Customer, CartItem
from customer.serializers import CartItemSerializer
from .models import Order, OrderItem
from .serializers import OrderSerializer, OrderItemSerializer
from io import StringIO
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from io import BytesIO

from post.models import Post, Topic
from post.serializers import PostSerializer, TopicSerializer

def place_order(request):
    if not request.user.is_authenticated:
        return redirect('signin')
    
    tagSerializer = TagSerializer(
        Tag.objects.all(), many=True)
    
    networkSerializer = NetworkSerializer(
        Network.objects.all(), many=True)
    
    pinned_posts = Post.objects.filter(is_pinned=True)
    topics = Topic.objects.all()
    
    cart_items = CartItem.objects.all().filter(customer=request.user)
    cart_itemSerializer = CartItemSerializer(cart_items, many=True)
    
    available_count = 0
    for item in cart_items:        
        if item.sim.is_available == True:
            available_count += 1
        else:
            item.delete()
    
    if available_count < cart_items.count():
        if request.method == 'POST':
            form = PlaceOrderForm(request.POST, request.FILES)
        else:
            initial_values = {
                'full_name': request.user.last_name + ' ' + request.user.first_name,
                'phone_number': request.user.phone_number,
                'email': request.user.email,
                'address': request.user.address,
                'gender': request.user.gender,
            }
            form = PlaceOrderForm(initial=initial_values)

        return render(request, 'place_order.html',
                    context={
                            "tags": tagSerializer.data,
                            "networks": networkSerializer.data,
                            "cart_count": cart_items.count(),
                            "cart_items": cart_itemSerializer.data,
                            "pinned_posts": PostSerializer(pinned_posts, many = True).data,
                            "topics": TopicSerializer(topics, many = True).data,
                            "form": request.form,
                        })
        
    if request.method == 'POST':
        form = PlaceOrderForm(request.POST, request.FILES)
        if form.is_valid():
            # Lưu đơn đặt hàng
            if cart_items.count() == 0: 
                return redirect('/')
            
            order = form.save(commit=False)
            order.order_status = 'PENDING'
            order.cccd_image = form.cleaned_data['cccd_image']
            order.portrait_image = form.cleaned_data['portrait_image']
            order.customer = request.user
            order.save()
            for item in cart_items:
                sim = SIM.objects.get(id = item.sim.id)
                orderItem = OrderItem(
                    order = order,
                    sim = sim
                )
                sim.is_available = False
                sim.is_visible = False
                sim.save()
                orderItem.save()
                item.delete()
            # Thông báo đặt hàng thành công
            return render(request, 'place_order_success.html', context={
                "tags": tagSerializer.data,
                "networks": networkSerializer.data,
                "cart_count": 0,
                "pinned_posts": PostSerializer(pinned_posts, many = True).data,
                "topics": TopicSerializer(topics, many = True).data,
                "order_id": order.id,
            })
        else:
            render(request, 'place_order.html',
                  context={
                        "tags": tagSerializer.data,
                        "networks": networkSerializer.data,
                        "cart_count": cart_items.count(),
                        "cart_items": cart_itemSerializer.data,
                        "pinned_posts": PostSerializer(pinned_posts, many = True).data,
                        "topics": TopicSerializer(topics, many = True).data,
                        "form": form,
                    })
    else:
        initial_values = {
            'full_name': request.user.last_name + ' ' + request.user.first_name,
            'phone_number': request.user.phone_number,
            'email': request.user.email,
            'address': request.user.address,
            'gender': request.user.gender,
        }
        form = PlaceOrderForm(initial=initial_values)


    return render(request, 'place_order.html',
                  context={
                        "tags": tagSerializer.data,
                        "networks": networkSerializer.data,
                        "cart_count": cart_items.count(),
                        "cart_items": cart_itemSerializer.data,
                        "pinned_posts": PostSerializer(pinned_posts, many = True).data,
                        "topics": TopicSerializer(topics, many = True).data,
                        "form": form,
                    })

def cancel_order(request):
    if not request.user.is_authenticated:
        return redirect('signin')
    
    tagSerializer = TagSerializer(
        Tag.objects.all(), many=True)
    
    networkSerializer = NetworkSerializer(
        Network.objects.all(), many=True)
    
    pinned_posts = Post.objects.filter(is_pinned=True)
    topics = Topic.objects.all()
    
    cart_items = CartItem.objects.all().filter(customer=request.user)
    cart_itemSerializer = CartItemSerializer(cart_items, many=True)
        
    if request.method == 'POST':
        id = request.POST.get('hiddenID')
        
        order = Order.objects.get(id = id)
        
        if order.order_status == 'PENDING':
            order.order_status = 'CANCELLED'
        
        orderItems = OrderItem.objects.all().filter(order = order)
        
        for item in orderItems:
            sim = item.sim
            sim.is_available = True
            sim.is_visible = True
            sim.save()
            
        order.save()
        return redirect('manage-order')
    
    return redirect('/')
    
    
def order_tracker(request, id):
    if not request.user.is_authenticated:
        return redirect('signin')
    
    if id is None:
        return redirect('/')
    
    order = Order.objects.get(id = id)
    
    if order.customer != request.user:
        return redirect('/')
    
    tagSerializer = TagSerializer(
        Tag.objects.all(), many=True)
    
    networkSerializer = NetworkSerializer(
        Network.objects.all(), many=True)
    
    pinned_posts = Post.objects.filter(is_pinned=True)
    topics = Topic.objects.all()
    
    cart_items = CartItem.objects.all().filter(customer=request.user)
    
    orderItem = OrderItem.objects.all().filter(order=order)
    orderItemSerializer = OrderItemSerializer(orderItem, many=True)
    
    return render(request, 'order_detailed.html',
                  context={
                        "tags": tagSerializer.data,
                        "networks": networkSerializer.data,
                        "cart_count": cart_items.count(),
                        "pinned_posts": PostSerializer(pinned_posts, many = True).data,
                        "topics": TopicSerializer(topics, many = True).data,
                        "order": order,
                        "orderItem": orderItemSerializer.data,
                    })
    
# defining the function to convert an HTML file to a PDF file
def html_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="invoice.pdf"'
    html = template.render(context_dict)

    pisa_status = pisa.CreatePDF(html, dest=response)

    if pisa_status.err:
      return HttpResponse(f'We had some errors <pre>{html}</pre>')

    return response
 
def order_pdf(request, id):
    if not request.user.is_authenticated:
        return redirect('signin')
    
    if id is None:
        return redirect('/')
    
    order = Order.objects.get(id = id)
    
    if order.customer != request.user:
        return redirect('/')

    orderItem = OrderItem.objects.all().filter(order=order)
    orderItemSerializer = OrderItemSerializer(orderItem, many=True)
    
    context={
        "order": order,
        "orderItem": orderItemSerializer.data,
    }
    # html = template.render(context)
    # response = HttpResponse(content_type='application/pdf')
    # response['Content-Disposition'] = 'attachment; filename="invoice.pdf"'

    
    pdf = html_to_pdf('invoice.html', context)
    return HttpResponse(pdf, content_type='application/pdf')
    
    

def manage_order(request):
    pinned_posts = Post.objects.filter(is_pinned=True)
    topics = Topic.objects.all()
    if not request.user.is_authenticated:
        return redirect('signin')
    
    tagSerializer = TagSerializer(
        Tag.objects.all(), many=True)
    
    networkSerializer = NetworkSerializer(
        Network.objects.all(), many=True)
    
    cart_items = CartItem.objects.all().filter(customer=request.user)
    
    order = Order.objects.filter(customer=request.user)
    orderSerializer = OrderSerializer(order, many=True)
    
    return render(request, 'manage_order.html',
                  context={
                        "tags": tagSerializer.data,
                        "networks": networkSerializer.data,
                        "cart_count": cart_items.count(),
                        "orders": orderSerializer.data,
                        "pinned_posts": PostSerializer(pinned_posts, many = True).data,
                        "topics": TopicSerializer(topics, many = True).data,
                    })