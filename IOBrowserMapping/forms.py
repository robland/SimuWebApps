from django.forms import ModelForm

from IOBrowserMapping.models import Rule, E3D_OBJECTS, Variable



class RuleForm(ModelForm):
    class Meta:
        model = Rule
        fields = '__all__'



