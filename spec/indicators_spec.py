# -*- coding: utf-8 -*-
from expects.testing import failure
from expects import *

from datetime import datetime, date
import dateutil.parser
import json
from pytz import timezone
import os

from esios import Esios
from esios.indicators import *


with description('Indicators file'):
    with before.all:
        ESIOS_TOKEN = os.getenv('ESIOS_TOKEN')
        self.token = ESIOS_TOKEN
        self.tz = timezone('Europe/Madrid')
        self.start_date = self.tz.localize(datetime(2017, 1, 1, 0, 0))
        self.end_date = self.tz.localize(datetime(2017, 1, 31, 23, 59))

    with context('ProfilePVPC'):
        with it('Returns ProfilePVPC instance'):
            e = Esios(self.token)
            profile = ProfilePVPC(e)
            assert isinstance(profile, ProfilePVPC)

        with it('Returns a valid ProfilePVPC20A'):
            e = Esios(self.token)
            profile = ProfilePVPC20A(e)
            assert isinstance(profile, ProfilePVPC20A)
            data = profile.get(self.start_date, self.end_date)
            expect(data['indicator']['short_name']).to(
                equal(u'Tarifa 2.0A (peaje por defecto)')
            )
            expect(data['indicator']['name']).to(
                contain(u'Perfiles de consumo')
            )
            expect(len(data['indicator']['values'])).to(equal(744))

        with it('Returns a valid ProfilePVPC20DHA'):
            e = Esios(self.token)
            profile = ProfilePVPC20DHA(e)
            assert isinstance(profile, ProfilePVPC20DHA)
            data = profile.get(self.start_date, self.end_date)
            profile.get(self.start_date, self.end_date)
            expect(data['indicator']['short_name']).to(
                equal(u'Tarifa 2.0.DHA (Eficiencia 2 periodos)')
            )
            expect(data['indicator']['name']).to(
                contain(u'Perfiles de consumo')
            )
            expect(len(data['indicator']['values'])).to(equal(744))

        with it('Returns a valid ProfilePVPC20DHS'):
            e = Esios(self.token)
            profile = ProfilePVPC20DHS(e)
            assert isinstance(profile, ProfilePVPC20DHS)
            data = profile.get(self.start_date, self.end_date)
            profile.get(self.start_date, self.end_date)
            expect(data['indicator']['short_name']).to(
                equal(u'Tarifa 2.0.DHS (vehículo eléctrico)')
            )
            expect(data['indicator']['name']).to(
                contain(u'Perfiles de consumo')
            )
            expect(len(data['indicator']['values'])).to(equal(744))

    with context('PricePVPC'):
        with it('Returns PricePVPC instance'):
            e = Esios(self.token)
            prices = PricePVPC(e)
            assert isinstance(prices, PricePVPC)

        with it('Returns a valid PricePVPC20A'):
            e = Esios(self.token)
            prices = PricePVPC20A(e)
            assert isinstance(prices, PricePVPC20A)
            data = prices.get(self.start_date, self.end_date)
            expect(data['indicator']['short_name']).to(
                equal(u'PVPC T. Defecto')
            )
            expect(data['indicator']['name']).to(
                contain(u'Término de facturación')
            )
            expect(len(data['indicator']['values'])).to(equal(744))

        with it('Returns a valid PricePVPC20DHA'):
            e = Esios(self.token)
            prices = PricePVPC20DHA(e)
            assert isinstance(prices, PricePVPC20DHA)
            data = prices.get(self.start_date, self.end_date)
            expect(data['indicator']['short_name']).to(
                equal(u'PVPC T. Eficiencia 2 periodos')
            )
            expect(data['indicator']['name']).to(
                contain(u'Término de facturación')
            )
            expect(len(data['indicator']['values'])).to(equal(744))

        with it('Returns a valid PricePVPC20DHS'):
            e = Esios(self.token)
            prices = PricePVPC20DHS(e)
            assert isinstance(prices, PricePVPC20DHS)
            data = prices.get(self.start_date, self.end_date)
            expect(data['indicator']['short_name']).to(
                equal(u'PVPC V. Eléctrico')
            )
            expect(data['indicator']['name']).to(
                contain(u'Término de facturación')
            )
            expect(len(data['indicator']['values'])).to(equal(744))

        with it('Returns a valid PricePVPC20A Summer-Winter'):
            e = Esios(self.token)
            prices = PricePVPC20A(e)
            assert isinstance(prices, PricePVPC20A)
            data = prices.get(
                self.tz.localize(datetime(2016, 10, 1, 0, 0)),
                self.tz.localize(datetime(2016, 10, 31, 23, 59)),
            )
            expect(data['indicator']['short_name']).to(
                equal(u'PVPC T. Defecto')
            )
            expect(data['indicator']['name']).to(
                contain(u'Término de facturación')
            )
            expect(dateutil.parser.parse(
                data['indicator']['values'][0]['datetime']
            ).hour).to(equal(0))

            # Summer hour 2 (24 * 29 + 3 = 699)
            # Summer 2:00
            summer_hour = data['indicator']['values'][698]['datetime']
            expect(dateutil.parser.parse(summer_hour).hour).to(equal(2))
            expect(dateutil.parser.parse(summer_hour).utcoffset().seconds).to(
                equal(7200)
            )
            # Winter 2:00
            winter_hour = data['indicator']['values'][699]['datetime']
            expect(dateutil.parser.parse(winter_hour).hour).to(equal(2))
            expect(dateutil.parser.parse(winter_hour).utcoffset().seconds).to(
                equal(3600)
            )

            expect(len(data['indicator']['values'])).to(equal(745))

        with it('Returns a valid PricePVPC20A Winter-Summer'):
            e = Esios(self.token)
            prices = PricePVPC20A(e)
            assert isinstance(prices, PricePVPC20A)
            data = prices.get(
                self.tz.localize(datetime(2016, 3, 1, 0, 0)),
                self.tz.localize(datetime(2016, 3, 31, 23, 59)),
            )
            expect(data['indicator']['short_name']).to(
                equal(u'PVPC T. Defecto')
            )
            expect(data['indicator']['name']).to(
                contain(u'Término de facturación')
            )

            expect(dateutil.parser.parse(
                data['indicator']['values'][0]['datetime']
            ).hour).to(equal(0))
            # Winter hour 2 (24 * 26 + 1 = 625)
            # Winter 1:00
            winter_hour = data['indicator']['values'][625]['datetime']
            expect(dateutil.parser.parse(winter_hour).hour).to(equal(1))
            expect(dateutil.parser.parse(winter_hour).utcoffset().seconds).to(
                equal(3600)
            )
            # Summer 3:00
            summer_hour = data['indicator']['values'][626]['datetime']
            expect(dateutil.parser.parse(summer_hour).hour).to(equal(3))
            expect(dateutil.parser.parse(summer_hour).utcoffset().seconds).to(
                equal(7200)
            )

            expect(len(data['indicator']['values'])).to(equal(743))
