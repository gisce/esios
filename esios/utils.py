# -*- coding: utf-8 -*-
from libsaas.services import base


def serialize_param(val):
    """ To use in get_params """
    if isinstance(val, (tuple, list)):
        # Only first element
        if val:
            return val[0]
        else:
            return ''
    else:
        return base.serialize_param(val)


def translate_param(val):
    """ To use in get_params """
    if val in ['taxonomy_terms']:
        return '{0}[]'.format(val)
    else:
        return val
