from django.db.models.expressions import Value
from django.db.models.fields import DecimalField
from django.db.models.functions.text import Ord
from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q, F, Func, ExpressionWrapper
from django.db.models import Count, Max, Min, Avg, Aggregate
from django.db import transaction
from django.db import connection

from store.models import Customer, Order, Product, OrderItem


def say_hello(request):

    #qs = Product.objects.filter(inventory=F('unit_price'))

    #qs1 = Product.objects.filter(Q(unit_price__gt=10) & Q(unit_price__lte=50))

    #qs = Product.objects.all().order_by('unit_price', '-title')

    # to sort and access the first element we use the 'earliest' method

    #product = Product.objects.earliest('unit_price')

    #print(product)

    # Limiting results
    #--------------------------------
    #qs = Product.objects.all()[:5]

    # to get to the second page or add an offset we use the follwoing
    #----------------------------------------------------------------
    #qs = Product.objects.all()[5:10]

    # selecting only requied field
    #-----------------------------------
    #qs = Product.objects.values('id', 'title')

    # to access the related filed also we use the following
    #qs = Product.objects.values('id', 'title', 'collection__title')
    # the above will gives us a dictonary and if we want to return a list we use the values_list method

    #orderitems = OrderItem.objects.values('product_id').distinct()
    #qs = Product.objects.filter(id__in=orderitems).order_by('title')

    # qs = Product.objects.filter(
    #     id=F('orderitem__product_id')).distinct().order_by('title')
    # print(len(list(qs)))

    #qs = Product.objects.select_related('collection').order_by('title')

    # Prefetch
    #-----------------------------------

    #qs = Product.objects.prefetch_related('promotions').select_related('collection').all()

    # Selecting related items
    #----------------------------------

    # Get the last 5 orders with their customer and items (incl product)
    #qs = Order.objects.order_by('-placed_at', 'customer_id')[:50]
    #qs = Order.objects.select_related('customer').order_by('-placed_at', 'customer_id')[:5]

    # qs = Order.objects.select_related('customer').prefetch_related('orderitem_set__product').order_by('-placed_at', 'customer_id')[:50]

    # for order in qs:
    #     print(order.customer.first_name, ' have orderd the following items:')
    #     for item in order.orderitem_set.all():
    #         print("     -   ",item.product.title)

    # Aggregation
    #---------------------------
    # from django.db.models import Count, Max, Min, Avg, Aggregate

    #result = Product.objects.aggregate(coun=Count('id'), min_price = Min('unit_price'))

    # Annotate (Adding aditional colums to the results)
    #-------------------------------
    # result = Customer.objects.annotate(
    #     is_new=Value('Gold') if F('membership') == Customer.MEMBERSHIP_GOLD else Value('Not Gold'))

    #result = Customer.objects.annotate(
    #    is_new=(Value('Premium Member') if F('membership') == 'G' else Value('Regular Member')))

    # Calling Database Functions
    #----------------------------------------------
    #

    #    result = Customer.objects.annotate(full_name=Func(
    #        F('first_name'), Value(' '), F('last_name'), function='CONCAT'))

    # result = Customer.objects.annotate(
    #     full_name=Concat('first_name', Value(' '), 'last_name'))

    # Using annotate to aggregate
    #------------------------------------------------
    #result = Customer.objects.annotate(orders_count=Count('order'))

    # Using expression wrapper
    #----------------------------------------------------
    # result = Product.objects.annotate(
    #     discounted_price=ExpressionWrapper(F('unit_price') * 0.8, output_field=DecimalField())
    # )

    # Querying GenericType

    # using transaction to revert if error occurs or to commit to queries together

    # with transaction.atomic():

    #     order = Order()
    #     order.customer_id = 1
    #     order.save()

    #     item = OrderItem()
    #     item.order = order
    #     item.product_id = 1
    #     item.quantity = 1
    #     item.unit_price = 10
    #     item.save()

    # Executing Raw SQL Queries
    #result = Product.objects.raw('SELECT * FROM store_product')
    #result = list(result)

    # Using connection object using cursor
    result = None
    with connection.cursor() as cursor:
        cursor.execute()
    

    
    return render(
        request,
        'hello.html',
        {
            'name': 'Saravanan',
            'result': list(result)
        },
    )
