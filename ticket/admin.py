from django.contrib import admin
from .models import OrderItem, Order, Ticket, TicketGroupPrice


class TicketInline(admin.TabularInline):
    model = Ticket
    extra = 0 
    fk_name = "group_price"

class TicketGroupPriceInline(admin.TabularInline):
    model = TicketGroupPrice
    extra = 1
 
class OrderItemInline(admin.TabularInline):
    extra = 0
    model = OrderItem

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "order_id",
        "payable",
        "is_ordered",
    )
    search_fields = ("order_id", "full_name")
    list_filter = ("is_ordered", )
    inlines = (OrderItemInline, )


@admin.register(TicketGroupPrice)
class TicketGroupPriceAdmin(admin.ModelAdmin):
    inlines = [TicketInline]
    list_display = ('destination','age_group','price','ticket_count','sold','balance')
    search_fields = ( 'destination','age_group', 'price')  
    list_filter = ( 'destination','age_group')