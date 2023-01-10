from django.http import JsonResponse
from django.shortcuts import redirect
from django.views.generic import DetailView, CreateView
from django.views.generic import ListView
from django.contrib import messages
from card.forms import CardForm, PersonForm
from card.models import Card, Person, CardHistory
from django.db.models import Q


class CardListView(ListView):  # ListView by default
    model = Card  # model = Card.objects.filter(deleted=False) # фильтруем не удаленные карты
    template_name = 'card/index.html'  # template_name = 'card/index.html'
    context_object_name = 'cards'  # context_object_name = 'cards' 

    def get_queryset(self):
        return Card.objects.filter(deleted=False)  # фильтруем не удаленные карты

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CardForm()
        return context

    # DetailView by slug field


class CardDetailView(DetailView):  # DetailView by slug field
    model = Card  # model = Card.objects.filter(deleted=False) # фильтруем не удаленные карты
    template_name = 'card/card.html'  # template_name = 'card/card.html'
    context_object_name = 'card'  # context_object_name = 'card'


class CreateCardView(CreateView):
    model = Card  # model = Card.objects.filter(deleted=False) # фильтруем не удаленные карты
    form_class = CardForm  # form_class = CardForm
    template_name = 'card/create_card.html'  # template_name = 'card/create_card.html'
    success_url = '/'  # success_url = '/'

    def form_valid(self, form):
        messages.success(self.request,
                         'Карта успешно создана')  # messages.success(self.request, 'Карта успешно создана')
        messages.error(self.request,
                       'Ошибка при создании карты')  # messages.error(self.request, 'Ошибка при создании карты')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['owner'] = Person.objects.get(pk=self.kwargs['pk'])
        return context


class CreateCardSelectPersonView(CreateView):
    model = Card
    form_class = CardForm
    template_name = 'card/card_and_select_person.html'
    success_url = '/'

    def form_valid(self, form):
        messages.success(self.request, 'Клиент успешно создан')
        messages.error(self.request, 'Ошибка при создании клиента')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['persons'] = Person.objects.all()
        return context


class CreatePersonView(CreateView):
    form_class = PersonForm
    template_name = 'card/new_person.html'
    success_url = '/'

    def form_valid(self, form):
        print('form_valid')
        messages.success(self.request, 'Новый пользователь успешно создан')
        messages.error(self.request, 'Ошибка при создании ногового пользователя')
        return super().form_valid(form)


class SearchCardView(ListView):
    model = Card
    template_name = 'card/index.html'
    context_object_name = 'cards'

    def get_queryset(self):
        query = self.request.GET.get('q')
        return Card.objects.filter(
            Q(number__icontains=query) |
            Q(owner__first_name__search=query) |
            Q(owner__last_name__search=query) |
            Q(owner__card__status__search=query)

        )

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q')
        return context


# AJAXs


def is_ajax(request):  # проверка на ajax запрос
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


# Ajax
def add_amount(request):
    if request.method == 'POST':
        card = Card.objects.get(slug=request.POST.get('card_id'))
        card.amount += int(request.POST.get('amount'))
        card.save()
        return redirect('card_detail', slug=card.slug)
    return JsonResponse({'status': False})


def update_card(request):
    if request.method == 'POST':
        card = Card.objects.get(slug=request.POST.get('card_id'))  # получаем карту по slug
        if request.POST.get('card_type') != 0:  # если тип карты не 0
            card.card_category = request.POST.get('card_type')  # то присваиваем ей тип карты
        if request.POST.get('card_status') != 0:  # если статус карты не 0
            card.status = request.POST.get('card_status')  # то присваиваем ей статус карты
        card.save()  # сохраняем изменения
        return redirect('card_detail', slug=card.slug)
    return JsonResponse({'status': False})


def delete_card(request):
    if request.method == 'POST':
        card = Card.objects.get(slug=request.POST.get('card_id'))
        card.deleted = True
        card.save()
        return redirect('/')
    return JsonResponse({'status': False})
