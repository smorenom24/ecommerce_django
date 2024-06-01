# Ecommerce Django Project

## Descripción

Este es un proyecto de comercio electrónico desarrollado con Django. El proyecto incluye varias características como gestión de productos, carritos de compras, autenticación de usuarios, y más. Aunque el proyecto está en desarrollo, proporciona una base sólida para un sitio de ecommerce funcional.

## Características

- Gestión de productos (crear, leer, actualizar, eliminar)
- Autenticación de usuarios (registro, inicio de sesión, cierre de sesión)
- Carrito de compras
- Sistema de categorías
- Cupones de descuentos

## Tecnologías utilizadas

- [Django](https://www.djangoproject.com/) - El framework principal utilizado para el desarrollo backend.
- [Bootstrap](https://getbootstrap.com/) - Para el diseño frontend.
- [SQLite](https://www.sqlite.org/index.html) - Base de datos por defecto (puede ser cambiada a PostgreSQL o MySQL).

## Instalación

### Requisitos previos

- Python 3.x
- pip (gestor de paquetes de Python)
- Virtualenv (opcional, pero recomendado)

### Pasos de instalación

1. Clona el repositorio:
   ```bash
   git clone https://github.com/tuusuario/ecommerce_django.git
   cd ecommerce_django
2. Crea y activa un entorno virtual:
    ```bash
    python -m venv venv
    source venv/bin/activate  # En Windows usa `venv\Scripts\activate`
3. Instala las dependencias: 
    ```bash
   pip install -r requirements.txt
4. Configura las variables de entorno:
Crea un archivo .env en el directorio principal del proyecto y define las variables pedidas en el archivo .envexample


5. Realiza las migraciones de la base de datos:
   ```bash
   python manage.py migrate
6. Inicia el servidor de desarrollo:
    ```bash
   python manage.py runserver

7. Accede a la aplicación en tu navegador:
    ```bash
       http://127.0.0.1:8000

## Uso

### Autenticación de usuario
* Registro: http://127.0.0.1:8000/accounts/register
* Login: http://127.0.0.1:8000/accounts/login

### Productos
* Home: http://127.0.0.1:8000/
* Producto en particular: http://127.0.0.1:8000/product/<slug>/
* Crear, leer, actualizar y eliminar productos desde el panel de administración.

### Carrito de compras:
* Ver carrito: http://127.0.0.1:8000/accounts/cart/

## To-Do

- [ ] Implementar pasarela de pago
- [ ] Mejorar el diseño frontend
- [ ] Corregir los vínculos para navegación en sitio
 
## Licencia

Este proyecto está bajo la licencia MIT. Consulta el archivo LICENSE para más detalles.

## Agradecimientos

* Plantilla HTML y diseño proporcionados por Canal de "YouTube Coding for All | Newton School". Agradecimientos especiales por sus recursos y tutoriales.

## Contacto

* Autor: Sebastián Moreno Martínez
* Email: sebastianmoreno@ug.uchile.cl
* Github: @smorenom24