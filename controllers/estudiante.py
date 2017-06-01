# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations
@auth.requires_membership("Estudiante")
def cuestionario_diagnostico():
    response.flash = T("Cuestionario de diagnóstico")
    response.title = T("Cuestionario de diagnóstico") + response.title

    diagnostico = db((db.diagnostico.activo == True) & (db.diagnostico.tipo == 0)).select().first()

    return dict(diagnostico=diagnostico, user=db.auth_user(auth.user.id))

def visor_secciones():
    '''
    Implementación de un visor de secciones de un diagnóstico dado
    '''
    if request.cid:
        user=db.auth_user(auth.user.id)
        sesion=db(db.secciones.id == user.ci_nivel).select().first()
        response.headers['web2py-component-flash']=T('Comenzar...')
        return dict(sesion=sesion)
    else:
        raise HTTP(403)

def visor_preguntas():
    '''
    Implementación de un visor de preguntas de un diagnóstico dado
    '''
    if request.cid:
        sesion = db.secciones(request.args(2))
        respuesta = imagenes = None

        if sesion.tipo_pregunta == "2-) Orientación":

            ultima_pregunta = db((db.diagnostico_inicial.id > 0) & (db.diagnostico_inicial.seccion == sesion.id) & (db.diagnostico_inicial.created_by == auth.user.id)).select().last()

            if ultima_pregunta:
                pregunta = db(db.orientacion.id > int(ultima_pregunta.pregunta_id)).select().first()
            else:
                pregunta = db(db.orientacion.id > 0).select().first()
            if pregunta:
                respuesta = db.diagnostico_inicial.insert(seccion=sesion.id, diagnostico=request.args(0), pregunta=pregunta.pregunta, pregunta_id=pregunta.id)
            else:
                user=db.auth_user(auth.user.id)
                diagnostico = db.diagnostico(request.args(0))

                nueva_sesion = db((db.secciones.id > sesion.id) & (db.secciones.id.belongs(diagnostico.secciones))).select().first()
                sesion = nueva_sesion

                if nueva_sesion:
                    user.update_record(ci_nivel=nueva_sesion.id)
                else:
                    user.update_record(ci_nivel=-1)
        elif sesion.tipo_pregunta == "3.1-) Atención y concentración/Dígitos en Regresión":

            ultima_pregunta_correcta = db((db.diagnostico_inicial.id > 0) & (db.diagnostico_inicial.seccion == sesion.id) & (db.diagnostico_inicial.created_by == auth.user.id) & (db.diagnostico_inicial.correcta == True)).select().last()

            ultima_pregunta= db((db.diagnostico_inicial.id > 0) & (db.diagnostico_inicial.seccion == sesion.id) & (db.diagnostico_inicial.created_by == auth.user.id)).select().last()
            if ultima_pregunta:
                digitos_regresion =  db((db.digitos_regresion.id == int(ultima_pregunta.pregunta_id))).select().first()

            if ultima_pregunta_correcta:

                if ultima_pregunta_correcta.id == ultima_pregunta.id:
                    pregunta = db((db.digitos_regresion.id > int(ultima_pregunta_correcta.pregunta_id)) & (db.digitos_regresion.secuencia == digitos_regresion.secuencia)).select().first()
                else:
                    pregunta = db((db.digitos_regresion.id > int(ultima_pregunta.pregunta_id)) & (db.digitos_regresion.secuencia == 1) & (db.digitos_regresion.tiempo == len(ultima_pregunta.pregunta.split('-')))).select().first()
            elif ultima_pregunta:
                pregunta = db((db.digitos_regresion.id > int(ultima_pregunta.pregunta_id)) & (db.digitos_regresion.secuencia == 1)).select().first()
            else:
                pregunta = db(db.digitos_regresion.id > 0).select().first()

            if pregunta:
                respuesta = db.diagnostico_inicial.insert(seccion=sesion.id, diagnostico=request.args(0), pregunta=pregunta.pregunta, pregunta_id=pregunta.id)
            else:
                user=db.auth_user(auth.user.id)
                diagnostico = db.diagnostico(request.args(0))

                nueva_sesion = db((db.secciones.id > sesion.id) & (db.secciones.id.belongs(diagnostico.secciones))).select().first()
                sesion = nueva_sesion

                if nueva_sesion:
                    user.update_record(ci_nivel=nueva_sesion.id)
                else:
                    user.update_record(ci_nivel=-1)
        elif sesion.tipo_pregunta == "3.2-) Atención y concentración/Detección Visual":

            ultima_pregunta = db((db.diagnostico_inicial.id > 0) & (db.diagnostico_inicial.seccion == sesion.id) & (db.diagnostico_inicial.created_by == auth.user.id)).select().last()
            if ultima_pregunta:
                pregunta = db(db.deteccion_visual.id > int(ultima_pregunta.pregunta_id)).select().first()
            else:
                pregunta = db(db.deteccion_visual.id > 0).select().first()
            if pregunta:
                respuesta = db.diagnostico_inicial.insert(seccion=sesion.id, diagnostico=request.args(0), pregunta=pregunta.pregunta, pregunta_id=pregunta.id)
                imagenes = db(db.deteccion_visual.id > 0).select(orderby='<random>')
            else:
                user=db.auth_user(auth.user.id)
                diagnostico = db.diagnostico(request.args(0))

                nueva_sesion = db((db.secciones.id > sesion.id) & (db.secciones.id.belongs(diagnostico.secciones))).select().first()
                sesion = nueva_sesion
                if nueva_sesion:
                    user.update_record(ci_nivel=nueva_sesion.id)
                else:
                    user.update_record(ci_nivel=-1)
        elif sesion.tipo_pregunta == "3.3-) Atención y concentración/20-3":

            ultima_pregunta = db((db.diagnostico_inicial.id > 0) & (db.diagnostico_inicial.seccion == sesion.id) & (db.diagnostico_inicial.created_by == auth.user.id)).select().last()
            if not ultima_pregunta:
                pregunta = "20-3"
            else:
                pregunta = None

            if pregunta:
                respuesta = db.diagnostico_inicial.insert(seccion=sesion.id, diagnostico=request.args(0), pregunta=pregunta, pregunta_id=pregunta)
            else:
                user=db.auth_user(auth.user.id)
                diagnostico = db.diagnostico(request.args(0))

                nueva_sesion = db((db.secciones.id > sesion.id) & (db.secciones.id.belongs(diagnostico.secciones))).select().first()
                sesion = nueva_sesion
                if nueva_sesion:
                    user.update_record(ci_nivel=nueva_sesion.id)
                else:
                    user.update_record(ci_nivel=-1)
        elif sesion.tipo_pregunta == "4-) Codificación/Memoria verbal":

            ultima_pregunta = db((db.diagnostico_inicial.id > 0) & (db.diagnostico_inicial.seccion == sesion.id) & (db.diagnostico_inicial.created_by == auth.user.id)).select().last()
            if ultima_pregunta:
                pregunta = db(db.memoria_verbal.id > int(ultima_pregunta.pregunta_id)).select().first()
            else:
                pregunta = db(db.memoria_verbal.id > 0).select().first()
            if pregunta:
                respuesta = db.diagnostico_inicial.insert(seccion=sesion.id, diagnostico=request.args(0), pregunta=pregunta.pregunta, pregunta_id=pregunta.id)
            else:
                user=db.auth_user(auth.user.id)
                diagnostico = db.diagnostico(request.args(0))

                nueva_sesion = db((db.secciones.id > sesion.id) & (db.secciones.id.belongs(diagnostico.secciones))).select().first()
                sesion = nueva_sesion
                if nueva_sesion:
                    user.update_record(ci_nivel=nueva_sesion.id)
                else:
                    user.update_record(ci_nivel=-1)
        elif sesion.tipo_pregunta == "5-) Lenguaje":

            ultima_pregunta = db((db.diagnostico_inicial.id > 0) & (db.diagnostico_inicial.seccion == sesion.id) & (db.diagnostico_inicial.created_by == auth.user.id)).select().last()
            if ultima_pregunta:
                pregunta = db(db.imagen_lenguaje.id > int(ultima_pregunta.pregunta_id)).select().first()
            else:
                pregunta = db(db.imagen_lenguaje.id > 0).select().first()
            if pregunta:
                respuesta = db.diagnostico_inicial.insert(seccion=sesion.id, diagnostico=request.args(0), pregunta=pregunta.pregunta, pregunta_id=pregunta.id)
            else:
                user=db.auth_user(auth.user.id)
                diagnostico = db.diagnostico(request.args(0))

                nueva_sesion = db((db.secciones.id > sesion.id) & (db.secciones.id.belongs(diagnostico.secciones))).select().first()
                sesion = nueva_sesion
                if nueva_sesion:
                    user.update_record(ci_nivel=nueva_sesion.id)
                else:
                    user.update_record(ci_nivel=-1)
        elif sesion.tipo_pregunta == "5.1-) Lenguaje/Repetición":

            ultima_pregunta = db((db.diagnostico_inicial.id > 0) & (db.diagnostico_inicial.seccion == sesion.id) & (db.diagnostico_inicial.created_by == auth.user.id)).select().last()
            if ultima_pregunta:
                pregunta = db(db.repeticion_lenguaje.id > int(ultima_pregunta.pregunta_id)).select().first()
            else:
                pregunta = db(db.repeticion_lenguaje.id > 0).select().first()
            if pregunta:
                respuesta = db.diagnostico_inicial.insert(seccion=sesion.id, diagnostico=request.args(0), pregunta=pregunta.pregunta, pregunta_id=pregunta.id)
            else:
                user=db.auth_user(auth.user.id)
                diagnostico = db.diagnostico(request.args(0))

                nueva_sesion = db((db.secciones.id > sesion.id) & (db.secciones.id.belongs(diagnostico.secciones))).select().first()
                sesion = nueva_sesion
                if nueva_sesion:
                    user.update_record(ci_nivel=nueva_sesion.id)
                else:
                    user.update_record(ci_nivel=-1)
        elif sesion.tipo_pregunta == "5.2-) Lenguaje/Comprensión":

            ultima_pregunta = db((db.diagnostico_inicial.id > 0) & (db.diagnostico_inicial.seccion == sesion.id) & (db.diagnostico_inicial.created_by == auth.user.id)).select().last()
            if ultima_pregunta:
                pregunta = db(db.comprension_lenguaje.id > int(ultima_pregunta.pregunta_id)).select().first()
            else:
                pregunta = db(db.comprension_lenguaje.id > 0).select().first()
            if pregunta:
                respuesta = db.diagnostico_inicial.insert(seccion=sesion.id, diagnostico=request.args(0), pregunta=pregunta.pregunta, pregunta_id=pregunta.id)
            else:
                user=db.auth_user(auth.user.id)
                diagnostico = db.diagnostico(request.args(0))

                nueva_sesion = db((db.secciones.id > sesion.id) & (db.secciones.id.belongs(diagnostico.secciones))).select().first()
                sesion = nueva_sesion
                if nueva_sesion:
                    user.update_record(ci_nivel=nueva_sesion.id)
                else:
                    user.update_record(ci_nivel=-1)
        elif sesion.tipo_pregunta == "5.3-) Lenguaje/Fluidez verbal":

            ultima_pregunta = db((db.diagnostico_inicial.id > 0) & (db.diagnostico_inicial.seccion == sesion.id) & (db.diagnostico_inicial.created_by == auth.user.id)).select().last()
            if ultima_pregunta:
                pregunta = db(db.fluidez_verbal.id > int(ultima_pregunta.pregunta_id)).select().first()
            else:
                pregunta = db(db.fluidez_verbal.id > 0).select().first()
            if pregunta:
                respuesta = db.diagnostico_inicial.insert(seccion=sesion.id, diagnostico=request.args(0), pregunta=pregunta.pregunta, pregunta_id=pregunta.id)
            else:
                user=db.auth_user(auth.user.id)
                diagnostico = db.diagnostico(request.args(0))

                nueva_sesion = db((db.secciones.id > sesion.id) & (db.secciones.id.belongs(diagnostico.secciones))).select().first()
                sesion = nueva_sesion
                if nueva_sesion:
                    user.update_record(ci_nivel=nueva_sesion.id)
                else:
                    user.update_record(ci_nivel=-1)
        elif sesion.tipo_pregunta == "6.1-) Funciones ejecutivas/Semejanzas":
            ultima_pregunta = db((db.diagnostico_inicial.id > 0) & (db.diagnostico_inicial.seccion == sesion.id) & (db.diagnostico_inicial.created_by == auth.user.id)).select().last()
            if ultima_pregunta:
                pregunta = db(db.semejanza.id > int(ultima_pregunta.pregunta_id)).select().first()
            else:
                pregunta = db(db.semejanza.id > 0).select().first()
            if pregunta:
                respuesta = db.diagnostico_inicial.insert(seccion=sesion.id, diagnostico=request.args(0), pregunta=pregunta.pregunta, pregunta_id=pregunta.id)
            else:
                user=db.auth_user(auth.user.id)
                diagnostico = db.diagnostico(request.args(0))

                nueva_sesion = db((db.secciones.id > sesion.id) & (db.secciones.id.belongs(diagnostico.secciones))).select().first()
                sesion = nueva_sesion
                if nueva_sesion:
                    user.update_record(ci_nivel=nueva_sesion.id)
                else:
                    user.update_record(ci_nivel=-1)
        elif sesion.tipo_pregunta == "6.2-) Funciones ejecutivas/Cálculo":
            ultima_pregunta = db((db.diagnostico_inicial.id > 0) & (db.diagnostico_inicial.seccion == sesion.id) & (db.diagnostico_inicial.created_by == auth.user.id)).select().last()
            if ultima_pregunta:
                pregunta = db(db.calculo.id > int(ultima_pregunta.pregunta_id)).select().first()
            else:
                pregunta = db(db.calculo.id > 0).select().first()
            if pregunta:
                respuesta = db.diagnostico_inicial.insert(seccion=sesion.id, diagnostico=request.args(0), pregunta=pregunta.pregunta, pregunta_id=pregunta.id)
            else:
                user=db.auth_user(auth.user.id)
                diagnostico = db.diagnostico(request.args(0))

                nueva_sesion = db((db.secciones.id > sesion.id) & (db.secciones.id.belongs(diagnostico.secciones))).select().first()
                sesion = nueva_sesion
                if nueva_sesion:
                    user.update_record(ci_nivel=nueva_sesion.id)
                else:
                    user.update_record(ci_nivel=-1)
        elif sesion.tipo_pregunta == "6.3-) Funciones ejecutivas/Secuenciación":
            ultima_pregunta = db((db.diagnostico_inicial.id > 0) & (db.diagnostico_inicial.seccion == sesion.id) & (db.diagnostico_inicial.created_by == auth.user.id)).select().last()
            if ultima_pregunta:
                pregunta = db(db.secuencia.id > int(ultima_pregunta.pregunta_id)).select().first()
            else:
                pregunta = db(db.secuencia.id > 0).select().first()
            if pregunta:
                respuesta = db.diagnostico_inicial.insert(seccion=sesion.id, diagnostico=request.args(0), pregunta=pregunta.pregunta, pregunta_id=pregunta.id)
            else:
                user=db.auth_user(auth.user.id)
                diagnostico = db.diagnostico(request.args(0))

                nueva_sesion = db((db.secciones.id > sesion.id) & (db.secciones.id.belongs(diagnostico.secciones))).select().first()
                sesion = nueva_sesion
                if nueva_sesion:
                    user.update_record(ci_nivel=nueva_sesion.id)
                else:
                    user.update_record(ci_nivel=-1)
        elif sesion.tipo_pregunta == "7.1-) Funciones de evocación/Memoria verbal espontanea":
            ultima_pregunta = db((db.diagnostico_inicial.id > 0) & (db.diagnostico_inicial.seccion == sesion.id) & (db.diagnostico_inicial.created_by == auth.user.id)).select().last()
            if ultima_pregunta:
                pregunta = db(db.mv_espontanea.id > int(ultima_pregunta.pregunta_id)).select().first()
            else:
                pregunta = db(db.mv_espontanea.id > 0).select().first()
            if pregunta:
                respuesta = db.diagnostico_inicial.insert(seccion=sesion.id, diagnostico=request.args(0), pregunta=pregunta.pregunta, pregunta_id=pregunta.id)
            else:
                user=db.auth_user(auth.user.id)
                diagnostico = db.diagnostico(request.args(0))

                nueva_sesion = db((db.secciones.id > sesion.id) & (db.secciones.id.belongs(diagnostico.secciones))).select().first()
                sesion = nueva_sesion
                if nueva_sesion:
                    user.update_record(ci_nivel=nueva_sesion.id)
                else:
                    user.update_record(ci_nivel=-1)
        else:
            pregunta = "Error no hay secciones activas"
        response.headers['web2py-component-flash']=T('Siguiente Pregunta')

        return dict(pregunta=pregunta, sesion=sesion, respuesta=respuesta, imagenes=imagenes)
    else:
        raise HTTP(403)

def guardar_respuesta():
    '''
    Guardar una pregunta, petición ajax
    '''
    import gluon.contrib.simplejson
    if request.ajax:

        respuesta_di = db.diagnostico_inicial(request.vars.id)

        if respuesta_di:
            correcta, puntos = __evaluar_respuesta(respuesta_di, request.vars.respuesta)
            respuesta_di.update_record(respuesta=request.vars.respuesta, correcta=correcta, puntos=puntos)
            return gluon.contrib.simplejson.dumps({'estado': True})
        else:
            return gluon.contrib.simplejson.dumps({'estado': False})
    else:
        return gluon.contrib.simplejson.dumps({'estado': False})

def __evaluar_respuesta(respuesta_di, respuesta):
    """
    Evaluar secciones por cada tipo
    """
    sesion = db.secciones(respuesta_di.seccion)

    if sesion.tipo_pregunta == "2-) Orientación":
        orientacion = db(db.orientacion.pregunta == respuesta_di.pregunta).select().first()
        if orientacion:
            from datetime import datetime
            if (((orientacion.respuesta == '0') and (str(datetime.now().day) == respuesta)) | ((orientacion.respuesta == '1') and (str(datetime.now().month) == respuesta)) | ((orientacion.respuesta == '2') and (str(datetime.now().year) == respuesta)) | ((orientacion.respuesta == '3') and (respuesta == auth.user.localidad)) | ((orientacion.respuesta == '4') and (respuesta == auth.user.ciudad))):
                return True, 1
    elif sesion.tipo_pregunta == "3.1-) Atención y concentración/Dígitos en Regresión":
        digitos_regresion = db(db.digitos_regresion.pregunta == respuesta_di.pregunta).select().first()
        if digitos_regresion:
            if digitos_regresion.respuesta == respuesta:
                return True, len(respuesta.split('-'))
    elif sesion.tipo_pregunta == "3.2-) Atención y concentración/Detección Visual":
        deteccion_visual = db(db.deteccion_visual.pregunta == respuesta_di.pregunta).select().first()
        if deteccion_visual:
            if deteccion_visual.respuesta == respuesta:
                return True, 1
    elif sesion.tipo_pregunta == "3.3-) Atención y concentración/20-3":
        puntos = 0
        valor = 20
        for r in respuesta:
            if r.isdigit():
                if ((str(valor - 3)) == r):
                    puntos = puntos + 1
                valor = int(r)
        return True, puntos
    elif sesion.tipo_pregunta == "4-) Codificación/Memoria verbal":
        memoria_verbal = db(db.memoria_verbal.pregunta == respuesta_di.pregunta).select().first()
        if memoria_verbal:
            puntos = 0
            for palabra in respuesta:
                if palabra in memoria_verbal.pregunta.split('-'):
                    puntos = puntos + 1
            x = (puntos*100)/len(memoria_verbal.pregunta.split('-'))
            if x > 50:
                return True, puntos
            else:
                return False, puntos
    elif sesion.tipo_pregunta == "5-) Lenguaje":
        imagen_lenguaje = db(db.imagen_lenguaje.pregunta == respuesta_di.pregunta).select().first()
        if imagen_lenguaje:
            if imagen_lenguaje.respuesta == respuesta:
                return True, sesion.puntos
    elif sesion.tipo_pregunta == "5.1-) Lenguaje/Repetición":
        repeticion_lenguaje = db(db.repeticion_lenguaje.pregunta == respuesta_di.pregunta).select().first()
        if repeticion_lenguaje:
            if repeticion_lenguaje.respuesta == respuesta:
                return True, sesion.puntos
    elif sesion.tipo_pregunta == "5.2-) Lenguaje/Comprensión":
        comprension_lenguaje = db(db.comprension_lenguaje.pregunta == respuesta_di.pregunta).select().first()
        if comprension_lenguaje:
            if comprension_lenguaje.respuesta == respuesta:
                return True, sesion.puntos
    elif sesion.tipo_pregunta == "5.3-) Lenguaje/Fluidez verbal":
        fluidez_verbal = db(db.fluidez_verbal.pregunta == respuesta_di.pregunta).select().first()
        if fluidez_verbal:
            puntos = 0
            for palabra in respuesta:
                if fluidez_verbal.respuesta == '0':
                    if palabra.startswith('f') or palabra.startswith('F'):
                        puntos = puntos + 0.3
            x = (puntos*100)/len(respuesta)
            if x > 50:
                return True, puntos
            else:
                return False, puntos
    elif sesion.tipo_pregunta == "6.1-) Funciones ejecutivas/Semejanzas":
        semejanza = db(db.semejanza.pregunta == respuesta_di.pregunta).select().first()

        if semejanza:
            return True, semejanza.respuesta.index(respuesta)
    elif sesion.tipo_pregunta == "6.2-) Funciones ejecutivas/Cálculo":
        calculo = db(db.calculo.pregunta == respuesta_di.pregunta).select().first()

        if calculo:
            if respuesta == calculo.respuesta:
                return True, 1
    elif sesion.tipo_pregunta == "6.3-) Funciones ejecutivas/Secuenciación":
        secuencia = db(db.secuencia.pregunta == respuesta_di.pregunta).select().first()

        if secuencia:
            if respuesta == secuencia.respuesta:
                return True, 1
    elif sesion.tipo_pregunta == "7.1-) Funciones de evocación/Memoria verbal espontanea":
        mv_espontanea = db(db.mv_espontanea.pregunta == respuesta_di.pregunta).select().first()

        puntos = 0

        if mv_espontanea:
            for r in respuesta:
                if not db(db.memoria_verbal.pregunta.contains(r)).isempty():
                    puntos = puntos + 1
            return True, puntos

    return False, 0

def get_tiempo():
    '''
    Get tiempo transcurrido de un diagnostico en curso
    '''
    import gluon.contrib.simplejson

    if request.ajax:
        respuesta_first = db((db.diagnostico_inicial.diagnostico == request.vars.diagnostico) & (db.diagnostico_inicial.created_by == auth.user.id)).select(orderby=db.diagnostico_inicial.created_on).first()
        if respuesta_first:
            time = request.now - respuesta_first.created_on
            return gluon.contrib.simplejson.dumps({'time': (time.seconds)*1000, 'start': True})
        time = request.now - request.now
        return gluon.contrib.simplejson.dumps({'time': 1000, 'start': True})
    else:
        return gluon.contrib.simplejson.dumps({'time': 0, 'start': False})

def form_datos_generales():
    user = db.auth_user(auth.user.id)
    diagnostico = db.diagnostico(request.args(0))
    sesion = db((db.secciones.id.belongs(diagnostico.secciones))).select().first()
    
    sexo = {'0': T('Masculino'), '1': T('Femenino')}
    escolaridad = {'0': T('Cero escolaridad'), '1': T('Primaria'), '2': T('Bachillerato'), '3': T('Prerapatoria'), '4': T('Universitario'), '5': T('Posgrado')}
    lateralidad = {'0': T('Derecho'), '1': T('Izquierdo')}

    formulario = SQLFORM.factory(
           Field('sexo', 'integer', label=T('Sexo'), requires = IS_IN_SET(sexo, zero=T('Choose one'), error_message=T('Choose one')), comment=T('Sexo del encuestado')),
           Field('escolaridad', 'integer', label=T('Escolaridad'), requires = IS_IN_SET(escolaridad, zero=T('Choose one'), error_message=T('Choose one')), comment=T('Escolaridad del encuestado')),
           Field('lateralidad', 'integer', label=T('Lateralidad'), requires = IS_IN_SET(lateralidad, zero=T('Choose one'), error_message=T('Choose one')),  comment=T('Lateralidad del encuestado')),
           Field('ciudad', 'string', label=T('Ciudad'), requires = IS_NOT_EMPTY(), comment=T('Ciudad donde se encuentra el encuestado')),
           Field('lugar', 'string', label=T('Lugar'), requires = IS_NOT_EMPTY(), comment=T('Lugar donde se encuentra el encuestado')),
           Field('enfermedad', 'list:reference antecedentes_medicos', label=T('Antecedentes Médicos'), requires = IS_IN_DB(db,'antecedentes_medicos.id','antecedentes_medicos.enfermedad', multiple=True), widget = SQLFORM.widgets.checkboxes.widget, default = lambda : [], comment=T('Antecedentes médicos del encuestado')), formstyle='bootstrap3_inline')

    if formulario.process().accepted:
        nueva_sesion=db((db.secciones.id > sesion.id) & (db.secciones.id.belongs(diagnostico.secciones))).select().first()
        sesion = nueva_sesion

        user.update_record(ci_nivel=nueva_sesion.id, sexo=formulario.vars.sexo, escolaridad=formulario.vars.escolaridad, lateralidad=formulario.vars.lateralidad, ciudad=formulario.vars.ciudad, lugar=formulario.vars.lugar, enfermedad=formulario.vars.enfermedad)
        response.flash = 'Respuesta agregada'
    elif formulario.errors:
        response.flash = 'El formulario tiene errores'
    return dict(formulario=formulario, user=user, sesion=sesion)

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
