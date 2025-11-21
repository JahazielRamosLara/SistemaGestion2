"""
Middleware para requerir autenticación en toda la aplicación.
Guarda este archivo como: core/middleware.py (o el nombre de tu app/middleware.py)
"""

from django.shortcuts import redirect
from django.urls import reverse
from django.conf import settings

class LoginRequiredMiddleware:
    """
    Middleware que requiere que el usuario esté autenticado para acceder a cualquier vista,
    excepto las URLs especificadas en EXEMPT_URLS.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        
        # URLs que NO requieren autenticación (puedes agregar más)
        self.exempt_urls = [
            '/login/',
            '/logout/',
            '/admin/login/',
            '/admin/logout/',
            '/accounts/login/',
            '/accounts/logout/',
        ]
        
        # También puedes obtenerlas de settings.py si lo prefieres:
        # self.exempt_urls = getattr(settings, 'LOGIN_EXEMPT_URLS', [])

    def __call__(self, request):
        # Obtener la URL actual
        path = request.path_info
        
        # Verificar si el usuario está autenticado
        if not request.user.is_authenticated:
            # Verificar si la URL está en la lista de exentos
            if not any(path.startswith(url) for url in self.exempt_urls):
                # Si no está autenticado y la URL no está exenta, redirigir a login
                login_url = settings.LOGIN_URL or '/login/'
                return redirect(f'{login_url}?next={path}')
        
        # Continuar con el request normalmente
        response = self.get_response(request)
        return response



# VERSIÓN ALTERNATIVA (Más flexible)

import re
from django.shortcuts import redirect
from django.conf import settings

class LoginRequiredMiddleware:
    """
    Middleware que requiere autenticación con soporte para regex en URLs exentas.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        
        # URLs exentas usando regex
        self.exempt_patterns = [
            r'^/login/',
            r'^/logout/',
            r'^/admin/login/',
            r'^/admin/logout/',
            r'^/accounts/login/',
            r'^/accounts/logout/',
            r'^/static/',  # Archivos estáticos
            r'^/media/',   # Archivos de media
        ]
        
        # Compilar los patrones
        self.exempt_regex = [re.compile(pattern) for pattern in self.exempt_patterns]

    def __call__(self, request):
        path = request.path_info
        
        if not request.user.is_authenticated:
            # Verificar si la URL coincide con algún patrón exento
            if not any(pattern.match(path) for pattern in self.exempt_regex):
                login_url = settings.LOGIN_URL or '/login/'
                return redirect(f'{login_url}?next={path}')
        
        response = self.get_response(request)
        return response