# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

@auth.requires_membership("Especialista")
def lista_diagnostico():
    response.flash = T("Listado de Diagnóstico")
    response.title = T("Listado de Diagnóstico") + response.title
    return dict()

@auth.requires_membership("Especialista")
def nuevo_diagnostico():
    response.flash = T("Nuevo Diagnóstico")
    response.title = T("Nuevo Diagnóstico") + response.title
    return dict()

@auth.requires_membership("Especialista")
def asignar_diagnostico():
    response.flash = T("Asignar Diagnóstico")
    response.title = T("Asignar Diagnóstico") + response.title
    return dict()
