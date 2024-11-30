from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import DestinationCity, DestinationImage, TouristDestination,DestinationSpecification,Testimonial,Contact,Blog,ThingsToDo,PartnerLogo


class DestinationSpecificationInline(admin.TabularInline):
    model = DestinationSpecification
    extra = 1  


class DestinationImageInline(admin.TabularInline):
    model = DestinationImage


class TouristDestinationInline(admin.TabularInline):
    model = TouristDestination
    extra = 1 
    fk_name = "city" # Number of empty forms to display


class DestinationCityAdmin(admin.ModelAdmin): 
    list_display = ('name',)  


class TouristDestinationAdmin(admin.ModelAdmin):
    list_display = ('name', 'city')  


class ContactAdmin(admin.ModelAdmin): 
    list_display = ('name',)  


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ("heading",)
    prepopulated_fields = {"slug": ("heading",)}


@admin.register(ThingsToDo)
class ThingsToDoAdmin(admin.ModelAdmin):
    list_display = ("city","place_name",)


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email')  
    

@admin.register(TouristDestination)
class TouristDestinationAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'popular_destination','prefernce')  
    inlines = [DestinationImageInline,DestinationSpecificationInline]


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('full_name','review_star_count') 


@admin.register(DestinationCity)
class DestinationCityAdmin(admin.ModelAdmin):
    list_display = ('name',)  


@admin.register(PartnerLogo)
class PartnerLogoAdmin(admin.ModelAdmin):
    list_display = ("name", "image_preview",)

    def image_preview(self, obj):
        if obj.image:
            return mark_safe(
                f'<img loading="lazy" src="{obj.image.url}" style="width:50px;height:50px;object-fit:contain;">'
            )
        return None
    
    image_preview.short_description = "Image Preview"

# admin.site.register(PackageDates)