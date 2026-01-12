# Introduccion

Libro: Kurose, J. F. and Ross, K. W. Computer Networking - A Top Down Approach. 7th Edition, Pearson, 2017.

## Redes de Computadoras

#### ¿Que tipos de dispositivos queremos interconectar por medio de redes?

Los dispositivos que queremos interconectar por medio de redes reciben el nombre de ***Hosts*** o **Sistemas Finales**, estos son dispositivos de cómputo.

---

#### ¿Que es una **Red de Computadoras**?

Una **Red de Computadoras** es un conjunto de sistemas finales interconectados.
<br>¿Que significa que dos computadoras estan interconectadas? Dos computadoras (o *Hosts* interconectados) estan **Interconectadas** si se pueden intercambiar informacion.
<br>¿De que manera puede hacerse la interconexion? La conexion puede hacerse por **Medio de Transmisión** como cables de cobre, fibra optica, microondas, etc. El intercambio de informacion entre *hosts* se hace por medio de **Señales** que viajan en los medios de transmisión.

---

#### ¿Que servicios o usos proporcionan las redes de computadoras?

* **Compartir Recursos**:
  * Recursos de hardware como impresoras, almacenamiento, etc.
  * Informacion como datos, archivos, etc.
* Usarlas como medio de comunicacion entre personas.
* **Socializar**: Como el uso de las redes sociales.
* **Trabajo Colaborativo**: Como la creacion de documentos entre varias personas en distintas localizaciones.
* **Comercio Electronico**
* **Entretenimiento**: como juegos, o distribucion de contenidos de TV por suscripcion (IPTV).

---

Existen distintos **Tipos de Redes de Computadoras**. Las redes de computadoras pueden venir en varios tamaños, formas y cumplir distintos propositos.

#### ¿Que hacer para que los *hosts* de varias redes de distinto tipo puedan compunicarse entre si?

Varias redes de computadoras pueden ser Interconectadas entre si para formar redes mas grandes y mas complejas, como por ejemplo el **Internet** es la red de redes mas grande.

---

### Tipos de Redes

![](../Teorico/Imagenes/tipoDeRedes.png)
* ***Personal Area Network***: Bluetooth.
* ***Local Area Network*** (**LAN**): WiFi.
* ***Metropolitan Area Network*** (**MAN**): 3G, 4G, 5G.
* ***Wide Area Network*** (**WAN**).
* ***The Internet***.

Todos estos tipos de redes, mientras mas chica es la distancia se trabaja con la estrategia de **Difusion** de Informacion, es decir, se envia la informacion a todos los *hosts* de la red. Es util en distancias cortas.
<br> En distancias mas largas se trabaja con enlaces de **Punto a Punto**. En este caso se envia la informacion a un solo *host* de la red.

---

### Sistemas Operativos de Red

![](../Teorico/Imagenes/sistemasOperativosDeRed.png)

---

### Aplicaciones de Red

![](../Teorico/Imagenes/aplicacionesDeRed.png)

Como vimos las redes de computadoras se usan para proveer disintos servicios, para proveer estos servicios se crean **Aplicaciones de Red**. Lo que hacen estas aplicaciones es acceder a los servicios de red, ofrecidos por el **SO de Red**, que se encarga de hacer uso de los protocolos. Se usan **APIs y Middlewares** para programarlas.

---

### Interredes

#### ¿Como comunicamos personas pertenecientes a redes diferentes?

Para comunicar a personas con diferentes tipos de redes, usamos las **Interredes**. La Interred es un conjunto de redes interconectadas.
<br> **Puerta de Enlace** son el punto o interfaz de una red que permite salir hacia afuera de la red y conectarse con una red cercana o de jerarquia superior. El ejemplo mas claro de una Interred es el **Internet**.

---

### Dispositivos IoT

Los Dispositivos IoT (*Internet of Things*) pueden:
* **Intercambiar Datos** con otros dispositivos y aplicaciones interconectados.
* **Recolectar Datos** de otros dispositivos y **Procesar los Datos** localmente, o enviarlos a servidores centralizados para procesarlos.
* **Realizar Tareas** localmente y otras tareas dentro de la infraestructura de la red basadas en restricciones temporales y de espacio como la memoria, capacidad de procesamiento, velocidad de comunicación y plazos, etc.

---

## Internet

La **Internet** es una red de redes que interconectan varias redes entre si, esta formada por billones de dispositivos de computacion conectados entre si. En la internet se ejecutan las **Aplicaciones de Red**. Para el envio y la recepcion de mensajes entre sistemas finales se usan **Protocolos**.

---

### Estructura de la Internet

Los *Hosts* acceden a la internet a traves de **Proveedores de Servicios de Internet de Acceso** (ISPs de Acceso) (***Internet Service Provider Access***).

---

#### ¿que tipos de ISP de acceso existe?

* Uso de **ISP Residenciales** (compañias de cables, telefonicas, fibra a la casa, etc.).
* Uso de **ISP Empresarial** (da acceso a sus empleados).
* Uso de **ISPs Universitaria** (da acceso a docentes, estudiantes y personal).
* Celualres (4G, 5G).
* **ISPs que Proveen Acceso a WiFi** (en aeropuertos, hoteles, restaurantes, parques, etc.).

---

#### ¿Como hacer para que dos *hosts* que estan conectados a diferentes ISPs de acceso puedan enviarse paquetes entre si?

Los ISPs de Acceso deben estar interconectados xd.
<br>Pero dados miles de ISPs de acceso, ¿Como los conectamos entre si?

![](../Teorico/Imagenes/conectarISPs1.png)
* En la figura, la los *access net* son una red diferente.

---

#### Idea 1: Conectar cada ISP de acceso a todo otro ISP de acceso.

![]()