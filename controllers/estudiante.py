# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations
def visor_preguntas():
    '''
    Implementación de un visor de preguntas de un diagnóstico dado
    '''
    if request.cid:
        pregunta = None
        respuesta_id = None

        diagnostico = db.diagnostico(request.args(0))

        if diagnostico:
            preguntas = db((db.pregunta.diagnostico == diagnostico.id)).select(orderby=db.pregunta.tipo|db.pregunta.ensayo|db.pregunta.created_on)
            consulta = ((db.respuesta.diagnostico == diagnostico.id) & (db.respuesta.created_by == auth.user.id))

            if len(preguntas) > len(db(consulta).select()):

                respuesta = db(consulta).select(orderby=db.respuesta.created_on).last()

                if respuesta:
                    if respuesta.created_on != respuesta.modified_on:
                        pregunta = preguntas[len(db(consulta).select())]
                        respuesta_id = db.respuesta.insert(diagnostico=diagnostico.id, pregunta=pregunta.id)
                    else:
                        respuesta_id = respuesta.id
                        pregunta = preguntas[len(db(consulta).select())-1]
                else:
                    pregunta = preguntas[len(db(consulta).select())]
                    respuesta_id = db.respuesta.insert(diagnostico=diagnostico.id, pregunta=pregunta.id)

                response.headers['web2py-component-flash']=T('Siguiente Pregunta')

        return dict(diagnostico=diagnostico, pregunta=pregunta, respuesta_id=respuesta_id)
    else:
        raise HTTP(403)

def guardar_respuesta():
    '''
    Guardar una pregunta, petición ajax
    '''
    import gluon.contrib.simplejson
    if request.ajax:

        respuesta = db.respuesta(request.vars.id)

        if respuesta:
            pregunta = db.pregunta(respuesta.pregunta)
            if pregunta.respuesta == request.vars.texto:
                respuesta.update_record(texto=request.vars.texto, pregunta=request.vars.pregunta, aciertos=1, intrusiones=0, correcta=True)
            else:
                respuesta.update_record(texto=request.vars.texto, pregunta=request.vars.pregunta, aciertos=0, intrusiones=1)
            return gluon.contrib.simplejson.dumps({'estado': True})
        else:
            return gluon.contrib.simplejson.dumps({'estado': False})
    else:
        return gluon.contrib.simplejson.dumps({'estado': False})

def get_tiempo():
    '''
    Get tiempo transcurrido de un diagnostico en curso
    '''
    import gluon.contrib.simplejson

    if request.ajax:
        diagnostico = db.diagnostico(request.vars.diagnostico)

        if diagnostico:
            respuesta_first = db((db.respuesta.diagnostico == diagnostico.id) & (db.respuesta.created_by == auth.user.id)).select(orderby=db.respuesta.created_on).first()
            respuesta_last = db((db.respuesta.diagnostico == diagnostico.id) & (db.respuesta.created_by == auth.user.id)).select(orderby=db.respuesta.created_on).last()
            if respuesta_first and respuesta_last:
                if ((diagnostico.respuesta.count() == diagnostico.pregunta.count()) and (respuesta_last.created_on != respuesta_last.modified_on)):
                    time = respuesta_last.modified_on - respuesta_first.created_on
                    return gluon.contrib.simplejson.dumps({'time': (1+time.seconds)*1000, 'start': False})
                time = request.now - respuesta_first.created_on
                return gluon.contrib.simplejson.dumps({'time': (1+time.seconds)*1000, 'start': True})
            return gluon.contrib.simplejson.dumps({'time': 1000, 'start': True})
        else:
            return gluon.contrib.simplejson.dumps({'time': 0, 'start': False})
    else:
        return gluon.contrib.simplejson.dumps({'time': 0, 'start': False})


@auth.requires_membership("Estudiante")
def cuestionario_diagnostico():
    response.flash = T("Cuestionario de diagnóstico")
    response.title = T("Cuestionario de diagnóstico") + response.title

    diagnostico = db((db.diagnostico.activo == True) & (db.diagnostico.tipo == 0)).select().first()

    return dict(diagnostico=diagnostico)

def diag_alternada():

    response.title = T("Atención Alternada") + response.title
    return dict()

def diag_dividida():

    response.title = T("Atención Dividida") + response.title
    return dict()

def diag_enfocada():

    response.title = T("Atención Enfocada") + response.title
    return dict()

def diag_selectiva():

    response.title = T("Atención Selectiva") + response.title
    return dict()

def diag_sostenida():

    response.title = T("Atención Sostenida") + response.title
    return dict()

def resultado_general():
    response.flash = T("Resultado General")
    response.title = T("Resultado General") + response.title
    return dict()

def resultado_alternada():

    response.title = T("Atención Alternada") + response.title
    return dict()

def resultado_dividida():

    response.title = T("Atención Dividida") + response.title
    return dict()

def resultado_enfocada():

    response.title = T("Atención Enfocada") + response.title
    return dict()

def resultado_selectiva():

    response.title = T("Atención Selectiva") + response.title
    return dict()

def resultado_sostenida():

    response.title = T("Atención Sostenida") + response.title
    return dict()
