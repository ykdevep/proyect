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

db.define_table('centro',
    Field('nombre', 'string', default='', label=T('Nombre del centro')),
    Field('nivel_educativo', 'string', default='', label=T('Nivel Educativo')),
    Field('direccion', 'string', default='', label=T('Dirección')),
    format='%(nombre)s')

db.centro._singular = T("Centro")
db.centro._plural = T("Centros")

db.centro.nivel_educativo.requires = IS_IN_SET({'Presscolar': T('Presscolar'), 'Primaria': T('Primaria'), 'Secundaria': T('Secundaria'), 'Media Superior': T('Media Superior'), 'Superior': T('Superior')}, zero=T('Choose one'), error_message=T('Choose one'))
db.centro.nombre.requires = IS_NOT_EMPTY()
db.centro.direccion.requires = IS_NOT_EMPTY()

auth.settings.extra_fields['auth_user']= [
  Field('centro', 'reference centro', label=T('Centro de procedencia'))]

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
auth.settings.actions_disabled=['retrieve_username', 'register','profile']#, 'request_reset_password']

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

'''NEWS_WIDTH = 2340
NEWS_HEIGTH = 600

db.define_table('banner',
   Field('titulo', 'string', label=T('Título')),
   Field('imagen', 'upload', uploadseparate = True, autodelete=True, label=T('Imagen'), comment=T('Image size '+str(NEWS_WIDTH)+'x'+str(NEWS_HEIGTH))),
   Field('publicar_en', 'date', default=request.now, label=T('Publicar en')),
   Field('habilitado', 'boolean', default=True, label=T('Está habilitado')),
   format='%(titulo)s')

db.banner._singular = T('Banner')
db.banner._plural = T('Banners')

db.banner.titulo.requires = IS_NOT_EMPTY()
db.banner.publicar_en.requires = IS_DATE()
db.banner.imagen.requires = [IS_EMPTY_OR(IS_IMAGE(extensions=('png', 'jpg', 'jpeg'), maxsize=(NEWS_WIDTH, NEWS_HEIGTH),  error_message=T('Image news format (png, jpeg, jpg), maxsize '+str(NEWS_WIDTH)+'x'+str(NEWS_HEIGTH))))]

db.banner.imagen.represent = lambda value, register: A(T('Click here for download or url copy'), _href=URL('default', 'download', args=[value]))
'''

db.define_table('nivel_atencional',
    Field('nombre', 'string', default='', label=T('Nombre'), comment=T('Atencion enfocada, Sostenida, Selectiva, Alternada, Dividida')),
    Field('descripcion', 'text', default='', label=T('Descripcion')),
    format='%(nombre)s')

db.nivel_atencional._singular = T('Nivel de atención')
db.nivel_atencional._plural = T('Niveles de atención')

db.nivel_atencional.nombre.requires = IS_NOT_EMPTY()


db.define_table('resultado_general',
    Field('fecha', 'date', default=request.now, label=T('Fecha')),
    Field('nivel_atencional', 'reference nivel_atencional', label=T('Nivel atencional')),
    Field('resultado', 'string', label=T('Resultado')),
    Field('observacion', 'text', default='', label=T('Observaciones')),
    format='%(id)s')

db.resultado_general._singular = T('Observación general')
db.resultado_general._plural = T('Observaciones generales')

db.resultado_general.fecha.requires = IS_DATE()
db.resultado_general.resultado.requires = IS_IN_SET({'Mejor': T('Mejor'), 'Igual': T('Igual'), 'Peor': T('Peor')}, zero=T('Choose one'), error_message=T('Choose one'))
db.resultado_general.observacion.requires = IS_NOT_EMPTY()


db.define_table('ejercicio',
    Field('hora_inicio', 'datetime', default=request.now, label=T('Hora de inicio')),
    Field('hora_fin', 'datetime', default=request.now, label=T('Hora de fin')),
    Field('tiempo_completar', 'double', label=T('Tiempo en completar')),
    Field('nivel_atencional', 'reference nivel_atencional', label=T('Nivel atencional')),
    Field('estudiante', 'reference auth_user', label=T('Estudiante')),
    format='%(id)s')

db.ejercicio._singular = T('Ejercicio')
db.ejercicio._plural = T('Ejercicios')

db.ejercicio.hora_inicio.requires = IS_DATETIME()
db.ejercicio.hora_fin.requires = IS_DATETIME()

db.ejercicio.tiempo_completar.compute = lambda r:r['hora_fin']-r['hora_inicio']


#Control Resultados {id estudiante, id evaluador, id ejercicio, # aciertos, # intrusiones, # omisiones, hora de inicio, hora fin, tiempo ejecucion (lo que se demora desde que empieza hasta que termina), tiempo eficacia}

db.define_table('control_resultado',
    Field('hora_inicio', 'datetime', default=request.now, label=T('Hora de inicio')),
    Field('hora_fin', 'datetime', default=request.now, label=T('Hora de fin')),
    Field('tiempo_ejecucion', 'double', label=T('Tiempo ejecución')),
    Field('tiempo_eficacia', 'double', label=T('Tiempo eficacia')),
    Field('aciertos', 'double', label=T('Número de aciertos')),
    Field('intrusiones', 'double', label=T('Número de intrusiones')),
    Field('omisiones', 'double', label=T('Número de omisiones')),
    Field('ejercicio', 'reference ejercicio', label=T('Ejercicio')),
    Field('estudiante', 'reference auth_user', label=T('Estudiante')),
    Field('evaluador', 'reference auth_user', label=T('Evaluador')),
    format='%(id)s')

db.control_resultado._singular = T('Control de resultado')
db.control_resultado._plural = T('Control de resultados')

db.control_resultado.hora_inicio.requires = IS_DATETIME()
db.control_resultado.hora_fin.requires = IS_DATETIME()

db.control_resultado.tiempo_ejecucion.compute = lambda r:r['hora_fin']-r['hora_inicio']
