from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import Transaction

# Create your views here.
def login_view(request):
    # Redirect to home if user is already authenticated
    if request.user.is_authenticated:
        return redirect('home')
        
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if not username or not password:
            messages.error(request, 'Please provide both username and password')
            return render(request, 'login.html')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Get the next parameter or default to home
            next_url = request.GET.get('next', 'home')
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid username or password')
    
    return render(request, 'login.html')


@login_required
def home(request):
    try:
        transactions = Transaction.objects.all().order_by('-timestamp')
        return render(request, 'home.html', {'transactions': transactions})
    except Exception as e:
        messages.error(request, str(e))
        return redirect('login')

def logout_view(request):
    logout(request)
    messages.success(request, 'Successfully logged out')
    return redirect('login')

@login_required
def transaction_detail(request, pk):
    try:
        transaction = get_object_or_404(Transaction, pk=pk)
        return render(request, 'partials/transaction_detail.html', {
            'transaction': transaction
        })
    except Exception as e:
        return HttpResponse(
            '''<div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title text-danger">Error</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    <p class="text-danger">Failed to load transaction details: {}</p>
                </div>
            </div>'''.format(str(e)),
            status=500
        )


