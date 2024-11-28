from django.db import models
from tinymce.models import HTMLField
from django.core.validators import MaxValueValidator
#models 
from core.models import BaseModel
from ticket.models import TicketGroupPrice
from django.urls import reverse_lazy


# Create your models here.
class DestinationCity(BaseModel):
    name = models.CharField(max_length=150)
    image = models.ImageField(upload_to='destinationcity_images/')
    image_short_heading = models.TextField(null=True, blank=True)
    image_short_text = models.TextField(null=True, blank=True)
    description_heading = models.TextField(null=True, blank=True)
    description = HTMLField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Destination City"
        
    def get_absolute_url(self):
        return reverse_lazy("web:destination", kwargs={"slug": self.slug})
    

    def get_destinations(self):
        return TouristDestination.objects.filter(city=self)
    
    def __str__(self):
        return self.name
    

class TouristDestination(BaseModel):
    city = models.ForeignKey("web.DestinationCity",on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = HTMLField()
    instant_confirmation = models.BooleanField(default=True)
    mobile_ticket = models.BooleanField(default=True)
    duration = models.CharField(max_length=100,blank=True,null=True)
    prefernce = models.BooleanField(default=True)
    popular_destination = models.BooleanField(default=False)
    common_age_note = models.CharField(max_length=100,blank=True,null=True,verbose_name="Common Age Note",default='Infants aged 3 and under can enter for free. Simply show their ID at the venue and enter.')
    class Meta:
        verbose_name_plural = "Tourist Destination"

    def __str__(self):
        return self.name
    
    def get_destination_specification(self):
        return DestinationSpecification.objecrs.filter(destination=self)
    
    def get_image(self):
        return DestinationImage.objects.filter(destination=self).first()
    
    def get_images(self):
        return DestinationImage.objects.filter(destination=self)
    
    def get_chepest_price(self):
        return TicketGroupPrice.objects.filter(destination=self).order_by('-price').first()
    
    def get_price(self):
        return TicketGroupPrice.objects.filter(destination=self,age_group='adult').first()
    
    def get_child_price(self):
        return TicketGroupPrice.objects.filter(destination=self,age_group='children').first()
    
    def get_related(self):
        return TouristDestination.objects.all().exclude(pk=self.pk)
    

class DestinationImage(models.Model):
    destination = models.ForeignKey("web.TouristDestination", on_delete=models.CASCADE,blank=True, null=True)
    image = models.ImageField(upload_to='tourist_destination_images/')  


class DestinationSpecification(models.Model):
    destination = models.ForeignKey(TouristDestination, on_delete=models.CASCADE)
    specification_heading = models.CharField(max_length=50)
    specification_content = HTMLField()

    def __str__(self):
        return f"{self.destination.name} - {self.specification_heading}"
    
    
class Testimonial(models.Model):
    image = models.ImageField(upload_to='testimonial_images/',blank=True, null=True)
    full_name = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    content = models.TextField()
    review_star_count = models.PositiveIntegerField(
        validators=[MaxValueValidator(5)],
        default=5,
        help_text="Product Rating(max:5)",
    )
    def __str__(self):
        return self.full_name    
    

class Blog(models.Model):
    tag = models.TextField()
    heading = models.TextField()
    slug = models.SlugField(max_length=300, unique=True)
    image = models.ImageField(upload_to='blog_images/')
    content_heading = models.TextField()
    content = HTMLField(null=True, blank=True)
    date = models.DateField()

    def __str__(self):
        return str(self.heading)


class ThingsToDo(models.Model):
    city = models.ForeignKey("web.DestinationCity",on_delete=models.CASCADE)
    image = models.ImageField(upload_to='thingstodo_images/')
    place_name = models.TextField()

    def __str__(self):
        return str(self.place_name)


class Contact(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    subject = models.CharField(max_length=255)
    your_message = models.TextField()

    def __str__(self):
        return self.name 


class FAQ(models.Model):
    question = models.CharField(max_length=255)
    answer = models.TextField()

    def __str__(self):
        return self.question
    

class PartnerLogo(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='partners_logos/')

    def __str__(self):
        return self.name

# class PackageDates(models.Model):
#     destination = models.ForeignKey(DestinationCity,on_delete=models.CASCADE)  
#     available_date = models.DateField()  

#     def __str__(self):
#         return f"{self.destination.name} - {self.available_date.strftime('%Y-%m-%d')}"
    
#     class Meta:
#         verbose_name = 'Package Date'
#         verbose_name_plural='Package Date'
   
    



    

    
    