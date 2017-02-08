# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

def cuestionario_diagnostico():
    response.flash = T("Cuestionario de diagnóstico")
    response.title = T("Cuestionario de diagnóstico") + response.title
    return dict()

def cuestionario_desarrollo():
    response.flash = T("Cuestionario de desarrollo")
    response.title = T("Cuestionario de desarrollo") + response.title
    return dict()

def nivel_atencion():
    response.flash = T("Nivel de Atención")
    response.title = T("Nivel de Atención") + response.title
    return dict()