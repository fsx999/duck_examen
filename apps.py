# coding=utf-8
from django.apps import AppConfig


class DuckExamen(AppConfig):
    name = "duck_examen"
    label = 'duck_examen'

    collapse_settings = [{
        "group_label": "Duck Examen",
        "icon": 'fa-fw fa fa-circle-o',
        "entries": [{
            "label": 'Etape settings deroule models',
            "icon": 'fa-fw fa fa-circle-o',
            "url": '/duck_examen/etapesettingsderoulemodel/',  # name or url
            "groups_permissions": [],  # facultatif
            "permissions": [],  # facultatif
        }, {
            "label": 'Type examens',
            "icon": 'fa-fw fa fa-circle-o',
            "url": '/duck_examen/typeexamen/',  # name or url
            "groups_permissions": [],  # facultatif
            "permissions": [],  # facultatif
        }, {
            "label": 'Parcours',
            "icon": 'fa-fw fa fa-circle-o',
            "url": '/duck_examen/parcours/',  # name or url
            "groups_permissions": [],  # facultatif
            "permissions": [],  # facultatif
        }],

        "groups_permissions": [],  # facultatif
        "permissions": [],  # facultatif
    },]