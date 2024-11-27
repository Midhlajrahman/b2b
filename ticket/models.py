import uuid
from django.utils import timezone
from django.db import models
from core.choices import AGE_GROUP_CHOICES
from django.urls import reverse_lazy
from core.models import BaseModel

  
class TicketGroupPrice(BaseModel):
    destination = models.ForeignKey("web.TouristDestination",on_delete=models.CASCADE)
    age_group = models.CharField(max_length=20, choices=AGE_GROUP_CHOICES)
    age_note = models.CharField(max_length=100,blank=True,null=True,verbose_name="Ticket Age Limit Note")
    price = models.DecimalField(max_digits=10, decimal_places=2) 
    
    def __str__(self):
        return f"{self.destination} - {self.age_group} - {self.price}"


    def get_tickets(self):
        return Ticket.objects.filter(ticket_type = self)

    def sold(self):
        return self.ticket_set.filter(status=True).count()

    def balance(self):
        return self.ticket_set.filter(status=False).count()
    
    def ticket_count(self):
        return self.ticket_set.all().count()
    

class Ticket(BaseModel):
    group_price = models.ForeignKey("ticket.TicketGroupPrice",on_delete=models.CASCADE)
    serial_number = models.CharField(max_length=100, unique=True)
    validity_from_date = models.DateField(null=True, blank=True)
    validity_end_date = models.DateField(null=True, blank=True)
    status = models.BooleanField(default=False)
    ticket_pdf = models.FileField(upload_to="tickets/",)

    class Meta:
        unique_together = ["serial_number", "group_price"]
    def __str__(self):
        return self.serial_number
    
def generate_order_id():
    timestamp = timezone.now().strftime("%y%m%d")
    unique_id = uuid.uuid4().hex[:6] 
    return f"{timestamp}{unique_id.upper()}"

class Order(models.Model):
    order_id = models.CharField(max_length=220, default=generate_order_id)
    user = models.ForeignKey("accounts.User", on_delete=models.CASCADE)
    payable = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    is_ordered = models.BooleanField(default=False)
    
    full_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15,)
    email = models.EmailField()
    country = models.CharField(max_length=100, blank=True, null=True,default="UAE")

    booked_date = models.DateField(null=True, blank=True)
    guest_adult = models.PositiveIntegerField(null=True, blank=True)
    guest_child = models.PositiveIntegerField( null=True, blank=True)
    ordered_at = models.DateTimeField(auto_now=False, auto_now_add=False)


    class Meta:
        ordering = ("-id",)

    def __str__(self):
        return f"{self.order_id}"
    
    def get_tickets(self):
        return OrderItem.objects.filter(order=self)
    
    def get_ticket(self):
        return OrderItem.objects.filter(order=self).first()
    
    def get_absolute_url(self):
        return reverse_lazy("web:order_view", kwargs={"pk": self.pk})
    
    def get_download_tickets_url(self):
        return reverse_lazy("web:download_tickets", kwargs={"order_id": self.order_id})

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    ticket =  models.ForeignKey("ticket.Ticket",on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.ticket}"
    

