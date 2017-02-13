# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations
def __validate(form, id_diagnostico, id_pregunta):
    '''
    Validando que exista un solo tipo de pregunta por cuestionario
    '''
    if id_pregunta:
        pregunta = db((db.pregunta.diagnostico == id_diagnostico) & (db.pregunta.tipo == form.vars.tipo)).select().first()
        if pregunta:
            if str(pregunta.id) != id_pregunta:
                form.errors.tipo = T("Ya existe una pregunta de tipo para este cuestionario")
    else:
        if not (db((db.pregunta.diagnostico == id_diagnostico) & (db.pregunta.tipo == form.vars.tipo)).isempty()):
            form.errors.tipo = T("Ya existe una pregunta de tipo para este cuestionario")

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

    diagnostico = preguntas = onvalidation = selectable = orderby = fields = None
    links = []
    linked_tables=[]

    if (("pregunta.diagnostico" in request.args) and not("pregunta" in request.args)):
        response.title = T('Gestionar preguntas del diagnóstico') + response.title
        response.flash = T('Gestionar preguntas del diagnóstico')
        mensaje = T('Gestionar preguntas del diagnóstico con identificador: ') + request.args(-1)
        diagnostico = db.diagnostico(request.args(2))
        preguntas = diagnostico.pregunta.select(orderby=db.pregunta.tipo)
        selectable = lambda ids: db(db.pregunta.id.belongs(ids)).delete()
        orderby = [db.pregunta.tipo]
        fields = [db.pregunta.id, db.pregunta.descripcion, db.pregunta.tipo, db.pregunta.puntos, db.pregunta.tiempo]
        onvalidation = lambda form : __validate(form, request.args(2), None)
    elif (("pregunta.diagnostico" in request.args) and ("pregunta" in request.args) and ("new" in request.args)):
        response.title = T('Pregunta del diagnóstico') + response.title
        response.flash = T('Pregunta del diagnóstico')
        mensaje = T('Pregunta del diagnóstico')
        onvalidation = lambda form : __validate(form, request.args(2), None)
    elif (("pregunta.diagnostico" in request.args) and ("pregunta" in request.args) and ("view" in request.args)):
        response.title = T('Pregunta del diagnóstico') + response.title
        response.flash = T('Pregunta del diagnóstico')
        mensaje = T('Pregunta del diagnóstico')
        onvalidation = lambda form : __validate(form, request.args(2), None)
    elif (("pregunta.diagnostico" in request.args) and ("pregunta" in request.args) and ("edit" in request.args)):
        response.title = T('Pregunta del diagnóstico') + response.title
        response.flash = T('Pregunta del diagnóstico')
        mensaje = T('Pregunta del diagnóstico')
        onvalidation = lambda form : __validate(form, request.args(2), request.args(-1))
    else:
        response.title = T('Gestionar Diagnósticos') + response.title
        response.flash = T('Gestionar Diagnósticos')
        mensaje = T('Gestionar Diagnósticos')
        selectable = lambda ids: db(db.diagnostico.id.belongs(ids)).delete()
        orderby = [db.diagnostico.tipo|~db.diagnostico.activo]
        linked_tables = [db.pregunta]

        links.append({'header': T('Total de puntos'), 'body': lambda row: __total_puntos(row.id)})

    grid = SQLFORM.smartgrid(db.diagnostico, selectable=selectable, linked_tables=linked_tables, links=links, fields=fields, orderby=orderby, onvalidation=onvalidation)

    heading=grid.elements('th')
    if heading:
           heading[0].append(INPUT(_type='checkbox', _onclick="jQuery('input[type=checkbox]').each(function(k){jQuery(this).attr('checked', 'checked');});"))

    return dict(grid=grid, mensaje=mensaje, diagnostico=diagnostico, preguntas=preguntas)

@auth.requires_membership("Especialista")
def nuevo_diagnostico_inicial():
    response.flash = T("Nuevo Diagnóstico Inicial")
    response.title = T("Nuevo Diagnóstico Inicial") + response.title

    form = SQLFORM(db.diagnostico, fields=['titulo', 'descripcion', 'activo'])

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
