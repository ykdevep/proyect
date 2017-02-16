# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

@auth.requires_membership("Administrador")
def users():
    selectable = lambda ids: db(db.auth_user.id.belongs(ids)).delete()

    fields = [db.auth_user.first_name, db.auth_user.email]

    grid = SQLFORM.smartgrid(db.auth_user, selectable=selectable, linked_tables=[db.auth_membership], exportclasses=dict(xml=False, html=False, json=False, csv_with_hidden_cols=False, tsv_with_hidden_cols=False))

    response.flash = T("Administrar usuarios")
    response.title = T("Administrar usuarios") + response.title

    heading=grid.elements('th')
    if heading:
           heading[0].append(INPUT(_type='checkbox', _onclick="jQuery('input[type=checkbox]').each(function(k){jQuery(this).attr('checked', 'checked');});"))
    return dict(grid=grid)

@auth.requires_membership("Administrador")
def new_admin():

    response.title = T("Nuevo Administrador") + response.title

    form = SQLFORM(db.auth_user)

    if form.validate():
        group = db(db.auth_group.role == "Administrador").select().first()

        if group:
            form.vars.id = db.auth_user.insert(**dict(form.vars))
            db.auth_membership.insert(user_id=form.vars.id, group_id=group.id)
            response.flash = T('Nuevo Administrador insertado')
        else:
            response.flash = T('No hay grupo denominado "Administrador"')
    elif form.errors:
        response.flash = T('El formulario tiene errores')
    else:
        response.flash = T('Por favor complete el formulario')
    return dict(form=form)

@auth.requires_membership("Administrador")
def new_student():

    response.title = T("Nuevo Estudiante") + response.title

    form = SQLFORM(db.auth_user)

    if form.validate():
        group = db(db.auth_group.role == "Estudiante").select().first()

        if group:
            form.vars.id = db.auth_user.insert(**dict(form.vars))
            db.auth_membership.insert(user_id=form.vars.id, group_id=group.id)
            response.flash = T('Nuevo Estudiante insertado')
        else:
            response.flash = T('No hay grupo denominado "Estudiante"')
    elif form.errors:
        response.flash = T('El formulario tiene errores')
    else:
        response.flash = T('Por favor complete el formulario')
    return dict(form=form)

@auth.requires_membership("Especialista")
def new_revisor():

    response.title = T("Nuevo Especialista") + response.title

    form = SQLFORM(db.auth_user)

    if form.validate():
        group = db(db.auth_group.role == "Especialista").select().first()

        if group:
            form.vars.id = db.auth_user.insert(**dict(form.vars))
            db.auth_membership.insert(user_id=form.vars.id, group_id=group.id)
            response.flash = T('Nuevo Especialista insertado')
        else:
            response.flash = T('No hay grupo denominado "Especialista"')
    elif form.errors:
        response.flash = T('El formulario tiene errores')
    else:
        response.flash = T('Por favor complete el formulario')
    return dict(form=form)

@auth.requires_membership("Especialista")
def new_user():

    response.title = T("Nuevo Visitante") + response.title

    form = SQLFORM(db.auth_user)

    if form.validate():
        group = db(db.auth_group.role == "Visitante").select().first()

        if group:
            form.vars.id = db.auth_user.insert(**dict(form.vars))
            db.auth_membership.insert(user_id=form.vars.id, group_id=group.id)
            response.flash = T('Nuevo Visitante insertado')
        else:
            response.flash = T('No hay grupo denominado "Visitante"')
    elif form.errors:
        response.flash = T('El formulario tiene errores')
    else:
        response.flash = T('Por favor complete el formulario')
    return dict(form=form)

@auth.requires_membership("Administrador")
def centros():
    selectable = lambda ids: db(db.centro.id.belongs(ids)).delete()

    fields = [db.centro.nombre, db.centro.nivel_educativo, db.centro.direccion]

    grid = SQLFORM.smartgrid(db.centro, selectable=selectable, linked_tables=[], exportclasses=dict(xml=False, html=False, json=False, csv_with_hidden_cols=False, tsv_with_hidden_cols=False))

    response.flash = T("Administrar centros")
    response.title = T("Administrar Centros") + response.title

    heading=grid.elements('th')
    if heading:
           heading[0].append(INPUT(_type='checkbox', _onclick="jQuery('input[type=checkbox]').each(function(k){jQuery(this).attr('checked', 'checked');});"))
    return dict(grid=grid)

@auth.requires_membership("Administrador")
def logs():
    selectable = lambda ids: db(db.banner.id.belongs(ids)).delete()

    grid = SQLFORM.smartgrid(db.auth_event, selectable=selectable, linked_tables=[], exportclasses=dict(xml=False, html=False, json=False, csv_with_hidden_cols=False, tsv_with_hidden_cols=False))

    response.flash = T("Administrar logs")
    response.title = T("Administrar logs") + response.title

    heading=grid.elements('th')
    if heading:
           heading[0].append(INPUT(_type='checkbox', _onclick="jQuery('input[type=checkbox]').each(function(k){jQuery(this).attr('checked', 'checked');});"))
    return dict(grid=grid)
