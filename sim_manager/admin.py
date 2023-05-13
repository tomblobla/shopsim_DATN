from django.contrib import admin
from .models import Network, SIM, Tag
from django.db.models import Q
from jet.admin import CompactInline

# Register your models here.
   

class TagInline(admin.TabularInline):
    model = SIM.tags.through
    extra = 1
    
class SIMInlineForNetwork(CompactInline):
    model = SIM
    extra = 1
    show_change_link = True    
    fields = ('phone_number', 'slug', 'price', 'discount', 'tags')
    prepopulated_fields = {
        'slug': ('phone_number',)
    }
    
    inlines = [TagInline]
    classes = ['collapse']

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == 'tags':
            kwargs['queryset'] = Tag.objects.all()
        return super().formfield_for_manytomany(db_field, request, **kwargs)
    
class SIMInlineForTag(admin.TabularInline):
    model = SIM.tags.through
    extra = 1
    show_change_link = True
    verbose_name = 'SIM'
    verbose_name_plural = 'Danh sách SIM'
    
class NetworkAdmin(admin.ModelAdmin):  # new
    readonly_fields = ['logo_preview', 'simcard_img_preview', 'goto_net']
    prepopulated_fields = {
        'slug': ('name',)
    }

    list_display = ('name', 'logo_preview', 'sim_count',
        'goto_net',)
    
    inlines = (SIMInlineForNetwork,)
    
class SIMAdmin(admin.ModelAdmin):
    list_display = (
        'phone_number',
        'get_originalpricestr',
        'get_salepricestr',
        'network',
        'get_tags',
        'get_discount',
        'created_date',
        'is_available',
        'is_visible',
        'goto_sim',
    )
    

    list_filter = ['network__name', 'tags__name', 'discount', 'is_available', 'is_visible']


    readonly_fields = ['sim_img_preview', 'goto_sim']
    
    
    prepopulated_fields = {
        'slug': ('phone_number', )
    }
    
    def get_list_filter(self, request):
        # return the built-in filter for the 'my_field' field
        return ['network__name', 'tags__name', 'discount']
    
    
    def get_search_results(self, request, queryset, search_term):
        search_term = search_term.replace(' ', '')
        if '-' in search_term:
            start_number, end_number = search_term.split('-')
            if ',' in start_number:
                start_number = start_number.split(',')
            else:
                start_number = [start_number]
                
            if ',' in end_number:
                end_number = end_number.split(',')
            else:
                end_number = [end_number]
            query = Q()
            for start_item in start_number:
                for end_item in end_number:
                    query |= Q(slug__startswith=start_item, slug__endswith=end_item)
               
            queryset = queryset.filter(query)
        elif ',' in search_term:
            li = search_term.split(',')
            query = Q()
            for item in li:
                query |= Q(slug__contains=item)
                queryset = queryset.filter(query)
        else:
            queryset = queryset.filter(
                slug__contains=search_term,
            )
        return queryset, True

    search_fields = ['slug']

class TagAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'sim_count',
        'goto_tag',
    )

    readonly_fields = ['goto_tag']
    
    prepopulated_fields = {
        'slug': ('name',)
    }   
    
    inlines = (SIMInlineForTag,)
    
  
admin.site.register(SIM, SIMAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Network, NetworkAdmin)
