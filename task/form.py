from django import forms
from django.utils.safestring import mark_safe

from task.models import Task
from utils.mixins import StyleFormMixin


class TaskForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Task
        fields = ('title', 'description', 'deadline')

    def __init__(self, *args, **kwargs):
        super(TaskForm, self).__init__(*args, **kwargs)
        self.fields['description'].required = False
        self.fields['deadline'].widget = forms.DateTimeInput(format='%Y-%m-%d %H:%M:%S',
                                                             attrs={'type': 'datetime-local', 'class': 'form-control'})

        # self.fields['deadline'].widget = forms.DateTimeInput(format='%Y-%m-%d %H:%M:%S',
        #                                                      attrs={'class': 'datetimefield form-control'})
