# -*- coding: utf-8 -*-
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
