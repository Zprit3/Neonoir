from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from extensions import db
from models import Jugador, Personaje, Casilla, Tarjeta, Partida, Enemigo, Evento, Zona, Npc, ObjetoVictoria, CasillaEstado, PersonajePartida, PersonajeTarjetas, Tablero, CasillaContenido, Tienda
from wtforms.fields import PasswordField
from flask_admin.form import SecureForm

class JugadorView(ModelView):
    form_overrides = dict(contrasena=PasswordField)
    form_base_class = SecureForm

    def on_model_change(self, form, model, is_created):
        if form.contrasena.data:
            model.set_password(form.contrasena.data)

admin = Admin(name='Admin Panel', template_mode='bootstrap3')

admin.add_view(JugadorView(Jugador, db.session))
admin.add_view(ModelView(Personaje, db.session))
admin.add_view(ModelView(Casilla, db.session))
admin.add_view(ModelView(Tarjeta, db.session))
admin.add_view(ModelView(Partida, db.session))
admin.add_view(ModelView(Enemigo, db.session))
admin.add_view(ModelView(Evento, db.session))
admin.add_view(ModelView(Zona, db.session))
admin.add_view(ModelView(Npc, db.session))
admin.add_view(ModelView(ObjetoVictoria, db.session))
admin.add_view(ModelView(CasillaEstado, db.session))
admin.add_view(ModelView(PersonajePartida, db.session))
admin.add_view(ModelView(PersonajeTarjetas, db.session))
admin.add_view(ModelView(Tablero, db.session))
admin.add_view(ModelView(CasillaContenido, db.session))
admin.add_view(ModelView(Tienda, db.session))

def init_app(app):
    admin.init_app(app)