# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

def show_carousel():
    """
    Componente que permite mostrar los banners habilitados
    """
    if request.cid:
        import datetime
        banners = db((db.banner.publicar_en <= datetime.datetime.today()) & (db.banner.habilitado == True) & (db.banner.imagen != "")).select(orderby =~ db.banner.publicar_en, limitby=(0,10), cache=(cache.ram, 60), cacheable=True)
        return dict(banners=banners)        
    else:
        raise HTTP(403)