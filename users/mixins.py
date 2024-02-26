from django.http import Http404


class AuthorRequiredMixin:
    """Проверка на авторство текущего пользователя"""

    def get_object(self, queryset=None):
        object = super().get_object()
        if not object.author == self.request.user:
            raise Http404

        return object
