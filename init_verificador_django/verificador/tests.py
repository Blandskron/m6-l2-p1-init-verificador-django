from django.test import TestCase
from django.urls import reverse, resolve
from django.http import HttpResponse

class VerificadorViewsTests(TestCase):
    
    def test_hola_view_status_code(self):
        """
        Valida que la vista simple 'hola' responda con código de estado 200.
        """
        response = self.client.get('/hola/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Hola mundo (sin HTML/template). Proyecto OK", response.content)

    def test_home_view_status_code_and_template(self):
        """
        Valida que la vista principal 'home' responda con 200 y use la plantilla home.html.
        """
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'verificador/home.html')
        self.assertContains(response, "Proyecto Django Inicializado y Verificado")

    def test_url_namespace_resolving(self):
        """
        Valida que el manejo de espacios de nombres (Namespaces) funcione correctamente
        al hacer reversión de URLs del módulo 'verificador'.
        """
        home_url = reverse('verificador:home')
        hola_url = reverse('verificador:hola')
        
        self.assertEqual(home_url, '/')
        self.assertEqual(hola_url, '/hola/')
        
        # Validar resoluciones de ruta
        self.assertEqual(resolve('/').view_name, 'verificador:home')
        self.assertEqual(resolve('/hola/').view_name, 'verificador:hola')

