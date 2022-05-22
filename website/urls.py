from .models import *
from django.contrib import admin
from django.http import HttpResponse
from django.urls import path, register_converter
from datetime import date


class DateConverter:
    # 20022.05.21
    regex = "20[0-9]{2}.[0-9]{2}.[0-9]{2}"

    def to_python(self, value: str):
        array = value.split('.')
        dt = date(year=int(array[0]), month=int(array[1]), day=int(array[2]))
        return dt

    def to_url(self, value: date):
        return f"{value.year}.{value.month}.{value.day}"


register_converter(DateConverter, 'date')




def articles_by_year(request, year):
    return HttpResponse(f"{year}-yilda chiqarilgan maqolalar")


def articles_by_year_month_day(request, year, month, day):
    return HttpResponse(f"{year}.{month}.{day}-yilda chiqarilgan maqolalar")


def articles_by_slug(request, year, month, day, title):
    return HttpResponse(f"{year}.{month}.{day}-yilda chiqarilgan {title}")


def articles_by_slug_converter(request, dt: date, title):
    return HttpResponse(f"{dt.year}.{dt.month}.{dt.day}-yilda ciqarilgan {title}")


def get_school(request):
    html = """<h2>School</h2>"""
    for item in School.objects():
        html += f'{item.name} <br>'
    return HttpResponse(html)


def get_class(request):
    print(request.GET)
    search_text = request.GET.get('search-text')
    print(search_text)

    html = """<h2>Class</h2>
        <table style='border: solid 1px'>
            <tr style='border: solid 1px'>
                <td style='border: solid 1px'>School nomi</td>
                <td style='border: solid 1px'>Class nomi</td>
            </tr>
    """
    for item in Class.objects():
        if search_text is None or search_text.lower() in item.name.lower():
            html += f"""
                    <tr style='border: solid 1px '>
                        <td style='border: solid 1px '>{item.school.name}</td>
                        <td style='border: solid 1px'>{item.name}</td>
                    </tr>
                """
    html += '</table>'
    return HttpResponse(html)


def get_student(request):
    print(request.GET)
    search_text = request.GET.get('search-text')
    print(search_text)

    html = """<h2>Student</h2>
        <table style='border: solid 1px'>
            <tr style='border: solid 1px'>
                <td style='border: solid 1px'>Class</td>
                <td style='border: solid 1px'>Surname</td>
                <td style='border: solid 1px'>Name</td>
                <td style='border: solid 1px'>Marks</td>
                <td style='border: solid 1px'>Fvorite science</td>
                <td style='border: solid 1px'>Neighborhood</td>
            </tr>
    """
    for item in Student.objects():
        if search_text is None or search_text.lower() in item.surname.lower():
            html += f"""
                    <tr style='border: solid 1px'>
                        <td style='border: solid 1px '>{item.Class.name}</td>
                        <td style='border: solid 1px'>{item.surname}</td>
                        <td style='border: solid 1px'>{item.name}</td>
                        <td style='border: solid 1px'>{item.marks}</td>
                        <td style='border: solid 1px'>{item.favorite_science}</td>
                        <td style='border: solid 1px'>{item.neighborhood}</td>
                    </tr>
                """
    html += '</table>'
    return HttpResponse(html)


def index(request):
    return HttpResponse("Salom Olam")


urlpatterns = [
    path('articles/2003/', articles_2003),
    path('articles/<int:year>/', articles_by_year),
    path('articles/<int:year>/<int:month>/<int:day>/', articles_by_year_month_day),
    path('articles/<int:year>/<int:month>/<int:day>/<slug:title>',
         articles_by_slug),
    path('articles/<date:dt>/<slug:title>',
         articles_by_slug_converter),
    path('', index),
    path('school/', get_school),
    path('class/', get_class),
    path('student/', get_student),
    path('admin/', admin.site.urls),
]
