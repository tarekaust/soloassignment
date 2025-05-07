from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Order, User
from django.contrib import messages
from django.db import models

def register(request):
    if request.method == 'POST':
        user_name = request.POST['user_name']
        full_name = request.POST['full_name']
        email = request.POST['email']
        phone = request.POST['phone']
        password = request.POST['password']  # not saved now
        user_type = request.POST.get('user_type', 'customer')

        # Check if the user is trying to create an admin account
        if user_type == 'admin' and email != 'superadmin@ecom.com':
            # Ensure the current session user is logged in and is an admin
            if not request.session.get('user_id') or request.session.get('login_type') != 'admin':
                messages.error(request, "Only an admin can create another admin user.")
                return redirect('login')

        try:
            user = User(
                user_name=user_name,
                full_name=full_name,
                email=email,
                phone=phone,
                user_type=user_type,
                password=password  # Save password if needed
            )
            user.save()
            messages.success(request, "Registration successful! Please login.")
            if request.session.get('login_type') == 'admin':
                # If the user is logged in as admin, redirect to admin dashboard
                return redirect('admin_dashboard')
            else:
                return redirect('login')
        except Exception as e:
            messages.error(request, f"Registration failed: {e}")

    return render(request, 'importer/register.html')


def login_view(request):
    if request.session.get('user_id'):
        return redirect('product_list')  # Already logged in

    if request.method == 'POST':
        user_name = request.POST.get('user_name')
        phone = request.POST.get('phone')
        login_type = request.POST.get('login_type')
        password = request.POST.get('password')  # not used now

        if not login_type:
            messages.error(request, "Please select a login type.")
            return render(request, 'importer/login.html')

        try:
            user = User.objects.get(user_name=user_name, phone=phone, password=password)
            request.session['user_id'] = user.id
            request.session['user_name'] = user.user_name
            request.session['phone'] = user.phone
            request.session['login_type'] = login_type  # Save login type in session

            messages.success(request, "Login successful!")

            if login_type == 'customer':
                return redirect('product_list')
            elif login_type == 'admin':
                return redirect('admin_dashboard')  # Example: you can create this admin page
            else:
                messages.error(request, "Invalid login type selected.")
                return render(request, 'importer/login.html')

        except User.DoesNotExist:
            messages.error(request, "Invalid credentials. Try again.")

    return render(request, 'importer/login.html')


def show_all_product(request):
    if not request.session.get('user_id'):
        return redirect('login')  # Force login if not logged in

    # Your existing product list logic here
    products = Product.objects.all()  # assuming you have a Product model
    query = request.GET.get('q')
    if query:
        products = products.filter(name__icontains=query)

    context = {'product': products}
    return render(request, 'importer/product_list.html', context)


def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        quantity = request.POST.get('quantity')
        buyer_phone = request.POST.get('buyer_phone')  # Get buyer_phone from the form

        # Create a new order
        Order.objects.create(
            product=product,
            quantity=quantity,
            buyer_phone=buyer_phone  # Save the phone number
        )

        return redirect('product_list')  # Redirect to a success page

    return render(request, 'importer/product_detail.html', {'product': product})


def logout_view(request):
    request.session.flush()  # Clear all session data
    messages.success(request, "Logged out successfully.")
    return redirect('login')  # Redirect back to login page


def admin_dashboard(request):
    if request.session.get('login_type') != 'admin':
        messages.error(request, "Access denied. Admins only.")
        return redirect('login')

    user_count = User.objects.count()
    order_count = Order.objects.count()

    users = User.objects.all().order_by('-id')
    orders = Order.objects.all().order_by('-id')

    # Calculate amount for each order
    for order in orders:
        try:
            product = Product.objects.get(id=order.product_id)
            order.amount = product.price * order.quantity
        except Product.DoesNotExist:
            order.amount = 0

    # For bar chart: orders per date
    orders_by_date = (
        Order.objects.extra(select={'date': "date(order_date)"})
        .values('date')
        .order_by('date')
        .annotate(count=models.Count('id'))
    )

    # For pie chart:
    non_admin_users = User.objects.exclude(user_type='admin')
    non_admin_user_count = non_admin_users.count()

    # Users who ordered
    users_with_orders = non_admin_users.filter(phone__in=Order.objects.values_list('buyer_phone', flat=True).distinct()).count()

    # Users who didn't order
    users_without_orders = non_admin_user_count - users_with_orders

    context = {
        'user_count': user_count,
        'order_count': order_count,
        'users': users,
        'orders': orders,
        'orders_by_date': orders_by_date,
        'users_with_orders': users_with_orders,
        'users_without_orders': users_without_orders,
    }

    return render(request, 'importer/admin_dashboard.html', context)


def order_history(request):
    if not request.session.get('user_id'):
        return redirect('login')  # Not logged in

    user_id = request.session.get('user_id')
    buyer_phone = request.session.get('phone')  # Get buyer_phone from session
    orders = Order.objects.filter(buyer_phone=buyer_phone).order_by('-order_date')

    # Calculate amount for each order
    for order in orders:
        try:
            product = Product.objects.get(id=order.product_id)  # Get product by ID
            order.amount = product.price * order.quantity  # Calculate total
        except Product.DoesNotExist:
            order.amount = 0  # If product not found, set amount to 0

    total_amount = sum(order.amount for order in orders)

    return render(request, 'importer/order_history.html', {'orders': orders, 'total_amount': total_amount})