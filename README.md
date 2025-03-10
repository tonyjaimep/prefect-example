# Workflow Managers

El propósito de esta práctica es reconocer el propósito de prefect para Python y
utilizar el tutorial adjunto para generar un ejemplo propio. Mi ejemplo
consistirá en un sistema de sincronización de datos de usuarios dummy.

Prefect es un motor de flujos de trabajo de código abierto. Permite orquestar
cargas de trabajo de una manera que reconoce relaciones entre los componentes
del trabajo y genera las secuencias de su ejecución.

# Ejemplo Propio

Para generar un sistema de sincronización de datos de usuarios dummy, se tienen
que obtener los datos, estructurarlos y luego almacenarlos en la base de datos.
Asumo que este tipo de información se debe de sincronizar cada minuto para
brevedad de pruebas.

## Funcionamiento

1. Hace una solicitud a jsonplaceholder para obtener una lista de usuarios.
2. Si la solicitud fue exitosa, le da estructura a la información de cada usuario.
3. Inserta la información estructurada de los usuarios a la base de datos.
4. Corre el flujo cada minuto.

# Demo



https://github.com/user-attachments/assets/a258c309-014d-4b4d-a858-472aab6f0532

