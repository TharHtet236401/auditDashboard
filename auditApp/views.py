from django.shortcuts import render
from .models import Transaction

# Create your views here.
def home(request):
    transactions = Transaction.objects.all()
    return render(request, 'home.html', {'transactions': transactions})

