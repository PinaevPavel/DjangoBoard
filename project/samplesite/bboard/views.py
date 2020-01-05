from django.http import HttpResponse, HttpResponseRedirect
from .models import Bb, Rubric
from django.shortcuts import render
from django.views.generic.edit import CreateView # базовый класс, реализует функциональность по созданию формы, выводу ее на экран с применением указанного шаблона, 
#получению занесенных данных в форму данных, проверке их на корректность, сохранению их в  новой записи модели и перенаправленю в случае успеха на интернет-адрес, который мы зададим.
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from .forms import BbForm # Импорь нужной формы
from django.urls import reverse_lazy, reverse # Эта функция принимает имя маршрута и значения всех входящих в маршрут URL параметров
from django.template.loader import get_template

class BbIndexView(TemplateView):
	template_name = 'bboard/index.html'

	def get_context_data(self, *args, **kwargs):
		context = super().get_context_data(*args, **kwargs)
		context['bbs'] = Bb.objects.all()
		context['rubrics'] = Rubric.objects.all()
		return context

class BbByRubricView(ListView):
	template_name = 'bboard/by_rubric.html'
	context_object_name = 'bbs' #атрибут, задает имя переменной контекста шаблона, в которой будет сохранен извлеченный набор записей

	def get_queryset(self): # метод, возвращает исходный набор записей из которого будут извлекаться записи.
		return Bb.objects.filter(rubric=self.kwargs['rubric_id'])

	def get_context_data(self, *args, **kwargs): #переопределяющий метод, создающий и возвращабщий контекст данных
		context = super().get_context_data(*args, **kwargs)
		context['current_rubric'] = Rubric.objects.get(pk=self.kwargs['rubric_id'])
		context['rubrics'] = Rubric.objects.all()
		return context

#def index(request):
	##template = loader.get_template('bboard/index.html') #Загружаем шаблон, с помощью функции get_template(). В качестве парамента передаем путь к файлу шаблона, отчитанному от папки template, результатом возвращенным функцией, станет экземпляр класса Template, представляющий хранящийся в заданном файле шаблон
	#bbs = Bb.objects.all()
	#rubrics = Rubric.objects.all()
	#context = {'bbs': bbs, 'rubrics': rubrics}
	#template = get_template('bboard/index.html')
	##return HttpResponse(request, 'bboard/index.html', context) # Запускаем обработку шаблона, в процессе которого шаблонизатор выполяет объеденение его с данными из контекста. Рендерин запускаеться вызовом метода render() класса Template.
	#return HttpResponse(template.render(context=context, request=request))
	
#def by_rubric(request, rubric_id):
	#bbs = Bb.objects.filter(rubric=rubric_id) # список объявления, отфильтрованных по полу ключа rubric
	#rubrics = Rubric.objects.all() 
	#current_rubric = Rubric.objects.get(pk=rubric_id) #Фильтруем из списка рубрик 1 объявление с нужным ИД pk - принимает что нужно искать
	#context = {'bbs': bbs, 'rubrics': rubrics, 'current_rubric': current_rubric}
	#return render(request, 'bboard/by_rubric.html', context)

class BbCreateView(CreateView):
	template_name = 'bboard/create.html' #Путь к файлу шаблона, который будет использован для вывода страницы с формой
	form_class = BbForm #класс формы, связанный с моделью
	success_url = reverse_lazy('index') # Интернет адрес, по которому будет выполнено перенаправление после успешного сохранения данных

	def get_context_data(self, **kwargs): #Метод, который будет генерировать панель навигации, содержащая список рубрик
		context = super().get_context_data(**kwargs) # получаем контекст шаблона из метода базового класса
		context['rubrics'] = Rubric.objects.all() # добовляем список рубрик 
		return context #возвращаем список в качесве результата

def add_and_save(request): #Данная контроллер функция выполняет и вывод формы на страницу и отправление POST Запроса с данным формы на сервер.
	if request.method == 'POST':
		bbf = BbForm(request.POST)
		if bbf.is_valid():
			bbf.save()
			return HttpResponseRedirect(reverse('by_rubric', kwargs={'rubric_id': bbf.cleaned_data['rubric'].pk})) # Метод HttpResponseRedirect, выполняет перенаправление после выполнения тела функции
			#kwargs - нужен для формирования параметризированного маршрута. задаются в виде словаря, ключи элементов соответствуют именами URL параметров, а значения элементов зададут значения параметров. 
			#Функция reverse формирует интернет адрес на основе объвленых в списках маршутор, атрибут cleaned_data, дает доступ к данным класса, получаем данные в виде словаря, фильтруем словарь по рубрики, и получаем его id через pk
		else:
			context = {'form': bbf}
			return render(request, 'bboard/create.html', context)
	else:
		bbf = BbForm()
		context = {'form': bbf}
		return render(request, 'bboard/create.html', context)

class BbDetailView(DetailView): #Выводит информаци о выбранном посетителем обявлении
	template_name = 'bboard/bb_detail.html'
	model = Bb #Атрибут, задает модель для извлечения записи

	def get_context_data(self, *args, **kwargs):
		context = super().get_context_data(*args, **kwargs)
		context['rubrics'] = Rubric.objects.all()
		return context

