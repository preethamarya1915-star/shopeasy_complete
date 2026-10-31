from decimal import Decimal
from django.contrib import messages
from django.db import transaction
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from .models import Product, Order, OrderItem
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm

def get_cart_data(request):
    cart = request.session.get("cart", {})
    items, total, count = [], Decimal("0.00"), 0
    for product_id, quantity in cart.items():
        product = Product.objects.filter(id=product_id).first()
        if not product or int(quantity) < 1:
            continue
        quantity = min(int(quantity), product.stock)
        subtotal = product.price * quantity
        items.append({"product": product, "quantity": quantity, "subtotal": subtotal})
        total += subtotal
        count += quantity
    return items, total, count

def home(request):
    products = Product.objects.all()
    query = request.GET.get("q", "").strip()
    category = request.GET.get("category", "").strip()
    sort = request.GET.get("sort", "")
    if query:
        products = products.filter(Q(name__icontains=query) | Q(description__icontains=query))
    if category:
        products = products.filter(category=category)
    if sort == "low":
        products = products.order_by("price")
    elif sort == "high":
        products = products.order_by("-price")
    cart_items, total, cart_count = get_cart_data(request)
    return render(request, "store/home.html", {
        "products": products, "query": query, "selected_category": category,
        "sort": sort, "categories": Product.CATEGORY_CHOICES,
        "cart_count": cart_count, "cart_items": cart_items,
    })

def add_to_cart(request, product_id):
    if request.method == "POST":
        product = get_object_or_404(Product, id=product_id)
        cart = request.session.get("cart", {})
        key = str(product.id)
        current = int(cart.get(key, 0))
        if current < product.stock:
            cart[key] = current + 1
            request.session["cart"] = cart
            messages.success(request, f"{product.name} added to your cart.")
        else:
            messages.error(request, "Sorry, the available stock limit has been reached.")
    return redirect(request.META.get("HTTP_REFERER", "home"))

def update_cart(request, product_id):
    if request.method == "POST":
        product = get_object_or_404(Product, id=product_id)
        try:
            quantity = int(request.POST.get("quantity", 1))
        except ValueError:
            quantity = 1
        cart = request.session.get("cart", {})
        if quantity <= 0:
            cart.pop(str(product_id), None)
        else:
            cart[str(product_id)] = min(quantity, product.stock)
        request.session["cart"] = cart
    return redirect("cart")

def remove_from_cart(request, product_id):
    if request.method == "POST":
        cart = request.session.get("cart", {})
        cart.pop(str(product_id), None)
        request.session["cart"] = cart
    return redirect("cart")

def cart_detail(request):
    items, total, count = get_cart_data(request)
    return render(request, "store/cart.html", {"cart_items": items, "total": total, "cart_count": count})

def checkout(request):
    items, total, count = get_cart_data(request)
    if not items:
        messages.info(request, "Your cart is empty.")
        return redirect("home")
    if request.method == "POST":
        name = request.POST.get("customer_name", "").strip()
        email = request.POST.get("email", "").strip()
        phone = request.POST.get("phone", "").strip()
        address = request.POST.get("address", "").strip()
        if not all([name, email, phone, address]):
            return render(request, "store/checkout.html", {
                "cart_items": items, "total": total, "cart_count": count,
                "error": "Please complete every field.",
            })
        with transaction.atomic():
            order = Order.objects.create(
            user=request.user if request.user.is_authenticated else None,
            customer_name=name,
            email=email,
            phone=phone,
            address=address,
            total_amount=total
)
            for item in items:
                product = Product.objects.select_for_update().get(id=item["product"].id)
                if product.stock < item["quantity"]:
                    messages.error(request, f"Not enough stock for {product.name}. Please update your cart.")
                    order.delete()
                    return redirect("cart")
                OrderItem.objects.create(
                    order=order, product=product, product_name=product.name,
                    price=product.price, quantity=item["quantity"]
                )
                product.stock -= item["quantity"]
                product.save(update_fields=["stock"])
        request.session["cart"] = {}
        return redirect("order_success", order_id=order.id)
    return render(request, "store/checkout.html", {
        "cart_items": items, "total": total, "cart_count": count,
    })

def order_success(request, order_id):
    order = get_object_or_404(Order.objects.prefetch_related("items"), id=order_id)
    return render(request, "store/order_success.html", {"order": order})
def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    return render(
        request,
        "store/product_detail.html",
        {"product": product}
    )
def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Account created successfully!")
            return redirect("home")
    else:
        form = UserCreationForm()

    return render(request, "store/register.html", {"form": form})


def user_login(request):
    if request.method == "POST":
        form = AuthenticationForm(
            request,
            data=request.POST
        )

        if form.is_valid():
            login(request, form.get_user())
            messages.success(request, "Welcome back!")
            return redirect("home")
    else:
        form = AuthenticationForm()

    return render(request, "store/login.html", {"form": form})


def user_logout(request):
    logout(request)
    return redirect("home")
@login_required
def order_history(request):
    orders = Order.objects.filter(
        user=request.user
    ).order_by("-created_at")

    return render(
        request,
        "store/order_history.html",
        {"orders": orders}
    )
@login_required
def profile(request):
    user_orders = Order.objects.filter(user=request.user)

    context = {
        "customer": request.user,
        "total_orders": user_orders.count(),
        "recent_orders": user_orders.order_by("-created_at")[:5],
    }

    return render(request, "store/profile.html", context)
