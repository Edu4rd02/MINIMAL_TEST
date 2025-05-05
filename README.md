# 🛒 MINIMAL - Tienda en Línea Básica

**MINIMAL** es un sistema de tienda en línea básico, diseñado para gestionar productos y ofrecer una interfaz tanto para usuarios como para administradores. Permite mostrar productos a los clientes, añadirlos al carrito y simular una compra. Los administradores pueden gestionar el inventario mediante operaciones CRUD (Crear, Leer, Actualizar y Eliminar), las cuales interactúan con una base de datos que almacena toda la información relacionada con los productos.

Este proyecto fue construido con **Flask** como infraestructura web, siguiendo un diseño minimalista y enfocado en una experiencia de usuario intuitiva. Se utilizaron herramientas de perfilado para identificar cuellos de botella y optimizar el rendimiento general del sistema, como `cProfile` y `memory_profiler`.

---

## ⚙️ Instalación y configuración

Sigue los siguientes pasos para clonar el repositorio, crear un entorno virtual, instalar las dependencias y ejecutar el sistema:

```bash
# Clonar el repositorio
git clone https://github.com/Edu4rd02/MINIMAL_TEST.git
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
