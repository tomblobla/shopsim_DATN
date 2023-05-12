from django.shortcuts import render, get_object_or_404, redirect
from sim_manager.models import SIM, Tag, Network
from sim_manager.serializers import SIMSerializer, TagSerializer, NetworkSerializer
from django.views.generic import View, TemplateView
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.db.models import F, FloatField, ExpressionWrapper
from django.db.models import Q
from customer.models import CartItem

def home(request):
    tagSerializer = TagSerializer(
        Tag.objects.all(), many=True)
    
    networkSerializer = NetworkSerializer(
        Network.objects.all(), many=True)
    
    sale_sims = SIM.objects.all().filter(is_available=True, is_visible=True, discount__gt=0)[:9]
    sale_simSerializer = SIMSerializer(sale_sims, many=True)
    
    cart_count = 0
    if request.user.is_authenticated:
        cart_count = CartItem.objects.all().filter(customer = request.user).count()
        
    context = {
        "tags": tagSerializer.data,
        "networks": networkSerializer.data,
        "sale_sims": sale_simSerializer.data,
        "cart_count": cart_count,
    }

    return render(request, 'home.html', context)


def shop(request):
    tagSerializer = TagSerializer(
        Tag.objects.all(), many=True)
    
    networkSerializer = NetworkSerializer(
        Network.objects.all(), many=True)

    simSerializer = SIMSerializer(
        SIM.objects.all().filter(is_available=True, is_visible=True).
        annotate(
            current_price=ExpressionWrapper(
                F('price') - (F('discount') / 100) * F('price'),
                output_field=FloatField()
            )
        ).order_by('current_price')[:8], many=True)
    
    
    cart_count = 0
    if request.user.is_authenticated:
        cart_count = CartItem.objects.all().filter(customer = request.user).count()
        
    context = {
        "tags": tagSerializer.data,
        "networks": networkSerializer.data,
        "sims": simSerializer.data,
        "cart_count": cart_count,
    }

    return render(request, 'shop.html', context)


def network(request, slug_network):
    tagSerializer = TagSerializer(
        Tag.objects.all(), many=True)
    
    networkSerializer = NetworkSerializer(
        Network.objects.all(), many=True)

    network = get_object_or_404(Network, slug=slug_network)
    simSerializer = SIMSerializer(
        SIM.objects.all().filter(is_available=True, is_visible=True, network=network).
        annotate(
            current_price=ExpressionWrapper(
                F('price') - (F('discount') / 100) * F('price'),
                output_field=FloatField()
            )
        ).order_by('current_price'), many=True)
    
    
    cart_count = 0
    if request.user.is_authenticated:
        cart_count = CartItem.objects.all().filter(customer = request.user).count()
        
    context = {
        "tags": tagSerializer.data,
        "networks": networkSerializer.data,
        "sims": simSerializer.data,
        "curr_net": network.slug,
        "cart_count": cart_count,
    }

    return render(request, 'shop.html', context)


def tag(request, slug_tag):
    tagSerializer = TagSerializer(
        Tag.objects.all(), many=True)
    
    networkSerializer = NetworkSerializer(
        Network.objects.all(), many=True)
    
    tag = get_object_or_404(Tag, slug=slug_tag)
    simSerializer = SIMSerializer(
        SIM.objects.all().filter(is_available=True, is_visible=True, tags=tag).
        annotate(
            current_price=ExpressionWrapper(
                F('price') - (F('discount') / 100) * F('price'),
                output_field=FloatField()
            )
        ).order_by('current_price'), many=True)
    
    
    cart_count = 0
    if request.user.is_authenticated:
        cart_count = CartItem.objects.all().filter(customer = request.user).count()
        
    context = {
        "tags": tagSerializer.data,
        "networks": networkSerializer.data,
        "sims": simSerializer.data,
        "curr_tag": tag.slug,
        "cart_count": cart_count,
    }

    return render(request, 'shop.html', context)



def sim(request, slug_sim):
    tagSerializer = TagSerializer(
        Tag.objects.all(), many=True)
    
    networkSerializer = NetworkSerializer(
        Network.objects.all(), many=True)
    
    sim = SIM.objects.get(slug=slug_sim)
    
    if not sim.is_visible and not request.user.is_admin:
        return home(request)
    
    other_sims = SIM.objects.all().filter(is_available=True, network=sim.network).exclude(id=sim.id).annotate(
            current_price=ExpressionWrapper(
                F('price') - (F('discount') / 100) * F('price'),
                output_field=FloatField()
            )
        ).order_by('current_price')
    
    simSerializer = SIMSerializer(
        other_sims[:8], many=True)
    
    cart_item = CartItem.objects.filter(sim=sim, customer=request.user).first()
    
    if cart_item:
        addedState = True
    else:
        addedState = False
    
    
    cart_count = 0
    if request.user.is_authenticated:
        cart_count = CartItem.objects.all().filter(customer = request.user).count()
        
    context = {
        "tags": tagSerializer.data,
        "networks": networkSerializer.data,
        "sim": sim,
        "addedState": addedState,
        "othersims_samenetwork": simSerializer.data,
        "cart_count": cart_count,
    }

    return render(request, 'detailed_sim.html', context)


def search_sim(request):
    search_input = request.POST.get('search_input').strip().replace('.',  '')
    
    tagSerializer = TagSerializer(
        Tag.objects.all(), many=True)
    
    networkSerializer = NetworkSerializer(
        Network.objects.all(), many=True)
    
    sims = SIM.objects.filter(slug__contains=search_input, is_visible=True).annotate(
            current_price=ExpressionWrapper(
                F('price') - (F('discount') / 100) * F('price'),
                output_field=FloatField()
            )
        ).order_by('current_price')
    
    
    cart_count = 0
    if request.user.is_authenticated:
        cart_count = CartItem.objects.all().filter(customer = request.user).count()
        
    context = {
        "tags": tagSerializer.data,
        "networks": networkSerializer.data,
        "sims": SIMSerializer(sims, many=True).data,
        "cart_count": cart_count,
    }

    return render(request, 'search_sim.html', context)


 
class SIMListView(View):
    def post(self, *args, **kwargs):
        page_number = self.request.POST.get('page_number')
        sim_slug = self.request.POST.get('sim_slug')
        sim = SIM.objects.get(slug=sim_slug)
        other_sims = SIM.objects.all().filter(is_available=True, is_visible=True, network=sim.network).exclude(id=sim.id)
        paginator = Paginator(other_sims, 8)
        page_obj = paginator.get_page(page_number)
        # print(page_number)
        data = SIMSerializer(page_obj, many=True).data
        if (int(page_number) > paginator.num_pages):
            data = None
        return JsonResponse({
            'data': data,
            })   
        
 
class SIMFilterListView(View):
    def post(self, *args, **kwargs):
        request = self.request
        networks = request.POST.getlist('networks[]')
        tags = request.POST.getlist('tags[]')
        page_number = request.POST.get('page_number')
        dateofBirth = request.POST.get('dateofBirth')
        curr_net = request.POST.get('curr_net')
        curr_tag = request.POST.get('curr_tag')
        order = request.POST.get('order')
        price_range = request.POST.get('priceRange')
        avoidNum = request.POST.get('avoidNum')
        startNum = request.POST.get('startNum')
        endNum = request.POST.get('endNum')
        
        if order == "price_increasing":
            queryset = SIM.objects.annotate(
                current_price=ExpressionWrapper(
                    F('price') - (F('discount') / 100) * F('price'),
                    output_field=FloatField()
                )
            ).order_by(F('current_price').asc())
        else: 
            queryset = SIM.objects.annotate(
                current_price=ExpressionWrapper(
                    F('price') - (F('discount') / 100) * F('price'),
                    output_field=FloatField()
                )
            ).order_by(F('current_price').desc())
        
        queryset = queryset.filter(is_available=True, is_visible=True)
        
        if price_range:
            minPrice, maxPrice = price_range.split('-')
            queryset = queryset.filter(current_price__gte=float(minPrice), current_price__lte=float(maxPrice))
        
        if dateofBirth:
            year, month, day = dateofBirth.split("-")
            dateofBirth = day + month + year
            print(dateofBirth)
            queryset = queryset.filter(slug__contains=dateofBirth)

        if curr_net:
            networks = [curr_net]
        if curr_tag:
            tags = [curr_tag]
            
        if networks:
            queryset = queryset.filter(Q(network__slug__in=networks))
            
        if tags:
            queryset = queryset.filter(Q(tags__slug__in=tags))
        
        if avoidNum:
            avoidNum = avoidNum.replace(' ', '')
            if ',' in avoidNum:
                avoidNums = avoidNum.split(',')
            else:
                avoidNums = [avoidNum]
            q_objects = Q()

            for substring in avoidNums:
                q_objects |= Q(my_field__icontains=substring)

            queryset = queryset.exclude(q_objects)
        
        
        if startNum:
            startNum = startNum.replace(' ', '')
            if ',' in startNum:
                startNums = startNum.split(',')
            else:
                startNums = [startNum]
            q_start = Q()
            for c in startNums:
                q_start |= Q(slug__startswith=c)
            queryset = queryset.filter(q_start)   
            
        if endNum:
            startNum = endNum.replace(' ', '')
            if ',' in endNum:
                endNums = endNum.split(',')
            else:
                endNums = [endNum]
            q_end = Q()
            for c in endNums:
                q_end |= Q(phone_number__endswith=c)
            queryset = queryset.filter(q_end)
        
        if order == "price_increasing":
            queryset.order_by(F('current_price').asc())
        else: 
            queryset.order_by(F('current_price').desc())
        
        
        # sim = SIM.objects.get(slug=sim_slug)
        # other_sims = SIM.objects.all().filter(is_available=True, network=sim.network).exclude(id=sim.id)
        paginator = Paginator(queryset, 8)
        page_obj = paginator.get_page(page_number)
        data = SIMSerializer(page_obj, many=True).data
        
        print(data)
        if (int(page_number) > paginator.num_pages):
            data = None
            
        return JsonResponse({
            'data': data,
            })   