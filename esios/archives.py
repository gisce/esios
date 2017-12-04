# -*- coding: utf-8 -*-
from datetime import datetime
from dateutil import relativedelta

from libsaas import http, parsers, port
from libsaas.services import base

from esios.utils import translate_param, serialize_param


LIQUICOMUN_PRIORITY = [
    'C7', 'A7', 'C6', 'A6', 'C5', 'A5', 'C4', 'A4', 'C3', 'A3', 'C2', 'A2',
    'C1', 'A1'
]


def parser_none(body, code, headers):
    return body


class Archive(base.RESTResource):
    path = 'archives'

    def get_filename(self):
        return self.__class__.__name__

    def order_key_function(self, param):
        return param['name']

    def validate_range(self, start, end):
        return True

    @base.apimethod
    def get(self, start_date, end_date, taxonomy_terms=None):
        assert isinstance(start_date, datetime)
        assert isinstance(end_date, datetime)
        if taxonomy_terms is None:
            taxonomy_terms = []
        assert isinstance(taxonomy_terms, (list, tuple))

        assert self.validate_range(start_date, end_date), "Dates are not in the expected range for the requested version"
        date_type = 'datos'
        start_date = start_date.isoformat()
        end_date = end_date.isoformat()
        locale = 'en'
        param_list = ('locale', 'start_date', 'end_date', 'date_type')
        if taxonomy_terms:
            param_list += ('taxonomy_terms',)
        params = base.get_params(
            param_list,
            locals(),
            translate_param=translate_param,
            serialize_param=serialize_param,
        )
        request = http.Request('GET', self.get_url(), params)

        return request, parsers.parse_json

    @base.apimethod
    def download(self, start_date, end_date, taxonomy_terms=None):
        assert isinstance(start_date, datetime)
        assert isinstance(end_date, datetime)
        if taxonomy_terms is None:
            taxonomy_terms = []
        assert isinstance(taxonomy_terms, (list, tuple))
        # gets filename from class name
        filename = self.get_filename()

        body = self.get(start_date, end_date, taxonomy_terms)
        regs = [a for a in body['archives'] if filename in a['name']]

        sorted_list = sorted(regs, key=self.order_key_function)
        # gets last (better) file
        url = sorted_list[0]['download']['url']

        request = http.Request('GET', self.parent.get_url() + url)

        return request, parser_none


class Liquicomun(Archive):

    def get_filename(self):
        return super(Liquicomun, self).get_filename().lower()

    def order_key_function(self, param):
        return LIQUICOMUN_PRIORITY.index(param['name'][:2])

    def get(self, start_date, end_date, taxonomy_terms=None):
        if taxonomy_terms is None:
            taxonomy_terms = []
        taxonomy_terms.append('Settlements')
        return super(Liquicomun, self).get(start_date, end_date, taxonomy_terms)


class Generic_Liquicomun(Archive):
    """ Generic Liquicomun class, suitable to subsitute Liquicomun, pending to clarify """

    # Liquicomun version
    version = None

    def order_key_function(self, param):
        if type(param) == list:
            param = param[0]
        name = param['name']

        assert name[:2] == self.version, "Expected version must be '{}', current '{}' ['{}']". format(self.version, name[:2], name)
        return LIQUICOMUN_PRIORITY.index(name[:2])


    def validate_range(self, start, end):
        pass


class A1_liquicomun(Generic_Liquicomun):
    """ This month and future """

    version = "A1"
    def validate_range(self, start, end):
        ## Validate range for A1 period (this month & future)
        ### toDo acotar future

        today = datetime.today()
        try:
            first_day_current_month = datetime(today.year, today.month, 1)
            assert start >= first_day_current_month

            last_day_current_month = first_day_current_month + relativedelta.relativedelta(months=1) - relativedelta.relativedelta(days=1)
            assert end <= last_day_current_month
        except:
            return False

        return True


class A2_liquicomun(Generic_Liquicomun):
    """ This month and future """

    version = "A2"
    def validate_range(self, start, end):
        ## Validate range for A2 period (just previous month)
        ### toDo acotar future
        today = datetime.today()
        try:
            first_day_previous_month = datetime(today.year, today.month, 1) - relativedelta.relativedelta(months=1)
            assert start >= first_day_previous_month

            last_day_previous_month = first_day_previous_month + relativedelta.relativedelta(months=1) - relativedelta.relativedelta(days=1)
            assert end <= last_day_previous_month
        except:
            return False

        return True
