from django import forms
from .models import PerevalAdded, Coords


class PerevalAddedForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(PerevalAddedForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        # coords = Coords.objects.filter(pk=instance.id)
        # print('id = ', instance.id)  #coords.get('latitude'))
        if instance and instance.id:
            self.fields['add_time'].required = False
            self.fields['add_time'].widget.attrs['disabled'] = 'disabled'
            self.fields['users'].required = False
            self.fields['users'].widget.attrs['disabled'] = 'disabled'

    class Meta:
        model = PerevalAdded
        fields = ['users', 'coords', 'add_time', 'beauty_title', 'title', 'other_titles', 'connect',
                  'level_winter', 'level_summer', 'level_autumn', 'level_spring', 'obj_status']
