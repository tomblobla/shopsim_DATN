from datetime import datetime
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import login, authenticate

from customer.serializers import CartItemSerializer
from .forms import SignupForm, LoginForm, CustomPasswordResetForm, CustomPasswordResetConfirmForm, UpdateCustomerForm, ChangePasswordForm
from django.contrib.auth.decorators import login_required
from .models import Customer
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth import update_session_auth_hash
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from sim_manager.models import SIM, Tag, Network
from sim_manager.serializers import SIMSerializer, TagSerializer, NetworkSerializer
from .models import Customer, CartItem

from django.contrib.auth.views import (
    PasswordResetView, 
    PasswordResetDoneView, 
    PasswordResetConfirmView,
    PasswordResetCompleteView
)

def signup(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Kích hoạt tài khoản trên simminhvu'
            message = render_to_string('acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )
            email.send()
            return render(request, 'redirect_page.html', {'message': 'Mail xác nhận đã được gửi, vui lòng truy cập vào hòm và ấn đường link xác nhận để có thể đăng nhập.', 'username': user.username})
            
        else:
            return render(request, 'signup.html', {'form': form, 'title': 'Đăng ký'})
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form, 'title': 'Đăng ký'})



def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = Customer.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Customer.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return render(request, 'redirect_page.html', {'message': 'Tài khoản đã được xác nhận thành công, vui lòng đăng nhập để thực hiện đặt hàng.'})
    else:
        return render(request, 'redirect_page.html', {'message': 'Link xác nhận không khả dụng, vui lòng thực hiện lại', 'username': user.username})
    
def resend_valid_mail(request, username):
    if not username:
        return render(request, 'redirect_page.html', {'message': 'Tài khoản không hợp lệ.'})
    current_site = get_current_site(request)
    user = Customer.objects.get(username = username)
    mail_subject = 'Kích hoạt tài khoản trên simminhvu'
    message = render_to_string('acc_active_email.html', {
        'user': user,
        'domain': current_site.domain,
        'uid':urlsafe_base64_encode(force_bytes(user.pk)),
        'token':account_activation_token.make_token(user),
    })
    to_email = user.email
    email = EmailMessage(
                mail_subject, message, to=[to_email]
    )
    email.send()
    return render(request, 'redirect_page.html', {'message': 'Mail xác nhận đã được gửi, vui lòng truy cập vào hòm và ấn đường link xác nhận để có thể đăng nhập.', 'username': user.username, 'title': 'Xác nhận tài khoản'})


def logout_view(request):
    logout(request)
    return redirect('/') # Redirect to your desired page after logout


def login_view(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            remember_me = form.cleaned_data.get('remember_me')
            
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                if not remember_me:
                    request.session.set_expiry(0)
                return redirect('/')
            else:
                form.add_error(None, 'Tài khoản hoặc mật khẩu không chính xác.')
    else:
        form = LoginForm(request)
    return render(request, 'signin.html', {'form': form, 'title': 'Đăng nhập'})

class CustomPasswordResetView(PasswordResetView):
    template_name = 'password_reset/password_reset.html'
    form_class = CustomPasswordResetForm
    email_template_name = 'password_reset/password_reset_email.html'
    subject_template_name = 'password_reset/password_reset_subject.txt'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Lấy lại mật khẩu'
        return context

class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name='password_reset/password_reset_message.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Lấy lại mật khẩu'
        context['message'] = 'Đã gửi link reset mật khẩu vào email.'
        return context

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name='password_reset/password_reset_confirm.html'
    form_class = CustomPasswordResetConfirmForm
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Cập nhật mật khẩu'
        return context

class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name='password_reset/password_reset_message.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Cập nhật mật khẩu'
        context['message'] = 'Thay đổi mật khẩu thành công.'
        return context
    

def customer_update(request):
    customer = request.user
    
    if not customer.is_authenticated:
        return redirect('/')
    
    if request.method == 'POST':
        form = UpdateCustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = UpdateCustomerForm(instance=customer)
    return render(request, 'customer_update.html', {'form': form, 'title': 'Thay đổi mật khẩu'})


def customer_update(request):
    customer = request.user
    
    if not customer.is_authenticated:
        return redirect('/')
    
    if request.method == 'POST':
        form = UpdateCustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = UpdateCustomerForm(instance=customer)
    return render(request, 'customer_update.html', {'form': form, 'title': 'Thay đổi thông tin'})


def change_password(request):
    customer = request.user
    
    if not customer.is_authenticated:
        return redirect('/')
    
    if request.method == 'POST':
        form = ChangePasswordForm(request.user, request.POST)

        if form.is_valid():
            customer = form.save()
            update_session_auth_hash(request, customer)  # Important!
            return redirect('/')

    else:
        form = ChangePasswordForm(customer)

    return render(request, 'change_password.html', {'form': form, 'title': 'Thay đổi mật khẩu'})


def cart(request):
    if not request.user.is_authenticated:
        return redirect('signin')
    
    tagSerializer = TagSerializer(
        Tag.objects.all(), many=True)
    
    networkSerializer = NetworkSerializer(
        Network.objects.all(), many=True)
    
    cart_items = CartItem.objects.all().filter(customer=request.user)
    cart_itemSerializer = CartItemSerializer(cart_items, many=True)
    
    cart_count = cart_items.count()
        
    context = {
        "tags": tagSerializer.data,
        "networks": networkSerializer.data,
        "cart_items": cart_itemSerializer.data,
        "cart_count": cart_count,
    }

    return render(request, 'cart.html', context)


def add_to_cart(request):
    customer = request.user
    
    if not customer.is_authenticated:
        return redirect('signin')
    
    sim_id = request.POST.get('hiddenID')
    sim = get_object_or_404(SIM, pk=sim_id, is_visible=True)

    # Check if the customer already has a cart item for this sim
    cart_item = CartItem.objects.filter(sim=sim, customer=customer).first()

    # If the customer already has a cart item for this sim, increment the quantity
    if not cart_item:
        # Otherwise, create a new cart item
        cart_item = CartItem(sim=sim, customer=customer)
        cart_item.save()

    return redirect('cart')


def remove_from_cart(request):
    customer = request.user
    
    if not customer.is_authenticated:
        return redirect('signin')
    
    cart_id = request.POST.get('hiddenID')
    cart_item = CartItem.objects.get(id=cart_id)

    # delete
    cart_item.delete()

    return redirect('cart')