from extensions import db
from models import CasillaContenido, Enemigo, Evento, Zona, Npc, PersonajePartida
from logica.combate import iniciar_combate
from logica.eventos import aplicar_efecto_evento
from logica.zonas import aplicar_efecto_zona
from logica.npcs import interactuar_npc
from logica.condiciones_victoria import verificar_condiciones_victoria #importamos

def aplicar_efectos_casilla(personaje, casilla, partida_id):
    contenidos = CasillaContenido.query.filter_by(casillaId=casilla.id).all()
    for contenido in contenidos:
        if contenido.contenidoTipo == 'enemigo':
            enemigo = Enemigo.query.get(contenido.contenidoId)
            iniciar_combate(partida_id, personaje.id, enemigo.id)
        elif contenido.contenidoTipo == 'evento':
            evento = Evento.query.get(contenido.contenidoId)
            aplicar_efecto_evento(personaje, evento, partida_id)
        elif contenido.contenidoTipo == 'zona':
            zona = Zona.query.get(contenido.contenidoId)
            aplicar_efecto_zona(personaje, zona, partida_id)
        elif contenido.contenidoTipo == 'npc':
            npc = Npc.query.get(contenido.contenidoId)
            interactuar_npc(personaje, npc)
    verificar_condiciones_victoria(partida_id, personaje.id)