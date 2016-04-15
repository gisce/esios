from expects.testing import failure
from expects import *

from datetime import datetime, timedelta
import calendar
import zipfile
from StringIO import StringIO
import json
import os


from esios import Esios
from esios.archives import Liquicomun

with description('Liquicomun file'):
    with before.all:
        ESIOS_TOKEN = os.getenv('ESIOS_TOKEN')
        self.token = ESIOS_TOKEN

    with context('Instance'):
        with it('Returns liquicomun instance'):
            e = Esios(self.token)
            liqui = Liquicomun(e)
            assert isinstance(liqui, Liquicomun)

        with it('Gets list'):
            today = datetime.today()
            start = datetime(today.year, today.month, 1)
            last_month_day = calendar.monthrange(today.year, today.month)[1]
            end = datetime(today.year, today.month, last_month_day)

            e = Esios(self.token)
            res = e.liquicomun().get(start, end)
            assert len(res) >= 0

        with it('Gets current liquicomun'):
            today = datetime.today()
            start = datetime(today.year, today.month, 1)
            last_month_day = calendar.monthrange(today.year, today.month)[1]
            end = datetime(today.year, today.month, last_month_day)

            e = Esios(self.token)
            res = e.liquicomun().download(start, end)
            c = StringIO(res)
            zf = zipfile.ZipFile(c)
            assert zf.testzip() is None
            assert zf.namelist()[0][:2] in ('A1', 'A2')

        with it('should download C2 or A3 for 3 months ago'):
            today = datetime.today() - timedelta(days=93)
            start = datetime(today.year, today.month, 1)
            last_month_day = calendar.monthrange(start.year, start.month)[1]
            end = datetime(start.year, start.month, last_month_day)

            e = Esios(self.token)
            res = e.liquicomun().download(start, end)
            c = StringIO(res)
            zf = zipfile.ZipFile(c)
            assert zf.testzip() is None
            assert zf.namelist()[0][:2] in ('A3', 'C2')

        with it('should download C6 o C5 for a year ago'):
            today = datetime.today() - timedelta(days=730)
            start = datetime(today.year, today.month, 1)
            last_month_day = calendar.monthrange(start.year, start.month)[1]
            end = datetime(start.year, start.month, last_month_day)

            e = Esios(self.token)
            res = e.liquicomun().download(start, end)
            c = StringIO(res)
            zf = zipfile.ZipFile(c)
            assert zf.testzip() is None
            assert zf.namelist()[0][:2] in ('C6', 'C5')

        with it('should download C7,A7,C6,A6,C5 or A5 for a long time ago'):
            today = datetime.today() - timedelta(days=730)
            start = datetime(today.year, today.month, 1)
            last_month_day = calendar.monthrange(start.year, start.month)[1]
            end = datetime(start.year, start.month, last_month_day)

            e = Esios(self.token)
            res = e.liquicomun().download(start, end)
            c = StringIO(res)
            zf = zipfile.ZipFile(c)
            assert zf.testzip() is None
            assert zf.namelist()[0][:2] in ('A7', 'C7', 'A6', 'C6', 'C5', 'A5')

# with description('A1 Liquicomun file'):
#     with before.all:
#         ESIOS_TOKEN = os.getenv('ESIOS_TOKEN')
#         self.token = ESIOS_TOKEN
#     with context('Instance'):
#         with it('Gets A1_liquicomun'):
#             today = datetime.today()
#             start = datetime(today.year, today.month, 1)
#             last_month_day = calendar.monthrange(today.year, today.month)[1]
#             end = datetime(today.year, today.month, last_month_day)
#
#             e = Esios(self.token)
#             res = e.A1_liquicomun().download(start, end)
#             c = StringIO(res)
#             zf = zipfile.ZipFile(c)
#             assert zf.testzip() is None
#             assert zf.namelist()[0][:2] == 'A1'
#
# with description('A2 Liquicomun file'):
#     with before.all:
#         ESIOS_TOKEN = os.getenv('ESIOS_TOKEN')
#         self.token = ESIOS_TOKEN
#     with context('Instance'):
#         with it('Gets A2_liquicomun'):
#             today = datetime.today()
#             start = datetime(today.year, today.month, 1)
#             last_month_day = calendar.monthrange(today.year, today.month)[1]
#             end = datetime(today.year, today.month, last_month_day)
#
#             e = Esios(self.token)
#             res = e.A2_liquicomun().download(start, end)
#             c = StringIO(res)
#             zf = zipfile.ZipFile(c)
#             assert zf.testzip() is None
#             assert zf.namelist()[0][:2] == 'A2'
