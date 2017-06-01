# -*- coding: utf-8 -*-
secciones = {'1-) Datos generales y antecedentes médicos': T('1-) Datos generales y antecedentes médicos'), '2-) Orientación': T('2-) Orientación'), '3.1-) Atención y concentración/Dígitos en Regresión': T('3.1-) Atención y concentración/Dígitos en Regresión'), '3.2-) Atención y concentración/Detección Visual': T('3.2-) Atención y concentración/Detección Visual'), '3.3-) Atención y concentración/20-3': T('3.3-) Atención y concentración/20-3'), '4-) Codificación/Memoria verbal': T('4-) Codificación/Memoria verbal'), '5-) Lenguaje': T('5-) Lenguaje'), '5.1-) Lenguaje/Repetición': T('5.1-) Lenguaje/Repetición'), '5.2-) Lenguaje/Comprensión': T('5.2-) Lenguaje/Comprensión'),'5.3-) Lenguaje/Fluidez verbal': T('5.3-) Lenguaje/Fluidez verbal'), '6-) Lectura': T('6-) Lectura'), '7-) Escritura': T('7-) Escritura'), '6.1-) Funciones ejecutivas/Semejanzas': T('6.1-) Funciones ejecutivas/Semejanzas'), '6.2-) Funciones ejecutivas/Cálculo': T('6.2-) Funciones ejecutivas/Cálculo'),'6.3-) Funciones ejecutivas/Secuenciación': T('6.3-) Funciones ejecutivas/Secuenciación'), '7.1-) Funciones de evocación/Memoria verbal espontanea': T('7.1-) Funciones de evocación/Memoria verbal espontanea')}

db.define_table('secciones',
   Field('tipo_pregunta', 'string', label=T('Tipo de pregunta'),  comment=T('Tipo de Pregunta de esta sección')),
   Field('descripcion', 'text', label=T('Descripción'), requires=IS_NOT_EMPTY(), comment=T('Descripción del diagnóstico')),
   Field('tiempo', 'integer', default=0, label=T('Tiempo'), requires=IS_NOT_EMPTY(), comment=T('Tiempo de cada pregunta, 0 no necesita tiempo')),
   Field('puntos', 'integer', default=0, label=T('Puntos'), requires=IS_NOT_EMPTY(), comment=T('Puntos por tipo de pregunta, 0 no tiene puntos')),
   format='%(tipo_pregunta)s')

db.secciones._singular = T('Sección')
db.secciones._plural = T('Secciones')

db.secciones.tipo_pregunta.requires = IS_IN_SET(secciones, zero=T('Choose one'), error_message=T('Choose one'))

tipo_diagnostico = {'0': T('Inicial'), '1': T('Atención Enfocada'), '2': T('Atención Sostenida'), '3': T('Atención Selectiva'), '4': T('Atención Alternada'), '5': T('Atención Dividida')}

db.define_table('diagnostico',
   Field('titulo', 'string', label=T('Título'), comment=T('Título del diagnóstico')),
   Field('descripcion', 'text', label=T('Descripción'), comment=T('Descripción del diagnóstico')),
   Field('tipo', 'string', label=T('Tipo de diagnóstico'), comment=T('Tipo de cuestionario diagnóstico')),
   Field('tiempo', 'integer', label=T('Tiempo de diagnóstico'), comment=T('Tiempo expresado en minutos del diagnóstico (m) vacío si no necesita tiempo')),
   Field('secciones', 'list:reference secciones', label=T("Tipos de preguntas activas"), comment=T("Activar tipos de preguntas por secciones para este cuestionario")),
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

db.diagnostico.secciones.requires = IS_IN_DB(db,'secciones.id','secciones.tipo_pregunta', multiple=True)
db.diagnostico.secciones.widget = SQLFORM.widgets.checkboxes.widget
db.diagnostico.secciones.default = lambda : []

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

db.define_table('antecedentes_medicos',
   Field('enfermedad', 'string', label=T('Enfermedad'), comment=T('Nombre de la enfermedad')),
   format='%(enfermedad)s')

db.antecedentes_medicos.enfermedad.requires = IS_NOT_EMPTY()

db.antecedentes_medicos._singular = T('Antecedente médico')
db.antecedentes_medicos._plural = T('Antecedentes médicos')

tipo_pregunta_orientacion = {'0': T('Día'), '1': T('Mes'), '2': T('Año'), '3': T('Localidad'), '4': T('Ciudad')}

db.define_table('orientacion',
   Field('pregunta', 'text', label=T('Pregunta'), comment=T('Pregunta')),
   Field('respuesta', 'text', label=T('Respuesta'), comment=T('Respuesta de la pregunta')),
   format='%(id)s')

db.orientacion._singular = T('Orientación')
db.orientacion._plural = T('Orientaciones')

db.orientacion.pregunta.requires = IS_NOT_EMPTY()
db.orientacion.respuesta.requires = IS_IN_SET(tipo_pregunta_orientacion, zero=T('Choose one'), error_message=T('Choose one'))

secuencia = {'0': T('Secuencia #1'), '1': T('Secuencia #2')}

db.define_table('digitos_regresion',
   Field('pregunta', 'text', label=T('Pregunta'), comment=T('Pregunta, números separados por guión ejemplo 2-4')),
   Field('respuesta', 'text', label=T('Respuesta'), comment=T('Respuesta de la pregunta, números separados por guión ejemplo 4-2')),
   Field('tiempo', 'integer', label=T('Tiempo'), compute=lambda r:len(r['pregunta'].split('-')), comment=T('Tiempo de la pregunta')),
   Field('secuencia', 'string', label=T('Secuencia'), comment=T('Secuencias de la pregunta')),
   format='%(id)s')

db.digitos_regresion._singular = T('Dígito en regresión')
db.digitos_regresion._plural = T('Dígitos en regresión')

db.digitos_regresion.pregunta.requires = IS_NOT_EMPTY()
db.digitos_regresion.respuesta.requires = IS_NOT_EMPTY()
db.digitos_regresion.secuencia.requires = IS_IN_SET(secuencia, zero=T('Choose one'), error_message=T('Choose one'))

db.define_table('deteccion_visual',
   Field('pregunta', 'upload', autodelete=True, uploadseparate = True, label=T('Pregunta'), comment=T('Suba una imagen para la prueba')),
   Field('respuesta', 'string', compute=lambda r:r['pregunta'], label=T('Respuesta'), comment=T('Respuesta de la pregunta')),
   Field('tiempo', 'integer', label=T('Tiempo'), comment=T('Tiempo de la pregunta')),
   format='%(id)s')

db.digitos_regresion._singular = T('Detección visual')
db.digitos_regresion._plural = T('Detecciones visuales')

db.define_table('memoria_verbal',
   Field('pregunta', 'text', label=T('Pregunta'), comment=T('Serie de palabras separadas por un guión, ejemplo gato-camisa-gallo-mano-fresa')),
   format='%(id)s')

db.memoria_verbal._singular = T('Detección visual')
db.memoria_verbal._plural = T('Detecciones visuales')

db.define_table('imagen_lenguaje',
   Field('pregunta', 'upload', autodelete=True, uploadseparate = True, label=T('Pregunta'), comment=T('Suba una imagen para la prueba')),
   Field('respuesta', 'string', label=T('Respuesta'), comment=T('Respuesta de la pregunta')),
   Field('opciones', 'list:string', label=T('Opciones'), comment=T('Opciones para este tipo de pregunta')),
   format='%(id)s')

db.imagen_lenguaje._singular = T('Imagen del lenguaje')
db.imagen_lenguaje._plural = T('Imagenes del lenguaje')

db.define_table('repeticion_lenguaje',
   Field('pregunta', 'string', label=T('Pregunta'), comment=T('Suba una imagen para la prueba')),
   Field('respuesta', 'string', compute=lambda r:r['pregunta'], label=T('Respuesta'), comment=T('Respuesta de la pregunta')),
   Field('tiempo', 'integer', label=T('Tiempo'), comment=T('Tiempo de la pregunta 5 segundos por una palabra, 10 segundos por una oración')),
   format='%(id)s')

db.repeticion_lenguaje._singular = T('Repetición del lenguaje')
db.repeticion_lenguaje._plural = T('Repeticiones del lenguaje')

db.define_table('comprension_lenguaje',
   Field('imagen', 'upload', autodelete=True, uploadseparate = True, label=T('Imagen'), comment=T('Suba una imagen para la prueba')),
   Field('pregunta', 'string', label=T('Pregunta'), comment=T('Pregunta')),
   Field('respuesta', 'string', label=T('Respuesta'), comment=T('Respuesta de la pregunta')),
   format='%(id)s')

db.comprension_lenguaje._singular = T('Comprensión del lenguaje')
db.comprension_lenguaje._plural = T('Comprensiones del lenguaje')

tipo_pregunta_fv = {'0': T('Palabras que empiezan con F'), '1': T('Palabras que nombren animales')}

db.define_table('fluidez_verbal',
   Field('pregunta', 'string', label=T('Pregunta'), comment=T('Pregunta')),
   Field('respuesta', 'string', label=T('Respuesta'), comment=T('Respuesta de la pregunta')),
   format='%(id)s')

db.fluidez_verbal._singular = T('Fluidez verbal')
db.fluidez_verbal._plural = T('Fluidez verbal')

db.fluidez_verbal.respuesta.requires = IS_IN_SET(tipo_pregunta_fv, zero=T('Choose one'), error_message=T('Choose one'))

db.define_table('semejanza',
   Field('pregunta', 'string', label=T('Pregunta'), comment=T('Pregunta')),
   Field('respuesta', 'list:string', label=T('Respuesta'), comment=T('Respuesta de la pregunta')),
   format='%(id)s')

db.semejanza._singular = T('Semejanza')
db.semejanza._plural = T('Semejanzas')

db.define_table('calculo',
   Field('pregunta', 'string', label=T('Pregunta'), comment=T('Pregunta')),
   Field('respuesta', 'string', compute=lambda r:eval(r['pregunta']), label=T('Respuesta'), comment=T('Respuesta de la pregunta')),
   format='%(id)s')

db.calculo._singular = T('Cálculo')
db.calculo._plural = T('Calculos')

db.define_table('secuencia',
   Field('pregunta', 'upload', autodelete=True, uploadseparate = True, label=T('Imagen'), comment=T('Suba una imagen para la prueba')),
   Field('respuesta', 'string', label=T('Respuesta'), comment=T('Secuencia de la pregunta')),
   format='%(id)s')

db.secuencia._singular = T('Secuencia')
db.secuencia._plural = T('Secuencias')

db.define_table('mv_espontanea',
   Field('pregunta', 'string',label=T('Pregunta'), comment=T('Pregunta')),
   format='%(id)s')

db.mv_espontanea._singular = T('Memoria verbal espontanea')
db.mv_espontanea._plural = T('Memoria verbal espontanea')


db.define_table('diagnostico_inicial',
   Field('seccion', 'reference secciones', label=T('Sección a la que pertenece')),
   Field('diagnostico', 'reference diagnostico', label=T('Diagnostico'), comment=T('Diagnostico')),
   Field('pregunta_id', 'string', label=T('Pregunta id'), comment=T('Pregunta id')),
   Field('pregunta', 'text', label=T('Pregunta'), comment=T('Pregunta')),
   Field('respuesta', 'text', label=T('Respuesta'), comment=T('Respuesta de la pregunta')),
   Field('correcta', 'boolean', default=False, label=T('Correcta'), comment=T('Respuesta correcta')),
   Field('puntos', 'integer', default=0, label=T('Puntos'), comment=T('Puntos')),
   format='%(id)s')
