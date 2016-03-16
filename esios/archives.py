# -*- coding: utf-8 -*-
from datetime import datetime
import json

from libsaas import http, parsers, port
from libsaas.services import base


def parser_none(body, code, headers):
    return body


class Archive(base.RESTResource):
    path = 'archives'

    def get_filename(self):
        return self.__class__.__name__

    @base.apimethod
    def get(self, start_date, end_date):
        assert isinstance(start_date, datetime)
        assert isinstance(end_date, datetime)
        date_type = 'datos'
        start_date = start_date.isoformat()
        end_date = end_date.isoformat()
        params = base.get_params(
            ('start_date', 'end_date', 'date_type'), locals()
        )
        request = http.Request('GET', self.get_url(), params)

        return request, parsers.parse_json

    @base.apimethod
    def download(self, start_date, end_date):
        assert isinstance(start_date, datetime)
        assert isinstance(end_date, datetime)
        # gets filename from class name
        filename = self.get_filename()

        body = self.get(start_date, end_date)
        regs = [a for a in body['archives'] if filename in a['name']]
        sorted_list = sorted(regs, key=lambda k: k['name'])
        # gets last (better) file
        url = sorted_list[-1]['download']['url']

        request = http.Request('GET', self.parent.get_url() + url)

        return request, parser_none


class Liquicomun(Archive):

    def get_filename(self):
        return super(Liquicomun, self).get_filename().lower()

class A1_liquicomun(Archive):
    pass
