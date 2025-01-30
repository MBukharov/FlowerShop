from django import forms
from .models import Order
from catalog.models import Flower
from users.models import CustomUser


class OrderForm(forms.ModelForm):

    delivery_address = forms.CharField(label='Адрес доставки', required=True, widget=forms.TextInput(attrs={'class': 'form-input'}))
    phone_number = forms.CharField(label='Телефон', required=True, widget=forms.TextInput(attrs={'class': 'form-input'}))

    class Meta:
        model = Order
        fields = ['delivery_address', 'phone_number']

    # products = forms.ModelMultipleChoiceField(
    #     queryset=Flower.objects.all(),
    #     widget=forms.CheckboxSelectMultiple,
    #     required=True,
    # )

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(OrderForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['phone_number'].initial = user.phone