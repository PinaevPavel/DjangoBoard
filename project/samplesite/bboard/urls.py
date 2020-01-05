#создаем список маршрутов для приложения bboard
from django.urls import path
from .views import BbCreateView, add_and_save, BbIndexView, BbDetailView, BbByRubricView #index, by_rubric

urlpatterns = [
	path('add/', BbCreateView.as_view(), name='add'), # В вызове функции path() подставляется не ссылка на сам контроллер-класс, а результат, возвращенный методом as_view() контроллера-класса.
	path('<int:rubric_id>/', BbByRubricView.as_view(), name='by_rubric'), # конструкция int - челочисленный тип парамента, а rubric_id имя парамента контроллера, которому будет присвоено значение этого url-парамента
	path('detail/<int:pk>/', BbDetailView.as_view(), name='detail'),
	#name - имя маршрута, необходимое для реализации обратного разрешения интернет-адресов
	path('', BbIndexView.as_view(), name='index'), #Пустая строка, означает корень пути из маршрута предыдущего уровля вложенности.
]