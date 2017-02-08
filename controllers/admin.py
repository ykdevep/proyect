# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations
@auth.requires_membership("Administrador")
def index():
    
    return dict()


@auth.requires_membership("Administrador")
def users():
    selectable = lambda ids: db(db.auth_user.id.belongs(ids)).delete()

    fields = [db.auth_user.first_name, db.auth_user.email, db.auth_user.centro]

    grid = SQLFORM.smartgrid(db.auth_user, selectable=selectable, linked_tables=[db.auth_membership], exportclasses=dict(xml=False, html=False, json=False, csv_with_hidden_cols=False, tsv_with_hidden_cols=False))

    response.flash = T("Administrar usuarios")
    response.title = T("Administrar usuarios") + response.title

    heading=grid.elements('th')
    if heading:
           heading[0].append(INPUT(_type='checkbox', _onclick="jQuery('input[type=checkbox]').each(function(k){jQuery(this).attr('checked', 'checked');});"))
    return dict(grid=grid)

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
def banners():
    selectable = lambda ids: db(db.banner.id.belongs(ids)).delete()

    fields = [db.banner.titulo, db.banner.imagen, db.banner.publicar_en, db.banner.habilitado]

    grid = SQLFORM.smartgrid(db.banner, selectable=selectable, linked_tables=[], exportclasses=dict(xml=False, html=False, json=False, csv_with_hidden_cols=False, tsv_with_hidden_cols=False))

    response.flash = T("Administrar banners")
    response.title = T("Administrar Banners") + response.title

    heading=grid.elements('th')
    if heading:
           heading[0].append(INPUT(_type='checkbox', _onclick="jQuery('input[type=checkbox]').each(function(k){jQuery(this).attr('checked', 'checked');});"))
    return dict(grid=grid)
