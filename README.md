# ExpenseFlow

**Una aplicación web responsiva para seguimiento de gastos personales, presupuestos y metas de ahorro.**

ExpenseFlow es una herramienta de gestión financiera basada en Django diseñada para ayudar a los usuarios a registrar sus gastos, establecer y monitorear presupuestos, y mantener metas de ahorro. La aplicación presenta un panel intuitivo, análisis completos con gráficos y un diseño responsivo que funciona perfectamente en dispositivos de escritorio y móviles.

## Características

- **Seguimiento de Gastos**: Registra y categoriza gastos con descripciones detalladas y seguimiento de fechas
- **Análisis del Panel**: Visualiza resumen de gastos, tendencias mensuales y desglose por categorías de un vistazo
- **Gestión de Presupuesto**: Establece presupuestos mensuales y monitorea el progreso de gastos contra tus objetivos
- **Metas de Ahorro**: Crea y rastrea objetivos de ahorro personalizados con visualización de progreso
- **Organización por Categorías**: Organiza gastos en categorías predefinidas (Alimentación, Transporte, Entretenimiento, Juegos, Suscripciones, Educación, Otros)
- **Filtrado y Búsqueda**: Encuentra gastos por categoría, rango de fechas o palabras clave
- **Gráficos y Visualizaciones**: Gráficos interactivos que muestran distribución de gastos y tendencias históricas
- **Autenticación de Usuarios**: Sistema seguro de registro e inicio de sesión
- **Diseño Responsivo**: Funciona perfectamente en dispositivos de escritorio, tablet y móviles
- **Tema Oscuro/Claro**: Cambia entre modos oscuro y claro para una visualización cómoda
- **Persistencia de Datos**: Base de datos SQLite para almacenamiento confiable de datos locales

## Stack Tecnológico

- **Backend**: Django 5.1.1
- **Base de Datos**: SQLite3
- **Frontend**: HTML5, CSS3, JavaScript
- **Estilos**: Bootstrap 5, CSS personalizado
- **Iconos**: Material Design Icons (MDI)
- **Gráficos**: Chart.js
- **Lenguaje**: Python 3

## Instalación

### Requisitos Previos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)
- git

### Instrucciones de Configuración

1. **Clonar el repositorio**
   ```bash
   git clone https://github.com/Rxdrig/expense-flow.git
   cd expenseflow
   ```

2. **Crear y activar un entorno virtual**
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate
   
   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

4. **Ejecutar migraciones de la base de datos**
   ```bash
   python manage.py migrate
   ```

5. **Crear una cuenta de superusuario (opcional, para acceso de administrador)**
   ```bash
   python manage.py createsuperuser
   ```

6. **Iniciar el servidor de desarrollo**
   ```bash
   python manage.py runserver
   ```

7. **Acceder a la aplicación**
   - Abre tu navegador y ve a `http://localhost:8000`
   - Crea una nueva cuenta o inicia sesión con tus credenciales
   - ¡Comienza a registrar tus gastos!

## Credenciales de Prueba

Para probar rápidamente la aplicación, puedes usar las siguientes credenciales:

- **Usuario**: `demo`
- **Contraseña**: `Demo1234`


## Uso

### Panel de Control
- Visualiza tu gasto total, gastos mensuales y metas de ahorro activas
- Ve transacciones recientes y estado del presupuesto
- Acceso rápido a todas las características principales

### Gastos
- **Agregar Gasto**: Crea nuevos registros de gastos con categoría, monto y descripción
- **Ver Todo**: Examina todos los gastos con opciones de filtrado
- **Filtrar**: Filtra por categoría, mes o busca por palabras clave
- **Editar/Eliminar**: Modifica o elimina registros de gastos

### Presupuesto
- Establece tu límite de presupuesto mensual
- Realiza seguimiento del progreso de gastos contra tu presupuesto
- Indicador visual que muestra el porcentaje de utilización del presupuesto

### Metas de Ahorro
- Crea múltiples objetivos de ahorro con nombres y montos personalizados
- Establece fechas límite opcionales
- Agrega emojis personalizados a tus metas
- Monitorea el progreso hacia cada meta

### Análisis
- **Por Categoría**: Gráfico circular que muestra la distribución de gastos entre categorías
- **Tendencias Mensuales**: Gráfico de barras que muestra patrones de gasto en los últimos 12 meses
- Descarga o imprime reportes para mantener registros

### Tema
- Haz clic en el botón de alternancia de tema para cambiar entre modos oscuro y claro
- Tu preferencia se guarda automáticamente

## Estructura del Proyecto

```
expenseflow/
├── core/                      # Aplicación principal de Django
│   ├── models.py             # Modelos de BD (Gasto, Presupuesto, MetaAhorro)
│   ├── views.py              # Lógica de vistas y manejadores de solicitudes
│   ├── forms.py              # Formularios de Django para entrada de usuario
│   ├── urls.py               # Enrutamiento de URLs
│   ├── admin.py              # Configuración del admin de Django
│   ├── migrations/           # Archivos de migración de BD
│   ├── templates/            # Plantillas HTML
│   │   ├── core/
│   │   ├── registration/
│   │   └── expenses/
│   └── static/               # Archivos estáticos (CSS, JavaScript, imágenes)
│       └── core/assets/
├── miweb/                     # Configuración del proyecto Django
│   ├── settings.py           # Configuración del proyecto
│   ├── urls.py               # Configuración principal de URLs
│   ├── wsgi.py               # Configuración WSGI
│   └── asgi.py               # Configuración ASGI
├── manage.py                 # Script de gestión de Django
├── db.sqlite3                # Base de datos local
├── requirements.txt          # Dependencias del proyecto
└── README.md                 # Este archivo
```

## Modelos

### Gasto (Expense)
- Usuario (ForeignKey a User)
- Título (CharField)
- Monto (DecimalField)
- Categoría (CharField con opciones)
- Fecha (DateField)
- Descripción (TextField, opcional)
- Marcas de tiempo Creado/Actualizado

### Presupuesto (Budget)
- Usuario (OneToOneField a User)
- Presupuesto Mensual (DecimalField)
- Marcas de tiempo Creado/Actualizado

### Meta de Ahorro (SavingGoal)
- Usuario (ForeignKey a User)
- Título (CharField)
- Monto Objetivo (DecimalField)
- Monto Ahorrado (DecimalField)
- Fecha Límite (DateField, opcional)
- Emoji (CharField)
- Marcas de tiempo Creado/Actualizado

## Autenticación

- Registro de usuario con validación de correo
- Autenticación segura de contraseñas
- Login/logout basado en sesiones
- Login requerido para todas las características financieras
- Gestión de perfil en el menú de navegación

## Endpoints API

La aplicación incluye endpoints API JSON para datos de gráficos:

- `GET /api/expenses-by-category/` - Devuelve datos de gastos agrupados por categoría
- `GET /api/expenses-by-month/` - Devuelve datos de gastos de los últimos 12 meses

## Contribución

Este es un proyecto personal de portafolio. Para mejoras o reportes de errores, siéntete libre de abrir un issue o enviar un pull request.

## Licencia

Este proyecto se proporciona tal cual para fines educativos y de portafolio.

## Autor

Creado como un proyecto personal de portafolio para demostrar capacidades de desarrollo web full-stack con Django, diseño responsivo y gestión de datos financieros.

## Mejoras Futuras


- Soporte multi-moneda
- Sincronización en la nube
- Reportes y análisis avanzados


---

**Nota**: Este es un proyecto de demostración que utiliza SQLite para almacenamiento local. Para uso en producción, considera usar PostgreSQL o MySQL, implementar manejo adecuado de errores, agregar pruebas completas y seguir las mejores prácticas de seguridad de Django. 
