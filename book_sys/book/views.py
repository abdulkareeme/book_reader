from django.shortcuts import render ,redirect ,HttpResponse
from django.http import Http404
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from .froms import *
from django.urls import reverse_lazy
from .models import *
from django.views.generic import ListView , DetailView
# Create your views here.

class CreateBook(LoginRequiredMixin , View):
    template= 'book/book_form.html'
    success_url = '/'
    def get(self , request):
        # if(2 == 2) :
        #     raise Http404()

        form = BookForm()
        upfile= UploadFile()
        ctx = {'form' : form  , 'upfile' : upfile}
        return render(request , self.template , ctx)
    
    def post (self , request):
        form = BookForm(request.POST)
        upfile= UploadFile(request.POST , request.FILES)
        if not form.is_valid() or not upfile.is_valid():
            ctx = {'form' : form}
            return render(request , self.template , ctx)
        b=form.save(commit=False)
        user=request.user
        b.owner=user
        b.save()
        f= request.FILES["upfile"]
        j=1
        for chunk in f.chunks():
            i=0 
            while i<len(chunk):
                Page.objects.create(content = chunk[i:i+1000] , book = b  , page_number = j)
                i+=1001
                j+=1
        return redirect (self.success_url)

class Main(ListView):
    model = Book
    template_name='book/index.html'

class DetailBook(LoginRequiredMixin , View):
    template_name = 'book/book.html'
    def get(self , request, pk):
        x = Read.objects.filter(user=request.user).all() #fix
        for i in x :
            print (i.page.book.title)
        print (x)
        return render(request , 'book/book.html')


from django.contrib.auth import login
from django.contrib import messages

def register_request(request):
	if request.method == "POST":
		form = UserCreateForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			messages.success(request, "Registration successful.")
			return redirect(reverse_lazy('all'))
		messages.error(request, "Unsuccessful registration. Invalid information.")
	form = UserCreateForm()
	return render (request=request, template_name="register.html", context={"register_form":form})


