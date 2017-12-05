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


def test_expected_to_work(the_class, start, end, expected_versions, next=0):
    """
    General expected to work method
    """
    res = the_class().download(start, end, next=next)

    c = BytesIO(res)
    zf = zipfile.ZipFile(c)
    assert zf.testzip() is None
    assert zf.namelist()[0][:2] in expected_versions



def test_expected_to_break(the_class, start, end, assert_message):
    """
    General assert to break method
    """
    it_works = True
    try:
        res = the_class().download(start, end)
    except:
        it_works = False

    assert not it_works, assert_message



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
            test_expected_to_work(the_class=self.e.liquicomun, start=start, end=end, expected_versions=expected_versions)
            
        with it('should download C2 or A3 for 3 months ago'):
            today = self.today - timedelta(days=93)
            start = datetime(today.year, today.month, 1)
            last_month_day = calendar.monthrange(start.year, start.month)[1]
            end = datetime(start.year, start.month, last_month_day)

            expected_versions = ('A3', 'C2')
            test_expected_to_work(the_class=self.e.liquicomun, start=start, end=end, expected_versions=expected_versions)

        with it('should download C6 o C5 for a year ago'):
            today = self.today - timedelta(days=730)
            start = datetime(today.year, today.month, 1)
            last_month_day = calendar.monthrange(start.year, start.month)[1]
            end = datetime(start.year, start.month, last_month_day)

            expected_versions = ('A5', 'A6', 'C6', 'C5')
            test_expected_to_work(the_class=self.e.liquicomun, start=start, end=end, expected_versions=expected_versions)

        with it('should download C7,A7,C6,A6,C5 or A5 for a long time ago'):
            today = self.today - timedelta(days=730)
            start = datetime(today.year, today.month, 1)
            last_month_day = calendar.monthrange(start.year, start.month)[1]
            end = datetime(start.year, start.month, last_month_day)

            expected_versions = ('A7', 'C7', 'A6', 'C6', 'C5', 'A5')
            test_expected_to_work(the_class=self.e.liquicomun, start=start, end=end, expected_versions=expected_versions)


    with context('A1 instance'):
        with it('can get the A1 for a valid date'):
            today = self.today
            start = datetime(today.year, today.month, 1)
            end = start + relativedelta.relativedelta(months=1) - relativedelta.relativedelta(days=1)


            expected_versions = ('A1')
            test_expected_to_work(the_class=self.e.A1_liquicomun, start=start, end=end, expected_versions=expected_versions)


        with it('can\'t get the A1 for an invalid date'):
            today = self.today

            # Previous month
            start = datetime(today.year, today.month, 1) - relativedelta.relativedelta(months=1)
            end = start + relativedelta.relativedelta(months=1) - relativedelta.relativedelta(days=1)

            error_message = "A1 for previous month must not work! This must be an A2"
            test_expected_to_break(the_class=self.e.A1_liquicomun, start=start, end=end, assert_message=error_message)


    with context('A2 instance'):
        with it('can get the related A2 for a valid date'):
            today = self.today

            # Previous month
            start = datetime(today.year, today.month, 1) - relativedelta.relativedelta(months=1)
            end = start + relativedelta.relativedelta(months=1) - relativedelta.relativedelta(days=1)

            expected_versions = ('A2')
            test_expected_to_work(the_class=self.e.A2_liquicomun, start=start, end=end, expected_versions=expected_versions)


        with it('can\'t get the related A2 for an invalid date'):
            today = self.today

            # This month
            start = datetime(today.year, today.month, 1)
            end = start + relativedelta.relativedelta(months=1) - relativedelta.relativedelta(days=1)

            error_message = "A2 for this month must not work! This must be an A1"
            test_expected_to_break(the_class=self.e.A2_liquicomun, start=start, end=end, assert_message=error_message)


    with context('C2 instance'):
        with it('can get the C2 for a valid date'):
            today = self.today

            # Previous month
            start = datetime(today.year, today.month, 1) - relativedelta.relativedelta(months=2)
            end = start + relativedelta.relativedelta(months=1) - relativedelta.relativedelta(days=1)

            expected_versions = ('C2')
            test_expected_to_work(the_class=self.e.C2_liquicomun, start=start, end=end, expected_versions=expected_versions)


        with it('can\'t get the C2 for an invalid date'):
            today = self.today

            # This month
            start = datetime(today.year, today.month, 1)
            end = start + relativedelta.relativedelta(months=1) - relativedelta.relativedelta(days=1)

            error_message = "C2 for this month must not work! This must be an A1"
            test_expected_to_break(the_class=self.e.C2_liquicomun, start=start, end=end, assert_message=error_message)


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
            test_expected_to_work(the_class=self.e.liquicomun, start=self.start, end=self.end, expected_versions=expected_versions, next=next)

        with it('can get the n=1 //a C4'):
            next = 1
            expected_versions = self.expected_version_list[next] # "C4"
            test_expected_to_work(the_class=self.e.liquicomun, start=self.start, end=self.end, expected_versions=expected_versions, next=next)
            
        with it('can get the n=2 //a C3'):
            next = 1
            expected_versions = self.expected_version_list[next] # "C4"
            test_expected_to_work(the_class=self.e.liquicomun, start=self.start, end=self.end, expected_versions=expected_versions, next=next)

        with it('can get the n=3 //a C2'):
            next = 3
            expected_versions = self.expected_version_list[next] # "C4"
            test_expected_to_work(the_class=self.e.liquicomun, start=self.start, end=self.end, expected_versions=expected_versions, next=next)
            
        with it('can\'t get the n=4 //last is n=3 C2!'):
            next = 4
            expected = "irreal"
            
            error_message = "The next 4 version for one year ago must not exist. Available '{}'".format(self.expected_version_list)
            test_expected_to_break(the_class=self.e.liquicomun, start=self.start, end=self.end, assert_message=error_message)

        with it('can\'t get the n=-1'):
            next = -1
            expected = "irreal"
            
            it_works = True
            try:
                res = self.e.liquicomun().download(self.start, self.end, next=next)
            except:
                it_works = False

            assert not it_works, "Negative next version must break"
