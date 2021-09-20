from django import forms
from order.models import Order
from authentication.models import CustomUser
from book.models import Book


class EditOrderForm(forms.ModelForm):
    user = forms.ModelChoiceField(queryset=CustomUser.objects.all(), required=True)
    book = forms.ModelChoiceField(queryset=Book.objects.all(), required=True)
    end_at = forms.DateTimeField(widget=forms.widgets.DateTimeInput())
    plated_end_at = forms.DateTimeField(widget=forms.widgets.DateTimeInput())

    class Meta:
        model = Order
        fields = ['user', 'book', 'end_at', 'plated_end_at']


