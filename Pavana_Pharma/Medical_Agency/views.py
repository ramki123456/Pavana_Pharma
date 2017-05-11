#! /usr/bin/python

from django.shortcuts import render, render_to_response
from Medical_Agency.models import Login
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_protect
from django.template import RequestContext
from Medical_Agency.models import ComplteStockDetails, DealersInfo
from django.template.loader import get_template
from django.template import Context
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText

import smtplib
import os
import pdfkit


def home(request):
    return render(
        request, 'index.html', locals(),
        context_instance=RequestContext(request))


def home1(request):
    return render(request, 'login1.html')


def login(request):
    try:
        # print request.GET['user']
        login_obj = Login.objects.get(username=request.POST['user'])
        if login_obj.password == request.POST['pwd']:
            request.session['user'] = request.POST['user']
            return render_to_response(
                'login.html', {'username': request.POST['user'].upper()})

        else:
            return HttpResponse('Password is not matched, Please try again')
    except Exception as e:
        print str(e)
        return HttpResponse('Username is not available')


def check_stock(request):
    stock_obj = ComplteStockDetails.objects.all()
    # import pdb
    # pdb.set_trace()
    return render_to_response('show_stock.html', {'data': stock_obj})
    # TODO: Write a function to show the detailed records of all the products.


def check_dealers(request):
    dealer_obj = DealersInfo.objects.all()
    return render_to_response('show_dealers.html', {'data': dealer_obj})


def add_dealer(request):
    return render(request, 'add_dealer.html')


@csrf_protect
def add_dealer_to_db(request):
    dealer_name = request.POST.get('dealer_name')
    # print dealer_name
    dealer_dl1 = request.POST.get('dealer_dl1')
    dealer_dl2 = request.POST.get('dealer_dl2')
    dealer_tin = request.POST.get('dealer_tin')
    dealer_comapny_name = request.POST.get('dealer_company_name')
    dealer_addrs = request.POST.get('dealer_addrs')
    dealer_phone = request.POST.get('dealer_phone')
    dealer_email = request.POST.get('dealer_email')
    # import pdb
    # pdb.set_trace()
    if dealer_name == '' or dealer_name:
        if dealer_dl1 == '' or dealer_dl1:
            if dealer_dl2 == '' or dealer_dl2:
                if dealer_tin == '' or dealer_tin:
                    try:
                        dealer_obj = DealersInfo.objects.get(
                            dealer_dl1=dealer_dl1)
                    except:
                        dealer_obj = None
                    if not dealer_obj:
                        dealer_obj1 = DealersInfo(
                            dealer_name=dealer_name,
                            dealer_company_name=dealer_comapny_name,
                            dealer_dl1=dealer_dl1,
                            dealer_dl2=dealer_dl2,
                            dealer_tin=dealer_tin,
                            dealer_addrs=dealer_addrs,
                            dealer_phone=dealer_phone,
                            dealer_email=dealer_email)
                        dealer_obj1.save()
                        return HttpResponseRedirect('/home/')
                    else:
                        return HttpResponse('Dealer Already Exists')
                else:
                    return HttpResponse("Please enter correct Tin Number")
            else:
                return HttpResponse("Please enter correct DL2 Number")
        else:
            return HttpResponse("Please enter correct DL1 Number")
    else:
        return HttpResponse("Please enter correct Dealer Name")


def billing_page(request):
    objs = ComplteStockDetails.objects.all()
    return render_to_response('billing_page.html', {'objs': objs},
                              context_instance=RequestContext(request))


@csrf_protect
def show_billing_cart(request):
    dictionary = dict(request.POST.viewitems())
    test_list = []
    for key in range(len(dictionary.get('item_name_s'))):
        if key != str(''):
            try:
                bill_stock_obj = ComplteStockDetails.objects.get(
                    batch_num=int(dictionary.get('item_name_s')[key]))
            except:
                bill_stock_obj = None
        else:
            pass

        if bill_stock_obj:
            total_price = float(
                bill_stock_obj.price_per_unit) * float(
                dictionary.get('qnt')[key])
            test_list.append(
                {'obj': bill_stock_obj,
                 'quantity': dictionary.get('qnt')[key], 'tp': total_price})
        else:
            pass
    sum_of_all_elements = sum([x['tp'] for x in test_list])

    return render_to_response('show_final_billing_cart.html', {
        'test_list': test_list, 'sum': sum_of_all_elements},
        context_instance=RequestContext(request))


@csrf_protect
def go_final_billing(request):
    final_list = []
    dictionary = dict(request.POST)
    batch_numbers = dictionary['batch_nums']
    item_names = dictionary['item_nums']
    company_names = dictionary['company_names']
    ppus = dictionary['ppus']
    quantities = dictionary['quantities']
    tps = dictionary['tps']
    for i in range(len(batch_numbers)):
        try:
            obj = ComplteStockDetails.objects.get(batch_num=batch_numbers[i])
        except:
            obj = None
        if obj:
            obj.quantity = int(obj.quantity) - int(quantities[i])
            obj.save()
            final_list.append([batch_numbers[i], item_names[i],
                               company_names[i], ppus[i], quantities[i],
                               tps[i]])

    c = get_template('final_billing.html').render(
        Context({'final_list': final_list, 'sum': dictionary['sum']}))

    fp = open('billing.html',
              'w')
    fp.write(c)
    fp.close()
    return render_to_response(
        'final_billing.html',
        {'final_list': final_list,
         'sum': dictionary['sum']}, context_instance=RequestContext(request))


def send_mail(request):
    msg = MIMEMultipart('alternative')
    msg['From'] = 'h_sarma@ymail.com'
    msg['To'] = 'h.sarma212@gmail.com'
    msg['Subject'] = "Your Invoice Details Bill"
    c = open('billing.html',
             'r').read()
    part2 = MIMEText(c, 'html')
    msg.attach(part2)
    mailserver = smtplib.SMTP("smtp.mail.yahoo.com",587)
    mailserver.ehlo()
    mailserver.starttls()
    mailserver.ehlo()
    mailserver.login('h_sarma@ymail.com', 'GhsKanna212$')
    mailserver.sendmail('h_sarma@ymail.com',
                        'h.sarma212@gmail.com',
                        msg.as_string())
    mailserver.close()
    return render(request, 'login1.html')


def prev_billing(request):
    pass
    # TODO: Write a function to show all the previous billings.


def add_stock(request):
    return render_to_response(
        'add_stock.html',
        {'no_of_items': range(int(request.GET['items']))},
        context_instance=RequestContext(request))


@csrf_protect
def add_stock_to_db(request):
    dictionary = dict(request.POST.viewitems())

    for i in range(len(dictionary.values()[0])):
        try:
            data = ComplteStockDetails.objects.get(
                batch_num=dictionary.values()[1][i])

        except:
            data = None

        if not data:
            stock_obj = ComplteStockDetails(
                batch_num=dictionary.values()[1][i],
                item_name=dictionary.values()[0][i],
                company=dictionary.values()[2][i],
                price_per_unit=dictionary.values()[6][i],
                manf_data=dictionary.values()[3][i],
                exp_data=dictionary.values()[5][i],
                quantity=dictionary.values()[9][i],
                comments=dictionary.values()[4][i],
                dealer=DealersInfo.objects.get(
                    dealer_name=dictionary.values()[7][i]))
            stock_obj.save()
        else:
            if data.item_name == dictionary.values()[0][i]:
                data.quantity = data.quantity + int(dictionary.values()[9][i])
                data.save()
            else:
                return HttpResponse("Item Name is not matched")

    return HttpResponse('Success')


def check_item_wise_page(request):
    return render(request, 'check_stock_item_wise.html')


def show_item_wise(request):
    stock_obj = ComplteStockDetails.objects.get(item_name=request.GET.get(
        'check_item_name'))
    return render_to_response(
        'conditioned_stock.html', {'data': [stock_obj], 'search': 'ITEM NAME'})


def check_company_wise_page(request):
    return render(request, 'check_stock_company_wise.html')


def show_company_wise(request):
    stock_obj = ComplteStockDetails.objects.filter(company=request.GET.get(
        'check_company_name'))
    return render_to_response(
        'conditioned_stock.html',
        {'data': stock_obj, 'search': 'COMPANY NAME'})


def check_batch_number_wise_page(request):
    return render(request, 'check_stock_batch_wise.html')


def show_batch_num_wise(request):
    stock_obj = ComplteStockDetails.objects.get(batch_num=int(request.GET.get(
        'check_batch_num')))
    return render_to_response(
        'conditioned_stock.html',
        {'data': [stock_obj], 'search': 'BATCH NUMBER'})


def print_page(request):
    pdfkit.from_file('billing.html', 'out.pdf')
    os.system('lpr out.pdf')
    return HttpResponseRedirect('/home')
