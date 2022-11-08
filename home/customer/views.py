from django.shortcuts import render, redirect
from home.models import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required


@login_required(login_url='/kirish/')
def customer(request):
    if request.user.type == 3:
        if request.method == 'POST':
            try:
                post_qayerdan = request.POST.get('viloyatdan')
                post_qayerga = request.POST.get('viloyatga')
                post_narx = request.POST.get('narx')
                post_odam_soni = request.POST.get('odam_soni')
                post_location = request.POST.get('location')

                # filter

                qayerdan = Region.objects.get(id=post_qayerdan)
                qayerga = Region.objects.get(id=post_qayerga)
                narx = Price.objects.get(id=post_narx)

                data = TempOrder()
                data.qayerdan = qayerdan
                data.qayerga = qayerga
                data.location = post_location
                data.person_count = post_odam_soni
                data.price = narx
                data.client_name = request.user.first_name
                data.client_phone = request.user.phone
                data.customer = request.user
                data.save()
                return redirect('customer-kutish', data.id)
            except Exception as e:
                print(e)
                return redirect('customer')
        return render(request, 'customer/index.html')
    elif request.user.type == 1 or request.user.type == 2:
        return redirect('driver')


@login_required(login_url='/kirish/')
def review(request, id):
    if request.user.type == 3:
        order = TempOrder.objects.get(id=id)

        context = {
            'order': order
        }
        return render(request, 'customer/review.html', context)
    elif request.user.type == 1 or request.user.type == 2:
        return redirect('driver')


@login_required(login_url='/kirish/')
def delete_order(request, id):
    if request.user.type == 3:
        try:
            order = Order.objects.get(id=id)
        except Exception as e:
            print(e)
            order = TempOrder.objects.get(id=id)
        order.delete()
        return redirect('customer-my-orders')
    elif request.user.type == 1 or request.user.type == 2:
        return redirect('driver')


@login_required(login_url='/kirish/')
def right_order(request, id):
    if request.user.type == 3:
        temp_order = TempOrder.objects.get(id=id)

        data = Order()
        data.status = 'yangi'
        data.qayerdan = temp_order.qayerdan
        data.qayerga = temp_order.qayerga
        data.location = temp_order.location
        data.person_count = temp_order.person_count
        data.price = temp_order.price
        data.client_phone = temp_order.client_phone
        data.client_name = temp_order.client_name
        data.customer = request.user
        data.save()

        temp_order.delete()
        return redirect('customer')
    elif request.user.type == 1 or request.user.type == 2:
        return redirect('driver')


@login_required(login_url='/kirish/')
def myorders(request):
    if request.user.type == 3:
        orders = Order.objects.filter(customer=request.user).order_by('-id')

        context = {
            'myorders': orders
        }
        return render(request, 'customer/myorders.html', context)
    elif request.user.type == 1 or request.user.type == 2:
        return redirect('driver')


@login_required(login_url='/kirish/')
def order_detail(request, id):
    if request.user.type == 3:
        order = Order.objects.get(id=id)

        context = {
            'order': order
        }
        return render(request, 'customer/order_detail.html', context)
    elif request.user.type == 1 or request.user.type == 2:
        return redirect('driver')

@login_required(login_url='/kirish/')
def black_list(request, id):
    if request.user.type == 3:
        order = Order.objects.get(id=id)

        if order.driver:
            order.blacklist = order.driver
            order.driver = None
            order.status = 'yangi'
            order.save()
            return redirect('customer-my-orders')
    elif request.user.type == 1 or request.user.type == 2:
        return redirect('driver')

@login_required(login_url='/kirish/')
def customer_order_update(request, id):
    return redirect('customer-order-detail', id)
