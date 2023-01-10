from django.urls import path

from card.views import CardListView, CardDetailView, CreateCardView
from card.views import CreatePersonView, CreateCardSelectPersonView
from card.views import add_amount, update_card, delete_card

# создаем список с путями для нашего приложения card

urlpatterns = [
    path('', CardListView.as_view(), name='index'),
    path('card/<slug:slug>/', CardDetailView.as_view(), name='card_detail'),
    path('create_person/', CreatePersonView.as_view(), name='create_person'),
    # ajax
    path('add_amount/', add_amount, name='add_amount'),
    path('update_card/', update_card, name='update_card'),
    path('delete_card/', delete_card, name='delete_card'),
    path('create_card/<int:pk>/', CreateCardView.as_view(), name='create_card'),
    path('create_card_select_person/', CreateCardSelectPersonView.as_view(), name='create_card_select_person'),
]
