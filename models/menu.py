# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

# ----------------------------------------------------------------------------------------------------------------------
# Customize your APP title, subtitle and menus here
# ----------------------------------------------------------------------------------------------------------------------

response.logo = H5(A('Logo', XML('&trade;&nbsp;'),
                  _class="navbar-brand-name", _href=URL('default', 'index'),
                  _id="index", **{'_data-target': "#index"}))
response.title = request.application.replace('_', ' ').title()
response.subtitle = ''


# ----------------------------------------------------------------------------------------------------------------------
# read more at http://dev.w3.org/html5/markup/meta.name.html
# ----------------------------------------------------------------------------------------------------------------------
response.meta.author = myconf.get('app.author')
response.meta.description = myconf.get('app.description')
response.meta.keywords = myconf.get('app.keywords')
response.meta.generator = myconf.get('app.generator')

# ----------------------------------------------------------------------------------------------------------------------
# your http://google.com/analytics id
# ----------------------------------------------------------------------------------------------------------------------
response.google_analytics_id = None

# ----------------------------------------------------------------------------------------------------------------------
# this is the main application menu add/remove items as required
# ----------------------------------------------------------------------------------------------------------------------

PRODUCTION_MENU = True


# ----------------------------------------------------------------------------------------------------------------------
# provide shortcuts for development. remove in production
# ----------------------------------------------------------------------------------------------------------------------

def _():
    # ------------------------------------------------------------------------------------------------------------------
    # shortcuts
    # ------------------------------------------------------------------------------------------------------------------
    app = request.application
    ctr = request.controller
    # ------------------------------------------------------------------------------------------------------------------
    # useful links to internal and external resources
    # ------------------------------------------------------------------------------------------------------------------
    response.title = ' | ' +request.application.replace('_',' ').title()

    if(auth.has_membership('Administrador')):
        response.menu += [(CAT(XML('<ico class="glyphicon glyphicon-lock"></ico> '), T('Administrar')),False, URL(), [
            ("new_admin", False, A(CAT(XML('<ico class="glyphicon glyphicon-user"></ico> '), T('Nuevo Administrador')), _href=URL("admin", "new_admin"), **{'_data-target': "#new_admin"})),
            ("new_revisor", False, A(CAT(XML('<ico class="glyphicon glyphicon-user"></ico> '), T('Nuevo Especialista')), _href=URL("admin", "new_revisor"), **{'_data-target': "#new_revisor"})),
            ("new_student", False, A(CAT(XML('<ico class="glyphicon glyphicon-user"></ico> '), T('Nuevo Estudiante')), _href=URL("admin", "new_student"), **{'_data-target': "#new_student"})),
            ("new_user", False, A(CAT(XML('<ico class="glyphicon glyphicon-user"></ico> '), T('Nuevo Visitante')), _href=URL("admin", "new_user"), **{'_data-target': "#new_user"})),
            ("users", False, A(CAT(XML('<ico class="glyphicon glyphicon-user"></ico> '), T('Gestionar rol a usuario')), _href=URL("admin", "users"), **{'_data-target': "#users"})),
            ("centros", False, A(CAT(XML('<ico class="glyphicon glyphicon-home"></ico> '), T('Gestionar Centros')), _href=URL("admin", "centros"), **{'_data-target': "#centros"})),
           ]
        )]
        response.menu += [(CAT(XML('<ico class="glyphicon glyphicon-tasks"></ico> '), T('Estadísticas de Uso')),False, URL(), [
            ("logs", False, A(CAT(XML('<ico class="glyphicon glyphicon-tasks"></ico> '), T('Administrar logs')), _href=URL("admin", "logs"), **{'_data-target': "#logs"}))]
        )]
    if (auth.has_membership('Especialista')):
        response.menu += [(CAT(XML('<ico class="glyphicon glyphicon-edit"></ico> '), T('Diagnóstico Inicial')), False, URL(), [
            ("lista_diagnostico", False, A(CAT(XML('<ico class="glyphicon glyphicon-th-list"></ico> '), T('Lista Diagnóstico')), _href=URL("especialista", "lista_diagnostico"), **{'_data-target': "#lista_diagnostico"})),
            ("nuevo_diagnostico", False, A(CAT(XML('<ico class="glyphicon glyphicon-plus"></ico> '), T('Nuevo Diagnóstico')), _href=URL("especialista", "nuevo_diagnostico"), **{'_data-target': "#nuevo_diagnostico"})),
            ("asignar_diagnostico", False, A(CAT(XML('<ico class="glyphicon glyphicon-list-alt"></ico> '), T('Asignar Diagnóstico')), _href=URL("especialista", "asignar_diagnostico"), **{'_data-target': "#asignar_diagnostico"})),
            ]
        )]
        
        response.menu += [(CAT(XML('<ico class="glyphicon glyphicon-edit"></ico> '), T('Mejorar Atención')), False, URL(), []
        )]
        
        response.menu += [(CAT(XML('<ico class="glyphicon glyphicon-edit"></ico> '), T('Estadísticas')), False, URL(), [
            ("reportes_estadisticas_generales", False, A(CAT(XML('<ico class="glyphicon glyphicon-list-alt"></ico> '), T('Reportes de estadísticas generales')), _href=URL("reportes", "reportes_estadisticas_generales"), **{'_data-target': "#reportes_estadisticas_generales"})),
            ("reportes_estadisticas_personalizadas", False, A(CAT(XML('<ico class="glyphicon glyphicon-list-alt"></ico> '), T('Reportes de estadísticas personalizadas')), _href=URL("reportes", "reportes_estadisticas_personalizadas"), **{'_data-target': "#reportes_estadisticas_personalizadas"}))]
        )]
        response.menu += [(CAT(XML('<ico class="glyphicon glyphicon-edit"></ico> '), T('Evaluaciones')), False, URL(), []
        )]
    if (auth.has_membership('Estudiante')):
        response.menu += [(CAT(XML('<ico class="glyphicon glyphicon-edit"></ico> '), T('Diagnósticos Realizados')), False, URL(), [
            ("cuestionario_diagnostico", False, A(CAT(XML('<ico class="glyphicon glyphicon-edit"></ico> '), T('Diagnóstico Inicial')), _href=URL("estudiante", "cuestionario_diagnostico"), **{'_data-target': "#cuestionario_diagnostico"})),
            ("diag_enfocada", False, A(CAT(XML('<ico class="glyphicon glyphicon-edit"></ico> '), T('Atención Enfocada')), _href=URL("estudiante", "diag_enfocada"), **{'_data-target': "#diag_enfocada"})),
            ("diag_sostenida", False, A(CAT(XML('<ico class="glyphicon glyphicon-edit"></ico> '), T('Atención Sostenida')), _href=URL("estudiante", "diag_sostenida"), **{'_data-target': "#diag_sostenida"})),
            ("diag_selectiva", False, A(CAT(XML('<ico class="glyphicon glyphicon-edit"></ico> '), T('Atención Selectiva')), _href=URL("estudiante", "diag_selectiva"), **{'_data-target': "#diag_selectiva"})),
            ("diag_alternada", False, A(CAT(XML('<ico class="glyphicon glyphicon-edit"></ico> '), T('Atención Alternada')), _href=URL("estudiante", "diag_alternada"), **{'_data-target': "#diag_alternada"})),
            ("diag_dividida", False, A(CAT(XML('<ico class="glyphicon glyphicon-edit"></ico> '), T('Atención Dividida')), _href=URL("estudiante", "diag_dividida"), **{'_data-target': "#diag_dividida"})),
          ]
        )]
        response.menu += [(CAT(XML('<ico class="glyphicon glyphicon-edit"></ico> '), T('Resultados')), False, URL(), [
            ("resultado_general", False, A(CAT(XML('<ico class="glyphicon glyphicon-edit"></ico> '), T('Resultado General')), _href=URL("estudiante", "resultado_general"), **{'_data-target': "#resultado_general"})),
            ("resultado_enfocada", False, A(CAT(XML('<ico class="glyphicon glyphicon-edit"></ico> '), T('Atención Enfocada')), _href=URL("estudiante", "resultado_enfocada"), **{'_data-target': "#resultado_enfocada"})),
            ("resultado_sostenida", False, A(CAT(XML('<ico class="glyphicon glyphicon-edit"></ico> '), T('Atención Sostenida')), _href=URL("estudiante", "resultado_sostenida"), **{'_data-target': "#resultado_sostenida"})),
            ("resultado_selectiva", False, A(CAT(XML('<ico class="glyphicon glyphicon-edit"></ico> '), T('Atención Selectiva')), _href=URL("estudiante", "resultado_selectiva"), **{'_data-target': "#resultado_selectiva"})),
            ("resultado_alternada", False, A(CAT(XML('<ico class="glyphicon glyphicon-edit"></ico> '), T('Atención Alternada')), _href=URL("estudiante", "resultado_alternada"), **{'_data-target': "#resultado_alternada"})),
            ("resultado_dividida", False, A(CAT(XML('<ico class="glyphicon glyphicon-edit"></ico> '), T('Atención Dividida')), _href=URL("estudiante", "resultado_dividida"), **{'_data-target': "#resultado_dividida"})),
          ]
        )]
    if (auth.has_membership('Visitante')):
        response.menu += [(CAT(XML('<ico class="glyphicon glyphicon-list-alt"></ico> '), T('Estadísticas Generales')), False, URL(), [
            ("general", False, A(CAT(XML('<ico class="glyphicon glyphicon-list-alt"></ico> '), T('Generales')), _href=URL("visitante", "general"), **{'_data-target': "#general"})),
            ("enfocada", False, A(CAT(XML('<ico class="glyphicon glyphicon-edit"></ico> '), T('Atención Enfocada')), _href=URL("visitante", "enfocada"), **{'_data-target': "#enfocada"})),
            ("sostenida", False, A(CAT(XML('<ico class="glyphicon glyphicon-edit"></ico> '), T('Atención Sostenida')), _href=URL("visitante", "sostenida"), **{'_data-target': "#sostenida"})),
            ("selectiva", False, A(CAT(XML('<ico class="glyphicon glyphicon-edit"></ico> '), T('Atención Selectiva')), _href=URL("visitante", "selectiva"), **{'_data-target': "#selectiva"})),
            ("alternada", False, A(CAT(XML('<ico class="glyphicon glyphicon-edit"></ico> '), T('Atención Alternada')), _href=URL("visitante", "alternada"), **{'_data-target': "#alternada"})),
            ("dividida", False, A(CAT(XML('<ico class="glyphicon glyphicon-edit"></ico> '), T('Atención Dividida')), _href=URL("visitante", "dividida"), **{'_data-target': "#dividida"})),
            ]
        )]

if PRODUCTION_MENU:
    _()
