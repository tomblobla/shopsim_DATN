from django.shortcuts import render

# Create your views here.


def tags(request):
    context = {}
    return render(request, 'admin_sim_tags.html', context)
