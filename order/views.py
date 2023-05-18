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
from io import BytesIO
from shopsim import settings
from post.models import Post, Topic
from post.serializers import PostSerializer, TopicSerializer
from .vnpay import vnpay



from django.template.loader import render_to_string
from weasyprint import HTML



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
            
            if order.payment_method == 'TRANSFER':
                return payment(request = request, order_id=order.id)
            
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
    print('cancel')
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
    

def generate_pdf(request, context):
    # Get the HTML template
    html_string = render_to_string('invoice.html', context=context)

    # Generate PDF using weasyprint
    pdf_file = HTML(string=html_string).write_pdf()

    # Create a HTTP response with PDF content type
    response = HttpResponse(content_type='application/pdf')

    # Set the content disposition header to force download the PDF file
    response['Content-Disposition'] = 'inline; filename="hddt.pdf"'

    # Write the PDF file content to the response
    response.write(pdf_file)

    return response
 
def order_pdf(request, id):
    if not request.user.is_authenticated:
        return redirect('signin')
    
    if id is None:
        return redirect('/')
    
    order = Order.objects.get(id = id)
    
    if order.customer != request.user and not request.user.is_admin:
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

    
    # pdf = html_to_pdf('invoice.html', context)
    # return HttpResponse(pdf, content_type='application/pdf')
    return generate_pdf(request, context)
    
    

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
    
def payment_view(request):
    if request.method == 'POST':
        hiddenID = request.POST.get('hiddenID')
        return payment(order_id = hiddenID, request = request)
    else:
        redirect('/')
    
import hashlib
import hmac

def hmacsha512(key, data):
    byteKey = key.encode('utf-8')
    byteData = data.encode('utf-8')
    return hmac.new(byteKey, byteData, hashlib.sha512).hexdigest()


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

from datetime import datetime

def payment(order_id, request):

    if request.method == 'POST':
        # Process input data and build url payment
        order_id = order_id
        order = Order.objects.get(id=order_id)
        amount = order.get_total_price_int()
        ipaddr = get_client_ip(request)
        # Build URL Payment
        vnp = vnpay()
        vnp.requestData['vnp_Version'] = '2.1.0'
        vnp.requestData['vnp_Command'] = 'pay'
        vnp.requestData['vnp_TmnCode'] = settings.VNPAY_TMN_CODE
        vnp.requestData['vnp_Amount'] = amount * 100
        vnp.requestData['vnp_CurrCode'] = 'VND'
        vnp.requestData['vnp_TxnRef'] = order_id
        vnp.requestData['vnp_OrderInfo'] = 'Thanh toan hoa don ngay ' + order.order_date.strftime("%m/%d/%Y, %H:%M:%S")
        vnp.requestData['vnp_OrderType'] = 'billpayment'
        vnp.requestData['vnp_Locale'] = 'vn'


        vnp.requestData['vnp_CreateDate'] = datetime.now().strftime('%Y%m%d%H%M%S')  # 20150410063022
        vnp.requestData['vnp_IpAddr'] = ipaddr
        vnp.requestData['vnp_ReturnUrl'] = settings.VNPAY_RETURN_URL
        vnpay_payment_url = vnp.get_payment_url(settings.VNPAY_PAYMENT_URL, settings.VNPAY_HASH_SECRET_KEY)
        print(vnpay_payment_url)
        return redirect(vnpay_payment_url)
    else:
        return redirect('/')


def payment_return(request):
    tagSerializer = TagSerializer(
        Tag.objects.all(), many=True)
    
    networkSerializer = NetworkSerializer(
        Network.objects.all(), many=True)
    
    pinned_posts = Post.objects.filter(is_pinned=True)
    topics = Topic.objects.all()
    
    inputData = request.GET
    if inputData:
        vnp = vnpay()
        vnp.responseData = inputData.dict()
        order_id = inputData['vnp_TxnRef']
        amount = int(inputData['vnp_Amount']) / 100
        order_desc = inputData['vnp_OrderInfo']
        vnp_TransactionNo = inputData['vnp_TransactionNo']
        vnp_ResponseCode = inputData['vnp_ResponseCode']
        vnp_TmnCode = inputData['vnp_TmnCode']
        vnp_PayDate = inputData['vnp_PayDate']
        vnp_BankCode = inputData['vnp_BankCode']
        vnp_CardType = inputData['vnp_CardType']
        if vnp.validate_response(settings.VNPAY_HASH_SECRET_KEY):
            if vnp_ResponseCode == "00":
                order = Order.objects.get(id=order_id)
                date_format = "%Y%m%d%H%M%S"

                # Convert the string to a datetime object
                datetime_obj = datetime.strptime(vnp_PayDate, date_format)

                order.paid_date = datetime_obj
                order.is_paid = True
                order.transaction_id = vnp_TransactionNo
                order.save()
                return render(request, "payment_return.html", context={
                        "tags": tagSerializer.data,
                        "networks": networkSerializer.data,
                        "cart_count": 0,
                        "pinned_posts": PostSerializer(pinned_posts, many = True).data,
                        "topics": TopicSerializer(topics, many = True).data,
                        "message": "Thanh toán thành công",
                        "order_id": order_id,
                    })
            else:
                return render(request, "payment_return.html", context={
                        "tags": tagSerializer.data,
                        "networks": networkSerializer.data,
                        "cart_count": 0,
                        "pinned_posts": PostSerializer(pinned_posts, many = True).data,
                        "topics": TopicSerializer(topics, many = True).data,
                        "message": "Thanh toán thất bại",
                        "order_id": order_id,
                    })
        else:
            return render(request, "payment_return.html", context={
                        "tags": tagSerializer.data,
                        "networks": networkSerializer.data,
                        "cart_count": 0,
                        "pinned_posts": PostSerializer(pinned_posts, many = True).data,
                        "topics": TopicSerializer(topics, many = True).data,
                        "message": "Thanh toán thất bại",
                        "order_id": order_id,
                    })
    else:
        return redirect("/")

