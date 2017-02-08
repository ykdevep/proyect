# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

@auth.requires_membership("evaluador")
def reportes_estadisticas_personalizadas():
    response.flash = T("Reportes y estadisticas personalizadas")
    response.title = T("Reportes y estadisticas personalizadas") + response.title
    return dict()

def reportes_estadisticas_generales():
    response.flash = T("Reportes y estadisticas generales")
    response.title = T("Reportes y estadisticas personalizadas") + response.title
    return dict()