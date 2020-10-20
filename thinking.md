#Priority Guides

##Vistas
###Vista Principal
**Texto:** Intervalo ascendente/descendente.
**Acción:** Seleccionar entre intervalo ascendente o descendente.
**Texto:** Intervalos.
**Cuadrícula:**
- **Imagen:** Intervalo.
- **Texto:** Nombre del intervalo.
- **Acción:** Seleccionar un intervalo.

###Vista del Intervalo
**Acción:** Retroceder.
**Texto: **Nombre de intervalo.
**Texto:** Ejemplo de intervalo.
**Texto:** Información de las canciones del intervalo (título, enlace, favoritos).
**Texto:** Favoritos.
**Acción:** Activar para filtrar por favoritos.
##Decisiones
Hemos decidido simplificar al máximo la interfaz de usuario, enfocándonos en un diseño lo más minimalista posible. 

Para ello, en la pantalla principal se introducirá un selector que permite cambiar entre intervalos ascendentes o descendentes. Además, para la selección del intervalo optaremos por una vista en cuadrícula de iconos. Cada icono hace referencia a uno de los doce intervalos disponibles en la API. 

Una vez seleccionado un intervalo, se nos presentará una pantalla con toda la información acerca del mismo. En ella veremos: el nombre del intervalo, un ejemplo de dos notas cuya distancia sea la del intervalo, una vista en árbol que nos permitirá mostrar la información sobre las canciones del intervalo seleccionado (título, enlace y favoritos) y un selector que nos permite filtrar únicamente aquellas canciones que estén en favoritos. 
Esta pantalla cuenta además con un botón de retroceso que nos permite volver a la pantalla principal.
