from expects.testing import failure
from expects import *

from datetime import datetime, timedelta
from dateutil import relativedelta
import calendar
import zipfile
from io import BytesIO
import json
import os

from esios import Esios
from esios.archives import Liquicomun, A1_liquicomun, A2_liquicomun, C2_liquicomun
from esios.archives import P48Cierre


def test_expected_to_work(the_class, start, end, expected_versions, next=0):
    """
    General expected to work method
    """
    res = the_class().download(start, end, next=next)

    c = BytesIO(res)
    zf = zipfile.ZipFile(c)
    assert zf.testzip() is None
    assert zf.namelist()[0][:2] in expected_versions
    return True


def test_expected_to_break(the_class, start, end, assert_message, next=0):
    """
    General assert to break method
    """
    it_works = True
    try:
        res = the_class().download(start, end, next=next)
    except:
        it_works = False

    assert not it_works, assert_message
    return True

def validate_P48cierre(xml):
    xsd_path = 'esios/data'
    xsd_file = 'P48Cierre-esios-MP.xsd'

    from lxml import etree, objectify
    from lxml.etree import XMLSyntaxError

    xmlschema_doc = etree.parse(xsd_path + '/' + xsd_file)
    xmlschema = etree.XMLSchema(xmlschema_doc)

    parser = objectify.makeparser(schema=xmlschema)
    try:
        objectify.fromstring(xml, parser)
        return True
    except XMLSyntaxError as e:
        return False


with description('Base Liquicomun'):
    with before.all:
        ESIOS_TOKEN = os.getenv('ESIOS_TOKEN')
        self.token = ESIOS_TOKEN

        self.today = datetime.today()

        self.e = Esios(self.token)

    with context('Instance'):
        with it('Returns liquicomun instance'):
            liqui = Liquicomun(self.e)
            assert isinstance(liqui, Liquicomun)

        with it('Gets list'):
            today = self.today
            start = datetime(today.year, today.month, 1)
            last_month_day = calendar.monthrange(today.year, today.month)[1]
            end = datetime(today.year, today.month, last_month_day)

            res = self.e.liquicomun().get(start, end)
            assert len(res) >= 0

        with it('Gets current liquicomun'):
            today = self.today
            start = datetime(today.year, today.month, 1)
            last_month_day = calendar.monthrange(today.year, today.month)[1]
            end = datetime(today.year, today.month, last_month_day)

            expected_versions = ('A1', 'A2')
            assert test_expected_to_work(the_class=self.e.liquicomun, start=start, end=end, expected_versions=expected_versions)

        with it('should download C2 or A3 for 3 months ago'):
            today = self.today - timedelta(days=93)
            start = datetime(today.year, today.month, 1)
            last_month_day = calendar.monthrange(start.year, start.month)[1]
            end = datetime(start.year, start.month, last_month_day)

            expected_versions = ('A3', 'C2')
            assert test_expected_to_work(the_class=self.e.liquicomun, start=start, end=end, expected_versions=expected_versions)

        with it('should download C6 o C5 for a year ago'):
            today = self.today - timedelta(days=730)
            start = datetime(today.year, today.month, 1)
            last_month_day = calendar.monthrange(start.year, start.month)[1]
            end = datetime(start.year, start.month, last_month_day)

            expected_versions = ('A5', 'A6', 'C6', 'C5')
            assert test_expected_to_work(the_class=self.e.liquicomun, start=start, end=end, expected_versions=expected_versions)

        with it('should download C7,A7,C6,A6,C5 or A5 for a long time ago'):
            today = self.today - timedelta(days=730)
            start = datetime(today.year, today.month, 1)
            last_month_day = calendar.monthrange(start.year, start.month)[1]
            end = datetime(start.year, start.month, last_month_day)

            expected_versions = ('A7', 'C7', 'A6', 'C6', 'C5', 'A5')
            assert test_expected_to_work(the_class=self.e.liquicomun, start=start, end=end, expected_versions=expected_versions)


    with context('A1 instance'):
        with it('can get the A1 for a valid date'):
            today = self.today
            start = datetime(today.year, today.month, 1) + relativedelta.relativedelta(months=1)
            end = start + relativedelta.relativedelta(months=1) - relativedelta.relativedelta(days=1)

            expected_versions = ('A1')
            assert test_expected_to_work(the_class=self.e.A1_liquicomun, start=start, end=end, expected_versions=expected_versions)


        with it('can\'t get the A1 for an invalid date'):
            today = self.today

            # Previous month
            start = datetime(today.year, today.month, 1) - relativedelta.relativedelta(months=1)
            end = start + relativedelta.relativedelta(months=1) - relativedelta.relativedelta(days=1)

            error_message = "A1 for previous month must not work! This must be an A2"
            assert test_expected_to_break(the_class=self.e.A1_liquicomun, start=start, end=end, assert_message=error_message)


    with context('A2 instance'):
        with it('can get the related A2 for a valid date'):
            today = self.today

            # today
            start = end = datetime(today.year, today.month, today.day)
            expected_versions = ('A2')
            assert test_expected_to_work(the_class=self.e.A2_liquicomun, start=start, end=end, expected_versions=expected_versions)


        with it('can\'t get the related A2 for an invalid date'):
            today = self.today

            # This month
            start = datetime(today.year, today.month, 1)
            end = start + relativedelta.relativedelta(months=1) - relativedelta.relativedelta(days=1)

            error_message = "A2 for this month must not work! This must be an A1"
            assert test_expected_to_break(the_class=self.e.A2_liquicomun, start=start, end=end, assert_message=error_message)


    with context('C2 instance'):
        with it('can get the C2 for a valid date'):
            today = self.today

            # Previous month
            start = datetime(today.year, today.month, 1) - relativedelta.relativedelta(months=2)
            end = start + relativedelta.relativedelta(months=1) - relativedelta.relativedelta(days=1)

            expected_versions = ('C2')
            assert test_expected_to_work(the_class=self.e.C2_liquicomun, start=start, end=end, expected_versions=expected_versions)


        with it('can\'t get the C2 for an invalid date'):
            today = self.today

            # This month
            start = datetime(today.year, today.month, 1)
            end = start + relativedelta.relativedelta(months=1) - relativedelta.relativedelta(days=1)

            error_message = "C2 for this month must not work! This must be an A1"
            assert test_expected_to_break(the_class=self.e.C2_liquicomun, start=start, end=end, assert_message=error_message)


    with context('Instance with next'):
        with before.all:
            # Expected C5, C4, C3, C2
            self.expected_version_list = ["C5", "C4", "C3", "C2"]
            today = self.today

            # A year ago
            self.start = datetime(today.year, today.month, 1) - relativedelta.relativedelta(months=12)
            self.end = self.start + relativedelta.relativedelta(months=1) - relativedelta.relativedelta(days=1)

        with it('can get the n=0 //a C5'):
            next = 0
            expected_versions = self.expected_version_list[next] # "C5"
            assert test_expected_to_work(the_class=self.e.liquicomun, start=self.start, end=self.end, expected_versions=expected_versions, next=next)

        with it('can get the n=1 //a C4'):
            next = 1
            expected_versions = self.expected_version_list[next] # "C4"
            assert test_expected_to_work(the_class=self.e.liquicomun, start=self.start, end=self.end, expected_versions=expected_versions, next=next)

        with it('can get the n=2 //a C3'):
            next = 1
            expected_versions = self.expected_version_list[next] # "C4"
            assert test_expected_to_work(the_class=self.e.liquicomun, start=self.start, end=self.end, expected_versions=expected_versions, next=next)

        with it('can get the n=3 //a C2'):
            next = 3
            expected_versions = self.expected_version_list[next] # "C4"
            assert test_expected_to_work(the_class=self.e.liquicomun, start=self.start, end=self.end, expected_versions=expected_versions, next=next)

        with it('can\'t get the n=4 //last is n=3 C2!'):
            next = 4
            expected = "irreal"
            error_message = "The next 4 version for one year ago must not exist. Available '{}'".format(self.expected_version_list)
            assert test_expected_to_break(the_class=self.e.liquicomun, start=self.start, end=self.end, assert_message=error_message, next=next)

        with it('can\'t get the n=-1'):
            next = -1
            expected = "irreal"
            error_message = "Negative next version must break"
            assert test_expected_to_break(the_class=self.e.liquicomun, start=self.start, end=self.end, assert_message=error_message, next=next)


with description('P48Cierre'):
    with before.all:
        ESIOS_TOKEN = os.getenv('ESIOS_TOKEN')
        self.token = ESIOS_TOKEN

        self.today = datetime.today()

        self.e = Esios(self.token)

    with context('Instance'):
        with it('Returns P48Cierre instance'):
            liqui = P48Cierre(self.e)
            assert isinstance(liqui, P48Cierre)

        with it('Gets list'):
            today = self.today
            start = datetime(today.year, today.month, 1)
            last_month_day = calendar.monthrange(today.year, today.month)[1]
            end = datetime(today.year, today.month, last_month_day)

            res = self.e.p48cierre().get(start, end)
            assert len(res) >= 0

        with it('Gets Yesterday p48'):
            today = self.today

            start = today.replace(hour=0, minute=0, second=0, microsecond=0) - relativedelta.relativedelta(days=1)
            end = today.replace(hour=23, minute=59, second=59, microsecond=0) - relativedelta.relativedelta(days=1)
            res = P48Cierre(self.e).download(start, end)

            assert validate_P48cierre(res)
            assert not validate_P48cierre(res + b'ERROR')

        with it('Gets today and yesterday p48'):
            today = self.today

            start = today.replace(hour=0, minute=0, second=0, microsecond=0) - relativedelta.relativedelta(days=1)
            end = today.replace(hour=23, minute=59, second=59, microsecond=0)
            res = P48Cierre(self.e).download(start, end)

            c = BytesIO(res)
            zf = zipfile.ZipFile(c)
            assert zf.testzip() is None
            expected_filenames = [
                'p48cierre_{}.xml'.format(start.strftime('%Y%m%d')),
                'p48cierre_{}.xml'.format(end.strftime('%Y%m%d')),
                'p48_{}'.format(today.strftime('%Y%m%d'))]

            assert len(zf.namelist()) == 2
            for filename in zf.namelist():
                if len(filename) == 22:
                    assert filename in expected_filenames
                else:
                    assert filename[:12] in expected_filenames

        with it('Gets current month p48'):
            today = self.today
            start = datetime(today.year, today.month, 1)
            last_month_day = calendar.monthrange(today.year, today.month)[1]
            end = datetime(today.year, today.month, today.day > 1 and today.day - 1 or 1)

            res = P48Cierre(self.e).download(start, end)

            c = BytesIO(res)
            zf = zipfile.ZipFile(c)
            assert zf.testzip() is None
            expected_filenames = []
            for day in range(0, today.day):
                p48_day = start + relativedelta.relativedelta(days=day)
                expected_filenames.append('p48cierre_{}.xml'.format(p48_day.strftime('%Y%m%d')))

            assert len(zf.namelist()) == today.day - 1
            for filename in zf.namelist():
                    assert filename in expected_filenames
