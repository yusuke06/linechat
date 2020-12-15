from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from .models import BoardModel
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView
from django.urls import reverse_lazy
# Create your views here.
def signupfunc(request):
    if request.method == 'POST':
        username2 = request.POST['username']
        password2 = request.POST['password']
        macaddress2 = request.POST['macaddress']

        
        try:
            User.objects.get(username=username2)
            return render(request, 'signup.html', {'error':'このユーザーは登録されています'})
        except:
            user = User.objects.create_user(username2, '', password2)
            user.last_name = macaddress2
            user.save()
            return render(request, 'signup.html', {'some':100})
    return render(request, 'signup.html', {'some':100})

def loginfunc(request):
    if request.method == 'POST':
        username2 = request.POST['username']
        password2 = request.POST['password']
        user = authenticate(request, username=username2, password=password2)
        if user is not None:
            login(request, user)
            # Redirect to a success page.
            return redirect('list')
        else:
            return redirect('login')
            # Return an 'invalid login' error message.
    return render(request, 'login.html')
@login_required
def listfunc(request):
    object_list = BoardModel.objects.all()
    return render(request, 'list.html', {'object_list':object_list})


def logoutfunc(request):
    logout(request)
    return redirect('login')
    # Redirect to a success page.    


def detailfunc(request, pk):
    object = BoardModel.objects.get(pk=pk)
    return render(request, 'detail.html', {'object':object})

def goodfunc(request, pk):
    post = BoardModel.objects.get(pk=pk)
    post.good = int(post.good) + 1
    post.save()
    return redirect('list')

def readfunc(request, pk):
    post = BoardModel.objects.get(pk=pk)
    post2 = request.user.get_username()
    if post2 in post.readtext:
        return redirect('list')
    else:
        post.read += 1
        post.readtext = str(post.read) + ' ' + str(post2)
        print(type(post2))
        post.save()
        return redirect('list') 

class BoardCreate(CreateView):
    template_name = 'create.html'
    model = BoardModel
    fields = ('title','content', 'author', 'images')
    success_url = reverse_lazy('list')    



























