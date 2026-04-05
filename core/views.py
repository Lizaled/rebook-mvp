from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login
from django.urls import reverse_lazy
from .models import Book
from .forms import CustomUserCreationForm, BookForm
from django.contrib.auth.decorators import login_required

# 1. Каталог книг (Публичный)
class BookListView(ListView):
    model = Book
    template_name = 'core/catalog.html'
    context_object_name = 'books'
    
    def get_queryset(self):
        # Показываем только доступные книги
        return Book.objects.filter(status='available').order_by('-created_at')

# 2. Регистрация
def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('catalog')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

# 3. Добавление книги (Только для авторизованных)
class BookCreateView(LoginRequiredMixin, CreateView):
    model = Book
    form_class = BookForm
    template_name = 'core/add_book.html'
    success_url = reverse_lazy('profile')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        # Для MVP автоматически назначаем первое попавшееся сообщество или дефолтное, 
        # если у пользователя оно есть. В реальном проекте это берется из профиля.
        # Здесь оставим null или потребует доработки модели User.
        # Для простоты MVP: пусть админ вручную назначит community пользователю или книге, 
        # либо добавим поле выбора сообщества в форму.
        # Добавим поле community в форму временно для MVP, если нужно, или установим дефолт.
        
        # Упрощение: Если у пользователя нет сообщества, книга будет без него (или ошибка, если поле required).
        # В ПР-03 community_id required для Book. 
        # Исправление: Добавим выбор сообщества в форму или возьмем первое.
        # Для чистоты кода MVP предположим, что мы выбираем первое активное сообщество, если не указано иное.
        from .models import Community
        if not form.instance.community_id:
            first_community = Community.objects.first()
            if first_community:
                form.instance.community = first_community
            else:
                # Создадим тестовое, если нет (крайний случай)
                form.instance.community = Community.objects.create(name="Default Community", type="family")
                
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

# 4. Профиль пользователя
@login_required
def profile_view(request):
    user_books = Book.objects.filter(owner=request.user).order_by('-created_at')
    # Подсчет простой статистики
    books_given = user_books.count()
    # EcoMetric пока считаем условно: 1 книга = 2 кг CO2 (пример)
    co2_saved = books_given * 2 
    
    context = {
        'user_books': user_books,
        'books_given': books_given,
        'co2_saved': co2_saved,
    }
    return render(request, 'core/profile.html', context)