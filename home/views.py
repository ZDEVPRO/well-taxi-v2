from django.shortcuts import render, redirect
from asyncio.log import logger
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from home.forms import NewUserForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from home.models import *
from django.http import JsonResponse, HttpResponse


@login_required(login_url='/kirish/')
def homeView(request):
    if request.user.is_authenticated:
        user = request.user
        return switcher(user)
    else:
        return redirect('kirish')


def switcher(user):
    try:
        if user.type == 1:
            return redirect('driver-home')
        elif user.type == 2:
            return redirect('driver-home')
        elif user.type == 3:
            return redirect('customer')
        else:
            return redirect('logout')
    except Exception as e:
        logger.error(f"{e}")
        return redirect('logout')


def customer_register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                user.type = 3
                user.first_name = request.POST.get('first_name')
                user.last_name = request.POST.get('last_name')
                user.username = request.POST.get('username')
                user.phone = request.POST.get('phone')
                password1 = request.POST.get('password1')
                password2 = request.POST.get('password2')
                if password1 == password2:
                    user.password1 = password1
                    user.password2 = password2
                    user.save()
                login(request, user)
                messages.success(request,
                                 "Muvoffaqiyatli ro'yxatdan o'tildi! Endi Ro'yxatdan o'tgan fodalanuvchi nomingiz va parolingizni kiriting!")
                return redirect("customer-login")
            except Exception as e:
                print(e)
                messages.error(request, 'Foydalanuvchi nomi yoki parol xato')
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm()
    return render(request=request, template_name="registration/customer/register.html", context={"form": form})


def customer_login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'Foydalanuvchi nomi yoki Parol Xato!')
                return redirect('home')
        else:
            messages.error(request, 'Foydalanuvchi nomi yoki Parol Xato!')
    form = AuthenticationForm()
    context = {'login_form': form}
    return render(request, 'registration/customer/login.html', context)


def driver_login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, "Foydalanuvchi nomi yoki parol xato!")
        else:
            messages.error(request, 'Foydalanuvchi nomi yoki parol xato!')
            return redirect('driver-login')
    form = AuthenticationForm()
    context = {'login_form': form}
    return render(request, 'registration/driver/login.html', context)


def logout_view(request):
    logout(request)
    return redirect('kirish')


def kirish(request):
    return render(request, 'registration/kirish.html')

@login_required(login_url='/kirish/')
def getorders_driver(request):
    if request.method == 'GET':
        try:
            try:
                myfilter = Filter.objects.get(user=request.user)

                # barchasi to'g'ri kelsa
                if myfilter.status == 'filter' and myfilter.qayerdan is not None and myfilter.qayerga is not None:
                    orders_all = Order.objects.filter(status='yangi', qayerdan__nomi=myfilter.qayerdan,
                                                      qayerga__nomi=myfilter.qayerga).order_by('-id')
                # qayerdan kelsa
                elif myfilter.status == 'filter' and myfilter.qayerdan is not None and myfilter.qayerga is None:
                    orders_all = Order.objects.filter(status='yangi', qayerdan__nomi=myfilter.qayerdan).order_by('-id')
                # qayerga kelsa
                elif myfilter.status == 'filter' and myfilter.qayerga is not None and myfilter.qayerdan is None:
                    orders_all = Order.objects.filter(status='yangi', qayerga__nomi=myfilter.qayerga).order_by('-id')
                # status barchasi bo'lsa
                elif myfilter.status == 'barchasi':
                    orders_all = Order.objects.filter(status='yangi').order_by('-id')
                else:
                    orders_all = Order.objects.filter(status='yangi').order_by('-id')

                active_orders_count = orders_all.count()
                kutish_orders_count = Order.objects.filter(status='kutish').count()
                olindi_orders_count = Order.objects.filter(status='olindi').count()

                context = {
                    'count': active_orders_count,
                    'kutish_count': kutish_orders_count,
                    'olindi_count': olindi_orders_count,
                    'orders': list(orders_all.values())
                }

                return JsonResponse(context)
            except Exception as e:
                print(e)
                print(e)
                print(e)
                nfilter = Filter()
                nfilter.user = request.user
                nfilter.qayerdan = None
                nfilter.qayerga = None
                nfilter.status = 'barchasi'
                nfilter.save()
                return redirect('getorders-driver')


        except Exception as e:
            try:
                mfilter = Filter.objects.get(user=request.user)

                if mfilter is None:
                    new_filter = Filter()
                    new_filter.user = request.user
                    new_filter.qayerdan = None
                    new_filter.qayerga = None
                    new_filter.status = 'barchasi'
                    new_filter.save()
                elif mfilter is not None:
                    print(e)
                    print(e)
                    print(e)
            except Exception as e:
                print(e)
                print(e)
                print(e)
                new_filter = Filter()
                new_filter.user = request.user
                new_filter.qayerdan = None
                new_filter.qayerga = None
                new_filter.status = 'barchasi'
                new_filter.save()

            return JsonResponse({'xato': 'xatolik!'})

@login_required(login_url='/kirish/')
def get_customer_order_detail(request, id):
    try:
        obj = Order.objects.get(id=id)
        context = {
            'id': obj.id,
            'status': obj.status,
            'qayerdan': obj.qayerdan_nomi,
            'qayerga': obj.qayerga_nomi,
            'client_phone': obj.client_phone,
            'location': obj.location,
            'driver_phone': obj.driver_phone,
            'price_nomi': obj.price_nomi,
            'person_count': obj.person_count
        }
        return JsonResponse(context)
    except Exception as e:
        print(e)
        JsonResponse({'xato': 'Xatolik!'})

@login_required(login_url='/kirish/')
def getorders_customer(request):
    try:
        queryset = Order.objects.filter(customer=request.user).order_by('-id')
        return JsonResponse({'myorders': list(queryset.values())})
    except Exception as e:
        return e

@login_required(login_url='/kirish/')
def get_top_orders_driver(request):
    if request.method == 'GET':
        try:
            try:
                myfilter = Filter.objects.get(user=request.user)

                # barchasi to'g'ri kelsa
                if myfilter.status == 'filter' and myfilter.qayerdan is not None and myfilter.qayerga is not None:
                    orders_all = Order.objects.filter(status='yangi', qayerdan__nomi=myfilter.qayerdan,
                                                      qayerga__nomi=myfilter.qayerga).order_by('-id')[:2]
                # qayerdan kelsa
                elif myfilter.status == 'filter' and myfilter.qayerdan is not None and myfilter.qayerga is None:
                    orders_all = Order.objects.filter(status='yangi', qayerdan__nomi=myfilter.qayerdan).order_by('-id')[
                                 :2]
                # qayerga kelsa
                elif myfilter.status == 'filter' and myfilter.qayerga is not None and myfilter.qayerdan is None:
                    orders_all = Order.objects.filter(status='yangi', qayerga__nomi=myfilter.qayerga).order_by('-id')[
                                 :2]
                # status barchasi bo'lsa
                elif myfilter.status == 'barchasi':
                    orders_all = Order.objects.filter(status='yangi').order_by('-id')[:2]
                else:
                    orders_all = Order.objects.filter(status='yangi').order_by('-id')[:2]

                active_orders_count = orders_all.count()
                kutish_orders_count = Order.objects.filter(status='kutish').count()
                olindi_orders_count = Order.objects.filter(status='olindi').count()

                context = {
                    'count': active_orders_count,
                    'kutish_count': kutish_orders_count,
                    'olindi_count': olindi_orders_count,
                    'orders': list(orders_all.values())
                }

                return JsonResponse(context)
            except Exception as e:
                print(e)
                nfilter = Filter()
                nfilter.user = request.user
                nfilter.qayerdan = None
                nfilter.qayerga = None
                nfilter.status = 'barchasi'
                nfilter.save()
                return redirect('getorders-driver')


        except Exception as e:
            try:
                mfilter = Filter.objects.get(user=request.user)

                if mfilter is None:
                    new_filter = Filter()
                    new_filter.user = request.user
                    new_filter.qayerdan = None
                    new_filter.qayerga = None
                    new_filter.status = 'barchasi'
                    new_filter.save()
                elif mfilter is not None:
                    print(e)
                    print(e)
                    print(e)
            except Exception as e:
                print(e)
                print(e)
                print(e)
                new_filter = Filter()
                new_filter.user = request.user
                new_filter.qayerdan = None
                new_filter.qayerga = None
                new_filter.status = 'barchasi'
                new_filter.save()

            return JsonResponse({'xato': 'xatolik!'})

@login_required(login_url='/kirish/')
def get_myorders_customer(request):
    myorders = Order.objects.filter(customer=request.user)
    count = myorders.count()

    context = {
        'orders': list(myorders.values()),
        'count': count
    }
    return JsonResponse(context)
