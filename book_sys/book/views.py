from django.shortcuts import render ,redirect ,HttpResponse ,get_object_or_404
from django.http import Http404
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from .froms import *
from django.urls import reverse , reverse_lazy
from .models import *
from django.views.generic import ListView , DetailView , UpdateView, DeleteView
from django.db.models import Max
# Create your views here.

class CreateBook(LoginRequiredMixin , View):
    template= 'book/book_form.html'
    success_url = '/'
    def get(self , request):
        if request.user.profile.account_type == 1 :
             raise Http404()
        form = BookForm()
        upfile= UploadFile()

        ctx = {'form' : form  , 'upfile' : upfile}
        return render(request , self.template , ctx)
    
    def post (self , request):
        form = BookForm(request.POST)
        upfile= UploadFile(request.POST , request.FILES)
        if not form.is_valid() or not upfile.is_valid():
            ctx = {'form' : form , 'upfile' : upfile}
            return render(request , self.template , ctx)
        b=form.save(commit=False)
        b.owner=request.user.profile
        b.save()
        add_categories= BookForm(request.POST , instance=b)
        add_categories.save()

        f= request.FILES["upfile"]
        page_number =1
        l=0
        for chunk in f.chunks():
            i=0 
            chunk = str(chunk)
            
            while i<len(chunk):
                j=i+900
                j=min(j,len(chunk))
                k=15
                while(j!=len(chunk) and chunk[j]!=' ' and k>0):
                    k-=1
                    j-=1
                page_content = chunk[i:j].split('\n')
                content = str()
                for row in page_content :
                    content += row
                    content += '\n'
                Page.objects.create(content = content , book = b  , page_number = page_number)
                i+=901
                page_number+=1
        return redirect (self.success_url)

class Main(ListView):
    model = Book
    template_name='book/index.html'

class DetailBook(LoginRequiredMixin , View):
    template_name = 'book/list_page.html'
    def get(self , request, pk):
        x = Read.objects.filter(user__user__id = request.user.id).filter(page__book__id = pk)
        if(x):
            return redirect(reverse('detail_page',
            kwargs={'book_pk' : pk , 'page_num' : x[0].page.page_number }))
        else :
            pages= Page.objects.filter(book__id = pk).order_by('page_number')
            return render(request , self.template_name,{'pages' : pages})

class DetailPage (LoginRequiredMixin , View):
    template_name = 'book/book.html'
    def get(self , request , book_pk  , page_num):
        try :
            x = Page.objects.filter(book__id = book_pk).get(page_number = page_num)
        except Page.DoesNotExist :
            raise Http404('Page Dose Not Exist')
        last_page = Page.objects.filter(book_id = book_pk).aggregate(Max('page_number'))
        return render(request , self.template_name , {'info':x , 'last_page' : last_page['page_number__max']})
    
    def post(self , request , book_pk  , page_num):
        last_page = Read.objects.filter(page__book__id = book_pk , user__user__id = request.user.id)
        if 'next' in request.POST:
            if(last_page.exists()):
                page = Page.objects.filter(book__id = book_pk).get(page_number = page_num +1)
                last_page.update(page = page)
            else :
                next_page = Page.objects.filter(book__id = book_pk).get(page_number = page_num+1)
                Read.objects.create(page = next_page , user = request.user.profile)
            return redirect(reverse('detail_page',kwargs={'book_pk' : book_pk , 'page_num' : page_num+1}))
        else :
            if(last_page.exists()):
                page = Page.objects.filter(book__id = book_pk).get(page_number = page_num -1)
                last_page.update(page = page)
            else :
                previous_page = Page.objects.filter(book__id = book_pk).get(page_number = page_num-1)
                Read.objects.create(page = previous_page , user = request.user.profile)
            return redirect(reverse('detail_page',kwargs={'book_pk' : book_pk , 'page_num' : page_num-1}))
            
class ProfileView(View):
    def get(self , request):
        
        return render(request , 'book/profile.html')

class OwnerUpdateBook(LoginRequiredMixin , View) :
    model = Book
    success_url = '/'
    template = 'book/book_form.html'

    def get(self, request, pk):
        book = get_object_or_404(self.model, pk=pk)
        if request.user.profile != book.owner :
            raise Http404()
        form = BookForm(instance=book)
        ctx = {'form': form}
        return render(request, self.template, ctx)

    def post(self, request, pk):
        book = get_object_or_404(self.model, pk=pk)
        form = BookForm(request.POST, instance=book)
        if not form.is_valid():
            ctx = {'form': form}
            return render(request, self.template, ctx)
        if request.user.profile != book.owner :
            raise Http404()
        form.save()
        return redirect(self.success_url)

class OwnerDeleteBook(LoginRequiredMixin , DeleteView):
    model = Book
    template_name = 'book/delete_form.html'
    success_url = '/'
    def get_queryset(self,*args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(owner= self.request.user.profile)
    
def search(request):
    if request.method == 'GET' and 'search' in request.GET :
        list_books=Book.objects.filter(title__icontains= request.GET['search'])
        return render(request , 'book/filter.html' , {'list_books' : list_books})
class MyBooksView(LoginRequiredMixin , View):
    def get(self , request):
        books = Book.objects.filter(owner = request.user.profile)
        return render(request,'book/my_books.html',{'my_books':books})

class CreateCategory(LoginRequiredMixin , CreateView):
    model= Category
    fields= '__all__'
    success_url=reverse_lazy('create_book')
    
from django.contrib.auth import login
from django.contrib import messages


def register_request(request):
    if(request.method == "POST") :
        UserForm = UserCreateForm(request.POST)
        profile_form = ProfileForm(request.POST)
        if UserForm.is_valid() and profile_form.is_valid() :
            user = UserForm.save()
            profile = profile_form.save(commit= False)
            profile.user=user
            profile.save()
            login(request , user)
            messages.success(request, "Registration successful.")
            return redirect(reverse_lazy('all'))
        return render(request , 'register.html' ,{'register_form' : UserForm ,"profile" : profile_form } )
    UserForm = UserCreateForm()
    profile_form = ProfileForm()
    return render(request=request , template_name="register.html",
     context={"register_form":UserForm , "profile" : profile_form})