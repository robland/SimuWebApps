from django.forms import ModelForm

from IOBrowserMapping.models import Rule


class RuleForm(ModelForm):
    class Meta:
        model = Rule
        fields = '__all__'



