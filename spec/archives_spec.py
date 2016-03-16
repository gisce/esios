from expects.testing import failure
from expects import *

from datetime import datetime, timedelta
import calendar
import zipfile
from StringIO import StringIO
import json
import os

ESIOS_TOKEN = '67c6aff80ca331eec78e1f62b7ffc6799e2674d82d57c04104a612db43496db3'

from esios import Esios
from esios.archives import Liquicomun

with description('Liquicomun file'):
    with context('Instance'):
        with before.all:
            self.token = ESIOS_TOKEN

        with it('Returns liquicomun instance'):
            e = Esios(self.token)
            liqui = Liquicomun(e)
            assert isinstance(liqui, Liquicomun)

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
            assert zf.namelist()[0][:2] == 'A1'

        with it('should download C2 for 3 months ago'):
            today = datetime.today() - timedelta(days=93)
            start = datetime(today.year, today.month, 1)
            last_month_day = calendar.monthrange(start.year, start.month)[1]
            end = datetime(start.year, start.month, last_month_day)

            e = Esios(self.token)
            res = e.liquicomun().download(start, end)
            c = StringIO(res)
            zf = zipfile.ZipFile(c)
            assert zf.testzip() is None
            assert zf.namelist()[0][:2] == 'C2'

with description('A1 Liquicomun file'):
    with context('Instance'):
        with before.all:
            self.token = ESIOS_TOKEN

        with it('Gets A1_liquicomun'):
            today = datetime.today()
            start = datetime(today.year, today.month, 1)
            last_month_day = calendar.monthrange(today.year, today.month)[1]
            end = datetime(today.year, today.month, last_month_day)

            e = Esios(self.token)
            res = e.A1_liquicomun().download(start, end)
            c = StringIO(res)
            zf = zipfile.ZipFile(c)
            assert zf.testzip() is None
            assert zf.namelist()[0][:2] == 'A1'
