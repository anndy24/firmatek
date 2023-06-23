from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views.generic import ListView, UpdateView, DetailView
from .models import Project
from django.core.paginator import Paginator, EmptyPage
from django.urls import reverse_lazy
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import user_passes_test

from .models import Firmuser
from .models import *
from .forms import FirmuserForm, SignUpForm, ProjectForm
from .forms import *
# Create your views here.

def index(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Вы вошли в систему")
            if user.is_superuser:
                return redirect("index")  # Редирект для суперпользователя
            else:
                return redirect("projects")  # Редирект для обычного пользователя
        else:
            messages.warning(request, "Произошла ошибка, попробуйте еще раз")
            return redirect("index")
    else:
        return render(request, 'firmusers/index.html', {'firmusers': Firmuser.objects.all()})


def view_firmuser(request, id):
  firmuser = Firmuser.objects.get(pk=id)
  return HttpResponseRedirect(reverse('index'))

def superuser_check(user):
    return user.is_superuser

@user_passes_test(superuser_check)
@login_required(login_url='/')
def tasks(request):
    projects = Project.objects.all()
    selected_project = request.GET.get('project')
    if selected_project:
        tasks = Task.objects.filter(project_id=selected_project)
    else:
        tasks = Task.objects.all()

    # Добавление пагинации
    items_per_page = 9  # Количество задач на странице
    paginator = Paginator(tasks, items_per_page)
    page_number = request.GET.get('page')
    try:
        page = paginator.get_page(page_number)
    except EmptyPage:
        page = paginator.get_page(paginator.num_pages)

    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save()
            formset = SubtaskFormSet(request.POST, instance=task)
            if formset.is_valid():
                formset.save()
                return redirect('tasks')
    else:
        form = TaskForm()
        formset = SubtaskFormSet()

    context = {
        'tasks': page,  # Используем объект Page вместо списка tasks
        'projects': projects,
        'selected_project': selected_project,
        'form': form,
        'formset': formset,
        'page_obj': page,  # Передаем объект Page в контекст шаблона
    }

    return render(request, 'firmusers/tasks.html', context)


class ProjectListView(LoginRequiredMixin, ListView):
    model = Project
    template_name = 'firmusers/projects.html'
    context_object_name = 'projects'
    paginate_by = 3

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ProjectForm()
        return context
    
    def post(self, request, *args, **kwargs):
        form = ProjectForm(request.POST, request.FILES)
        
        if form.is_valid():
            form.save()
            messages.success(request, 'Проект успешно сохранен.')
            return redirect('projects')
        else:
            messages.error(request, 'При сохранении проекта произошла ошибка.')
            context = self.get_context_data(**kwargs)
            context['form'] = form
            return self.render_to_response(context)

    def get_queryset(self):
        user = self.request.user
        query = self.request.GET.get('search')

        if user.is_superuser:
            # Если пользователь администратор, выводятся все проекты
            if query:
                # Фильтрация проектов по наименованию или описанию, содержащих запрос
                queryset = Project.objects.filter(Q(title__icontains=query) | Q(description__icontains=query))
            else:
                queryset = Project.objects.all()
        else:
            # В противном случае производится фильтрация по профессии пользователя
            if query:
                # Фильтрация проектов по наименованию или описанию, содержащих запрос, и доступным профессиям пользователя
                queryset = Project.objects.filter(
                    Q(title__icontains=query) | Q(description__icontains=query),
                    professions=user.professions
                )
            else:
                queryset = Project.objects.filter(professions=user.professions)

        return queryset

    
class PodryadListView(LoginRequiredMixin, ListView):
    model = Profession
    template_name = 'firmusers/podryadchiks.html'
    context_object_name = 'professions'
    paginate_by = 3

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ProfessionForm()
        return context
    
    def post(self, request, *args, **kwargs):
        form = ProfessionForm(request.POST, request.FILES)
        
        if form.is_valid():
            form.save()
            messages.success(request, 'Подрядчик успешно сохранен.')
            return redirect('podryad')
        else:
            messages.error(request, 'При сохранении подрядчика произошла ошибка.')
            context = self.get_context_data(**kwargs)
            context['form'] = form
            return self.render_to_response(context)

    def get_queryset(self):
        user = self.request.user
        query = self.request.GET.get('search')

        if user.is_superuser:
            # Если пользователь администратор, выводятся все подрядчики
            if query:
                # Фильтрация проектов по наименованию или описанию, содержащих запрос
                queryset = Profession.objects.filter(Q(name__icontains=query))
            else:
                queryset = Profession.objects.all()
        else:
            # В противном случае производится фильтрация по подрядчику пользователя
            if query:
                queryset = Profession.objects.filter(
                    Q(name__icontains=query),
                    professions=user.professions
                )
            else:
                queryset = Profession.objects.filter(professions=user.professions)

        return queryset

@user_passes_test(superuser_check)
@login_required(login_url='/')
def edit_project(request, id):
    project = get_object_or_404(Project, pk=id)

    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            messages.success(request, 'Проект успешно отредактирован.')
            return redirect('projects')
        else:
            messages.error(request, 'При редактировании проекта произошла ошибка.')
    else:
        form = ProjectForm(instance=project)

    return render(request, 'firmusers/edit_project.html', {
        'form': form,
        'project': project
    })

@user_passes_test(superuser_check)
@login_required(login_url='/')
def edit_podryad(request, id):
    podryad = get_object_or_404(Profession, pk=id)

    if request.method == 'POST':
        form = ProfessionForm(request.POST, instance=podryad)
        if form.is_valid():
            form.save()
            messages.success(request, 'Подрядчик успешно отредактирован.')
            return redirect('podryad')
        else:
            messages.error(request, 'При редактировании подрядчика произошла ошибка.')
    else:
        form = ProfessionForm(instance=podryad)

    return render(request, 'firmusers/edit_podryad.html', {
        'form': form,
        'project': podryad
    })


def delete_project(request, id):
  if request.method == 'POST':
    firmuser = Project.objects.get(pk=id)
    firmuser.delete()
    messages.success(request, 'Проект успешно удален.')
  return HttpResponseRedirect(reverse('projects'))
    
def delete_task(request, id):
  if request.method == 'POST':
    task = Task.objects.get(pk=id)
    task.delete()
    messages.success(request, 'Задача успешно удален.')
  return HttpResponseRedirect(reverse('tasks'))

def delete_podryad(request, id):
  if request.method == 'POST':
    firmuser = Profession.objects.get(pk=id)
    firmuser.delete()
    messages.success(request, 'Подрядчик успешно удален.')
  return HttpResponseRedirect(reverse('podryad'))

def add(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = FirmuserForm(request.POST)
            if form.is_valid():
                new_firmuser = form.save(commit=False)
                new_firmuser.password = form.cleaned_data['password']  # Сохраняем значение пароля
                new_firmuser.save()
                phone_number = form.cleaned_data['phone']
                Phone.objects.create(user=new_firmuser, name=phone_number)
                return render(request, 'firmusers/add.html', {
                    'form': FirmuserForm(),
                    'success': True
                })
        else:
            form = FirmuserForm()
        return render(request, 'firmusers/add.html', {
            'form': form
        })
    else:
        messages.error(request, "Вам нужно авторизоваться")
        return redirect("index")


def edit(request, id):
    if request.user.is_authenticated:
        firmuser = Firmuser.objects.get(pk=id)
        phone_number = ""
        car_number = ""
        try:
            phone = Phone.objects.get(user=firmuser)
            phone_number = phone.name
        except Phone.DoesNotExist:
            pass
        try:
            car = CarNumber.objects.get(user=firmuser)
            car_number = car.number
        except CarNumber.DoesNotExist:
            pass

        if request.method == 'POST':
            form = FirmuserForm(request.POST, instance=firmuser)
            if form.is_valid():
                new_firmuser = form.save(commit=False)
                password = form.cleaned_data['password']
                if password:
                    new_firmuser.set_password(password)
                new_firmuser.save()
                new_phone_number = form.cleaned_data['phone']
                new_car_number = form.cleaned_data['number']
                if phone_number:  # Если номер телефона уже существует, обновляем его значение
                    phone.name = new_phone_number
                    phone.save()
                else:  # Иначе, создаем новый объект Phone
                    Phone.objects.create(user=new_firmuser, name=new_phone_number)
                if car_number:  # Если номер машины уже существует, обновляем его значение
                    car.number = new_car_number
                    car.save()
                else:  # Иначе, создаем новый объект CarNumber
                    CarNumber.objects.create(user=new_firmuser, number=new_car_number)
                return render(request, 'firmusers/edit.html', {
                    'form': form,
                    'success': True
                })
        else:
            form = FirmuserForm(instance=firmuser, initial={'phone': phone_number, 'number': car_number})  # Устанавливаем начальное значение полей phone и number
        return render(request, 'firmusers/edit.html', {
            'form': form
        })
    else:
        messages.error(request, "Вам нужно авторизоваться")
        return redirect("index")


def delete(request, id):
  if request.method == 'POST':
    firmuser = Firmuser.objects.get(pk=id)
    firmuser.delete()
  return HttpResponseRedirect(reverse('index'))

def logout_user(request):
    logout(request)
    messages.success(request, "Вы вышли из системы")
    return redirect("index")


def register_user(request):
    form = SignUpForm()

    if request.method == "POST":
        form = SignUpForm(request.POST)

        if form.is_valid():
            user = form.save()  # Сохраняем пользователя, включая номер телефона и номер машины
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password1"]
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "Вы зарегистрированы")
            return redirect("projects")
        else:
            messages.error(request, "Произошла ошибка при регистрации")

    return render(request, "firmusers/register.html", {"form": form})

@user_passes_test(superuser_check)
@login_required(login_url='/')
def edit_task_with_subtasks(request, id):
    task = get_object_or_404(Task, pk=id)
    SubtaskFormSet = inlineformset_factory(Task, Subtask, form=SubtaskForm, extra=0, can_delete=True)

    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        formset = SubtaskFormSet(request.POST, instance=task)
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            messages.success(request, 'Задача и подзадачи успешно отредактированы.')
            return redirect('tasks')
        else:
            messages.error(request, 'При редактировании задачи и подзадач произошла ошибка.')
    else:
        form = TaskForm(instance=task)
        formset = SubtaskFormSet(instance=task)

    return render(request, 'firmusers/edit_task.html', {
        'form': form,
        'formset': formset,
        'task': task
    })

def profile(request, id):
    if request.user.is_authenticated:
        firmuser = Firmuser.objects.get(pk=id)
        phone_number = ""
        car_number = ""
        try:
            phone = Phone.objects.get(user=firmuser)
            phone_number = phone.name
        except Phone.DoesNotExist:
            pass
        try:
            car = CarNumber.objects.get(user=firmuser)
            car_number = car.number
        except CarNumber.DoesNotExist:
            pass

        if request.method == 'POST':
            if firmuser != request.user:  # Проверяем, что пользователь редактирует свой собственный профиль
                messages.error(request, "Вы можете редактировать только свой профиль")
                return redirect("index")

            form = ProfileForm(request.POST, instance=firmuser)
            if form.is_valid():
                new_firmuser = form.save(commit=False)
                password = form.cleaned_data['password']
                if password:
                    new_firmuser.set_password(password)
                new_firmuser.save()
                new_phone_number = form.cleaned_data['phone']
                new_car_number = form.cleaned_data['number']
                if phone_number:  # Если номер телефона уже существует, обновляем его значение
                    phone.name = new_phone_number
                    phone.save()
                else:  # Иначе, создаем новый объект Phone
                    Phone.objects.create(user=new_firmuser, name=new_phone_number)
                if car_number:  # Если номер машины уже существует, обновляем его значение
                    car.number = new_car_number
                    car.save()
                else:  # Иначе, создаем новый объект CarNumber
                    CarNumber.objects.create(user=new_firmuser, number=new_car_number)
                return render(request, 'firmusers/profile.html', {
                    'form': form,
                    'success': True
                })
        else:
            if firmuser != request.user:  # Проверяем, что пользователь просматривает свой собственный профиль
                messages.error(request, "Вы можете просматривать только свой профиль")
                return redirect("projects")

            form = ProfileForm(instance=firmuser, initial={'phone': phone_number, 'number': car_number})  # Устанавливаем начальное значение полей phone и number
        return render(request, 'firmusers/profile.html', {
            'form': form
        })
    else:
        messages.error(request, "Вам нужно авторизоваться")
        return redirect("index")

def project_open(request, id):
    project = get_object_or_404(Project, pk=id)
    return render(request, 'firmusers/project_open.html', {'project': project})

class ArchiveListView(LoginRequiredMixin, ListView):
    model = Project
    template_name = 'firmusers/archive.html'
    context_object_name = 'archive'
    paginate_by = 9
        
    def get_queryset(self):
        user = self.request.user
        query = self.request.GET.get('search')
        
        if user.is_superuser:
            if query:
                queryset = Project.objects.filter(
                    Q(title__icontains=query) | Q(description__icontains=query),
                    is_active=False
                )
            else:
                queryset = Project.objects.filter(is_active=False)
        else:
            if query:
                queryset = Project.objects.filter(
                    Q(title__icontains=query) | Q(description__icontains=query),
                    professions__in=user.professions.all(),
                    is_active=False
                )
            else:
                queryset = Project.objects.filter(
                    professions__in=user.professions.all(),
                    is_active=False
                )

        return queryset
