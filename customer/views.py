from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import SignupForm, LoginForm
from .models import Customer
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.core.mail import EmailMessage

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
    return render(request, 'redirect_page.html', {'message': 'Mail xác nhận đã được gửi, vui lòng truy cập vào hòm và ấn đường link xác nhận để có thể đăng nhập.', 'username': user.username})


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
            form.add_error(None, 'Tài khoản hoặc mật khẩu không hợp lệ.')
    else:
        form = LoginForm(request)
    return render(request, 'signin.html', {'form': form, 'title': 'Đăng nhập'})