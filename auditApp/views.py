from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.core.paginator import Paginator
from .models import Transaction
from .forms import TransactionForm

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
        transactions_list = Transaction.objects.all().order_by('-timestamp')
        
        # Debug information
        total_count = transactions_list.count()
        if total_count == 0:
            messages.info(request, 'No transactions in database. Please run python manage.py generate_fake_transactions to create some test data.')
        
        paginator = Paginator(transactions_list, 10)  # Show 10 transactions per page
        page = request.GET.get('page', 1)
        transactions = paginator.get_page(page)
        
        # If it's an HTMX request, return only the table partial
        if request.headers.get('HX-Request'):
            return render(request, 'partials/transaction.html', {'transactions': transactions})
            
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
        messages.error(request, str(e))
        return redirect('home')

@login_required
def update_status(request, pk):
    try:
        if request.method != 'POST':
            return HttpResponse('Method not allowed', status=405)
            
        transaction = get_object_or_404(Transaction, pk=pk)
        new_status = request.POST.get('status')
        
        if new_status not in ['Approved', 'Pending', 'Rejected']:
            return messages.error(request, 'Invalid status')
            
        transaction.status = new_status
        if new_status == 'Approved':
            transaction.approved_by = request.user
        else:
            transaction.approved_by = None
        transaction.save()
        
        # Get current page from request
        page = request.GET.get('page', 1)
        
        # Return the updated transaction list with pagination
        transactions_list = Transaction.objects.all().order_by('-timestamp')
        paginator = Paginator(transactions_list, 10)
        transactions = paginator.get_page(page)
        
        return render(request, 'partials/transaction.html', {'transactions': transactions})
        
    except Exception as e:
        return HttpResponse(str(e), status=500)

@login_required
def update_flag(request, pk):
    try:
        if request.method != 'POST':
            return HttpResponse('Method not allowed', status=405)
            
        transaction = get_object_or_404(Transaction, pk=pk)
        is_flagged = request.POST.get('is_flagged') == 'true'
        
        transaction.isFlagged = is_flagged
        transaction.save()
        
        # Get current page from request
        page = request.GET.get('page', 1)
        
        # Return the updated transaction list with pagination
        transactions_list = Transaction.objects.all().order_by('-timestamp')
        paginator = Paginator(transactions_list, 10)
        transactions = paginator.get_page(page)
        
        return render(request, 'partials/transaction.html', {'transactions': transactions})
        
    except Exception as e:
        return HttpResponse(str(e), status=500)

def add_transaction(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = TransactionForm()
    return render(request, 'partials/transaction_form.html', {'form': form})
