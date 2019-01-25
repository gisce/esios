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
    def download(self, start_date, end_date, taxonomy_terms=None, next=0):
        """
        Download the best available version for a range of dates and the desired taxonomy terms.A1_liquicomun

        Optionally fetch the next (n) available version instead of the higher one (next=1, 2, 3, ..., n)
        """
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

        # Assert that desired next exists, and fetch it
        assert type(next) == int and next >= 0, "Desired next value is not correct."
        assert (len(sorted_list) >= next + 1), "The desired version (next +{}) is not available. Available versions '{}'".format(next, ", ".join ([name['name'][:2] for name in sorted_list]))
        url = sorted_list[next]['download']['url']

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
    expected_range_start = None
    expected_range_end = None

    def order_key_function(self, param):
        if type(param) == list:
            param = param[0]
        name = param['name']

        assert name[:2] == self.version, "Expected version must be '{}', current '{}' ['{}']". format(self.version, name[:2], name)
        return LIQUICOMUN_PRIORITY.index(name[:2])


    def validate_range(self, start, end):
        """ Validate range for generic period """
        try:
            assert start >= self.expected_range_start
            assert end <= self.expected_range_end
        except:
            return False

        return True


class A1_liquicomun(Generic_Liquicomun):
    """ A1: This month and future """
    ### toDo acotar future
    version = "A1"

    # First day of current month
    expected_range_start = datetime.today().replace(day=1, hour=0, minute=0, second=0, microsecond=0)

    # Last day of current month
    expected_range_end = expected_range_start + relativedelta.relativedelta(months=2) - relativedelta.relativedelta(days=1)


class A2_liquicomun(Generic_Liquicomun):
    """ A2: Just previous month """
    version = "A2"

    # First day of -1 month
    expected_range_start = datetime.today().replace(day=1, hour=0, minute=0, second=0, microsecond=0) - relativedelta.relativedelta(months=1)

    # Last day of -1 month
    expected_range_end = datetime.today()


class C2_liquicomun(Generic_Liquicomun):
    """ C2: <=-2months last day to <=-2months last day """
    version = "C2"

    # Last day of -2 month
    expected_range_start = datetime.today().replace(day=1, hour=0, minute=0, second=0, microsecond=0) - relativedelta.relativedelta(months=1) - relativedelta.relativedelta(days=1)

    # Last day of -2 month
    expected_range_end = expected_range_start

    def validate_range(self, start, end):
        """ Validate C2 range  start < 31/-2n and end <= 31/-2n """
        try:
            assert start <= self.expected_range_start
            assert end <= self.expected_range_end
        except:
            return False

        return True
