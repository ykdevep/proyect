# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

# -------------------------------------------------------------------------
# This is a sample controller
# - index is the default action of any application
# - user is required for authentication and authorization
# - download is for downloading files uploaded in the db (does streaming)
# -------------------------------------------------------------------------


@auth.requires_login()
def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html

    if you need a simple wiki simply replace the two lines below with:
    return auth.wiki()
    """
    response.title = T("Home page") + response.title
    return dict()


def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    also notice there is http://..../[app]/appadmin/manage/auth to allow administrator to manage users
    """
    response.title = T("Autenticación | SIMEAT")

    '''form_login = FORM(INPUT(_name='email', _class="form-control form-login wow fadeInLeft", _placeholder=T("Correo"), requires=IS_NOT_EMPTY()),
                      INPUT(_name='password', _class="form-control form-login wow fadeInRight", _type="password", _placeholder=T("Contraseña"),requires=IS_NOT_EMPTY()),
                      INPUT(_type='submit', _value=T("Ingresar"), _class="wow fadeInLeft"), _class="waves-light")

    if form_login.accepts(request,session):
        user = auth.login_bare(form_login.vars.email, form_login.vars.password)
        if user:
            redirect(request.vars._next)
        else:
            response.flash = T('Usuario o contraseña no válidos')
    elif form_login.errors:
        response.flash = T('El formulario tiene errores')
    else:'''

    return dict(form=auth())


@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()
