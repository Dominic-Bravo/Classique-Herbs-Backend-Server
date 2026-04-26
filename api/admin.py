from django.contrib import admin
from api.models import Category, Customer, Order, OrderItem, Product


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('price_at_purchase',)


class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'status', 'total_amount', 'order_date')
    list_filter = ('status', 'order_date')
    search_fields = ('customer__email', 'customer__psid', 'customer__name')
    list_editable = ('status',)
    actions = ['delete_selected']
    save_on_top = True
    inlines = [OrderItemInline]
    readonly_fields = ('total_amount',)


class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'price', 'stock_quantity')
    list_filter = ('category',)
    search_fields = ('name', 'description')
    list_editable = ('price', 'stock_quantity')
    actions = ['delete_selected']
    save_on_top = True


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description')
    search_fields = ('name',)
    list_editable = ('description',)
    actions = ['delete_selected']
    save_on_top = True


class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'psid', 'phone')
    search_fields = ('name', 'email', 'psid')
    list_filter = ('email',)
    list_editable = ('email', 'phone')
    actions = ['delete_selected']
    save_on_top = True


class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'product', 'quantity', 'price_at_purchase')
    search_fields = ('order__id', 'product__name')
    list_editable = ('quantity', 'price_at_purchase')
    actions = ['delete_selected']
    save_on_top = True


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
    
