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

![](../Teorico/Imagenes/conectarSPIs2.png)

---

#### Idea 2: Conectar cada ISP de acceso a un ISP global de transito

![](../Teorico/Imagenes/conectarISPs3.png)
* Cada ISP de Acceso se conecta a un ISP global de transito.

---

#### Idea 3: Es mas conveniente tener ISPs globales de transito que conectan los ISPs de Acceso

![](../Teorico/Imagenes/conectarISPs4.png)

---

Las ISP de acceso son interconectadas a traves de redes ISP nacionales e internacionales de mas alto nivel llamados **ISPs de Capa Superior** o **Globales de Transito**, consiste de enrutadores de alta velocidad interconectados con enlaces de fibra optica de alta velocidad. Estas son ISP que proveen **Servicios de Transito**.

#### ¿Que Conclusiones podemos sacar sobre el diagrama anterior?

Las ISP globales de transito deben estar interconectadas entre si y cada red ISP, ya sea de acceso o de capa superior, es manejada independientemente.

Los ISP globales de transito NO tienen presencia en cada ciudad o region del mundo ¿Y esto que implica? Esto hace que algunas ISP de acceso no se puedan conectar directamente con los ISP globales. La solucion: En una region puede haber un **ISP Regional** al cual se conectan los ISP de acceso en la region.

![](../Teorico/Imagenes/conectarISP5.png)

---

#### ¿Cuales son las consecuencias de la solucion anterior?

* Cada ISP regional se conecta con ISPs globales de transito.
* Los ISPs de acceso pagan al ISP regional al cual se conectan, y cada ISP regional paga al ISP global de transito al cual se conecta.
* En algunos lugares un ISP regional puede cubrir un pais entero y ese ISP regional se conectan otros ISP regionales.

---

Por ultimo tenemos las redes proovedoras de contenido (como Google, Facebook, Microsoft, etc.). Estas pueden ejecturae su propia red, para traer servicios, y contenido cerca de los usuarios.

#### ¿Porque se usan estas redes?

Se usan para reducir pagos a redes de transito global y para tener control sobre como sus servicios son entregaods a los usuarios.

#### ¿A que redes se conectan las redes proveedoras de contenido?

Se conectan a ISP regionales e ISP de acceso. Podrian llegar a usar un ISP de transito si no le queda otra.

![](../Teorico/Imagenes/conectarISPs6.png)

---

Si pensamos a la internet como una red formada por niveles que forman una jerarquia, tendriamos la siguiente jerarquia:

![](../Teorico/Imagenes/jerarquiaInternet.png)
* "*Tier-1*" **ISPs Comerciales** (redes globales de transito) no tienen una cobertura nacional e internacional.
* **Redes Proovedoras de Contenido**.
* En el medio ISP regionales.
* Y al ultimo las ISPs de Acceso.

---

## Internet de las Cosas (IoT) (*Internet of Things*)

#### ¿Que es el IoT?

Es la extencion del internet desde las "Computadoras" a "Objetos", sin la necesidad de una persona en el medio.
<br> IoT nace de paradigmas de redes anterior y los abarca:
* ***Machine-to-Machine*** (**M2M**): Redes para conectar maquinas entre si.
* ***Radio-Frequency ID*** (**RFID**): Se usa para chips embebidos en productos que hacen saltar alarmas.
* ***Wireless Sensor Networks*** (**WSN**): Sensores distribuidos conectados a una red.
* ***Mobile Ad-Hoc Networks*** (**MANET**): Se usa para redes de autos que se comunican entre ellos.
* **Domotica** (***Smart home***): Dispositivos hogareños conectados en red.
* **Vehiculos** (***Vehicle to everything***).
* **Industria** (**Industria 4.0**): Se conectan dispositivos en sistemas productivos, en una fabrica.
* ***Cyber-physical systems*** (**CPS**)

La IoT mezcla todo junto y lo logra gracias a la combinacion de tecnicas de computacion de las siguientes areas:
* Procesamiento de tiempo real,
* *Ambient intelligence*,
* IA,
* *Machine learning*: *Includes deep learning*,
* *Big Data*,
* Computo en la nube.

---

## Redes de Area Amplia (WANs) (*Wide Area Networks*)

Una **Red de Area Amplia** (**WAN**) cubre un area geografica grande, tipicamente un pais o hasta un continente.

