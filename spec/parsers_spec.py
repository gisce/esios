# -*- coding: utf-8 -*-
from expects.testing import failure
from expects import *

from datetime import datetime
from dateutil.relativedelta import relativedelta

import json
import os

from esios import Esios
from esios.parsers import P48CierreParser
from pytz import timezone

LOCAL_TZ = timezone('Europe/Madrid')
UTC_TZ = timezone('UTC')


def validate_json(result):
    expect(result).to(be_a(str))

    data = json.loads(result)

    expect(data).to(be_a(list))
    expect(len(data)).to(be_above(22))
    expect(data[0]).to(be_a(dict))
    expect(data[0]).to(
        have_keys('hour', 'up', 'value', 'cierre', 'utc_timestamp', 'local_timestamp')
    )
    for register in data:
        # validate timestamps
        local_datetime, local_offset = register['local_timestamp'].split('+')
        is_dst = local_offset != '01:00'
        local_ts = LOCAL_TZ.localize(datetime.strptime(local_datetime, '%Y-%m-%d %H:%M:%S'), is_dst=is_dst)
        utc_ts = UTC_TZ.localize(datetime.strptime(register['utc_timestamp'], '%Y-%m-%d %H:%M:%S+00:00'))
        expect(register['local_timestamp']).to_not(equal(register['utc_timestamp']))
        expected_local_ts = LOCAL_TZ.normalize(utc_ts.astimezone(LOCAL_TZ))
        expect(local_ts).to(equal(expected_local_ts))


def validate_data(result, start, end, cierre=None):
    data = json.loads(result)

    target_data = [x for x in data
                   if start <= LOCAL_TZ.normalize(LOCAL_TZ.localize(
            datetime.strptime(x['local_timestamp'][:18], '%Y-%m-%d %H:%M:%S'))) <= end]

    max_date = max([d['local_timestamp'] for d in target_data])
    min_date = min([d['local_timestamp'] for d in target_data])

    hours = int(((end - start).total_seconds() / 3600) + 1)
    expect(len(target_data)).to(be_above_or_equal(hours))  # can include True and False values for "cierre" field

    expect(min_date).to(equal(str(start)))
    expect(max_date).to(equal(str(end)))

    if cierre is not None:
        for c in data:
            expect(c['cierre']).to(equal(cierre))


with description('Esios Parsers'):
    with before.all:
        ESIOS_TOKEN = os.getenv('ESIOS_TOKEN')
        self.token = ESIOS_TOKEN

        self.today = datetime.today()

        self.e = Esios(self.token)

    with context('p48CierreParser: p48cierre files parser'):

        with context('Can download data from esios'):
            with it('Creates an instance'):
                parser = P48CierreParser(self.e)
                expect(parser).to(be_a(P48CierreParser))

            with it('may be parsed as json'):
                parser = P48CierreParser(self.e)

                today = datetime.now()
                start = LOCAL_TZ.localize(
                    today.replace(hour=0, minute=0, second=0, microsecond=0) - relativedelta(days=1)
                )
                end = LOCAL_TZ.localize(
                    today.replace(hour=23, minute=59, second=59, microsecond=0)
                )

                result = parser.get_data_json('SOMEC01', start, end)

                validate_json(result)
                validate_data(result, start + relativedelta(hours=1), end + relativedelta(seconds=1))

        with context('parses local files'):

            with it('gets a zipfile and may be parsed as json'):
                parser = P48CierreParser(self.e)
                result = parser.get_data_json_from_file('SOMEC01', 'spec/data/p48cierre.zip')

                validate_json(result)
                # contains full 2020/09/15 and full 2020/09/17
                data = json.loads(result)
                expect(len(data)).to(equal(48))
                local_timestamps = [r['local_timestamp'] for r in data]
                ts_template = '2020-09-{:02} {:02}:00:00+02:00'
                # 2020/09/15
                for hour in range(1, 24):
                    expect(local_timestamps).to(contain(ts_template.format(15, hour)))
                expect(local_timestamps).to(contain(ts_template.format(16, 0)))
                # 2020/09/17
                for hour in range(1, 24):
                    expect(local_timestamps).to(contain(ts_template.format(17, hour)))
                expect(local_timestamps).to(contain(ts_template.format(18, 0)))

                # cierre
                for c in data:
                    if '2020-09-15' in c['local_timestamp']:
                        expect(c['cierre']).to(be_true)
                    elif '2020-09-16' in c['local_timestamp']:
                        expect(c['cierre']).to(be_true)
                    elif '2020-09-17' in c['local_timestamp']:
                        expect(c['cierre']).to(be_false)
                    elif '2020-09-18' in c['local_timestamp']:
                        expect(c['cierre']).to(be_false)


            with it('gets a p48cierre xml file and may be parsed as json'):
                parser = P48CierreParser(self.e)
                result = parser.get_data_json_from_file('SOMEC01', 'spec/data/p48cierre_20200915.xml')

                validate_json(result)
                validate_data(
                    result, LOCAL_TZ.localize(datetime(2020, 9, 15, 1, 0)), LOCAL_TZ.localize(datetime(2020, 9, 16, 0, 0), True)
                )


            with it('gets a p48 xml file and may be parsed as json'):
                parser = P48CierreParser(self.e)
                result = parser.get_data_json_from_file('SOMEC01', 'spec/data/p48_2020091618.xml')

                validate_json(result)
                validate_data(
                    result, LOCAL_TZ.localize(datetime(2020, 9, 17, 1, 0)), LOCAL_TZ.localize(datetime(2020, 9, 18, 0, 0), False)
                )

            with it('gets 25 registers for a p48cierre xml file from October saving time day'):
                parser = P48CierreParser(self.e)
                result = parser.get_data_json_from_file('SOMEC01', 'spec/data/p48cierre_20191027.xml')

                validate_json(result)
                validate_data(
                    result, LOCAL_TZ.localize(datetime(2019, 10, 27, 1, 0)), LOCAL_TZ.localize(datetime(2019, 10, 28, 0, 0)), True
                )
                data = json.loads(result)
                expect(len(data)).to(equal(25))

            with it('gets 23 registers for a p48cierre xml file from March saving time day'):
                parser = P48CierreParser(self.e)
                result = parser.get_data_json_from_file('SOMEC01', 'spec/data/p48cierre_20200329.xml')

                validate_json(result)
                validate_data(
                    result, LOCAL_TZ.localize(datetime(2020, 3, 29, 1, 0)), LOCAL_TZ.localize(datetime(2020, 3, 30, 0, 0)), True
                )

                data = json.loads(result)
                expect(len(data)).to(equal(23))