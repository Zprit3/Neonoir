# Neonoir: Juego de Tablero con API REST y Tiempo Real

Neonoir es un juego de tablero desarrollado en Python utilizando Flask, SQLAlchemy, SocketIO y otras tecnologías. El juego cuenta con una API RESTful para gestionar datos y SocketIO para la comunicación en tiempo real, brindando una experiencia interactiva a los jugadores.

## Descripción del Proyecto

Neonoir es un juego de tablero donde los jugadores compiten por alcanzar ciertos objetivos de victoria. El juego incluye:

- **Tablero dinámico:** El tablero se genera aleatoriamente al inicio de cada partida.
- **Personajes:** Cada jugador controla un personaje con características únicas.
- **Casillas:** El tablero está compuesto por casillas que tienen diferentes efectos al caer en ellas (eventos, combate, zonas).
- **Combate:** Los jugadores pueden enfrentarse a enemigos en combates.
- **Eventos:** Las casillas pueden activar eventos que modifican el estado del juego.
- **Zonas:** Las casillas pueden pertenecer a zonas que modifican el estado del juego.
- **NPCs:** Hay personajes no jugables (NPCs) con los que se puede interactuar.
- **Tiendas:** Los jugadores pueden visitar tiendas y comprar tarjetas.
- **Objetos de victoria:** Los jugadores deben conseguir estos objetos para poder ganar.
- **Condiciones de Victoria:** El juego tiene diferentes condiciones para ganar una partida.
- **Tiempo Real:** Actualización del juego en tiempo real a través de SocketIO.
- **Administrador:** Se puede utilizar un panel de administrador con flask-admin para gestionar los datos del juego.

## Funcionamiento de la API REST

La API REST de Neonoir permite interactuar con el juego mediante solicitudes HTTP. Aquí se describen las principales rutas y sus funciones:

### Rutas Generales

- **`GET /csrf_token`**: Devuelve un token CSRF para proteger las rutas.

### Rutas de Entidades

- **Casillas (`/rutas/casillas`)**:
  - `GET /casillas`: Obtener todas las casillas.
  - `GET /casillas/<id>`: Obtener una casilla específica.
  - `POST /casillas`: Crear una nueva casilla.
  - `PUT /casillas/<id>`: Actualizar una casilla.
  - `DELETE /casillas/<id>`: Eliminar una casilla.
- **Enemigos (`/rutas/enemigos`)**:
  - `GET /enemigos`: Obtener todos los enemigos.
  - `GET /enemigos/<id>`: Obtener un enemigo específico.
  - `POST /enemigos`: Crear un nuevo enemigo.
  - `PUT /enemigos/<id>`: Actualizar un enemigo.
  - `DELETE /enemigos/<id>`: Eliminar un enemigo.
  - `POST /enemigos/<id>/combatir`: Permite que un personaje combata a un enemigo
- **Eventos (`/rutas/eventos`)**:
  - `GET /eventos`: Obtener todos los eventos.
  - `GET /eventos/<id>`: Obtener un evento específico.
  - `POST /eventos`: Crear un nuevo evento.
  - `PUT /eventos/<id>`: Actualizar un evento.
  - `DELETE /eventos/<id>`: Eliminar un evento.
- **Jugadores (`/rutas/jugadores`)**:
  - `GET /jugadores`: Obtener todos los jugadores.
  - `GET /jugadores/<id>`: Obtener un jugador específico.
  - `POST /jugadores`: Crear un nuevo jugador.
  - `PUT /jugadores/<id>`: Actualizar un jugador.
  - `DELETE /jugadores/<id>`: Eliminar un jugador.
- **NPCs (`/rutas/npc`)**:
  - `GET /npcs`: Obtener todos los NPCs.
  - `GET /npcs/<id>`: Obtener un NPC específico.
  - `POST /npcs`: Crear un nuevo NPC.
  - `PUT /npcs/<id>`: Actualizar un NPC.
  - `DELETE /npcs/<id>`: Eliminar un NPC.
- **Objetos de Victoria (`/rutas/objetos_victoria`)**:
  - `GET /objetos`: Obtener todos los objetos de victoria.
  - `GET /objetos/<id>`: Obtener un objeto de victoria específico.
  - `POST /objetos`: Crear un nuevo objeto de victoria.
  - `PUT /objetos/<id>`: Actualizar un objeto de victoria.
  - `DELETE /objetos/<id>`: Eliminar un objeto de victoria.
- **Partidas (`/rutas/partidas`)**:
  - `GET /partidas`: Obtener todas las partidas.
  - `GET /partidas/<id>`: Obtener una partida específica.
  - `POST /partidas`: Crear una nueva partida.
  - `PUT /partidas/<id>`: Actualizar una partida.
  - `DELETE /partidas/<id>`: Eliminar una partida.
- **Personajes (`/rutas/personajes`)**:
  - `GET /personajes`: Obtener todos los personajes.
  - `GET /personajes/<id>`: Obtener un personaje específico.
  - `POST /personajes`: Crear un nuevo personaje.
  - `PUT /personajes/<id>`: Actualizar un personaje.
  - `DELETE /personajes/<id>`: Eliminar un personaje.
- **Personajes en Partidas (`/rutas/personajes_partidas`)**:
  - `GET /personajes_partidas`: Obtener todos los personajes en partidas.
  - `GET /personajes_partidas/<id>`: Obtener el estado de un personaje específico en una partida.
  - `POST /personajes_partidas`: Crear un nuevo estado de personaje en una partida.
  - `PUT /personajes_partidas/<id>`: Actualizar el estado de un personaje en una partida.
  - `DELETE /personajes_partidas/<id>`: Eliminar el estado de un personaje en una partida.
- **Tarjetas (`/rutas/tarjetas`)**:
  - `GET /tarjetas`: Obtener todas las tarjetas.
  - `GET /tarjetas/<id>`: Obtener una tarjeta específica.
  - `POST /tarjetas`: Crear una nueva tarjeta.
  - `PUT /tarjetas/<id>`: Actualizar una tarjeta.
  - `DELETE /tarjetas/<id>`: Eliminar una tarjeta.
- **Tiendas (`/rutas/tiendas`)**:
  - `GET /tiendas`: Obtener todas las tiendas.
  - `GET /tiendas/<id>`: Obtener una tienda específica.
  - `POST /tiendas`: Crear una nueva tienda.
  - `PUT /tiendas/<id>`: Actualizar una tienda.
  - `DELETE /tiendas/<id>`: Eliminar una tienda.
  - `POST /tiendas/<id>/comprar/<id_tarjeta>`: Permite a un jugador comprar una tarjeta en una tienda.
- **Zonas (`/rutas/zonas`)**:
  - `GET /zonas`: Obtener todas las zonas.
  - `GET /zonas/<id>`: Obtener una zona específica.
  - `POST /zonas`: Crear una nueva zona.
  - `PUT /zonas/<id>`: Actualizar una zona.
  - `DELETE /zonas/<id>`: Eliminar una zona.
- **Casillas estados (`/rutas/casillas_estados`)**
  - `GET /casillas_estados`: Obtener todas las casillas estados.
  - `GET /casillas_estados/<id>`: Obtener una casilla estado especifica.
  - `POST /casillas_estados`: Crear una nueva casilla estado.
  - `PUT /casillas_estados/<id>`: Actualizar una casilla estado.
  - `DELETE /casillas_estados/<id>`: Eliminar una casilla estado.

**NOTA:** Las rutas se describen con un ejemplo, pero tienen la misma estructura.

## Variables de entorno

- `FLASK_ENV`: define si esta en produccion o desarrollo.
- `SECRET_KEY`: clave para el uso de flask y sus funciones de seguridad.

## Ejecución del Proyecto

1.  **Clonar el repositorio:**

    ```bash
    git clone <URL_DEL_REPOSITORIO>
    cd Neonoir
    ```

2.  **Crear y activar el entorno virtual:**

    ```bash
    python3 -m venv .venv
    source .venv/bin/activate  # En Linux/macOS
    .venv\Scripts\activate  # En Windows
    ```

3.  **Instalar las dependencias:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Inicializar la base de datos (opcional):**

    ```bash
    python scripts/init_casillas.py
    python scripts/init_enemigos.py
    python scripts/init_eventos.py
    python scripts/init_jugadores.py
    python scripts/init_objetos_victoria.py
    python scripts/init_personajes.py
    python scripts/init_tiendas.py
    python scripts/init_zonas.py
    # (Ejecutar el resto de los scripts init que se hayan implementado)
    ```

5.  **Ejecutar la aplicación:**

    ```bash
    flask run
    ```

6.  **Utilizar el panel de administrador**
    - Ir a la ruta `http://127.0.0.1:5000/admin`

## Pruebas

Para ejecutar las pruebas unitarias, dirígete a la carpeta `tests` y ejecuta:

    python test_eventos.py

## Estructura del Proyecto

```bash
El proyecto está organizado en las siguientes carpetas y archivos:

Neonoir/
├── .gitignore            # Archivo para ignorar archivos y carpetas en Git
├── .env                  # Archivo para variables de entorno
├── app.py                # Punto de entrada principal de la aplicación Flask
├── extensions.py         # Inicialización de extensiones de Flask (db, csrf)
├── models.py             # Definición de los modelos de la base de datos
├── sockets.py            # Lógica de SocketIO para comunicación en tiempo real
├── admin.py              # Configuración de Flask-Admin
├── csrf.py               # Configuración del blueprint para CSRF
├── requirements.txt      # Lista de dependencias del proyecto
├── instance/             # Carpeta donde se guarda la base de datos (neonoir.db)
│   └── neonoir.db        # Base de datos SQLite
├── logica/               # Lógica de negocio del juego
│   ├── __init__.py       # Archivo de inicialización de la carpeta
│   ├── casillas.py       # Lógica para el manejo de casillas
│   ├── combate.py        # Lógica para el sistema de combate
│   ├── condiciones_victoria.py # Lógica para verificar condiciones de victoria
│   ├── dados.py          # Lógica para lanzar dados (no aparece en los archivos, pero se menciona en combate.py, se debe agregar)
│   ├── eventos.py        # Lógica para aplicar efectos de eventos
│   ├── npcs.py           # Lógica para la interacción con NPCs (No aparece en los archivos)
│   ├── tablero.py        # Lógica para la generación del tablero de juego
│   └── zonas.py          # Lógica para aplicar efectos de zonas
├── rutas/                # Definición de las rutas de la API REST
│   ├── __init__.py       # Archivo de inicialización de la carpeta
│   ├── casillas.py       # Rutas para casillas
│   ├── enemigos.py       # Rutas para manejar enemigos
│   ├── eventos.py        # Rutas para manejar eventos (no aparece en los archivos)
│   ├── jugadores.py      # Rutas para manejar jugadores
│   ├── npc.py            # Rutas para manejar npc (no aparece en los archivos)
│   ├── objetos_victoria.py # Rutas para manejar objetos de victoria(no aparece en los archivos)
│   ├── partidas.py       # Rutas para manejar partidas (no aparece en los archivos)
│   ├── personajes.py     # Rutas para manejar personajes
│   ├── personajes_partidas.py # Rutas para manejar personajes en las partidas
│   ├── tarjetas.py       # Rutas para manejar tarjetas(no aparece en los archivos)
│   └── tiendas.py        # Rutas para manejar tiendas
│   └── zonas.py          # Rutas para manejar zonas(no aparece en los archivos)
│   └── casillas_estados.py # Rutas para manejar casillas en las partidas.
├── scripts/              # Scripts para inicializar datos en la base de datos
│   ├── __init__.py       # Archivo de inicialización de la carpeta
│   ├── init_casillas.py      # Script para inicializar la tabla Casillas
│   ├── init_enemigos.py # Script para inicializar la tabla Enemigos
│   ├── init_eventos.py       # Script para inicializar la tabla Eventos
│   ├── init_jugadores.py    # Script para inicializar la tabla Jugadores
│   ├── init_npcs.py          # Script para inicializar la tabla NPCs (no aparece en los archivos)
│   ├── init_objetos_victoria.py # Script para inicializar la tabla ObjetosVictoria
│   ├── init_personajes.py   # Script para inicializar la tabla Personajes
│   ├── init_tarjetas.py      # Script para inicializar la tabla Tarjetas(no aparece en los archivos)
│   ├── init_tiendas.py       # Script para inicializar la tabla Tiendas (no aparece en los archivos)
│   └── init_zonas.py         # Script para inicializar la tabla Zonas
└── tests/ # Carpeta para tests
    └── test_eventos.py # Archivo para realizar test a los eventos.
└── .venv/ # Carpeta de entorno virtual
└── templates/ # Carpeta de templates
    └── index.html # archivo de ejemplo para utilizar los templates
```
