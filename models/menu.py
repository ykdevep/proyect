# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

# ----------------------------------------------------------------------------------------------------------------------
# Customize your APP title, subtitle and menus here
# ----------------------------------------------------------------------------------------------------------------------

response.logo = A('Brand', XML('&trade;&nbsp;'),
                  _class="navbar-brand-name", _href=URL('default', 'index'),
                  _id="index", **{'_data-target': "#index"})
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
        response.menu += [(CAT(XML('<ico class="glyphicon glyphicon-lock"></ico> '), T('Administrador')),False, URL(), [
            ("users", False, A(CAT(XML('<ico class="glyphicon glyphicon-user"></ico> '), T('Administrar usuarios')), _href=URL("admin", "users"), **{'_data-target': "#users"})),
            ("centros", False, A(CAT(XML('<ico class="glyphicon glyphicon-home"></ico> '), T('Administrar Centros')), _href=URL("admin", "centros"), **{'_data-target': "#centros"})),
            ("banners", False, A(CAT(XML('<ico class="glyphicon glyphicon-picture"></ico> '), T('Administrar Banners')), _href=URL("admin", "banners"), **{'_data-target': "#banners"}))]
        )]
    if (auth.has_membership('Especialista')):
        response.menu += [(CAT(XML('<ico class="glyphicon glyphicon-edit"></ico> '), T('Especialista')), False, URL(), [
            ("cuestionario_evaluacion", False, A(CAT(XML('<ico class="glyphicon glyphicon-edit"></ico> '), T('Cuestionario Evaluación ')), _href=URL("evaluador", "cuestionario_evaluacion"), **{'_data-target': "#cuestionario_evaluacion"})),
            ("cuestionario_desarrollo", False, A(CAT(XML('<ico class="glyphicon glyphicon-edit"></ico> '), T('Cuestionario de desarrollo')), _href=URL("evaluador", "cuestionario_desarrollo"), **{'_data-target': "#cuestionario_desarrollo"})),
            ("reportes_estadisticas_generales", False, A(CAT(XML('<ico class="glyphicon glyphicon-list-alt"></ico> '), T('Reportes de estadísticas generales')), _href=URL("reportes", "reportes_estadisticas_generales"), **{'_data-target': "#reportes_estadisticas_generales"})),
            ("reportes_estadisticas_personalizadas", False, A(CAT(XML('<ico class="glyphicon glyphicon-list-alt"></ico> '), T('Reportes de estadísticas personalizadas')), _href=URL("reportes", "reportes_estadisticas_personalizadas"), **{'_data-target': "#reportes_estadisticas_personalizadas"})),
            ("users_evaluador", False, A(CAT(XML('<ico class="glyphicon glyphicon-user"></ico> '), T('Administrar usuarios')), _href=URL("evaluador", "users_evaluador"), **{'_data-target': "#users_evaluador"})),
            ("centros_evaluador", False, A(CAT(XML('<ico class="glyphicon glyphicon-home"></ico> '), T('Administrar centros')), _href=URL("evaluador", "centros_evaluador"), **{'_data-target': "#centros_evaluador"})),
            ("nivel_atencional_evaluador", False, A(CAT(XML('<ico class="glyphicon glyphicon-th-list"></ico> '), T('Administrar niveles de atención')), _href=URL("evaluador", "nivel_atencional_evaluador"), **{'_data-target': "#nivel_atencional_evaluador"}))]
        )]
    else:
        if (auth.user_id):
            response.menu += [(CAT(XML('<ico class="glyphicon glyphicon-user"></ico> '), T('Estudiante')), False, URL(), [
                ("reportes_estadisticas_generales", False, A(CAT(XML('<ico class="glyphicon glyphicon-list-alt"></ico> '), T('Reportes de estadísticas generales')), _href=URL("reportes", "reportes_estadisticas_generales"), **{'_data-target': "#reportes_estadisticas_generales"})),
                ("cuestionario_diagnostico", False, A(CAT(XML('<ico class="glyphicon glyphicon-edit"></ico> '), T('Cuestionario Diagnóstico ')), _href=URL("estudiante", "cuestionario_diagnostico"), **{'_data-target': "#cuestionario_diagnostico"})),
                ("cuestionario_desarrollo", False, A(CAT(XML('<ico class="glyphicon glyphicon-edit"></ico> '), T('Cuestionario de desarrollo')), _href=URL("estudiante", "cuestionario_desarrollo"), **{'_data-target': "#cuestionario_desarrollo"})),
                ("nivel_atencion", False, A(CAT(XML('<ico class="glyphicon glyphicon-th-list"></ico> '), T('Nivel de atención')), _href=URL("estudiante", "nivel_atencion"), **{'_data-target': "#nivel_atencion"})),
              ]
            )]
        else:
            response.menu += [(CAT(XML('<ico class="glyphicon glyphicon-user"></ico> '), T('Reportes')), False, URL(), [
                ("reportes_estadisticas_generales", False, A(CAT(XML('<ico class="glyphicon glyphicon-list-alt"></ico> '), T('Reportes de estadísticas generales')), _href=URL("reportes", "reportes_estadisticas_generales"), **{'_data-target': "#reportes_estadisticas_generales"})),
                ]
            )]

if PRODUCTION_MENU:
    _()
