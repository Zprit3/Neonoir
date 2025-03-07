from flask import Flask, render_template, url_for
from dotenv import load_dotenv
from extensions import db, csrf
from rutas import jugadores, personajes, casillas, tarjetas, partidas, enemigos, eventos, zonas, npc, objetos_victoria, casillas_estados, personajes_partidas, tiendas
from admin import init_app
from csrf import csrf_bp
from flask_socketio import SocketIO
import sockets, os

socketio = SocketIO()

def create_app():
    load_dotenv()
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///neonoir.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

    db.init_app(app)
    csrf.init_app(app)
    init_app(app)
    app.register_blueprint(csrf_bp)
    app.register_blueprint(jugadores.jugadores_bp, url_prefix='/jugadores')
    app.register_blueprint(personajes.personajes_bp, url_prefix='/personajes')
    app.register_blueprint(casillas.casillas_bp, url_prefix='/casillas')
    app.register_blueprint(tarjetas.tarjetas_bp, url_prefix='/tarjetas')
    app.register_blueprint(partidas.partidas_bp, url_prefix='/partidas')
    app.register_blueprint(enemigos.enemigos_bp, url_prefix='/enemigos')
    app.register_blueprint(eventos.eventos_bp, url_prefix='/eventos')
    app.register_blueprint(zonas.zonas_bp, url_prefix='/zonas')
    app.register_blueprint(npc.npc_bp, url_prefix='/npc')
    app.register_blueprint(objetos_victoria.objetos_victoria_bp, url_prefix='/objetos_victoria')
    app.register_blueprint(casillas_estados.casillas_estados_bp, url_prefix='/casillas_estados')
    app.register_blueprint(personajes_partidas.personajes_partidas_bp, url_prefix='/personajes_partidas')
    app.register_blueprint(tiendas.tiendas_bp, url_prefix='/tiendas')

    @app.route('/')
    def index():
        return render_template('index.html')

    with app.app_context():
        db.create_all()

    socketio.init_app(app)
    sockets.configure_sockets(socketio)

    return app

if __name__ == '__main__':
    app = create_app()
    socketio.run(app, debug=True)