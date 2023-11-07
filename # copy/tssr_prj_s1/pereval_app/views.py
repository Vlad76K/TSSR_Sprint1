from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
import json
from django.http import JsonResponse
from django.views import View
from .models import PerevalAdded, PerevalImages, Authors, StatusList, Coords


def submit_data(request):
    try:
        data = json.loads(request.body.decode("utf-8"))

        """ проверим формат JSON на наличие необходимых полей """
        api_check = APICheckView()
        api_check.api_data = data
        its_right = api_check.check_json()
        if len(its_right.get('missing_keys')) > 0:
            raise AttributeError(its_right.get('missing_keys'))

        """ загрузим инфо о пользователе, если такого нет в системе (уникальный емейл """
        user_email = data['user']['email']
        user_item = Authors.objects.filter(user_email=user_email)
        if user_item.exists():
            user_item = Authors.objects.filter(user_email=user_email)[0]
        else:
            user_fam = data['user']['fam']
            user_name = data['user']['name']
            user_otc = data['user']['otc']
            user_phone = data['user']['phone']
            user_data = {
                'user_fam': user_fam,
                'user_name': user_name,
                'user_otc': user_otc,
                'user_phone': user_phone,
                'user_email': user_email,
            }
            user_item = Authors.objects.create(**user_data)

        latitude = data['coords']['latitude']
        longitude = data['coords']['longitude']
        height = data['coords']['height']

        coords_data = {
            'latitude': latitude,
            'longitude': longitude,
            'height': height,
        }
        coords_item = Coords.objects.create(**coords_data)

        """ загрузим информацию о гео-объекте """
        add_time = data['add_time']
        beauty_title = data.get('beauty_title')
        connect = data.get('connect')
        other_titles = data.get('other_titles')
        title = data.get('title')
        level_autumn = data['level']['autumn']
        level_spring = data['level']['spring']
        level_summer = data['level']['summer']
        level_winter = data['level']['winter']
        image_data = data['images']

        geo_data = {
            'add_time': add_time,
            'beauty_title': beauty_title,
            'connect': connect,
            'other_titles': other_titles,
            'title': title,
            'level_autumn': level_autumn,
            'level_spring': level_spring,
            'level_summer': level_summer,
            'level_winter': level_winter,
            'users': user_item,
            'coords': coords_item,
        }
        geo_item = PerevalAdded.objects.create(**geo_data)

        geo_status = StatusList.objects.filter(pk=0)
        geo_item.status.add(*geo_status)

        """ Добавим информацию о фотографиях """
        for imd in image_data:
            image_data = {
                'image_data': imd['data'],
                'image_title': imd['title'],
                'image_go': geo_item,   # GeoObjects.objects.filter(pk=geo_item)
            }
            PerevalImages.objects.create(**image_data)

        data = {"message": f"В базу добавлена новая запись с id: {geo_item.id}"}

        return JsonResponse(data, status=200)
    except AttributeError as err:  # 400 — Bad Request (при нехватке полей);
        data = {"message": f"Отсутствуют поля:{err}"}
        return JsonResponse(data, status=400)
    except:  # 500 — ошибка при выполнении операции;
        data = {"message": f"Ошибка при выполнении операции!"}
        return JsonResponse(data, status=500)

class APICheckView(TemplateView):
    api_data = {}

    def check_json(self):
        context = {}
        context['missing_keys'] = []

        required_keys = ['beauty_title', 'title', 'other_titles', 'connect', 'add_time',
                         'coords', 'latitude', 'longitude', 'height',
                         'user', 'fam', 'name', 'otc', 'phone', 'email',
                         'level', 'winter', 'summer', 'autumn', 'spring',
                         'images']

        for key in required_keys:
            if key == 'fam' or key == 'name' or key == 'otc' or key == 'phone' or key == 'email':
                if key not in self.api_data.get('user'):
                    context['missing_keys'].append(key)
            elif key == 'latitude' or key == 'longitude' or key == 'height':
                if key not in self.api_data.get('coords'):
                    context['missing_keys'].append(key)
            elif key == 'winter' or key == 'summer' or key == 'autumn' or key == 'spring':
                if key not in self.api_data.get('level'):
                    context['missing_keys'].append(key)
            else:
                if key not in self.api_data:
                    context['missing_keys'].append(key)

        return context

# Create your views here.
@method_decorator(csrf_exempt, name='dispatch')
class SubmitData(View):

    def post(self, request):
        return submit_data(request)
