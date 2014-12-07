from django.shortcuts import render

# Create your views here.

def index(request):
    request.session.modified = True
    return render(request, 'index.html')
