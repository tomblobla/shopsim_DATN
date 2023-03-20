from django.contrib import admin
from .models import Network, SIM, Tag
from django.db.models import Q
from jet.admin import CompactInline
from django.contrib.admin.widgets import ForeignKeyRawIdWidget
# Register your models here.
   
class SIMInlineForNetwork(CompactInline):
    model = SIM
    extra = 1
    show_change_link = True    
    fields = ('phone_number', 'price', 'discount', 'is_available', 'tags')
    
from django.contrib.admin.widgets import ForeignKeyRawIdWidget

class SIMInlineForTag(admin.TabularInline):
    model = SIM.tags.through
    extra = 1
    show_change_link = True
    verbose_name = 'SIM'
    verbose_name_plural = 'Danh sách SIM'
    
class NetworkAdmin(admin.ModelAdmin):  # new
    readonly_fields = ['logo_preview', 'simcard_img_preview']
    prepopulated_fields = {
        'slug': ('name',)
    }

    list_display = ('name', 'logo_preview', 'sim_count')
    
    inlines = (SIMInlineForNetwork,)
    
class SIMAdmin(admin.ModelAdmin):
    list_display = (
        'phone_number',
        'get_originalprice',
        'get_saleprice',
        'network',
        'get_tags',
        'get_discount',
        'created_date',
        'is_available'
    )
    

    list_filter = ['network__name', 'tags__name', 'discount']

    prepopulated_fields = {
        'slug': ('phone_number', )
    }
    
    def get_tags(self, obj):
        return "\n".join([t.name for t in obj.tags.all()])
    
    def get_discount(self, obj):
        return str(obj.discount) + '%'
    
    get_tags.short_description = 'Loại SIM'
    get_discount.short_description = 'Giảm'
    
    def get_search_results(self, request, queryset, search_term):
        try:
            # Split the search term into two numbers
            start_number, end_number = search_term.split('-')

            # Filter the queryset based on the search criteria
            queryset = queryset.filter(
                phone_number__startswith=start_number,
                phone_number__endswith=end_number,
            )

            # Return the filtered queryset and a boolean indicating if the search term was found
            return queryset, True
        except ValueError:
            # Return an empty queryset if the search term is not in the correct format
            return queryset, False

    search_fields = ['phone_number']

class TagAdmin(admin.ModelAdmin):
    list_display = (
        'name',
    )
    
    prepopulated_fields = {
        'slug': ('name',)
    }   
    
    inlines = (SIMInlineForTag,)
    
  
admin.site.register(SIM, SIMAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Network, NetworkAdmin)
