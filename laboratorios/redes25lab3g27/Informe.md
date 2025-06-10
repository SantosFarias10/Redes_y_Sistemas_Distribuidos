# Protocolos de Resolucion de conflictos en congestion y flujo

## Resumen

Este trabajo se centró en el análisis y diseño de protocolos para manejar problemas de congestión y flujo en redes de comunicación, utilizando el simulador **OMNeT++**. En la **primera parte**, se extendió un modelo básico de colas para incorporar limitaciones de capacidad (tasa de transferencia y tamaño de buffers), evaluando su impacto en el tráfico de red bajo dos casos de estudio. Los resultados mostraron que, aunque ambos casos presentaban un cuello de botella, la ubicación del problema variaba: en el primer caso, la limitación estaba en la cola del receptor, mientras que en el segundo, era la cola intermedia la que generaba congestión. Esto permitió diferenciar entre problemas de control de flujo (receptor) y control de congestión (red). 

En la **segunda parte**, se diseñó e implementó un sistema de control de congestión y de flujo. El algoritmo de control de flujo se implementó mediante un protocolo de feedback entre los módulos `TransportTx` y `TransportRx`, utilizando paquetes especializados (FeedbackPkt) para regular la tasa de transmisión según el estado del buffer del receptor. 
El algoritmo de congestión fue implementado agregando datos relevantes a los feedbacks que ya se tenían para ser posteriormente evaluándolos en el nodo emisor.

---

## Introduccion 

En las redes de comunicación, el manejo eficiente del tráfico de datos es fundamental para garantizar un rendimiento óptimo y evitar pérdidas de información. Dos conceptos clave en este ámbito son el control de flujo y el control de congestión. Mientras que el primero regula la velocidad de transmisión entre emisor y receptor para evitar desbordamientos, el segundo gestiona el tráfico en la red para prevenir colapsos por saturación.

En la primera parte del trabajo, se evaluaron dos casos de estudio con configuraciones distintas de tasas de transferencia y buffers limitados:

* Caso 1:

    - Configuracion:
        
        * `NodeTx --> Queue`: 1 Mbps, delay = 100us.

        * `Queue --> NodeRx`: 1 Mbps, delay = 100us.

        * `Queue --> Sink`: 0.5 Mbps.

    - Problema:

        * Con `GenerationInterval = 0.1`, el cuello de botella se produce entre NodeRx y Sink, ya que la tasa de procesamiento del receptor es insuficiente para manejar el flujo de entrada.

        * Con `GenerationInterval = 1`, el tráfico se normaliza y no hay saturación.

Caso de `GenerationInterval = 0.1`:

![Caso 1: GenerationInterval = 0,1](../redes25lab3g27/registroDeFotos/Caso_1_GenerationInterval=0,1.png)

Caso de `GenerationInterval = 1`:

![Caso 1: GenerationInterval = 1](../redes25lab3g27/registroDeFotos/caso_de_estudio_1_generationInterval=1.png)

* Caso 2:

    - Configuracion:

        * `NodeTx --> Queue`: 1 Mbps, delay = 100us.

        * `Queue --> NodeRx`: 0.5 Mbps, delay = 100us.

        * `Queue --> Sink`: 1 Mbps.

    - Problema:

        * Con `GenerationInterval = 0.1`, la congestión ocurre en la Queue, ya que recibe paquetes más rápido de lo que puede enviarlos a NodeRx.

        * Con `GenerationInterval = 1`, el flujo se equilibra y no hay pérdidas.

Caso de `GenerationInterval = 0,1`:

![Caso 2: GenerationInterval = 0,1](../redes25lab3g27/registroDeFotos/GenerationInteral=0,1.png)

Caso de `GenerationInterval = 1`:

![Caso 2: GenerationInterval = 1](../redes25lab3g27/registroDeFotos/caso_de_estudio_2_generationInterval=1.png)

Estos dos casos nos permitieron diferenciar entre:

* **Control de Flujo**: Regula la velocidad de transmisión para evitar que el receptor se sature (problema en NodeRx).

* **Control de Congestion**: Gestiona el tráfico en la red para evitar colapsos en nodos intermedios (problema en la Queue/Nube).

Para abordar los problemas de control de flujo y congestión en redes de comunicación, se utilizó una **metodología basada en simulación discreta**, la cual permite modelar sistemas dinámicos mediante eventos discretos en el tiempo. Esta técnica es especialmente útil para analizar el comportamiento de redes bajo diferentes condiciones sin necesidad de implementaciones físicas costosas.

El estudio se realizó en **OMNeT++**, un entorno de simulación modular y orientado a eventos discretos, ideal para redes de comunicación.

### Tarea de Analisis:

Para medir los problemas de flujo y congestion que tenia la simulacion inicialmente, realizamos unos graficos dentro de OMNeT++ para poder analizar dichos problemas desde otro punto de vista.
Una vez realizados los graficos cambiando el GenerationInterval entre 0.1, 0.15, 0.16, 0.5 y 1 para ver la diferencia de comportamiento de las graficas, podemos observar como ambas graficas cuando se hacen con el mismo GenerationInterval se ven casi identicas, lo unico que cambia es que queue se llena de paquetes en cada caso, en el caso 1, la cola del NodeRx, en el caso2, la de la nube. A pesar de eso, la perdida de paquetes (linea roja) tiene el mismo comportamiento en ambos casos.
Se puede observar en ambas graficas que dependiendo del GenerationInterval las colas se llenaran mas o menos rapido o directamente no se van a llenar, en nuestro caso en particular, el limite lo encontramos aproximadamente en el GenerationInterval=0.16, los valores mas chicos siempre generaran que se llene la cola y haya perdida de paquetes y los valores mayores haran que nunca se llene la cola.
Analizando el codigo del Network.ned podemos ver que el limitante de ambos casos es el datarate y el delay de envio de paquetes en las colas respectivas de cada caso, al tener un datarate de envio de la mitad del tamanio del datarate de las otros canales, la cola se termina llenando con el pasar del tiempo a menos que el GenerationInterval se vuelva tan chico que haga que no sea posible que los otros canales puedan bombardear de paquetes a las queue lentas.

---

## Metodo

### Algoritmo de control de Flujo:

El algoritmo de control de flujo que implementamos fue hecho en `TransportTx` y `TransportRx`, funciona mediante un mecanismo que permite al receptor (TransportRx) informar al transitor (TransportTx), mediante un Feedback, sobre el estado de su cola. Tiene como objetivo evitar la saturacion y perdida de paquetes.
##### ¿Como detectamos el estado de la cola?

Cuando `TransportTx` recibe un paquete, verifica el nivel de ocupacion de su buffer:

* Si la cola esta al **50%** de su capacidad, envia un Feedback indicando que el transmisor debe reducir un poco su tasa de envio.

![Cola al 50%](../redes25lab3g27/registroDeFotos/Cola_al_50.png)

* Si la cola esta al **75%** de su capacidad, envia un Feedback indicando que el transmisor debe reducir un poco su tasa de envio de paquetes.

* Si la cola esta **llena**, descarta el paquete entrante y registra la perdida.
#### Implementación
Dentro de Rx, se producen paquetes de feedback de tipo ASK_SLOW, constante definida al principio del archivo del mismo; también implementada en Tx.
Estos paquetes son enviados hacia Tx, quién al encontrar paquetes de tipo ASK_SLOW, realiza las comparaciones previas.

### Algoritmo de control de Congestion:

Cada cierta cantidad de paquetes enviados, el emisor revisará si hubo alguno para los cuales no haya recibido un ack. En caso positivo, reducirá de forma drástica su velocidad de envío.

Debido a que los paquetes de feedback ya informan el estado del buffer receptor, la única opción es que se estén perdiendo paquetes en la nube.

##### TransportTx (Tx)

Tx es el nodo encargado de enviar paquetes y guardar aquellos que sean relevantes de forma que pueda aprovechar su espacio lo mejor posible. La ejecución dentro de él funciona en el siguiente orden:

1. Recibe un paquete

2. Guarda una copia

3. Envía el paquete

4. Envía 10 paquetes más.

5. Por cada paquete del cual reciba un ack, eliminará su copia.

6. Cada CHECK_INTERVAL¹ paquetes enviados, buscará dentro de la primera mitad para los cuales no haya recibido un ack y lo reenviará.

7. En caso de tener que reenviar algún paquete, reducirá su velocidad de envio.

1: Constante con valor numérico entero, definida al inicio de TransportTx.cc
##### TransportRx (Rx)

Rx es el nodo encargado de verificar la integridad de paquetes enviados al sink/cliente. Para esto:

1. Guarda en un array, una lista de los últimos paquetes enviados al cliente.

2. Envía feedbacks por cada paquete enviado al cliente, dentro de los cuales se informan tanto la situación de su buffer como la identificación del paquete recibido.
     En caso de necesitar que Tx reduzca su taza de envío, asignará el tipo ASK_SLOW a estos paquetes. Caso contrario, solamente serán de tipo INFO_PACKET

3. Si vuelve a recibir un paquete ya enviado, no lo enviará de nuevo al cliente debido a que ya estaba registrado. 

---
## Resultados
CASO1 muestra una distribución más concentrada en las colas de recepción (2 de 4 nodos)  CASO2 distribuye más uniformemente entre colas generales y de recepción
#### Interpretación de las Diferencias

1. **Control de Flujo solo (CASO1)**:
    - Los paquetes tienden a acumularse en las colas de recepción
    - Esto sugiere que el sistema prioriza la entrega pero puede tener problemas para procesar los paquetes recibidos
    - Posible congestión en los nodos receptores        
2. **Control de Flujo + Congestión (CASO2)**:
    - La carga se distribuye más entre colas generales
    - El sistema parece balancear mejor la carga entre diferentes tipos de colas
    - Las colas generales adicionales probablemente actúan como buffers para manejar picos de tráfico
    - Menos concentración en las colas de recepción sugiere mejor manejo de la congestión
#### Conclusión
La implementación adicional de control de congestión en CASO2 logra:
- Mejor distribución de la carga de paquetes
- Menos acumulación en puntos específicos (colas de recepción)
- Mayor capacidad para manejar variaciones en el tráfico
---

## Discusión

### Colas saturadas

Al llenarse una cola, se enviará un paquete de feedback con un tipo especial, el cual hará que el emisor reduzca la frecuencia con la que envía paquetes.

### Reenvío de paquetes

Los módulos que envian y reciben paquetes de distintos tipos (Ya sean de datos o Feedback), reenviaban los paquetes de feedback. Fue solucionado agregando un identificador numérico a los paquetes de feedback.

### Documentación cMessage

La documentación de esta clase estaba en una [página](https://doc.omnetpp.org/omnetpp/api/classomnetpp_1_1cMessage.html) distinta al [manual](https://doc.omnetpp.org/omnetpp/manual/) que fue tanto el otorgado como el que aparecía como principal en la mayoría de búsquedas en internet.

### Network.ned

Si bien esta extensión de archivo es usada comunmente alrededor de aquellos archivos cuyo contenido sea relacionado a networks, su lenguaje es específico de omnet++.

Debido a esta característica, leer, entender y aprender cómo modificarlo llevó más tiempo de lo esperado.

### Múltiples envíos por una misma línea

Al necesitar compartir información entre los módulos emisores y receptores, se generaron conflictos debido a que se estaban intenndo enviar o reenviar, ya sean paquetes de feedback o de datos, a través de un mismo canal.

El problema venía debido a que se utilizan dos mensajes de distinto tipo y al llegar un mensaje solo se verificaba si uno de esos dos tipos se agendaba; produciendo que se intenten enviar dos paquetes de distinto tipo por una misma línea, al mismo tiempo.

### endServiceEvent message

Este mensaje es enviado por los objetos (principalmente queues) a sí mismos para "agendar" el envío de un paquete al pasar un tiempo determinado.

Su implementación consiste en: 

* Crear un cMessage con endServiceEvent como identificador.

* Si la cola está vacía y recibe un paquete, se mete el paquete en la cola y agenda un endServiceEvent.

* Cuando llega el tiempo en el que fue agendado el mensaje, el objeto se envía el paquete a sí mismo.

* Busca el primer paquete que encuentra en la cola y lo envía (Si la cola está vacía, no hace nada).

* Agenda un nuevo endServiceEvent.

### Dup

Los paquetes tienen un método de duplicado que permite guardar una copia de estos. No obstante, esta copia también recibe un cambio en su "ownership" cuando el paquete original (del cual se obtuvo la copia) es enviado.

Este problema evita que la copia pueda ser tanto borrada como reenviada, por lo que este método debe utilizarse no para guardar una copia, si no, que al momento de ser enviada. 

Ej: `pktCopy = (pkt->dup);` generará errores al intentar ejecutar `send(pktCopy)` en caso de que `pkt` ya haya sido enviado. En su lugar se tendrá que realizar `pktCopy = pkt;` y luego `send(pktCopy->dup)`

---

## Referencias

### IAs usadas

ChatGPT:

- Utilizado para averigüar si ciertas ideas eran posibles.
	 Ejemplos: Agregar encabezados (Hacer una copia de un objeto y "mapearla" a un hijo, cosa no posible nativamente en C++)
- Averigüar sobre ownership, qué es y si es conveniente utilizarlo
- Propiedades nativas de C++: ¿Tiene diccionarios? ¿Existe la función max? ¿Cómo iterar dentro de sus diccionarios? ¿Cómo encontrar la primera función dentro de uno?

DeepSeek:
- Debido a la falta de tiempo, se le pidió un análisis de la comparativa de los resultados de los gráficos.

---

## Preguntas

### ¿Que diferencia se observa entre el caso 1 y 2?

* **Caso 1**: Al cambiar el `GenerationInterval` de **0,1** a **1** en `Network.NodeTX.gen.GenerationInterval` en el `omnetpp.ini`:

`GenerationInterval = 0,1`: La velocidad en la que `NodeRx` procesa es demasiada lenta. Esto causa que se **genere un cuello de botella** entre `NodeRx` y el `Sink`, ya que a medida que que van llegando paquetes a la `Network`, `NodeRx` va a tardar en procesar los paquetes y enviarselos `Sink`.

`GenerationInterval = 1`: La velocidad en la que `NodeRx` procesa es lo suficientemente normal, para que cuando lleguen paquetes, `NodeRx`los procese lo suficientemente rapido para enviarlos a `Sink` sin que se ***Genere cuello de botella*.

* **Caso 2**: Al cambiar el `GenerationInterval` de **0,1** a **1** en `Network.NodeTX.gen.GenerationInterval` en el `omnetpp.ini`:

`GenerationInterval = 0,1`: La generacion de paquetes en `NodeTx` es muy rapido. Esto provoca que los paquetes lleguen a la `Network` mas rapido de lo que este puede enviarselo al `NoteRx`, **Generando un cuello de botella** entre `NodeTx` y la `Network`, o sea, la `Queue` se satura porque su capacidad de envio es menor que la tasa de llegada de paquetes.

`GenerationInterval = 1`: Al generar los paquetes mas lentamente, la tasa de llegada a `NodeRx` disminuye, permitiendo que este procese y envie los paquetes a `Sink` sin acumularlos en la `Network`, por lo tanto **NO se genera cuello de botella**

---

### Investigacion de Control de Flujo y Congestion

#### ¿Qué es el control de Flujo?

Control de flujo se refiere un conjunto de procedimientos utilizados para gestionar la velocidad a la que se transmiten los datos entre los nodos.

#### ¿Para qué sirve?

Es fundamental para mantener el equilibrio en la velocidad de transmisión de datos entre un emisor y un receptor, evitando un posible desbordamiento de datos si el emisor transmite datos a mayor vleocidad que lo que el receptor puede procesar. Se puede mejorar significativamente el rendimiento de la red, reducir la transmisión y aumentar la eficiencia al evitar la perdida de datos.

#### ¿Qué es la congestión?

Se define como un estado de los sistemas ocurrido en la capa de red, en las situaciones en las que el trafico de mensajes aumenta tanto que ralentiza los tiempos de respuestas normales de una red determinada. Otro efecto negativo es, por ejemplo, que el retraso de respuesta impacta directamente sobre el rendimiento; llegando en las peores circunstancias a ser el causante de una retransmisión.

#### ¿Qué es el control congestion?

Es la metodología encargada del manejo de entrada de paquetes de datos en la red, por lo que constribuye a utilizar la infraestructura compartida de red, al tiempo que impide una congestión de red en el sistema. Se enfoca en ordenar el sistema de tráfico, compartiendo el ancho de banda entre los clientes que lo requiera.

---

### ¿Cómo se comporta su algoritmo de control de flujo y congestión?

### Algoritmo de control de Flujo
El algoritmo de control de flujo fue implementado en `TransportTx` y `TransportRx`.
Se los llamarán Tx y Rx por simplicidad,
Este mecanismo mantiene un flujo de información desde Rx hacia Tx, informando constantemente la situación del buffer de Rx, para que así Tx pueda decidir qué hacer.
#### ¿Como se detecta el estado de la cola?
Cuando Tx recibe un paquete, compara el estado de su buffer con el de Rx y:
- Si la capacidad restante del buffer de Rx es mayor a la de Tx, no cambia nada.

* Si la cola de Rx **50%** de su capacidad, reduce levemente su tasa de envío. Esta ralentización se mantendrá hasta que Rx tenga una capacidad disponible mayor al 50%.
![Cola al 50%](../redes25lab3g27/registroDeFotos/Cola_al_50.png)

* Si el buffer de Rx está al **75%** de su capacidad, Tx disminuirá drásticamente su velocidad de envío.
### Algoritmo de control de congestión
Cada cierta cantidad de paquetes enviados, el emisor revisará si hubo alguno para los cuales no haya recibido un ack. En caso positivo, reducirá de forma drástica su velocidad de envío.

Debido a que los paquetes de feedback ya informan el estado del buffer receptor, la única opción es que se estén perdiendo paquetes en la nube.

---

### ¿Funciona para el caso de estudio 1 y 2 por igual? ¿Por qué?

No funciona para el caso de estudio 1 y 2 por igual, ya que fueron pensados e implementados para resolver los problemas por separados.



