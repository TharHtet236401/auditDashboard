from django import forms
from .models import Transaction

class TransactionForm(forms.ModelForm):
    amount = forms.DecimalField(widget=forms.NumberInput(attrs={'class': 'form-control'}), min_value=0)

    class Meta:
        model = Transaction
        fields = ['amount', 'status', 'merchant']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-control'}),
            'merchant': forms.TextInput(attrs={'class': 'form-control'}),
        }

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

    def clean_status(self):
        status = self.cleaned_data.get('status')
        if status not in dict(Transaction.status):
            raise forms.ValidationError("Invalid status")
        return status



