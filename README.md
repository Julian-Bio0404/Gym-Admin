# Gym-Admin
REST API de Gym-Admin. Una aplicacion que permite crear cuentas de usuarios de un gimnasio, crear membresias y hacer reservas para entrenamientos y citas con fisioterapeutas.

----
### Features
- Inscripción de usuarios asíncronamente
- Verificación de cuenta
- Inicio de sesión 
- Ver detalle de un usuario
- Actualización parcial o completa de datos de usuario
- Actualización parcial o completa de perfil de usaurio
- Actualización de contraseña 
- Activación de membresia
- Listado de usaurios
- Reservar cupo de sesión de entrenamiento (*training reserve*) (*limite max de 26 debido a la pandemia*)
- Listar reservas de sesión de entrenamiento
- Detalle de la reserva
- Eliminar una reserva
- Crear una cita con fisioterapeuta (appointment)
- Listar citas por fisioterapeuta
- Lista completa de citas fisiterapéuticas 
- Tarea periódica diaria que descuenta un día a las membresías de usuarios
- Tarea periódica cada dos horas que elimina citas fisioterapéuticas y reservas vencidas
----

### Skills  
- Python
- Django
- Django REST Framework
- Jason Web Token Authentication
- RabbitMQ
- Celery *tarea asíncrona*
- Celery *tareas periódicas*
- Postman *documentación API REST*
----

### Documentación 
#### Para correr el proyecto:
- Clone este proyecto
- Cree un ambiente virtual donde alojará el proyecto
- Diríjase a la raíz del proyecto e instale los requerimientos con pip install -r requirements.txt
- Instale en su máquina erlang-OPT==23.3 y rabbitmq-server==3.8.19
- Corra py manage.py runserver 

#### Para ver la documentacion de la API REST y ver cómo hacer request a esta, puede:
- Importar el archivo documentation.postman_collection a su cuenta de Postman, para jugar con ella.
- O visite la documentación en: https://documenter.getpostman.com/view/15752557/TzmCitvq 