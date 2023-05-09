from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Customer
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import AuthenticationForm

class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=200, required=True, error_messages={
        'unique': 'Email đã được sử dụng',
        'invalid': 'Email không hợp lệ',
        'required': 'Vui lòng nhập email',
    })
    phone_number = forms.CharField(max_length=30, required=True, error_messages={
        'unique': 'Số điện thoại đã được sử dụng',
        'required': 'Vui lòng nhập số điện thoại',
    })
    address = forms.CharField(max_length=300, required=True, error_messages={
        'required': 'Vui lòng nhập địa chỉ',
    })
    
    MALE = 'M'
    FEMALE = 'F'
    GENDER_CHOICES = (
        (MALE, 'Nam'),
        (FEMALE, 'Nữ'),
    )
    gender = forms.ChoiceField(choices=GENDER_CHOICES)
    
    class Meta:
        model = Customer
        fields = ('username', 'email', 'password1', 'password2', 'first_name', 'last_name', 'gender', 'address')
        labels = {
            'username': 'Tên đăng nhập',
            'email': 'Email',
            'password1': 'Mật khẩu',
            'password2': 'Xác nhận mật khẩu',
            'first_name': 'Tên',
            'last_name': 'Họ',
            'phone_number': 'Số điện thoại',
            'address': 'Địa chỉ',
            'gender': 'Giới tính',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Update HTML attributes for each field
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'id': 'floatingInput',
            'placeholder': 'Tên đăng nhập',
        })
        self.fields['email'].widget.attrs.update({
            'class': 'form-control',
            'id': 'floatingInput',
            'placeholder': 'name@example.com',
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'id': 'floatingPassword',
            'placeholder': 'Mật khẩu',
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'id': 'floatingPassword',
            'placeholder': 'Xác nhận mật khẩu',
        })
        self.fields['first_name'].widget.attrs.update({
            'class': 'form-control',
            'id': 'floatingInput',
            'placeholder': 'Tên',
        })
        self.fields['last_name'].widget.attrs.update({
            'class': 'form-control',
            'id': 'floatingInput',
            'placeholder': 'Họ',
        })
        self.fields['phone_number'].widget.attrs.update({
            'class': 'form-control',
            'id': 'floatingInput',
            'placeholder': 'Số điện thoại',
        })
        self.fields['address'].widget.attrs.update({
            'class': 'form-control',
            'id': 'floatingInput',
            'placeholder': 'Địa chỉ',
        })
        self.fields['gender'].widget.attrs.update({
            'class': 'form-control',
            'id': 'floatingInput',
            'placeholder': 'Giới tính',
        })
        
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Customer.objects.filter(email=email).exists():
            raise ValidationError('Email đã được đăng ký.')
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if Customer.objects.filter(username=username).exists():
            raise ValidationError('Tên đăng nhập đã được sử dụng.')
        return username

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if Customer.objects.filter(phone_number=phone_number).exists():
            raise ValidationError('Số điện thoại đã được đăng ký.')
        return phone_number
    
    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Mật khẩu xác nhận không khớp với mật khẩu đã nhập.')
        
        # check if the password meets the minimum length requirement
        if len(password2) < 8:
            raise forms.ValidationError('Mật khẩu phải dài ít nhất 8 ký tự.')

        # check if the password is too common
        common_passwords = ['123456', 'password', 'qwerty', '123456789', '12345678', '12345', '1234567', 'password1', '123123', 'admin', 'welcome', '123qwe', '1234567890', 'password123']
        if password2.lower() in common_passwords:
            raise forms.ValidationError('Mật khẩu quá dễ đoán, vui lòng chọn mật khẩu khác.')

        return password2
    
    
    

class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Tên đăng nhập", max_length=30, 
                               widget=forms.TextInput(attrs={'class': 'form-control', 
                                                             'placeholder': 'Tên đăng nhập'}))
    password = forms.CharField(label="Mật khẩu", max_length=30, 
                               widget=forms.PasswordInput(attrs={'class': 'form-control', 
                                                                 'placeholder':'Mật khẩu'}))
    
    remember_me = forms.BooleanField(required=False, initial=True, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))