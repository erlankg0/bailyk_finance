from django.urls import path
from card.views import index, CardListView

# создаем список с путями для нашего приложения card

urlpatterns = [
    path('', CardListView.as_view(), name='index'),
    path('card/<slug:slug>/', index, name='card_detail'),
]
