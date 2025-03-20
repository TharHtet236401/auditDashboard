from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.core.paginator import Paginator
from .models import Transaction, TransactionHistory
from .forms import TransactionForm
from .signals import set_current_user
from .forms import UserRegistrationForm
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from django.db import DatabaseError
from django.db.models import Count
from django.core.serializers.json import DjangoJSONEncoder
import json

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

def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration successful. Please login.')
            return redirect('login')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserRegistrationForm()

    return render(request, 'register.html', {'form': form})
            
@login_required
def home(request):
    try:
        transactions_list = Transaction.objects.all().order_by('-timestamp')
        
        # Apply filters if they exist
        status_filter = request.GET.get('status', '')
        flag_filter = request.GET.get('flag', '')
        
        filters = Q()
        if status_filter:  # Only filter if a specific status is selected
            filters &= Q(status=status_filter)
            
        if flag_filter:  # Only filter if a specific flag is selected
            is_flagged = flag_filter == 'Flagged' # it will get true if the flag is Flagged
            filters &= Q(isFlagged=is_flagged)
        
        if filters:
            transactions_list = transactions_list.filter(filters)

        paginator = Paginator(transactions_list, 10)
        page = request.GET.get('page', 1)
        transactions = paginator.get_page(page)
        
        if request.headers.get('HX-Request'):
            # For main content updates (including filters)
            if 'main-content' in request.headers.get('HX-Target', ''):
                return render(request, 'partials/transaction.html', {'transactions': transactions})
            # For full container updates
            return render(request, 'partials/home_content.html', {'transactions': transactions})
        
        return render(request, 'home.html', {'transactions': transactions})
    except Exception as e:
        messages.error(request, str(e))
        # Instead of redirecting, render the home template with an empty transaction list
        return render(request, 'home.html', {'transactions': []})

def logout_view(request):
    logout(request)
    messages.success(request, 'Successfully logged out')
    return redirect('login')

@login_required
def transaction_detail(request, pk):
    try:
        transaction = Transaction.objects.get(pk=pk)
        return render(request, 'partials/transaction_detail.html', {
            'transaction': transaction
        })
    except ObjectDoesNotExist:
        messages.error(request, 'Transaction not found.')
        return redirect('home')
    except DatabaseError as e:
        messages.error(request, 'A database error occurred.')
        # Log the error for debugging
        print(f"Database error: {e}")
        return redirect('home')

@login_required
def update_status(request, pk):
    try:
        # Set current user for history tracking
        set_current_user(request.user)
        
        if request.method != 'POST':
            return HttpResponse('Method not allowed', status=405)
            
        transaction = get_object_or_404(Transaction, pk=pk)
        new_status = request.POST.get('status')
        
        if new_status not in ['Approved', 'Pending', 'Rejected']:
            return messages.error(request, 'Invalid status')
            
        transaction.status = new_status
        if new_status == 'Approved':
            transaction.approved_by = request.user
        elif new_status == 'Pending':
            transaction.approved_by = None
        elif new_status == 'Rejected':
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
        messages.error(request, str(e))
        return redirect('home')

@login_required
def update_flag(request, pk):
    try:
        # Set current user for history tracking
        set_current_user(request.user)
        
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
        messages.error(request, str(e))
        return redirect('home')

@login_required
def add_transaction(request):
    try:
        if request.method == 'POST':
            form = TransactionForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('home')
            else:
                messages.error(request, 'Please correct the errors below.')
                # If it's an HTMX request, return the form partial
                if request.headers.get('HX-Request'):
                    return render(request, 'partials/transaction_form.html', {'form': form})
                # If it's a regular request, return the full page
                return render(request, 'partials/transaction_form.html', {'form': form})
        else:
            form = TransactionForm()

        # For GET requests
        if request.headers.get('HX-Request'):
            return render(request, 'partials/transaction_form.html', {'form': form})
        return render(request, 'partials/transaction_form.html', {'form': form})
        
    except Exception as e:
        messages.error(request, str(e))
        return redirect('home')

@login_required
def all_transaction_history(request):
    try:
        # Get all history entries ordered by timestamp
        history = TransactionHistory.objects.all().select_related(
            'transaction', 'changed_by'
        ).order_by('-changed_at')
        
        # Setup pagination
        paginator = Paginator(history, 20)  # Show 20 entries per page
        page = request.GET.get('page', 1)
        history_entries = paginator.get_page(page)
        
        # If it's an HTMX request, return just the history content
        if request.headers.get('HX-Request'):
            return render(request, 'partials/all_history.html', {
                'history': history_entries
            })
        
        # For non-HTMX requests, return the full page
        return render(request, 'partials/all_history.html', {
            'history': history_entries
        })
        
    except Exception as e:
        messages.error(request, str(e))
        return redirect('home')

@login_required
def filter_transactions(request):
    try:
        status = request.GET.get('status', 'All')
        flag = request.GET.get('flag', 'All')
        
        transactions_list = Transaction.objects.all().order_by('-timestamp')
        
        if status != 'All':
            transactions_list = transactions_list.filter(status=status)
            
        if flag != 'All':
            is_flagged = flag == 'Flagged'
            transactions_list = transactions_list.filter(isFlagged=is_flagged)
        
        paginator = Paginator(transactions_list, 10)
        page = request.GET.get('page', 1)
        transactions = paginator.get_page(page)
        
        return render(request, 'partials/transaction.html', {'transactions': transactions})
    except Exception as e:
        messages.error(request, str(e))
        return redirect('home')

def delete_transaction(request, pk):
    try:
        transaction = Transaction.objects.get(pk=pk)
        print(transaction)
        transaction.delete()
        return redirect('home')
    except Exception as e:
        messages.error(request, str(e))
        return redirect('home')
    
def multiple_delete_transaction(request):
    try:
        transaction_ids = request.POST.getlist('transaction_ids')

        if not transaction_ids:
            messages.warning(request, "No transactions selected for deletion.")
            return redirect('home')

        transactions = Transaction.objects.filter(id__in=transaction_ids)

        if not transactions.exists():
            messages.warning(request, "No matching transactions found.")
            return redirect('home')

        transactions.delete()
        messages.success(request, "Selected transactions have been deleted successfully.")
        
    except DatabaseError as db_err:
        messages.error(request, f"Database error occurred: {db_err}")
    except Exception as e:
        messages.error(request, f"An unexpected error occurred: {e}")

    return redirect('home')


def analytics_view(request):
    try:
        # Get status counts
        status_counts = Transaction.objects.values('status').annotate(count=Count('status'))
        
        # Convert to dictionary format and ensure all statuses are represented
        status_data = {
            'Approved': 0,
            'Pending': 0,
            'Rejected': 0
        }
        
        # Update with actual counts
        for item in status_counts:
            if item['status'] in status_data:
                status_data[item['status']] = item['count']
        
        # Debug print
        print("Status data before JSON:", status_data)
        
        # Convert to JSON string
        json_data = json.dumps(status_data)
        print("JSON data:", json_data)  # Debug print
        
        return render(request, 'partials/analytics.html', {
            'status_data': json_data
        })
        
    except Exception as e:
        print("Error in analytics_view:", str(e))  # Debug print
        messages.error(request, f"Error generating analytics: {str(e)}")
        return redirect('home')
