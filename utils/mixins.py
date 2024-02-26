from django.http import Http404


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name == 'is_active' or field_name == 'is_published':
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'


class CreatorRequiredMixin:
    """Проверка на авторство текущего пользователя"""

    def get_object(self, queryset=None):
        object = super().get_object()
        if not object.user == self.request.user:
            raise Http404
        return object
