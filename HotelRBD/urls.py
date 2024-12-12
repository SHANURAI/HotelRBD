from django.contrib import admin
from django.urls import path
from main import views

urlpatterns = [
path('admin/', admin.site.urls),
    # Главная страница
    path('', views.index, name='index'),

    # Редактирование записи (для составных ключей)

    # Редактирование записи (для одиночного ключа)
    path('<str:table>/<int:key1>/edit/', views.edit_record, name='edit_record'),

    # Удаление записи (для составных ключей)

    # Удаление записи (для одиночного ключа)
    path('<str:table>/<int:key1>/delete/', views.delete_record, name='delete_record'),

    # Добавление записи
    path('<str:table>/add/', views.add_record, name='add_record'),
    path('<str:table>/<int:key1>/<int:key2>/<int:key3>/edit/', views.edit_record, name='edit_record_composite'),
    path('<str:table>/<int:key1>/<int:key2>/<int:key3>/delete/', views.delete_record, name='delete_record_composite'),
    path('signup', views.sign_up, name="signup"),
path('logout', views.logout_user,name="logout"),
path('login/', views.login_user, name="login"),

]