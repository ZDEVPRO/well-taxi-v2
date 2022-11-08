from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect

from home.models import *

@login_required(login_url='/kirish/')
def driver_home(request):
    if request.user.type == 1 or request.user.type == 2:
        try:
            myfilter = Filter.objects.get(user=request.user)

            if myfilter:
                # barchasi to'g'ri kelsa
                if myfilter.status == 'filter' and myfilter.qayerdan is not None and myfilter.qayerga is not None:
                    orders_all = Order.objects.filter(status='yangi', qayerdan__nomi=myfilter.qayerdan,
                                                      qayerga__nomi=myfilter.qayerga).order_by('-id')[:2]
                # qayerdan kelsa
                elif myfilter.status == 'filter' and myfilter.qayerdan is not None and myfilter.qayerga is None:
                    orders_all = Order.objects.filter(status='yangi', qayerdan__nomi=myfilter.qayerdan).order_by('-id')[:2]
                # qayerga kelsa
                elif myfilter.status == 'filter' and myfilter.qayerga is not None and myfilter.qayerdan is None:
                    orders_all = Order.objects.filter(status='yangi', qayerga__nomi=myfilter.qayerga).order_by('-id')[:2]
                # status barchasi bo'lsa
                elif myfilter.status == 'barchasi':
                    orders_all = Order.objects.filter(status='yangi').order_by('-id')[:2]
                else:
                    orders_all = Order.objects.filter(status='yangi').order_by('-id')[:2]

                regions = Region.objects.all()
                count = orders_all.count()

                context = {
                    'orders': orders_all,
                    'count': count,
                    'regions': regions,
                    'myfilter': myfilter,

                }
                return render(request, 'driver/index.html', context)
            else:
                orders_all = Order.objects.filter(status='yangi').order_by('-id')[:2]
                regions = Region.objects.all()
                count = orders_all.count()
                context = {
                    'orders': orders_all,
                    'count': count,
                    'regions': regions,
                }
                return render(request, 'driver/index.html', context)
        except Exception as e:
            print(e)
            orders_all = Order.objects.filter(status='yangi').order_by('-id')[:2]
            regions = Region.objects.all()
            count = orders_all.count()

            context = {
                'orders': orders_all,
                'count': count,
                'regions': regions,
            }
            return render(request, 'driver/index.html', context)

    elif request.user.type == 3:
        return redirect('customer')


@login_required(login_url='/kirish/')
def index(request):
    if request.user.type == 1 or request.user.type == 2:
        try:
            myfilter = Filter.objects.get(user=request.user)

            if myfilter:
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

                regions = Region.objects.all()
                count = orders_all.count()

                context = {
                    'orders': orders_all,
                    'count': count,
                    'regions': regions,
                    'myfilter': myfilter,

                }
                return render(request, 'driver/orders.html', context)
            else:
                orders_all = Order.objects.filter(status='yangi').order_by('-id')
                regions = Region.objects.all()
                count = orders_all.count()
                context = {
                    'orders': orders_all,
                    'count': count,
                    'regions': regions,
                }
                return render(request, 'driver/orders.html', context)
        except Exception as e:
            print(e)
            orders_all = Order.objects.filter(status='yangi').order_by('-id')
            regions = Region.objects.all()
            count = orders_all.count()

            context = {
                'orders': orders_all,
                'count': count,
                'regions': regions,
            }
            return render(request, 'driver/orders.html', context)

    elif request.user.type == 3:
        return redirect('customer')

@login_required(login_url='/kirish/')
def accept_order(request, id):
    order = Order.objects.get(id=id)
    order.status = 'kutish'
    order.driver = request.user
    order.save()
    return redirect('driver-order-detail', id)

@login_required(login_url='/kirish/')
def accept_customer(request, id):
    order = Order.objects.get(id=id)
    order.status = 'olindi'
    order.client_in_car = 'ha'
    order.save()
    return redirect('driver-myorders')

@login_required(login_url='/kirish/')
def filter_order(request):
    if request.method == 'POST':
        viloyatdan = request.POST.get('viloyatdan')
        viloyatga = request.POST.get('viloyatga')

        user = request.user

        try:
            old_filter = Filter.objects.get(user=request.user)
            if viloyatga == None and viloyatdan == None:
                old_filter.qayerdan = None
                old_filter.qayerga = None
                old_filter.status = 'barchasi'
                old_filter.save()
                return redirect('driver')
            elif viloyatdan != '' and viloyatga == None and viloyatga == '':
                old_filter.qayerdan = viloyatdan
                old_filter.status = 'filter'
                old_filter.save()
                return redirect('driver')
            elif viloyatga is not None and viloyatga != '' and viloyatdan == None and viloyatdan == '':
                old_filter.qayerga = viloyatga
                old_filter.status = 'filter'
                old_filter.save()
                return redirect('driver')
            elif viloyatga != '' and viloyatdan != '':
                old_filter.qayerdan = viloyatdan
                old_filter.qayerga = viloyatga
                old_filter.status = 'filter'
                old_filter.save()
                return redirect('driver')

        except Exception as e:
            print(e)

            filter_data = Filter()
            filter_data.user = user
            filter_data.status = 'filter'
            filter_data.qayerdan = viloyatdan
            filter_data.qayerga = viloyatga
            filter_data.save()
            return redirect('driver')

@login_required(login_url='/kirish/')
def clean_filter(request):
    try:
        myfilter = Filter.objects.get(user=request.user)
        if myfilter:
            myfilter.qayerdan = None
            myfilter.qayerga = None
            myfilter.status = 'barchasi'
            myfilter.save()
            return redirect('driver')
        else:
            return redirect('driver')
    except Exception as e:
        print(e)
        return redirect('driver')


@login_required(login_url='/kirish/')
def myorders(request):
    if request.user.type == 1 or request.user.type == 2:
        myorder = Order.objects.filter(driver=request.user, status='olindi').order_by('-id')

        context = {
            'myorders': myorder
        }
        return render(request, 'driver/myorders.html', context)
    elif request.user.type == 3:
        return redirect('customer')


@login_required(login_url='/kirish/')
def order_detail(request, id):
    if request.user.type == 1 or request.user.type == 2:
        order = Order.objects.get(id=id)

        if request.method == 'POST':
            data = order
            data.status = 'olindi'
            data.driver = request.user
            data.save()
            return redirect('driver-order-detail', data.id)
        context = {
            'order': order
        }
        return render(request, 'driver/order_detail.html', context)
    elif request.user.type == 3:
        return redirect('customer')


@login_required(login_url='/kirish/')
def success_order(request, id):
    if request.user.type == 1 or request.user.type == 2:
        order = Order.objects.get(id=id)
        arch = ArchiveOrder()
        arch.status = 'yetkazildi'
        arch.qayerdan = order.qayerdan
        arch.qayerga = order.qayerga
        arch.person_count = order.person_count
        arch.price = order.price
        arch.client_phone = order.client_phone
        arch.client_name = order.client_name
        arch.customer = order.customer
        arch.driver = order.driver
        arch.save()
        order.delete()
        return redirect('driver-myorders')
    elif request.user.type == 3:
        return redirect('customer')


@login_required(login_url='/kirish/')
def client_in_car(request, id):
    if request.user.type == 1 or request.user.type == 2:
        order = Order.objects.get(id=id)
        order.client_in_car = 'Ha'
        order.save()
        return redirect('driver-order-detail', order.id)
    elif request.user.type == 3:
        return redirect('customer')


@login_required(login_url='/kirish/')
def close_order(request, id):
    if request.user.type == 1 or request.user.type == 2:
        order = Order.objects.get(id=id)
        order.driver = None
        order.status = 'yangi'
        order.save()
        return redirect('driver')
    return redirect('customer')


@login_required(login_url='/kirish/')
def kutish(request):
    if request.user.type == 1 or request.user.type == 2:
        kutish_orders = Order.objects.filter(driver=request.user, status='kutish').order_by('-id')

        context = {
            'kutish_orders': kutish_orders
        }
        return render(request, 'driver/kutish.html', context)
    elif request.user.type == 3:
        return redirect('customer')


@login_required(login_url='/kirish/')
def about_order(request, id):
    if request.user.type == 1 or request.user.type == 2:
        order = Order.objects.get(id=id)

        if request.method == 'POST':
            data = order
            data.status = 'olindi'
            data.driver = request.user
            data.save()
            return redirect('driver-order-detail', data.id)
        context = {
            'order': order
        }
        return render(request, 'driver/about_order.html', context)
    elif request.user.type == 3:
        return redirect('customer')
