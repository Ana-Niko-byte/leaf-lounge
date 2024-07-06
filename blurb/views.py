from django.shortcuts import render

# Create your views here.
def blurb(request):
    return render(
        request,
        'blurb/index.html'
    )