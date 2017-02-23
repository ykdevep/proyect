# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations
def get_pregunta():
    '''
    Componente que devuelve las preguntas de un tipo dado para el cuestionario activo
    '''
    if request.cid:
        preguntas = db((db.pregunta.diagnostico == request.args(0)) & (db.pregunta.tipo == request.args(1))).select(orderby=db.pregunta.ensayo|db.pregunta.created_on)
        return dict(preguntas=preguntas)
    else:
        raise HTTP(403)

def __total_puntos(id):
    '''
    Calculando total de puntos de un cuestionario
    '''
    suma = db.pregunta.puntos.sum()
    puntos = db(db.pregunta.diagnostico == id).select(suma).first()[suma]
    return A(CAT(XML('<i class="glyphicon glyphicon-ok"></i> '), puntos), _class="btn btn-warning", **{'_data-toggle': "tooltip", '_title': T("Total de puntos del cuestionario"), '_data-placement': "top"})

@auth.requires_membership("Especialista")
def gestionar_diagnostico():
    '''
    CRUD completo para gestionar diagnosticos kike tiene que ser asi
    '''

    diagnostico = preguntas = selectable = orderby = total_puntos = fields = None
    links = []
    linked_tables=[]

    if (("pregunta.diagnostico" in request.args) and not("pregunta" in request.args)):
        response.title = T('Gestionar preguntas del diagnóstico') + response.title
        response.flash = T('Gestionar preguntas del diagnóstico')
        mensaje = T('Gestionar preguntas del diagnóstico con identificador: ') + request.args(-1)
        diagnostico = db.diagnostico(request.args(2))
        total_puntos = __total_puntos(diagnostico.id)
        preguntas = diagnostico.pregunta.select(orderby=db.pregunta.tipo|db.pregunta.ensayo)
        selectable = lambda ids: db(db.pregunta.id.belongs(ids)).delete()
        orderby = [db.pregunta.tipo|db.pregunta.ensayo|db.pregunta.created_on]
        fields = [db.pregunta.texto, db.pregunta.tipo, db.pregunta.ensayo, db.pregunta.puntos, db.pregunta.tiempo]
    elif (("pregunta.diagnostico" in request.args) and ("pregunta" in request.args) and ("new" in request.args)):
        response.title = T('Pregunta del diagnóstico') + response.title
        response.flash = T('Pregunta del diagnóstico')
        mensaje = T('Pregunta del diagnóstico')
    elif (("pregunta.diagnostico" in request.args) and ("pregunta" in request.args) and ("view" in request.args)):
        response.title = T('Pregunta del diagnóstico') + response.title
        response.flash = T('Pregunta del diagnóstico')
        mensaje = T('Pregunta del diagnóstico')
    elif (("pregunta.diagnostico" in request.args) and ("pregunta" in request.args) and ("edit" in request.args)):
        response.title = T('Pregunta del diagnóstico') + response.title
        response.flash = T('Pregunta del diagnóstico')
        mensaje = T('Pregunta del diagnóstico')
    else:
        response.title = T('Gestionar Diagnósticos') + response.title
        response.flash = T('Gestionar Diagnósticos')
        mensaje = T('Gestionar Diagnósticos')
        selectable = lambda ids: db(db.diagnostico.id.belongs(ids)).delete()
        orderby = [db.diagnostico.tipo|~db.diagnostico.activo]
        linked_tables = [db.pregunta]

        links.append({'header': T('Total de puntos'), 'body': lambda row: __total_puntos(row.id)})

    grid = SQLFORM.smartgrid(db.diagnostico, selectable=selectable, linked_tables=linked_tables, links=links, fields=fields, orderby=orderby)

    heading=grid.elements('th')
    if heading:
           heading[0].append(INPUT(_type='checkbox', _onclick="jQuery('input[type=checkbox]').each(function(k){jQuery(this).attr('checked', 'checked');});"))

    return dict(grid=grid, mensaje=mensaje, diagnostico=diagnostico, preguntas=preguntas, total_puntos=total_puntos)

@auth.requires_membership("Especialista")
def nuevo_diagnostico_inicial():
    response.flash = T("Nuevo Diagnóstico Inicial")
    response.title = T("Nuevo Diagnóstico Inicial") + response.title

    form = SQLFORM(db.diagnostico, fields=['titulo', 'descripcion' 'activo', 'tiempo'])

    if form.validate():
        diagnostico = dict(form.vars)
        diagnostico['tipo'] = 0
        form.vars.id = db.diagnostico.insert(**diagnostico)

        response.flash = T('Nuevo cuestionario Diagnóstico Inicial insertado')

    elif form.errors:
        response.flash = T('El formulario tiene errores')
    else:
        response.flash = T('Por favor complete el formulario')
    return dict(form=form)
