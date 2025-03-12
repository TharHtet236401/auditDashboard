from django import forms
from .models import Transaction

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['merchant', 'amount']

    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        if amount <= 0:
            raise forms.ValidationError("Amount must be greater than 0")
        return amount

    def clean_merchant(self):
        merchant = self.cleaned_data.get('merchant')
        if not merchant:
            raise forms.ValidationError("Merchant is required")
        return merchant
