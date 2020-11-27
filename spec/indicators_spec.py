# -*- coding: utf-8 -*-
from expects.testing import failure
from expects import *
from mamba import *

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
                equal(u'Tarifa 2.0.A (peaje por defecto)')
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

        with it('Returns PriceEnergiaExcedentariaAutoconsumCompensacioSimplificada instance'):
            e = Esios(self.token)
            prices = PriceEnergiaExcedentariaAutoconsumCompensacioSimplificada(e)
            assert isinstance(prices, PriceEnergiaExcedentariaAutoconsumCompensacioSimplificada)

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

    with context('LinkBalanceMorocco'):
        with it('Returns LinkBalanceMorocco instance'):
            e = Esios(self.token)
            profile = LinkBalanceMorocco(e)
            assert isinstance(profile, LinkBalanceMorocco)
            data = profile.get(self.start_date, self.end_date)
            expect(data['indicator']['short_name']).to(
                equal(u'Saldo neto Marruecos telemedidas')
            )
            expect(data['indicator']['name']).to(
                contain(u'Saldo horario neto de interconexión con Marruecos telemedidas')
            )

    with context('Medium Hourly Price Components'):
        with it('Returns mhpMeasuredDeviationsFree'):
            #799
            # equivalent to grcosdnc Coste Desvios (9th field)
            e = Esios(self.token)
            profile = mhpMeasuredDeviationsFree(e)
            assert isinstance(profile, mhpMeasuredDeviationsFree)
            data = profile.get(self.start_date, self.end_date)
            expect(data['indicator']['short_name']).to(
                equal(u'Com. Libre')
            )
            expect(data['indicator']['name']).to(
                contain(u'Precio medio horario componente desvíos medidos contratación libre')
            )
        with it('Returns mhpPO146SaldoFree'):
            #802
            e = Esios(self.token)
            profile = mhpPO146BalanceFree(e)
            assert isinstance(profile, mhpPO146BalanceFree)
            data = profile.get(self.start_date, self.end_date)
            expect(data['indicator']['short_name']).to(
                equal(u'Com. Libre')
            )
            expect(data['indicator']['name']).to(
                contain(u'Precio medio horario componente saldo P.O.14.6 contratación libre')
            )
        with it('Returns mhpFalloNominacionUPGFree'):
            #803
            e = Esios(self.token)
            profile = mhpFalloNominacionUPGFree(e)
            assert isinstance(profile, mhpFalloNominacionUPGFree)
            data = profile.get(self.start_date, self.end_date)
            expect(data['indicator']['short_name']).to(
                equal(u'Com. Libre')
            )
            expect(data['indicator']['name']).to(
                contain(u'Precio medio horario componente fallo nominación UPG contratación libre')
            )
        with it('Returns mhpDailyMarket instance'):
            #805
            e = Esios(self.token)
            profile = mhpDailyMarket(e)
            assert isinstance(profile, mhpDailyMarket)
            data = profile.get(self.start_date, self.end_date)
            expect(data['indicator']['short_name']).to(
                equal(u'Mercado Diario')
            )
            expect(data['indicator']['name']).to(
                contain(u'Precio medio horario componente mercado diario ')
            )

        with it('Returns mhpPBF instance'):
            #806
            e = Esios(self.token)
            profile = mhpPBF(e)
            assert isinstance(profile, mhpPBF)
            data = profile.get(self.start_date, self.end_date)
            expect(data['indicator']['short_name']).to(
                equal(u'Restricciones PBF')
            )
            expect(data['indicator']['name']).to(
                contain(u'Precio medio horario componente restricciones PBF ')
            )
        with it('Returns mhpRealTimeRestrictions instance'):
            #807
            e = Esios(self.token)
            profile = mhpRealTimeRestrictions(e)
            assert isinstance(profile, mhpRealTimeRestrictions)
            data = profile.get(self.start_date, self.end_date)
            expect(data['indicator']['short_name']).to(
                equal(u'Restricciones TR')
            )
            expect(data['indicator']['name']).to(
                contain(u'Precio medio horario componente restricciones tiempo real ')
            )
        with it('Returns mhpAdditionalPowerReservation instance'):
            #810
            e = Esios(self.token)
            profile = mhpAdditionalPowerReservation(e)
            assert isinstance(profile, mhpAdditionalPowerReservation)
            data = profile.get(self.start_date, self.end_date)
            expect(data['indicator']['short_name']).to(
                equal(u'Reserva Potencia Adicional Subir')
            )
            expect(data['indicator']['name']).to(
                contain(u'Precio medio horario componente reserva de potencia adicional a subir ')
            )
        with it('Returns mhpSecondaryBand instance'):
            #811
            e = Esios(self.token)
            profile = mhpSecondaryBand(e)
            assert isinstance(profile, mhpSecondaryBand)
            data = profile.get(self.start_date, self.end_date)
            expect(data['indicator']['short_name']).to(
                equal(u'Banda Secundaria')
            )
            expect(data['indicator']['name']).to(
                contain(u'Precio medio horario componente banda secundaria ')
            )
        with it('Returns mhpDesviationsBalance instance'):
            #813
            e = Esios(self.token)
            profile = mhpDesviationsBalance(e)
            assert isinstance(profile, mhpDesviationsBalance)
            data = profile.get(self.start_date, self.end_date)
            expect(data['indicator']['short_name']).to(
                equal(u'Saldo Desvíos')
            )
            expect(data['indicator']['name']).to(
                contain(u'Precio medio horario componente saldo de desvíos ')
            )
        with it('Returns mhpPO146Balance'):
            #815
            e = Esios(self.token)
            profile = mhpPO146Balance(e)
            assert isinstance(profile, mhpPO146Balance)
            data = profile.get(self.start_date, self.end_date)
            expect(data['indicator']['short_name']).to(
                equal(u'Saldo P.O.14.6')
            )
            expect(data['indicator']['name']).to(
                contain(u'Precio medio horario componente saldo P.O.14.6 ')
            )
        with it('Returns PriceMedioAnualMercadoDiario'):
            #961
            e = Esios(self.token)
            profile = PriceMedioAnualMercadoDiario(e)
            assert isinstance(profile, PriceMedioAnualMercadoDiario)
            data = profile.get(self.start_date, self.end_date)
            expect(data['indicator']['short_name']).to(
                equal(u'mercado diario')
            )
            expect(data['indicator']['name']).to(
                contain(u'Precio medio anual componente mercado diario')
            )
        with it('Returns mhpInterruptibilityServiceFree instance'):
            #1276
            e = Esios(self.token)
            profile = mhpInterruptibilityServiceFree(e)
            assert isinstance(profile, mhpInterruptibilityServiceFree)
            data = profile.get(self.start_date, self.end_date)
            expect(data['indicator']['short_name']).to(
                equal(u'Com. Libre')
            )
            expect(data['indicator']['name']).to(
                contain(u'Precio medio horario componente servicio de interrumpibilidad contratación libre')
            )

        with it('Returns mhpInterruptibilityService instance'):
            #1277
            e = Esios(self.token)
            profile = mhpInterruptibilityService(e)
            assert isinstance(profile, mhpInterruptibilityService)
            data = profile.get(self.start_date, self.end_date)
            expect(data['indicator']['short_name']).to(
                equal(u'Servicio de interrumpibilidad')
            )
            expect(data['indicator']['name']).to(
                contain(u'Precio medio horario componente servicio de interrumpibilidad ')
            )
        with it('Returns mhpPowerFactorControlFree instance'):
            #1286
            e = Esios(self.token)
            profile = mhpPowerFactorControlFree(e)
            assert isinstance(profile, mhpPowerFactorControlFree)
            data = profile.get(self.start_date, self.end_date)
            expect(data['indicator']['short_name']).to(
                equal(u'Com. Libre')
            )
            expect(data['indicator']['name']).to(
                contain(u'Precio medio horario componente control factor potencia contratación libre')
            )
        with it('Returns mhpPowerFactorControl instance'):
            #1286
            e = Esios(self.token)
            profile = mhpPowerFactorControl(e)
            assert isinstance(profile, mhpPowerFactorControl)
            data = profile.get(self.start_date, self.end_date)
            expect(data['indicator']['short_name']).to(
                equal(u'Control factor de potencia')
            )
            expect(data['indicator']['name']).to(
                contain(u'Precio medio horario componente control factor potencia ')
            )
        with it('Returns mhpEnergyBalanceFree instance'):
            #1366
            e = Esios(self.token)
            profile = mhpEnergyBalanceFree(e)
            assert isinstance(profile, mhpEnergyBalanceFree)
            data = profile.get(self.start_date, self.end_date)
            expect(data['indicator']['short_name']).to(
                equal(u'Incumplimiento energía balance CL')
            )
            expect(data['indicator']['name']).to(
                contain(u'Precio medio horario componente incumplimiento energía de balance contratación libre')
            )