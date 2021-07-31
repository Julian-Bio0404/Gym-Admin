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
- Listado de usuarios
- Reservar cupo de sesión de entrenamiento (*training reserve*) (*limite max de 26 debido a la pandemia*)
- Listar reservas de sesión de entrenamiento
- Detalle de la reserva
- Eliminar una reserva
- Crear una cita con fisioterapeuta (appointment)
- Listar citas por fisioterapeuta
- Lista completa de citas fisiterapéuticas 
- Tarea periódica diaria que descuenta un día a las membresías de usuarios y las elimina después de 30 días
- Tarea periódica cada dos horas que elimina citas fisioterapéuticas y reservas vencidas
----

### Skills  
- Python
- Django
- Django REST Framework
- Json Web Token Authentication
- RabbitMQ
- Celery *tarea asíncrona*
- Celery *tareas periódicas*
- Postman *documentación API REST*
- Docker
----

### Documentación 
#### Para correr el proyecto:
- Clone este proyecto con: git clone https://github.com/Julian-Bio0404/Gym-Admin.git
- Construya las imágenes con: docker-compose build 
- Levante los servicios con: docker-compose up
- En otra ventana de consola, corra: docker-compose run --rm celeryworker bash
- Una vez dentro de bash, ejecute: celery -A taskapp worker --loglevel=info,
  es aquí que se imprimirá en consola el Token de verificación de la cuenta después de hacer Sign-up

#### Para ver la documentacion de la API REST y ver cómo hacer request a esta, puede:
- Importar el archivo documentation.postman_collection a su cuenta de Postman, para jugar con ella.
- O visite la documentación en: https://documenter.getpostman.com/view/15752557/TzmCitvq 