from django.shortcuts import render, redirect, get_object_or_404
from .models import Task
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required


from django.shortcuts import render, redirect, get_object_or_404
from .models import Task
from django.contrib.auth.decorators import login_required

@login_required
def home(request):
    filter_option = request.GET.get('filter', 'all')  # get filter query param
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        if title:
            Task.objects.create(title=title, description=description, user=request.user)
            return redirect('home')

    # Apply filters based on query param
    if filter_option == 'completed':
        tasks = Task.objects.filter(user=request.user, completed=True)
    elif filter_option == 'pending':
        tasks = Task.objects.filter(user=request.user, completed=False)
    else:
        tasks = Task.objects.filter(user=request.user)

    context = {
        'tasks': tasks,
        'filter': filter_option,
    }
    return render(request, 'tasks/home.html', context)


@login_required
def complete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.completed = True
    task.save()
    return redirect('home')


@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.delete()
    return redirect('home')


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'tasks/signup.html', {'form': form})


@login_required
def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)

    if request.method == 'POST':
        task.title = request.POST.get('title')
        task.description = request.POST.get('description')
        task.save()
        return redirect('home')

    return render(request, 'tasks/edit_task.html', {'task': task})
