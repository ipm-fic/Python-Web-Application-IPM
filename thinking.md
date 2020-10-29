# Priority Guides
## Vistas
### Vista Principal (Ventana Principal)
**Texto:** Intervalo ascendente/descendente

**Acción:** Seleccionar entre intervalo ascendente o descendente

**Texto:** Intervalos

**Botones:** Nombre del intervalo

**Acción:** Ver intervalo
### Vista del Intervalo (Ventanas de Respuesta del Servidor)
**Texto:** Nombre de intervalo

**Texto:** Ejemplo de intervalo

**Texto:** Información sobre las canciones del intervalo (título, url, favoritos)

**Texto:** Favoritos

**Acción:** Filtrar por favoritos
## Decisiones
Hemos decidido simplificar al máximo la interfaz de usuario, enfocándonos en un diseño lo más minimalista posible.

Para ello, en la pantalla principal se implementará un filtro selector que permite realizar la búsqueda con intervalo ascendente o descendente. 

Además, para la selección del intervalo optaremos por la utilización de botones. Cada botón hace referencia a uno de los doce intervalos disponibles en la API.

Se usan tanto botones como switches por su sencillez de interacción y claridad a la hora de seleccionar información en el programa.

Una vez seleccionado un intervalo, se nos presentará una nueva ventana con toda la información acerca del mismo. En ella se muestra: el nombre del intervalo seleccionado, un ejemplo de dos notas cuya distancia sea la del intervalo, la información sobre las canciones del intervalo seleccionado (título, url y favoritos) y un filtro para seleccionar únicamente aquellas canciones que estén en favoritos. 

El objetivo de usar una nueva ventana para cada intervalo es permitir la posibilidad de visualizar varios intervalos de manera simultánea.

