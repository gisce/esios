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

    with it('Returns a valid PricePVPC20TD'):
        e = Esios(self.token)
        prices = PricePVPC20TD(e)
        assert isinstance(prices, PricePVPC20TD)
        data = prices.get(
            self.tz.localize(datetime(2021, 6, 1, 0, 0)),
            self.tz.localize(datetime(2021, 6, 30, 23, 59)),
        )
        expect(data['indicator']['short_name']).to(
            equal(u'PVPC T. 2.0TD')
        )
        expect(data['indicator']['name']).to(
            contain(u'Término de facturación')
        )
        expect(dateutil.parser.parse(
            data['indicator']['values'][0]['datetime']
        ).hour).to(equal(0))

        # Commented till a month is complete
        expect(len(data['indicator']['values']) / 5).to(equal(720))  # there are 5 different subsystems for each hour

    with it('Returns a valid ProfilePVPC20TD'):
        e = Esios(self.token)
        profiles = ProfilePVPC20TD(e)
        assert isinstance(profiles, ProfilePVPC20TD)
        data = profiles.get(
            self.tz.localize(datetime(2021, 6, 1, 0, 0)),
            self.tz.localize(datetime(2021, 6, 30, 23, 59)),
        )
        expect(data['indicator']['short_name']).to(
            equal(u'Tarifa 2.0TD')
        )
        expect(data['indicator']['name']).to(
            contain(u'Perfiles de consumo a efectos de facturación del PVPC Tarifa 2.0TD')
        )
        expect(dateutil.parser.parse(
            data['indicator']['values'][0]['datetime']
        ).hour).to(equal(0))

        # Commented till a month is complete
        expect(len(data['indicator']['values']) / 5).to(equal(720))  # there are 5 different subsystems for each hour

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

    with context('PMDSNP'):
        with it('Returns pmd_snp instance'):
            # 573
            e = Esios(self.token)
            profile = pmd_snp(e)
            assert isinstance(profile, pmd_snp)
            data = profile.get(self.start_date, self.end_date)
            expect(data['indicator']['short_name']).to(
                equal(u'Precio medio demanda sistema')
            )
            expect(data['indicator']['name']).to(
                contain(u'Precio medio de la demanda en los SNP por sistema')
            )

    with context('RT3 Free'):
        with it('Returns pmh_pbf_free_RT3 instance'):
            # 793
            e = Esios(self.token)
            profile = pmh_pbf_free_RT3(e)
            assert isinstance(profile, pmh_pbf_free_RT3)
            data = profile.get(self.start_date, self.end_date)
            expect(data['indicator']['short_name']).to(
                equal(u'Com. Libre')
            )
            expect(data['indicator']['name']).to(
                contain(u'Precio medio horario componente restricciones PBF contrataci\xf3n libre')
            )

    with context('RT6 Free'):
        with it('Returns pmh_tiempo_real_free_RT6 instance'):
            # 794
            e = Esios(self.token)
            profile = pmh_tiempo_real_free_RT6(e)
            assert isinstance(profile, pmh_tiempo_real_free_RT6)
            data = profile.get(self.start_date, self.end_date)
            expect(data['indicator']['short_name']).to(
                equal(u'Com. Libre')
            )
            expect(data['indicator']['name']).to(
                contain(u'Precio medio horario componente restricciones tiempo real contrataci\xf3n libre')
            )

    with context('RT4 Free'):
        with it('Returns pmh_intradiario_free_RT4 instance'):
            # 796
            e = Esios(self.token)
            profile = pmh_intradiario_free_RT4(e)
            assert isinstance(profile, pmh_intradiario_free_RT4)
            data = profile.get(self.start_date, self.end_date)
            expect(data['indicator']['short_name']).to(
                equal(u'Com. Libre')
            )
            expect(data['indicator']['name']).to(
                contain(u'Precio medio horario componente restricciones intradiario contrataci\xf3n libre')
            )

    with context('PS3 Free'):
        with it('Returns pmh_res_pot_sub_free_PS3 instance'):
            # 797
            e = Esios(self.token)
            profile = pmh_res_pot_sub_free_PS3(e)
            assert isinstance(profile, pmh_res_pot_sub_free_PS3)
            data = profile.get(self.start_date, self.end_date)
            expect(data['indicator']['short_name']).to(
                equal(u'Com. Libre')
            )
            expect(data['indicator']['name']).to(
                contain(u'Precio medio horario componente reserva de potencia adicional a subir contrataci\xf3n libre')
            )

    with context('BS3 Free'):
        with it('Returns pmh_bs_free_BS3 instance'):
            # 798
            e = Esios(self.token)
            profile = pmh_bs_free_BS3(e)
            assert isinstance(profile, pmh_bs_free_BS3)
            data = profile.get(self.start_date, self.end_date)
            expect(data['indicator']['short_name']).to(
                equal(u'Com. Libre')
            )
            expect(data['indicator']['name']).to(
                contain(u'Precio medio horario componente banda secundaria contrataci\xf3n libre')
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
        with it('Returns pmh_saldo_desv_free_EXD'):
            #800
            e = Esios(self.token)
            profile = pmh_saldo_desv_free_EXD(e)
            assert isinstance(profile, pmh_saldo_desv_free_EXD)
            data = profile.get(self.start_date, self.end_date)
            expect(data['indicator']['short_name']).to(
                equal(u'Com. Libre')
            )
            expect(data['indicator']['name']).to(
                contain(u'Precio medio horario componente saldo de desv\xedos contrataci\xf3n libre')
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
        with it('Returns mhpIntraDailyMarket instance'):
            #808
            e = Esios(self.token)
            profile = mhpIntraDailyMarket(e)
            assert isinstance(profile, mhpIntraDailyMarket)
            data = profile.get(self.start_date, self.end_date)
            expect(data['indicator']['short_name']).to(
                equal(u'Mercado intradiario (subastas MIBEL y continuo)')
            )
            expect(data['indicator']['name']).to(
                contain(u'Precio medio horario componente mercado intradiario ')
            )
        with it('Returns mhpIntradailyMarketRestrictions instance'):
            #809
            e = Esios(self.token)
            profile = mhpIntradailyMarketRestrictions(e)
            assert isinstance(profile, mhpIntradailyMarketRestrictions)
            data = profile.get(self.start_date, self.end_date)
            expect(data['indicator']['short_name']).to(
                equal(u'Restricciones Intradiario')
            )
            expect(data['indicator']['name']).to(
                contain(u'Precio medio horario componente restricciones intradiario ')
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
        with it('Returns mhpMeasuredDsv instance'):
            #812
            e = Esios(self.token)
            profile = mhpMeasuredDsv(e)
            assert isinstance(profile, mhpMeasuredDsv)
            data = profile.get(self.start_date, self.end_date)
            expect(data['indicator']['short_name']).to(
                equal(u'Desv\xedos Medidos')
            )
            expect(data['indicator']['name']).to(
                contain(u'Precio medio horario componente desv\xedos medidos ')
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
        with it('Returns mhpCapPayments instance'):
            #814
            e = Esios(self.token)
            profile = mhpCapPayments(e)
            assert isinstance(profile, mhpCapPayments)
            data = profile.get(self.start_date, self.end_date)
            expect(data['indicator']['short_name']).to(
                equal(u'Pagos por capacidad')
            )
            expect(data['indicator']['name']).to(
                contain(u'Precio medio horario componente pago de capacidad ')
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
        with it('Returns mhpUpgNomination'):
            #816
            e = Esios(self.token)
            profile = mhpUpgNomination(e)
            assert isinstance(profile, mhpUpgNomination)
            data = profile.get(self.start_date, self.end_date)
            expect(data['indicator']['short_name']).to(
                equal(u'Fallo nominaci\xf3n UPG')
            )
            expect(data['indicator']['name']).to(
                contain(u'Precio medio horario componente fallo nominaci\xf3n UPG ')
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
            #1285
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
        with it('Returns mhpEnergyBalanceInc instance'):
            #1368
            e = Esios(self.token)
            profile = mhpEnergyBalanceInc(e)
            assert isinstance(profile, mhpEnergyBalanceInc)
            data = profile.get(self.start_date, self.end_date)
            expect(data['indicator']['short_name']).to(
                equal(u'Incumplimiento energ\xeda balance')
            )
            expect(data['indicator']['name']).to(
                contain(u'Precio medio horario componente incumplimiento energ\xeda de balance ')
            )
