# -*- coding: utf-8 -*-

# -------------------------------------------------------------------------
# This scaffolding model makes your app work on Google App Engine too
# File is released under public domain and you can use without limitations
# -------------------------------------------------------------------------

if request.global_settings.web2py_version < "2.14.1":
    raise HTTP(500, "Requires web2py 2.13.3 or newer")

# -------------------------------------------------------------------------
# if SSL/HTTPS is properly configured and you want all HTTP requests to
# be redirected to HTTPS, uncomment the line below:
# -------------------------------------------------------------------------
# request.requires_https()

# -------------------------------------------------------------------------
# app configuration made easy. Look inside private/appconfig.ini
# -------------------------------------------------------------------------
from gluon.contrib.appconfig import AppConfig

# -------------------------------------------------------------------------
# once in production, remove reload=True to gain full speed
# -------------------------------------------------------------------------
myconf = AppConfig(reload=True)

if not request.env.web2py_runtime_gae:
    # ---------------------------------------------------------------------
    # if NOT running on Google App Engine use SQLite or other DB
    # ---------------------------------------------------------------------
    db = DAL(myconf.get('db.uri'),
             pool_size=myconf.get('db.pool_size'),
             migrate_enabled=myconf.get('db.migrate'),
             check_reserved=['all'])
else:
    # ---------------------------------------------------------------------
    # connect to Google BigTable (optional 'google:datastore://namespace')
    # ---------------------------------------------------------------------
    db = DAL('google:datastore+ndb')
    # ---------------------------------------------------------------------
    # store sessions and tickets there
    # ---------------------------------------------------------------------
    session.connect(request, response, db=db)
    # ---------------------------------------------------------------------
    # or store session in Memcache, Redis, etc.
    # from gluon.contrib.memdb import MEMDB
    # from google.appengine.api.memcache import Client
    # session.connect(request, response, db = MEMDB(Client()))
    # ---------------------------------------------------------------------

# -------------------------------------------------------------------------
# by default give a view/generic.extension to all actions from localhost
# none otherwise. a pattern can be 'controller/function.extension'
# -------------------------------------------------------------------------
response.generic_patterns = ['*'] if request.is_local else []
# -------------------------------------------------------------------------
# choose a style for forms
# -------------------------------------------------------------------------
response.formstyle = myconf.get('forms.formstyle')  # or 'bootstrap3_stacked' or 'bootstrap2' or other
response.form_label_separator = myconf.get('forms.separator') or ''

# -------------------------------------------------------------------------
# (optional) optimize handling of static files
# -------------------------------------------------------------------------
response.optimize_css = 'concat,minify,inline'
response.optimize_js = 'concat,minify,inline'

# -------------------------------------------------------------------------
# (optional) static assets folder versioning
# -------------------------------------------------------------------------
# response.static_version = '0.0.0'

# -------------------------------------------------------------------------
# Here is sample code if you need for
# - email capabilities
# - authentication (registration, login, logout, ... )
# - authorization (role based authorization)
# - services (xml, csv, json, xmlrpc, jsonrpc, amf, rss)
# - old style crud actions
# (more options discussed in gluon/tools.py)
# -------------------------------------------------------------------------

from gluon.tools import Auth, Service, PluginManager

# host names must be a list of allowed host names (glob syntax allowed)
auth = Auth(db, host_names=myconf.get('host.names'))
service = Service()
plugins = PluginManager()

auth.settings.extra_fields['auth_user']= [
  Field('fecha_nacimiento', 'date', default=request.now, label=T('Fecha de Nacimiento'))]

# -------------------------------------------------------------------------
# create all tables needed by auth if not custom tables
# -------------------------------------------------------------------------
auth.define_tables(username=False, signature=False)

db._common_fields.append(auth.signature)

# -------------------------------------------------------------------------
# configure email
# -------------------------------------------------------------------------
mail = auth.settings.mailer
mail.settings.server = 'logging' if request.is_local else myconf.get('smtp.server')
mail.settings.sender = myconf.get('smtp.sender')
mail.settings.login = myconf.get('smtp.login')
mail.settings.tls = myconf.get('smtp.tls') or False
mail.settings.ssl = myconf.get('smtp.ssl') or False

# all we need is login
auth.settings.actions_disabled=['retrieve_username', 'register']#,'profile']#, 'request_reset_password']

# -------------------------------------------------------------------------
# configure auth policy
# -------------------------------------------------------------------------
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = False
auth.settings.create_user_groups = None

auth.settings.remember_me_form = False

# -------------------------------------------------------------------------
# Define your tables below (or better in another model file) for example
#
# >>> db.define_table('mytable', Field('myfield', 'string'))
#
# Fields can be 'string','text','password','integer','double','boolean'
#       'date','time','datetime','blob','upload', 'reference TABLENAME'
# There is an implicit 'id integer autoincrement' field
# Consult manual for more options, validators, etc.
#
# More API examples for controllers:
#
# >>> db.mytable.insert(myfield='value')
# >>> rows = db(db.mytable.myfield == 'value').select(db.mytable.ALL)
# >>> for row in rows: print row.id, row.myfield
# -------------------------------------------------------------------------

# -------------------------------------------------------------------------
# after defining tables, uncomment below to enable auditing
# -------------------------------------------------------------------------
# auth.enable_record_versioning(db)

tipo_pregunta = {'0': T('Orientación'), '1': T('Dígitos en progresión'), '2': T('Dígitos en regresión'), '3': T('Cubos en progresión'), '4': T('Detección visual'), '5': T('Detección de dígitos'), '6': T('Series sucesivas')}
tipo_diagnostico = {'0': T('Inicial'), '1': T('Atención Enfocada'), '2': T('Atención Sostenida'), '3': T('Atención Selectiva'), '4': T('Atención Alternada'), '5': T('Atención Dividida')}
numero_ensayo = {'0': T('Ensayo #1'), '1': T('Ensayo #2')}


db.define_table('diagnostico',
   Field('titulo', 'string', label=T('Título'), comment=T('Título del diagnóstico')),
   Field('descripcion', 'text', label=T('Descripción'), comment=T('Descripción del diagnóstico')),
   Field('tipo', 'string', label=T('Tipo de diagnóstico'), comment=T('Tipo de cuestionario diagnóstico')),
   Field('tiempo', 'integer', label=T('Tiempo de diagnóstico'), comment=T('Tiempo expresado en minutos del diagnóstico (m) vacío si no necesita tiempo')),
   Field('activo', 'boolean', default=False, label=T('Activo'), comment=T('¿Cuestionario activo? Solo puede habrá uno activado por tipo.')),
   format='%(titulo)s')

db.diagnostico._singular = T('Diagnóstico')
db.diagnostico._plural = T('Diagnósticos')

db.diagnostico.titulo.requires = [IS_NOT_EMPTY(), IS_NOT_IN_DB(db, 'diagnostico.titulo')]
db.diagnostico.descripcion.requires = IS_NOT_EMPTY()
db.diagnostico.tipo.requires = IS_IN_SET(tipo_diagnostico, zero=T('Choose one'), error_message=T('Choose one'))

db.diagnostico.tipo.represent = lambda valor, registro: tipo_diagnostico[valor]
db.diagnostico.tiempo.represent = lambda valor, registro: CAT(valor, ' ',T('minutos'))
db.diagnostico.titulo.represent = lambda value, register: A(value, _title=register.descripcion, **{'_data-toggle': "tooltip", '_data-placement': "right"})

def desactivarDiagnostico(f):
    """
    Desactivar cuestionario diagnóstico activo
    """
    try:
        if f.has_key('activo') and f.has_key('tipo'):
            if f['activo']:
                db((db.diagnostico.id > 0) & (db.diagnostico.tipo == f['tipo'])).update(activo=False)
        return None
    except Exception, e:
        return True

db.diagnostico._before_insert.append(lambda f: desactivarDiagnostico(f))
db.diagnostico._before_update.append(lambda s,f: desactivarDiagnostico(f))


db.define_table('pregunta',
   Field('texto', 'string', label=T('Pregunta'), comment=T('Pregunta')),
   Field('respuesta', 'string', label=T('Respuesta'), comment=T('Respuesta de la pregunta')),
   Field('descripcion', 'string', label=T('Descripción'), comment=T('Descripción de la pregunta')),
   Field('tipo', 'string', label=T('Tipo'), comment=T('Tipo de pregunta')),
   Field('ensayo', 'string', label=T("Ensayo"), comment=T('Número de ensayo')),
   Field('tiempo', 'double', label=T('Tiempo'), default=0.0, comment=T('Tiempo de visualización de la pregunta espresado en segundos (s)')),
   Field('puntos', 'integer',  label=T('Puntos'), default=1, comment=T('Evaluación de la pregunta')),
   Field('diagnostico', 'reference diagnostico', writable=False, readable=False, label=T('Diagnóstico')),
   format='%(id)s')

db.pregunta._singular = T('Pregunta')
db.pregunta._plural = T('Preguntas')

db.pregunta.descripcion.requires = [IS_NOT_EMPTY()]
db.pregunta.texto.requires = [IS_NOT_EMPTY()]
db.pregunta.tiempo.requires = [IS_NOT_EMPTY()]
db.pregunta.puntos.requires = [IS_NOT_EMPTY()]
db.pregunta.tipo.requires = IS_IN_SET(tipo_pregunta, zero=T('Choose one'), error_message=T('Choose one'))
db.pregunta.ensayo.requires = IS_IN_SET(numero_ensayo, zero=T('Choose one'), error_message=T('Choose one'))

db.pregunta.tipo.represent = lambda valor, registro: tipo_pregunta[valor]
db.pregunta.ensayo.represent = lambda valor, registro: numero_ensayo[valor]


db.define_table('respuesta',
   Field('pregunta', 'reference pregunta', label=T('Pregunta'), comment=T('Pregunta')),
   Field('texto', 'text', label=T('Respuesta'), comment=T('Respuesta de la pregunta ')),
   Field('diagnostico', 'reference diagnostico', label=T('Diagnostico'), comment=T('Diagnostico')),
   Field('aciertos', 'integer', label=T('Aciertos'), comment=T('Aciertos de la respuesta')),
   Field('intrusiones', 'integer', label=T('Intruciones'), comment=T('Intrusiones de la respuesta')),
   Field('correcta', 'boolean', default=False, label=T('Correcta'), comment=T('Respuesta correcta')),
   format='%(id)s')
