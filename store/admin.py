from re import search
from django.contrib import admin, messages
from django.contrib.admin.decorators import action
from django.db import models
from django.db.models.aggregates import Count
from django.db.models.query import QuerySet
from django.http.request import HttpRequest
from .models import Collection, Order, OrderItem, Product, Customer
from django.utils.html import format_html, urlencode
from django.urls import reverse
# Register your models here.

#https://docs.djangoproject.com/en/3.2/ref/contrib/admin/#modeladmin-options


class InventoryFilter(admin.SimpleListFilter):

    title = 'inventory'
    parameter_name = 'inventory'

    def lookups(self, request, model_admin):
        return [('<10', 'Low')]

    def queryset(self, request, queryset: QuerySet):
        if self.value() == '<10':
            return queryset.filter(inventory__lt=10)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    autocomplete_fields = ['collection']
    prepopulated_fields = {
        'slug' : ['title']
    }
    actions = ['clear_inventory']
    list_display = [
        'title', 'unit_price', 'inventory', 'inventory_status',
        'collection_title'
    ]
    list_editable = ['unit_price']
    list_filter = ['collection', 'last_update', InventoryFilter]
    list_per_page = 10
    list_select_related = ['collection']
    search_fields = ['title']

    def collection_title(self, product):
        return product.collection.title

    @admin.display(ordering='inventory')
    def inventory_status(self, product):
        if product.inventory < 10:
            return 'Low'
        return 'Ok'

    @admin.action(description="Clear Inventory")
    def clear_inventory(self, request, queryset):
        updated_count = queryset.update(inventory=0)
        self.message_user(
            request,
            f'{updated_count} products were successfully updated.',
        )


class CollectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'products_count']
    list_per_page = 10
    ordering = ['-title']
    list_select_related = ['featured_product']
    search_fields = ['title']

    @admin.display(ordering='products_count')
    def products_count(self, collection):
        url = reverse("admin:store_product_changelist") + '?' + urlencode(
            {'collection__id': str(collection.id)})
        return format_html('<a href="{}">{}</a>', url,
                           collection.products_count)

    def get_queryset(self, request: HttpRequest) -> QuerySet:
        return super().get_queryset(request).annotate(
            products_count=Count('product'))


admin.site.register(Collection, CollectionAdmin)


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'membership', 'total_orders']
    list_per_page = 10
    list_editable = ['membership']
    search_fields = ['first_name__istartswith', 'last_name__istartswith']

    @admin.display(ordering='total_orders')
    def total_orders(self, customer):
        url = reverse("admin:store_order_changelist") + '?' + urlencode(
            {'customer__id': str(customer.id)})
        return format_html('<a href="{}">{}</a>', url, customer.total_orders)

    def get_queryset(self, request: HttpRequest) -> QuerySet:
        return super().get_queryset(request).annotate(
            total_orders=Count('order')).order_by('-total_orders',
                                                  'first_name', 'last_name')


class OrderItemInline(admin.TabularInline):
    autocomplete_fields = ['product']
    model = OrderItem
    min_num = 1
    max_num = 10
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    autocomplete_fields = ['customer']
    inlines = [OrderItemInline]
    list_display = ['id', 'placed_at', 'payment_status', 'customer']
    list_select_related = ['customer']