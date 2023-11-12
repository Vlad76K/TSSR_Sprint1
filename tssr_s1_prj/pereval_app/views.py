from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView, DetailView, UpdateView, ListView
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import PerevalAdded, PerevalImages, Authors, StatusList, Coords
from .serializers import PerevalSerializer, StatusSerializer, PerevalSerializerPatch, CoordsSerializer

""" проверка наличия всех полей в JSON-объекта """
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

""" пример использования APICheckView() """
# def submit_data(request):
#     try:
#         data = json.loads(request.body.decode("utf-8"))
#
#         """ проверим формат JSON на наличие необходимых полей """
#         api_check = APICheckView()
#         api_check.api_data = data
#         its_right = api_check.check_json()
#         if len(its_right.get('missing_keys')) > 0:
#             raise AttributeError(its_right.get('missing_keys'))
#     except AttributeError as err:  # 400 — Bad Request (при нехватке полей);
#         data = {"message": f"Отсутствуют поля:{err}"}
#         return JsonResponse(data, status=400)

""" сохранение данных об объекте (API) """
@method_decorator(csrf_exempt, name='dispatch')
class SubmitData(APIView):
    def post(self, request):
        serializer = PerevalSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

""" вывод информации о текущем статусе объекта """
class PerevalStatusGetAPIView(APIView):
    def get_object(self, pk, HTTP404=None):
        try:
            status_id = PerevalAdded.objects.filter(pk=pk).values('obj_status')
            st_id = status_id[0].get('obj_status')
            return StatusList.objects.filter(pk=st_id).values('id', 'name', 'parent')
        except StatusList.DoesNotExist:
            raise HTTP404

    """ sprint 2 - get """
    def get(self, request, *args, **kwargs):
        snippet = self.get_object(kwargs.get('pk'))
        serializer = StatusSerializer(snippet[0])
        return Response(serializer.data)

""" вывод и обновление информации о текущих координатах объекта """
class PerevalCoordsGetAPIView(APIView):
    def get_object(self, pk, HTTP404=None):
        try:
            return Coords.objects.get(pk=pk)
        except StatusList.DoesNotExist:
            raise HTTP404

    """ sprint 2 - get """
    def get(self, request, *args, **kwargs):
        snippet = self.get_object(kwargs.get('pk'))
        serializer = CoordsSerializer(snippet)
        return Response(serializer.data)

    """ обновление данных об объекте """
    def patch(self, request, *args, **kwargs):
        snippet = self.get_object(kwargs.get('pk'))
        serializer = CoordsSerializer(snippet, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

""" вывод данных о конкретном объекте по его id """
class PerevalGetAPIView(APIView):
    def get_object(self, pk, HTTP404=None):
        try:
            return PerevalAdded.objects.get(pk=pk)
        except PerevalAdded.DoesNotExist:
            raise HTTP404

    def get(self, request, *args, **kwargs):
        snippet = self.get_object(kwargs.get('pk'))
        serializer = PerevalSerializer(snippet)
        return Response(serializer.data)

""" вывод и обновление данных о конкретном объекте, если его статус = new
    координаты обновляются из отдельного представления: PerevalCoordsGetAPIView """
class PerevalPatchAPIView(APIView):
    def get_object(self, pk, HTTP404=None):
        try:
            status_id = PerevalAdded.objects.filter(pk=pk).values('obj_status')
            st_id = status_id[0].get('obj_status')
            if st_id == 0:
                return PerevalAdded.objects.get(pk=pk)
            data = 'Статус записи не позволяет ее менять!'
            raise ValueError(data)
        except PerevalAdded.DoesNotExist:
            raise HTTP404
        except ValueError:
            raise ValueError(data)

    def get(self, request, *args, **kwargs):
        snippet = self.get_object(kwargs.get('pk'))
        serializer = PerevalSerializerPatch(snippet)
        return Response(serializer.data)

    """ обновление данных об объекте """
    def patch(self, request, *args, **kwargs):
        snippet = self.get_object(kwargs.get('pk'))
        serializer = PerevalSerializerPatch(snippet, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

""" вывод всех объектов """
class GetAllObjectsList(generics.ListAPIView):
    serializer_class = PerevalSerializer

    def get_queryset(self):
        return PerevalAdded.objects.all()

""" вывод всех объектов пользователя с определенным email """
class GetObjectsListByUserEmail(generics.ListAPIView):
    serializer_class = PerevalSerializer

    def get_queryset(self):
        user_id = Authors.objects.filter(user_email=self.request.GET.get('user__email')).values('id')
        u_id = user_id[0].get('id')
        return PerevalAdded.objects.filter(users_id=u_id)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
