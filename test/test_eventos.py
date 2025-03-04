import unittest
from models import Evento, PersonajePartida, Npc
from logica.eventos import aplicar_efecto_evento
from extensions import db

class TestEventos(unittest.TestCase):
    def setUp(self):
        # Crear un personaje de prueba y un evento de prueba
        self.personaje = PersonajePartida(vida=100, oro=50, posicion=5, debuffs={})
        self.evento = Evento(modificacionVida=-20, modificacionOro=30, avanceCasillas=-2, debuffEstadistica="fuerzaReducida")
        db.session.add(self.personaje)
        db.session.add(self.evento)
        db.session.commit()

    def test_aplicar_efecto_evento(self):
        aplicar_efecto_evento(self.personaje, self.evento, 1) #1 es el id de la partida de prueba

        self.assertEqual(self.personaje.vida, 80)
        self.assertEqual(self.personaje.oro, 80)
        self.assertEqual(self.personaje.posicion, 3)
        self.assertEqual(self.personaje.debuffs, {"fuerzaReducida": 3})

    def test_aplicar_efecto_evento_npc(self):
        npc = Npc(nombre="Npc de prueba", dialogo="Hola, soy un NPC de prueba")
        db.session.add(npc)
        db.session.flush()
        evento_npc = Evento(npcId=npc.id)
        db.session.add(evento_npc)
        db.session.commit()

        aplicar_efecto_evento(self.personaje, evento_npc, 1)

        #puedes agregar aqui logica para verificar que el dialogo del npc se mostro correctamente

    def tearDown(self):
        db.session.delete(self.personaje)
        db.session.delete(self.evento)
        db.session.commit()

if __name__ == '__main__':
    unittest.main()