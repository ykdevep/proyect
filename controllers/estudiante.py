# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

def cuestionario_diagnostico():
    response.flash = T("Cuestionario de diagnóstico")
    response.title = T("Cuestionario de diagnóstico") + response.title
    return dict()

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
