# 🛒 MINIMAL - Tienda en Línea Básica

**MINIMAL** es un sistema de tienda en línea básico, diseñado para gestionar productos y ofrecer una interfaz tanto para usuarios como para administradores. Permite mostrar productos a los clientes, añadirlos al carrito y simular una compra. Los administradores pueden gestionar el inventario mediante operaciones CRUD (Crear, Leer, Actualizar y Eliminar), las cuales interactúan con una base de datos que almacena toda la información relacionada con los productos.

Este proyecto fue construido con **Flask** como infraestructura web, siguiendo un diseño minimalista y enfocado en una experiencia de usuario intuitiva. Se utilizaron herramientas de perfilado para identificar cuellos de botella y optimizar el rendimiento general del sistema, como `cProfile` y `memory_profiler`.

---

## ⚙️ Instalación y configuración

Sigue los siguientes pasos para clonar el repositorio, crear un entorno virtual, instalar las dependencias y ejecutar el sistema:

```bash
# Clonar el repositorio
git clone https://github.com/Edu4rd02/MINIMAL_TEST.git

# Dirigete a la dirección principal
cd MINIMAL_TEST

# Crear un entorno virtual
python -m venv venv

# Activar el entorno virtual
# En Windows:
venv\Scripts\activate
# En macOS/Linux:
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```
## 🛠️ Ejecutar el servidor de flask
Este proyecto se encuentra hosteado, pero de igual manera se puede correr el servidor de Flask. 
> ⚠️ **Nota:** El inicio de sesión con Google no funcionará en ejecución local, ya que el proyecto está configurado para un entorno específico en producción.

Para correr el servidor desde la dirección principal ingresa:
```bash
python -m app.main
```

## ✅ Ejecutar pruebas
Para ejecutar las pruebas hechas como parte del examen unidad 4, solo es necesario ejecutar el siguiente comando:

```bash
pytest
```

## 📊 Perfilado del rendimiento
Como parte del examen unidad 5, se usarón herramientas de perfilado como cProfile y memory_profiler, así como sus extensiones visuales como mprof y snakeviz. En dado caso de querer correr estas pruebas solo siga las siguientes indicaciones:

### Usar cProfile (análisis de CPU)
```bash
python -m cProfile -o salida.prof profile_funciones.py
snakeviz salida.prof
```
Esto mostrará de manera gráfica los tiempos de ejecucción de cada función en snakeviz.

### Usar memory_profiler (análisis de uso de memoria)
```bash
mprof run profile_funciones.py
mprof plot
```
Esto generará una gráfica visual del uso de memoria durante la ejecución.