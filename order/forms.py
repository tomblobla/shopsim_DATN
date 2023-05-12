from django import forms
from django.core.exceptions import ValidationError
from .models import Order

class PlaceOrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['full_name', 'phone_number', 'email', 'address', 'gender', 'message',
                  'cccd_image', 'portrait_image', 'payment_method']
        labels = {
            'full_name': 'Họ và tên',
            'phone_number': 'Số điện thoại',
            'email': 'Email',
            'address': 'Địa chỉ',
            'gender': 'Giới tính',
            'message': 'Yêu cầu khách hàng',
            'cccd_image': 'Ảnh CCCD đăng ký',
            'portrait_image': 'Ảnh chân dung đăng ký',
            'payment_method': 'Phương thức thanh toán',
        }
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control text-dark'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control text-dark'}),
            'email': forms.EmailInput(attrs={'class': 'form-control text-dark'}),
            'address': forms.TextInput(attrs={'class': 'form-control text-dark'}),
            'gender': forms.Select(attrs={'class': 'form-control text-dark ml-0'}),
            'message': forms.Textarea(attrs={'class': 'form-control text-dark', 'rows': 4,}),
            'cccd_image': forms.ClearableFileInput(attrs={'class': 'custom-file-input'}),
            'portrait_image': forms.ClearableFileInput(attrs={'class': 'custom-file-input', 'id': 'customFile'}),
            'payment_method': forms.Select(attrs={'class': 'form-control text-dark ml-0'}),
        }

    def clean_phone_number(self):
        # Hàm kiểm tra số điện thoại hợp lệ
        phone_number = self.cleaned_data['phone_number']
        if not phone_number.isnumeric():
            raise ValidationError('Số điện thoại không hợp lệ')
        return phone_number
