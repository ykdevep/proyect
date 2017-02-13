# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations
def visor_preguntas():
    '''
    Implementación de un visor de preguntas de un diagnóstico dado
    '''
    if request.cid:

        diagnostico = db.diagnostico(request.args(0))

        return dict(diagnostico=diagnostico)
    else:
        raise HTTP(403)

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
