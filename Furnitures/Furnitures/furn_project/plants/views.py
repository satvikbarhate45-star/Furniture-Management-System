from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from .models import Profile

# Register
def register(request):
    if request.method == 'POST':
        fname = request.POST['first_name']
        lname = request.POST['last_name']
        uname = request.POST['username']
        email = request.POST['email']
        contact = request.POST['contact']
        password = request.POST['password']

        # Create user
        user = User.objects.create_user(
            username=uname,
            email=email,
            password=password,
            first_name=fname,
            last_name=lname
        )

        # Save contact
        Profile.objects.create(user=user, contact=contact)

        return redirect('login')

    return render(request, 'register.html')


# Login
def user_login(request):
    if request.method == 'POST':
        uname = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=uname, password=password)

        if user is not None:
            login(request, user)

            if user.is_superuser:
                return redirect('admin_page')
            else:
                return redirect('home')
        else:
            return render(request, 'login.html', {'error': 'Invalid username or password'})

    return render(request, 'login.html')


# Home
def home(request):
    return render(request, 'home.html')


# Admin Page
def admin_page(request):
    return render(request, 'admin.html')



from django.contrib.auth.models import User
from .models import Plant, Booking

def admin_page(request):
    plants = Plant.objects.all()
    bookings = Booking.objects.all()
    users = User.objects.filter(is_superuser=False)

    return render(request, 'admin.html', {
        'plants': plants,
        'bookings': bookings,
        'users': users
    })
    
    
    
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Plant

def add_plant(request):
    if request.method == 'POST':
        plant_id = request.POST.get('plant_id')

        # 🔴 Check if ID already exists
        if Plant.objects.filter(plant_id=plant_id).exists():
            messages.error(request, "⚠️ Plant ID already exists! Please enter a different ID.")
            return redirect('add_plant')

        # ✅ Save if unique
        Plant.objects.create(
            plant_id=plant_id,
            name=request.POST.get('name'),
            info=request.POST.get('info'),
            price=request.POST.get('price'),
            image=request.FILES.get('image'),
            growth=request.POST.get('growth'),
            quality=request.POST.get('quality'),
            quantity=request.POST.get('quantity')
        )

        messages.success(request, "✅ Plant Added Successfully!")
        return redirect('add_plant')

    return render(request, 'addplants.html')

from django.shortcuts import render, get_object_or_404
from .models import Plant

def view_plant(request, id):
    plant = get_object_or_404(Plant, id=id)
    return render(request, 'adviewplant.html', {'plant': plant})


from django.shortcuts import render, redirect, get_object_or_404
from .models import Plant

def edit_plant(request, id):
    plant = get_object_or_404(Plant, id=id)

    if request.method == 'POST':
        plant.name = request.POST['name']
        plant.plant_type = request.POST['plant_type']
        plant.info = request.POST['info']
        plant.price = request.POST['price']
        plant.quantity = request.POST['quantity']
        plant.growth = request.POST['growth']
        plant.quality = request.POST['quality']

        # 🖼️ Update image only if new uploaded
        if request.FILES.get('image'):
            plant.image = request.FILES['image']

        plant.save()
        return redirect('admin_page')

    return render(request, 'adeditplant.html', {'plant': plant})


def delete_plant(request, id):
    plant = Plant.objects.get(id=id)
    plant.delete()
    return redirect('admin_page')


def view_all_plants(request):
    plants = Plant.objects.all()
    return render(request, 'adviewallplants.html', {'plants': plants})

from django.shortcuts import render, redirect
from .models import Plant

def us_view_plants(request):
    """
    User panel to view all plants in card layout.
    Uses session to store cart items.
    """
    plants = Plant.objects.all()

    # Initialize session cart if not exists
    if 'cart' not in request.session:
        request.session['cart'] = []

    # Pass cart items for header
    cart_items = request.session['cart']

    return render(request, 'us_view_plants.html', {
        'plants': plants,
        'cart_items': cart_items
    })
    

from django.shortcuts import render, redirect
from .models import Plant

def us_view_plants(request):
    """
    User panel to view all plants in card layout.
    Uses session to store cart items.
    """
    plants = Plant.objects.all()

    # Initialize session cart if not exists
    if 'cart' not in request.session:
        request.session['cart'] = []

    # Pass cart items for header
    cart_items = request.session['cart']

    return render(request, 'us_view_plants.html', {
        'plants': plants,
        'cart_items': cart_items
    })
    
    
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Plant

@csrf_exempt
def add_to_cart(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        plant_id = data['id']
        name = data['name']
        image = data['image']

        cart = request.session.get('cart', [])
        cart.append({'id': plant_id, 'name': name, 'image': image})
        request.session['cart'] = cart

        return JsonResponse({
            'cart_count': len(cart),
            'cart_items': cart
        })
        
from django.http import JsonResponse
import json

def remove_from_cart(request):
    if request.method == "POST":
        data = json.loads(request.body)
        plant_id = data.get("id")

        # Get cart from session
        cart = request.session.get("cart", [])

        # Remove item by id
        cart = [item for item in cart if str(item['id']) != str(plant_id)]

        # Save updated cart back to session
        request.session['cart'] = cart

        return JsonResponse({
            "cart_count": len(cart),
            "cart_items": cart
        })
        
        
from django.shortcuts import render, get_object_or_404
from .models import Plant

def us_view_plant_details(request, id):
    plant = get_object_or_404(Plant, id=id)
    return render(request, 'us_view_plant_details.html', {'plant': plant})



from django.shortcuts import render, redirect, get_object_or_404
from .models import Plant, Booking
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta

@login_required
def buy_plant(request, id):
    plant = get_object_or_404(Plant, id=id)

    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        contact = request.POST.get("contact")
        address = request.POST.get("address")
        state = request.POST.get("state")
        district = request.POST.get("district")
        location = request.POST.get("location")
        pincode = request.POST.get("pincode")
        pay_method = request.POST.get("pay_method")

        booking = Booking.objects.create(
            user=request.user,
            plant=plant,
            first_name=first_name,
            last_name=last_name,
            contact=contact,
            address=address,
            state=state,
            district=district,
            location=location,
            pincode=pincode,
            pay_method=pay_method,
            delivery_date=datetime.now() + timedelta(days=4),
            status="pending"
        )

        if pay_method == "online":
            # Redirect to dummy online payment page
            return redirect('online_payment', booking_id=booking.id)
        else:
            # Offline COD, redirect to congratulations page
            return redirect('order_success', booking_id=booking.id)

    return render(request, 'buyform.html', {'plant': plant})


from django.shortcuts import render, get_object_or_404, redirect
from .models import Booking

@login_required
def online_payment(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    if request.method == "POST":
        # Simulate payment success
        booking.status = "paid"
        booking.save()
        return redirect('order_success', booking_id=booking.id)
    return render(request, 'online_payment.html', {'booking': booking})

@login_required
def order_success(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    return render(request, 'congratulation.html', {'booking': booking})





from django.shortcuts import render, redirect, get_object_or_404
from .models import Booking
from django.contrib.auth.decorators import login_required

@login_required
def user_my_orders(request):
    bookings = Booking.objects.filter(user=request.user).order_by('-booking_date')
    return render(request, 'user_my_orders.html', {'bookings': bookings})

@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    if booking.status == "pending":
        booking.status = "cancelled"
        booking.save()
    return redirect('user_my_orders')



from django.contrib.auth import logout
from django.shortcuts import redirect

def user_logout(request):
    logout(request)
    return redirect('login')


from django.shortcuts import render, redirect, get_object_or_404
from .models import Booking
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from datetime import datetime, timedelta
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

@login_required
def admin_manage_orders(request):
    """
    Display all bookings for admin with options:
    Deliver, Cancel, Edit, Delete.
    Table updates dynamically with animations.
    """
    bookings = Booking.objects.all().order_by('-booking_date')
    return render(request, 'adminmanageorder.html', {'bookings': bookings})


@login_required
def mark_delivered(request, id):
    booking = get_object_or_404(Booking, id=id)
    booking.status = 'delivered'
    booking.save()
    messages.success(request, f"Booking #{booking.id} marked as Delivered.")
    return redirect('admin_manage_orders')

from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Booking
@login_required
def cancel_booking(request, booking_id):   # ✅ FIX HERE
    booking = get_object_or_404(Booking, id=booking_id)

    booking.status = "cancelled"
    booking.save()

    return redirect('user_my_orders')


@login_required
def delete_booking(request, id):
    booking = get_object_or_404(Booking, id=id)
    booking.delete()
    messages.success(request, f"Booking #{id} Deleted.")
    return redirect('admin_manage_orders')

from django.shortcuts import render, redirect, get_object_or_404
from .models import Booking, Plant
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta
from django.contrib import messages

# Edit Booking
@login_required
def edit_booking(request, id):
    booking = get_object_or_404(Booking, id=id)

    if request.method == "POST":
        booking.first_name = request.POST.get("first_name")
        booking.last_name = request.POST.get("last_name")
        booking.contact = request.POST.get("contact")
        booking.address = request.POST.get("address")
        booking.state = request.POST.get("state")
        booking.district = request.POST.get("district")
        booking.location = request.POST.get("location")
        booking.pincode = request.POST.get("pincode")
        booking.quantity = request.POST.get("quantity")
        booking.pay_method = request.POST.get("pay_method")

        # Update delivery date if needed (optional)
        booking.delivery_date = datetime.now() + timedelta(days=4)

        booking.save()
        messages.success(request, "Booking updated successfully.")
        return redirect('admin_manage_orders')

    return render(request, 'edit_booking.html', {'booking': booking})

# Delete Booking
@login_required
def delete_booking(request, id):
    booking = get_object_or_404(Booking, id=id)

    if request.method == "POST":
        booking.delete()
        messages.success(request, "Booking deleted successfully.")
        return redirect('admin_manage_orders')

    # Optional: confirmation page
    return render(request, 'confirm_delete_booking.html', {'booking': booking})


from django.shortcuts import render

def services_view(request):
    """
    Render the services page
    """
    return render(request, 'service.html')


from django.shortcuts import render

def about(request):
    return render(request, 'about.html')



from django.shortcuts import render

def contact(request):
    return render(request, 'contact.html')


from django.shortcuts import render
from .models import Contact  # assuming your model is Contact

def admin_user_issues(request):
    """
    Admin view to display all user-submitted issues/messages.
    """
    issues = Contact.objects.all().order_by('-created_at')  # latest first
    return render(request, 'admin_user_issues.html', {'issues': issues})

from django.shortcuts import render
from .models import Plant

def user_view_home_plants(request):
    plants = Plant.objects.all()   # fetch all plants from database
    return render(request, 'user_viewhomeplant.html', {'plants': plants})

from django.shortcuts import render, get_object_or_404
from .models import Plant

def plant_detail(request, id):
    plant = get_object_or_404(Plant, id=id)
    return render(request, 'plant_detail.html', {'plant': plant})


from django.shortcuts import get_object_or_404, redirect
from .models import Booking

def deliver_booking(request, id):
    booking = get_object_or_404(Booking, id=id)
    booking.status = "Delivered"
    booking.save()
    return redirect('admin_manage_orders')