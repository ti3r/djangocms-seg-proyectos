from django.forms import ModelForm
from seg_proyectos.models import EntradaHorasDetalle, EntradaHoras


class EntradaHorasForm(ModelForm):
    class Meta:
        model = EntradaHoras
        fields = '__all__'
        #exclude = ['usuario'] #Se obtiene del usuario login
        #widgets = {
        #    'fecha': DateInput(),
        #    'valor': NumberInput(),
        #}

    def is_valid(self):
        return self.is_bound and self.required_fields_for_calculation()

    def required_fields_for_calculation(self):
        ent = self.fields['entrada']
        return False
