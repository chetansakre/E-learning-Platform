from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import User
from .models import Author



class AuthorBackend(BaseBackend):
    def authenticate(self, request, name=None, password=None):
        try:
            author = Author.objects.get(name=name)
            # Here, you would implement your own logic for authentication
            # For demonstration, let's say you check a password
            if author.password == password:
                return author
            else:
                return None
        except Author.DoesNotExist:
            return None        