from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate , login , logout
from django.contrib.auth.decorators import login_required
from todo.models import Todo

def signup(request):
    if request.user.is_authenticated:   # ✅ Correct way
        return redirect('todo')

    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if User.objects.filter(username=name).exists():
            return render(request, 'signup.html', {'error': 'User already exists'})

        user = User.objects.create_user(username=name, email=email, password=password)
        login(request, user)  # auto login after signup
        return redirect('todo')

    return render(request, 'signup.html')


def loginn(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        password = request.POST.get('password')

        if User.objects.filter(username=name).exists()==False:
            return render(request, 'login.html', {
                'error': 'User dose not exists'
            })
        user = authenticate(request,username=name,password=password)
        print(user)
        if user is not None:
            login(request,user)
            print('login completed')
            return redirect('/todo')
        else:
            return redirect('/login',{'error':'login error'})
    return render(request, 'login.html')

@login_required(login_url='/login')
def todo(request):
    tasks = Todo.objects.filter(user=request.user)

    if request.method == 'POST':
        title = request.POST.get('title')

        if Todo.objects.filter(user=request.user, title=title).exists():
            return render(request, 'todo.html', {
                'error': 'This task already exists',
                'tasks': tasks
            })

        Todo.objects.create(title=title, user=request.user)
        tasks = Todo.objects.filter(user=request.user)  

    return render(request, 'todo.html', {'tasks': tasks})

@login_required(login_url='/login')
def edit(request, pk):
    task = Todo.objects.filter(user=request.user, srno=pk).first()
    
    if not task:
        return redirect('todo') 

    if request.method == 'POST':
        new_title = request.POST.get('title')

        if Todo.objects.filter(user=request.user, title=new_title).exclude(srno=pk).exists():
            return render(request, 'edit.html', {
                'task': task,
                'error': 'This task already exists'
            })

        task.title = new_title
        task.save()
        return redirect('todo')

    return render(request, 'edit.html', {'task': task})

@login_required(login_url='/login')
def delete(request, pk):
    task = Todo.objects.filter(user=request.user, srno=pk).first()

    if task:
        task.delete()

    return redirect('todo')

@login_required(login_url='/login')
def logoutt(request):
    logout(request)
    return redirect('login')
