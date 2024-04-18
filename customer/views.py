from django.shortcuts import render, redirect
from django.views import View
from .models import Category, Item, User, CartItem , Order, OrderItem , ContactMessage
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import ContactForm  # Import the ContactForm
from .models import ContactMessage

# views.py



class Index(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'customer/index.html')      

class Menu(View):
    def get(self, request, *args, **kwargs):
        try:
            # making datasets for each category to pass it in context
            appetizers = Item.objects.filter(category__name__contains = 'Appetizer')
            drinks = Item.objects.filter(category__name__contains = 'Drink')
            entres = Item.objects.filter(category__name__contains = 'Entre')
            deserts = Item.objects.filter(category__name__contains = 'Desert')
            takeouts = Item.objects.filter(category__name__contains = 'Takeout')
            context = {}
            # Check if data exists
            if (appetizers.exists() and drinks.exists() and entres.exists() and deserts.exists()):
            # if (appetizers.exists() and drinks.exists() and entres.exists() and deserts.exists() and takeouts.exists()):
                print("appetizers, drinks, entres and deserts  are not empty")
            
        
                context = {
                    'appetizers': appetizers,
                'entres': entres,
                'deserts': deserts,
                'drinks': drinks,

                } 
            else:
                print("One of the categories have no items")         
                
            return render(request, 'customer/menu.html', context)
        except Exception as e:
            print("The error is ", e)
    
    
def login_view(request):
    # if request.user.is_authenticated:
    #     return redirect('order')
    if request.method == 'POST':
        username = request.POST.get('uname')
        password = request.POST.get('pass')

        validate_user = authenticate(username=username, password=password)
        if validate_user is not None:
            login(request, validate_user)
            return redirect('index')
        else:
            messages.error(request, 'Wrong user name/password or user does not exist')
            return redirect('login')

    if request.user.is_authenticated:
        return render(request, 'customer/login.html', {"name": request.user.first_name})
    return render(request, 'customer/login.html', {})

def register(request):
    if request.user.is_authenticated:
        return redirect('index')
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        address = request.POST.get('address')

        if len(password) < 3:
            messages.error(request, 'Password must be at least 3 characters long')
            return redirect('register')
        if password.isalnum() == False:
            messages.error(request, 'Password must contain only numbers and alphabets')
            return redirect('register')

        get_all_users_by_username = User.objects.filter(username=username)        
        if get_all_users_by_username:
            messages.error(request, 'Username already exists, Choose another username.')
            return redirect('register')
        new_user = User.objects.create_user(first_name= first_name, last_name = last_name, username=username, password = password, email=email, address = address)
        new_user.save()

        messages.success(request, 'User created successfully, login now')
        return redirect('login')
    return render(request, 'customer/register.html', {})

def LogoutView(request):
    logout(request)
    return redirect('login')
@login_required
def product_list(request):
    products = Item.objects.all()
    return render(request, 'customer/order.html')
@login_required
def order_view(request):
    products = Item.objects.all()
    return render(request, 'customer/order.html',  context={'products': products})


def add_to_cart(request, product_id):
    if not request.user.is_authenticated:
        return redirect('register')  # Redirect to the registration page if the user is not authenticated

    product = Item.objects.get(id=product_id)
    cart_item, created = CartItem.objects.get_or_create(product=product, user=request.user)
                                                       
    cart_item.quantity += 1
    cart_item.save()
    return redirect('view_cart')

@login_required
def view_cart(request):
    CartItem.objects.filter(user=request.user.is_superuser).delete()
    cart_items = CartItem.objects.filter(user=request.user)
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    return render(request, 'customer/cart.html', {'cart_items': cart_items, 'total_price': total_price})

def remove_from_cart(request, item_id):
    cart_item = CartItem.objects.get(id=item_id)
    cart_item.delete()
    return redirect('view_cart')

def view_order(request):
    CartItem.objects.filter(user = request.user.is_superuser).delete()
    cart_items_cart = CartItem.objects.filter(user = request.user)
    if cart_items_cart.count() == 0:
        return redirect('order')
    total_price = sum(item.product.price * item.quantity for item in cart_items_cart)
    is_paid = True
    user = request.user
    new_order = Order.objects.create(is_paid = is_paid, user = user, total_price = total_price)
    new_order.save()
    for item in cart_items_cart:
        print(item.product.name)
        new_order.order_items.add(OrderItem.objects.create(product = item.product,user = item.user,quantity = item.quantity))
                                
                                                            
        order_items = new_order.order_items.all()
        new_order.save()
    CartItem.objects.filter(user = request.user).all().delete()    

    return render(request, 'customer/order_confirmation.html', {'order_items': order_items, 'order_total_price': total_price, 'user_address': request.user.address,'user_first_name': request.user.first_name})

                                                                
@login_required
def user_orders(request):
    user_orders = Order.objects.filter(user=request.user).all()
    return render(request, 'customer/user_orders.html', {'user_orders': user_orders})
@login_required
def my_account(request):
        my_account = request.user
        return render(request, 'customer/myaccount.html', {'my_account': my_account})

def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)  # Initialize the form with form data
        if form.is_valid():  # Check if the form data is valid
            form.save()  # Save the form data to the database
            return redirect('success')  # Redirect to a success page after saving
    else:
        form = ContactForm()  # Initialize an empty form for GET requests
    return render(request, 'customer/contact.html', {'form': form})

def success_view(request):
    return render(request, 'customer/success.html')


def privacypolicy_view(request):
    return render(request, 'customer/privacypolicy.html')     
def terms_of_services_view(request):
    return render(request, 'customer/terms.html')           
def accessibility_view(request):
    return render(request, 'customer/accessibility.html')    
def home_view(request):
    return render(request, 'customer/home.html')           
def product(request, product_id):
    product = Item.objects.get(pk=product_id)
    recently_viewed_products = None
    # We can pass any dictionary to the session, in this case it is recently_viewed
    if 'recently_viewed' in request.session:
        # If there is a product that's already been viewed, remove it and add it later at the first index as below
        if product_id in request.session['recently_viewed']:
            request.session['recently_viewed'].remove(product_id)

        recently_viewed_products = Item.objects.filter(pk__in=request.session['recently_viewed'])
        recently_viewed_products = sorted(recently_viewed_products, 
            key=lambda x: request.session['recently_viewed'].index(x.id)
            )
        request.session['recently_viewed'].insert(0, product_id)
        # if there are more than 5 itmes in the session, remove the last item
        if len(request.session['recently_viewed']) > 5:
            request.session['recently_viewed'].pop()
    # If there is no intem recently viewed, then current product is added to the recently viewed list
    else:
        request.session['recently_viewed'] = [product_id]
    # update the session every single time 
    request.session.modified = True
    
    context = {'product': product, 'recently_viewed_products': recently_viewed_products}
    return render(request, 'customer/product.html', context)   
    