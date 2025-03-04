from flask import Flask
from extensions import db
from rutas import jugadores, personajes, casillas, tarjetas, partidas, enemigos, eventos, zonas, npcs, objetosVictoria, casillasEstados, personajesPartidas

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///neonoir.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    # Registrar Blueprints
    app.register_blueprint(jugadores.jugadoresBp, url_prefix='/jugadores')
    app.register_blueprint(personajes.personajesBp, url_prefix='/personajes')
    app.register_blueprint(casillas.casillasBp, url_prefix='/casillas')
    app.register_blueprint(tarjetas.tarjetasBp, url_prefix='/tarjetas')
    app.register_blueprint(partidas.partidasBp, url_prefix='/partidas')
    app.register_blueprint(enemigos.enemigosBp, url_prefix='/enemigos')
    app.register_blueprint(eventos.eventosBp, url_prefix='/eventos')
    app.register_blueprint(zonas.zonasBp, url_prefix='/zonas')
    app.register_blueprint(npcs.npcsBp, url_prefix='/npcs')
    app.register_blueprint(objetosVictoria.objetosVictoriaBp, url_prefix='/objetosVictoria')
    app.register_blueprint(casillasEstados.casillasEstadosBp, url_prefix='/casillasEstados')
    app.register_blueprint(personajesPartidas.personajesPartidasBp, url_prefix='/personajesPartidas')

    with app.app_context():
        db.create_all()

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)