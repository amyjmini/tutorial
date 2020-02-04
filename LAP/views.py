from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage

from .forms import SheetForm

# Create your views here.
def home(request):
    context={}
    if request.method == 'POST':
        form = SheetForm(request.POST, request.FILES)
        if form.is_Valid():
            form.save()
            return redirect(endPage)
    else:
        form = SheetForm()
    return render(request, 'home.html', {'form': form})

def loadingPage(request):
    return render(request, 'loadingPage.html')

def endPage(request):
    return render(request, 'endPage.html')

def contactPage(request):
    return render(request, 'contactPage.html')

def upload(request):
    if request.method == 'POST':
        uploaded_file = request.FILES['document']
        print(uploaded_file.name)
        print(uploaded_file.size)
    return render(request, 'upload.html')
