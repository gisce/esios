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
        expect(len(data['indicator']['values'])).to(equal(720))

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

    with context('DemandaDiariaElectricaPeninsularPrevista'):
        with it('Returns DemandaDiariaElectricaPeninsularPrevista instance'):
            # 460
            e = Esios(self.token)
            # Hourly case
            profile = DemandaDiariaElectricaPeninsularPrevista(e)
            assert isinstance(profile, DemandaDiariaElectricaPeninsularPrevista)
            data = profile.get(self.start_date, self.end_date)
            expect(data['indicator']['short_name']).to(
                equal(u'Previsión diaria')
            )
            expect(data['indicator']['name']).to(
                contain(u'Previsión diaria de la demanda eléctrica peninsular')
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

    with context('mqhpDailyMarket'):
        with it('Returns mqhpDailyMarket instance'):
            # 600
            e = Esios(self.token)
            profile = mqhpDailyMarket(e)
            assert isinstance(profile, mqhpDailyMarket)
            start_date = self.tz.localize(datetime(2025, 10, 1, 0, 0))
            end_date = self.tz.localize(datetime(2025, 10, 1, 23, 45))
            data = profile.get(start_date, end_date)
            expect(data['indicator']['short_name']).to(
                equal(u'Mercado SPOT')
            )
            expect(data['indicator']['name']).to(
                equal(u'Precio mercado SPOT Diario')
            )
            values = [x for x in data['indicator']['values'] if 'Esp' in x['geo_name']]
            values = sorted(values, key=lambda d: d['datetime_utc'])
            expect(len(values)).to(
                equal(96)
            )
            expect(values[0]['value']).to(
                equal(105.1)
            )
            expect(values[-1]['value']).to(
                equal(101.52)
            )

    with context('PriceSpotIntradaily1'):
        with it('Returns PriceSpotIntradaily1 instance'):
            # 612
            e = Esios(self.token)
            profile = PriceSpotIntradaily1(e)
            assert isinstance(profile, PriceSpotIntradaily1)
            start_date = self.tz.localize(datetime(2021, 11, 1, 1, 0))
            end_date = self.tz.localize(datetime(2021, 12, 1, 0, 0))
            data = profile.get(start_date, end_date)
            expect(data['indicator']['short_name']).to(
                equal(u'Intradiario Sesión 1')
            )
            expect(data['indicator']['name']).to(
                equal(u'Precio mercado SPOT Intradiario Sesión 1')
            )
            # QH tests (since October 2025)
            start_date = self.tz.localize(datetime(2025, 10, 1, 0, 0))
            end_date = self.tz.localize(datetime(2025, 10, 1, 23, 59))
            data = profile.get(start_date, end_date)
            values = [x for x in data['indicator']['values'] if 'Esp' in x['geo_name']]
            values = sorted(values, key=lambda d: d['datetime_utc'])
            expect(len(values)).to(
                equal(96)
            )
            expect(values[0]['value']).to(
                equal(106.1)
            )
            expect(values[-1]['value']).to(
                equal(105.01)
            )

    with context('PriceSpotIntradaily2'):
        with it('Returns PriceSpotIntradaily2 instance'):
            # 613
            e = Esios(self.token)
            profile = PriceSpotIntradaily2(e)
            assert isinstance(profile, PriceSpotIntradaily2)
            start_date = self.tz.localize(datetime(2021, 11, 1, 1, 0))
            end_date = self.tz.localize(datetime(2021, 12, 1, 0, 0))
            data = profile.get(start_date, end_date)
            expect(data['indicator']['short_name']).to(
                equal(u'Intradiario Sesión 2')
            )
            expect(data['indicator']['name']).to(
                equal(u'Precio mercado SPOT Intradiario Sesión 2')
            )
            # QH tests (since October 2025)
            start_date = self.tz.localize(datetime(2025, 10, 1, 0, 0))
            end_date = self.tz.localize(datetime(2025, 10, 1, 23, 59))
            data = profile.get(start_date, end_date)
            values = [x for x in data['indicator']['values'] if 'Esp' in x['geo_name']]
            values = sorted(values, key=lambda d: d['datetime_utc'])
            expect(len(values)).to(
                equal(96)
            )
            expect(values[0]['value']).to(
                equal(102.75)
            )
            expect(values[-1]['value']).to(
                equal(115.15)
            )

    with context('PriceSpotIntradaily3'):
        with it('Returns PriceSpotIntradaily3 instance'):
            # 614
            e = Esios(self.token)
            profile = PriceSpotIntradaily3(e)
            assert isinstance(profile, PriceSpotIntradaily3)
            start_date = self.tz.localize(datetime(2021, 11, 1, 1, 0))
            end_date = self.tz.localize(datetime(2021, 12, 1, 0, 0))
            data = profile.get(start_date, end_date)
            expect(data['indicator']['short_name']).to(
                equal(u'Intradiario Sesión 3')
            )
            expect(data['indicator']['name']).to(
                equal(u'Precio mercado SPOT Intradiario Sesión 3')
            )
            # QH tests (since October 2025)
            start_date = self.tz.localize(datetime(2025, 10, 1, 0, 0))
            end_date = self.tz.localize(datetime(2025, 10, 1, 23, 59))
            data = profile.get(start_date, end_date)
            values = [x for x in data['indicator']['values'] if 'Esp' in x['geo_name']]
            values = sorted(values, key=lambda d: d['datetime_utc'])
            expect(len(values)).to(
                equal(48)
            )
            expect(values[0]['value']).to(
                equal(-9.34)
            )
            expect(values[-1]['value']).to(
                equal(106.52)
            )

    with context('PriceSpotIntradaily4'):
        with it('Returns PriceSpotIntradaily4 instance'):
            # 615
            e = Esios(self.token)
            profile = PriceSpotIntradaily4(e)
            assert isinstance(profile, PriceSpotIntradaily4)
            start_date = self.tz.localize(datetime(2021, 11, 1, 1, 0))
            end_date = self.tz.localize(datetime(2021, 12, 1, 0, 0))
            data = profile.get(start_date, end_date)
            expect(data['indicator']['short_name']).to(
                equal(u'Intradiario Sesión 4')
            )
            expect(data['indicator']['name']).to(
                equal(u'Precio mercado SPOT Intradiario Sesión 4')
            )

    with context('PriceSpotIntradaily5'):
        with it('Returns PriceSpotIntradaily5 instance'):
            # 616
            e = Esios(self.token)
            profile = PriceSpotIntradaily5(e)
            assert isinstance(profile, PriceSpotIntradaily5)
            start_date = self.tz.localize(datetime(2021, 11, 1, 1, 0))
            end_date = self.tz.localize(datetime(2021, 12, 1, 0, 0))
            data = profile.get(start_date, end_date)
            expect(data['indicator']['short_name']).to(
                equal(u'Intradiario Sesión 5')
            )
            expect(data['indicator']['name']).to(
                equal(u'Precio mercado SPOT Intradiario Sesión 5')
            )

    with context('PriceSpotIntradaily6'):
        with it('Returns PriceSpotIntradaily6 instance'):
            # 617
            e = Esios(self.token)
            profile = PriceSpotIntradaily6(e)
            assert isinstance(profile, PriceSpotIntradaily6)
            start_date = self.tz.localize(datetime(2021, 11, 1, 1, 0))
            end_date = self.tz.localize(datetime(2021, 12, 1, 0, 0))
            data = profile.get(start_date, end_date)
            expect(data['indicator']['short_name']).to(
                equal(u'Intradiario Sesión 6')
            )
            expect(data['indicator']['name']).to(
                equal(u'Precio mercado SPOT Intradiario Sesión 6')
            )

    with context('PriceSpotIntradaily7'):
        with it('Returns PriceSpotIntradaily7 instance'):
            # 618
            e = Esios(self.token)
            profile = PriceSpotIntradaily7(e)
            assert isinstance(profile, PriceSpotIntradaily7)
            start_date = self.tz.localize(datetime(2021, 11, 1, 1, 0))
            end_date = self.tz.localize(datetime(2021, 12, 1, 0, 0))
            data = profile.get(start_date, end_date)
            expect(data['indicator']['short_name']).to(
                equal(u'Intradiario Sesión 7')
            )
            expect(data['indicator']['name']).to(
                equal(u'Precio mercado SPOT Intradiario Sesión 7')
            )

    with context('PriceChargeBiasToUp'):
        with it('Returns PriceChargeBiasToUp instance'):
            # 686
            e = Esios(self.token)
            profile = PriceChargeBiasToUp(e)
            assert isinstance(profile, PriceChargeBiasToUp)
            start_date = self.tz.localize(datetime(2022, 1, 1, 1, 0))
            end_date = self.tz.localize(datetime(2022, 1, 31, 0, 0))
            data = profile.get(start_date, end_date)
            expect(data['indicator']['short_name']).to(
                equal(u'Desv\xedos a subir')
            )
            expect(data['indicator']['name']).to(
                equal(u'Precio de cobro desv\xedos a subir')
            )

    with context('PriceChargeBiasToDown'):
        with it('Returns PriceChargeBiasToDown instance'):
            # 687
            e = Esios(self.token)
            profile = PriceChargeBiasToDown(e)
            assert isinstance(profile, PriceChargeBiasToDown)
            start_date = self.tz.localize(datetime(2022, 1, 1, 1, 0))
            end_date = self.tz.localize(datetime(2022, 1, 31, 0, 0))
            data = profile.get(start_date, end_date)
            expect(data['indicator']['short_name']).to(
                equal(u'Precio de pago desv\xedos a bajar')
            )
            expect(data['indicator']['name']).to(
                equal(u'Precio de pago desv\xedos a bajar')
            )

    with context('ChargeBiasHigherProduction'):
        with it('Returns ChargeBiasHigherProduction instance'):
            # 726
            e = Esios(self.token)
            profile = ChargeBiasHigherProduction(e)
            assert isinstance(profile, ChargeBiasHigherProduction)
            start_date = self.tz.localize(datetime(2022, 1, 1, 1, 0))
            end_date = self.tz.localize(datetime(2022, 1, 31, 0, 0))
            data = profile.get(start_date, end_date)
            expect(data['indicator']['short_name']).to(
                equal(u'Mayor producci\xf3n')
            )
            expect(data['indicator']['name']).to(
                equal(u'Coste de los desv\xedos medidos de mayor producci\xf3n')
            )

    with context('ChargeBiasLowerProduction'):
        with it('Returns ChargeBiasLowerProduction instance'):
            # 727
            e = Esios(self.token)
            profile = ChargeBiasLowerProduction(e)
            assert isinstance(profile, ChargeBiasLowerProduction)
            start_date = self.tz.localize(datetime(2022, 1, 1, 1, 0))
            end_date = self.tz.localize(datetime(2022, 1, 31, 0, 0))
            data = profile.get(start_date, end_date)
            expect(data['indicator']['short_name']).to(
                equal(u'Menor producci\xf3n')
            )
            expect(data['indicator']['name']).to(
                equal(u'Coste de los desv\xedos medidos de menor producci\xf3n')
            )

    with context('PMM Free'):
        with it('Returns pmh_pmm_free instance'):
            # 792
            e = Esios(self.token)
            profile = pmh_pmm_free(e)
            assert isinstance(profile, pmh_pmm_free)
            data = profile.get(self.start_date, self.end_date)
            expect(data['indicator']['short_name']).to(
                equal(u'Com. Libre')
            )
            expect(data['indicator']['name']).to(
                contain(u'Precio medio horario componente mercado diario contrataci\xf3n libre')
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
        with it('Returns DemandaDiariaElectricaPeninsularReal instance'):
            # 1293
            e = Esios(self.token)
            # Hourly case
            profile = DemandaDiariaElectricaPeninsularReal(e)
            assert isinstance(profile, DemandaDiariaElectricaPeninsularReal)
            data = profile.get(self.start_date, self.end_date)
            expect(data['indicator']['short_name']).to(
                equal(u'Demanda real')
            )
            expect(data['indicator']['name']).to(
                contain(u'Demanda real')
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
        with it('Returns mhpEnergyBalanceCUR instance'):
            #1367
            e = Esios(self.token)
            profile = mhpEnergyBalanceCUR(e)
            assert isinstance(profile, mhpEnergyBalanceCUR)
            data = profile.get(self.start_date, self.end_date)
            expect(data['indicator']['short_name']).to(
                equal(u'Incumplimiento energía balance CR')
            )
            expect(data['indicator']['name']).to(
                contain(u'Precio medio horario componente incumplimiento energía de balance comercialización de referencia')
            )
        with it('Returns mhpEnergyBalanceInc instance'):
            # 1368
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
        with it('Returns PriceMedioHorarioMAJ3total instance'):
            # 1901
            e = Esios(self.token)
            profile = PriceMedioHorarioMAJ3total(e)
            assert isinstance(profile, PriceMedioHorarioMAJ3total)
            data = profile.get(self.start_date, self.end_date)
            expect(data['indicator']['short_name']).to(
                equal(u'Mecanismo de ajuste TOT_MAJ3')
            )
            expect(data['indicator']['name']).to(
                contain(u'Precio medio horario componente RD-L 10/2022 restricciones t\xe9cnicas y mercados de balance ')
            )
        with it('Returns PriceMedioHorarioMAJ3nocur instance'):
            # 1902
            e = Esios(self.token)
            profile = PriceMedioHorarioMAJ3nocur(e)
            assert isinstance(profile, PriceMedioHorarioMAJ3nocur)
            data = profile.get(self.start_date, self.end_date)
            expect(data['indicator']['short_name']).to(
                equal(u'Mecanismo de ajuste CLI_MAJ3')
            )
            expect(data['indicator']['name']).to(
                contain(u'Precio medio horario componente RD-L 10/2022 restricciones t\xe9cnicas y mercados de balance contrataci\xf3n libre')
            )
        with it('Returns PriceMedioHorarioMAJ3cur instance'):
            # 1903
            e = Esios(self.token)
            profile = PriceMedioHorarioMAJ3cur(e)
            assert isinstance(profile, PriceMedioHorarioMAJ3cur)
            data = profile.get(self.start_date, self.end_date)
            expect(data['indicator']['short_name']).to(
                equal(u'Mecanismo de ajuste CUR_MAJ3')
            )
            expect(data['indicator']['name']).to(
                contain(u'Precio medio horario componente RD-L 10/2022 restricciones t\xe9cnicas y mercados de balance comercializadores de referencia')
            )
        with it('Returns PriceMedioHorarioAJOStotal instance'):
            # 1904
            e = Esios(self.token)
            profile = PriceMedioHorarioAJOStotal(e)
            assert isinstance(profile, PriceMedioHorarioAJOStotal)
            data = profile.get(self.start_date, self.end_date)
            expect(data['indicator']['short_name']).to(
                equal(u'Mecanismo de ajuste TOT_AJOS')
            )
            expect(data['indicator']['name']).to(
                contain(u'Precio medio horario componente RD-L 10/2022 mercado diario e intradiario - diferencia por liquidaci\xf3n con medidas')
            )
        with it('Returns PriceMedioHorarioAJOSnocur instance'):
            # 1905
            e = Esios(self.token)
            profile = PriceMedioHorarioAJOSnocur(e)
            assert isinstance(profile, PriceMedioHorarioAJOSnocur)
            data = profile.get(self.start_date, self.end_date)
            expect(data['indicator']['short_name']).to(
                equal(u'Mecanismo de ajuste CLI_AJOS')
            )
            expect(data['indicator']['name']).to(
                contain(u'Precio medio horario componente RD-L 10/2022 mercado diario e intradiario - dif. por liq. con medidas contrataci\xf3n libre')
            )
        with it('Returns PriceMedioHorarioAJOScur instance'):
            # 1906
            e = Esios(self.token)
            profile = PriceMedioHorarioAJOScur(e)
            assert isinstance(profile, PriceMedioHorarioAJOScur)
            data = profile.get(self.start_date, self.end_date)
            expect(data['indicator']['short_name']).to(
                equal(u'Mecanismo de ajuste CUR_AJOS')
            )
            expect(data['indicator']['name']).to(
                contain(u'Precio medio horario componente RD-L 10/2022 mercado diario e intradiario - dif. por liq. con med. comerc. referencia')
            )
        with it('Returns PriceMedioHorarioAJOMtotal instance'):
            # 1907
            e = Esios(self.token)
            profile = PriceMedioHorarioAJOMtotal(e)
            assert isinstance(profile, PriceMedioHorarioAJOMtotal)
            data = profile.get(self.start_date, self.end_date)
            expect(data['indicator']['short_name']).to(
                equal(u'Mecanismo de ajuste TOT_AJOM')
            )
            expect(data['indicator']['name']).to(
                contain(u'Precio medio horario componente RD-L 10/2022 mercado diario e intradiario ')
            )
        with it('Returns PriceMedioHorarioAJOMnocur instance'):
            # 1908
            e = Esios(self.token)
            profile = PriceMedioHorarioAJOMnocur(e)
            assert isinstance(profile, PriceMedioHorarioAJOMnocur)
            data = profile.get(self.start_date, self.end_date)
            expect(data['indicator']['short_name']).to(
                equal(u'Mecanismo de ajuste CLI_AJOM')
            )
            expect(data['indicator']['name']).to(
                contain(u'Precio medio horario componente RD-L 10/2022 mercado diario e intradiario contrataci\xf3n libre')
            )
        with it('Returns PriceMedioHorarioAJOMcur instance'):
            # 1909
            e = Esios(self.token)
            profile = PriceMedioHorarioAJOMcur(e)
            assert isinstance(profile, PriceMedioHorarioAJOMcur)
            data = profile.get(self.start_date, self.end_date)
            expect(data['indicator']['short_name']).to(
                equal(u'Mecanismo de ajuste CUR_AJOM')
            )
            expect(data['indicator']['name']).to(
                contain(u'Precio medio horario componente RD-L 10/2022 mercado diario e intradiario comercializadores de referencia')
            )

        with it('Returns PriceMedioHorarioAJOMcur instance'):
            # 1930
            e = Esios(self.token)
            profile = PriceSRAD(e)
            assert isinstance(profile, PriceSRAD)
            data = profile.get(self.start_date, self.end_date)
            expect(data['indicator']['short_name']).to(
                equal(u'Precio marginal en el servicio de respuesta activa de la demanda')
            )
            expect(data['indicator']['name']).to(
                contain(u'Precio marginal en el servicio de respuesta activa de la demanda')
            )

        with it('Returns PrecioMercadoDiario instance'):
            # 600
            e = Esios(self.token)
            profile = PrecioMercadoDiario(e)
            assert isinstance(profile, PrecioMercadoDiario)
            data = profile.get(self.start_date, self.end_date)
            expect(data['indicator']['short_name']).to(
                equal(u'Mercado SPOT')
            )
            expect(data['indicator']['name']).to(
                contain(u'Precio mercado SPOT Diario')
            )

        with it('Returns PrecioDesviosSubir instance'):
            # 686
            e = Esios(self.token)
            profile = PrecioDesviosSubir(e)
            assert isinstance(profile, PrecioDesviosSubir)
            data = profile.get(self.start_date, self.end_date)
            expect(data['indicator']['short_name']).to(
                equal(u'Desvíos a subir')
            )
            expect(data['indicator']['name']).to(
                contain(u'Precio de cobro desvíos a subir')
            )

        with it('Returns PrecioDesviosBajar instance'):
            # 687
            e = Esios(self.token)
            profile = PrecioDesviosBajar(e)
            assert isinstance(profile, PrecioDesviosBajar)
            data = profile.get(self.start_date, self.end_date)
            expect(data['indicator']['short_name']).to(
                equal(u'Precio de pago desvíos a bajar')
            )
            expect(data['indicator']['name']).to(
                contain(u'Precio de pago desvíos a bajar')
            )

    with context('Generation-Demand Components'):
        with it('Returns GenerationDemandDeviation'):
            # 1338
            # equivalent to grcosdnc Coste Desvios (9th field)
            e = Esios(self.token)
            profile = GenerationDemandDeviation(e)
            assert isinstance(profile, GenerationDemandDeviation)
            data = profile.get(self.start_date, self.end_date)
            expect(data['indicator']['short_name']).to(
                equal(u'Volumen desvíos')
            )
            expect(data['indicator']['name']).to(
                contain(u'Volumen neto de los desv\xedos generaci\xf3n-demanda')
            )

        with it('Returns DemandNationalReal'):
            # 2037
            e = Esios(self.token)
            profile = DemandNationalReal(e)
            assert isinstance(profile, DemandNationalReal)
            data = profile.get(self.start_date, self.end_date)
            expect(data['indicator']['short_name']).to(
                equal(u'Demanda real nacional')
            )
            expect(data['indicator']['name']).to(
                contain(u'Demanda real nacional')
            )

        with it('Returns DemandNationalForecasted'):
            # 2052
            e = Esios(self.token)
            profile = DemandNationalForecasted(e)
            assert isinstance(profile, DemandNationalForecasted)
            data = profile.get(self.start_date, self.end_date)
            expect(data['indicator']['short_name']).to(
                equal(u'Demanda real prevista nacional')
            )
            expect(data['indicator']['name']).to(
                contain(u'Demanda real prevista nacional')
            )

        with it('Returns DemandNationalScheduled'):
            # 2053
            e = Esios(self.token)
            profile = DemandNationalScheduled(e)
            assert isinstance(profile, DemandNationalScheduled)
            data = profile.get(self.start_date, self.end_date)
            expect(data['indicator']['short_name']).to(
                equal(u'Demanda real programada nacional')
            )
            expect(data['indicator']['name']).to(
                contain(u'Demanda real programada nacional')
            )

        with it('Returns DemandNationalForecastedForSNP'):
            # 2084
            e = Esios(self.token)
            profile = DemandNationalForecastedForSNP(e)
            assert isinstance(profile, DemandNationalForecastedForSNP)
            data = profile.get(self.start_date, self.end_date)
            expect(data['indicator']['short_name']).to(
                equal(u'Demanda prevista nacional para sistemas no peninsulares')
            )
            expect(data['indicator']['name']).to(
                contain(u'Demanda prevista nacional para sistemas no peninsulares')
            )

        with it('Returns DemandPeninsularReal'):
            # 1293
            e = Esios(self.token)
            profile = DemandPeninsularReal(e)
            assert isinstance(profile, DemandPeninsularReal)
            data = profile.get(self.start_date, self.end_date)
            expect(data['indicator']['short_name']).to(
                equal(u'Demanda real')
            )
            expect(data['indicator']['name']).to(
                contain(u'Demanda real')
            )

        with it('Returns DemandPeninsularRealSumGeneration'):
            # 10004
            e = Esios(self.token)
            profile = DemandPeninsularRealSumGeneration(e)
            assert isinstance(profile, DemandPeninsularRealSumGeneration)
            data = profile.get(self.start_date, self.end_date)
            expect(data['indicator']['short_name']).to(
                equal(u'Demanda real suma generaci\xf3n')
            )
            expect(data['indicator']['name']).to(
                contain(u'Demanda real suma de generaci\xf3n')
            )

        with it('Returns DemandPeninsularForecasted'):
            # 544
            e = Esios(self.token)
            profile = DemandPeninsularForecasted(e)
            assert isinstance(profile, DemandPeninsularForecasted)
            data = profile.get(self.start_date, self.end_date)
            expect(data['indicator']['short_name']).to(
                equal(u'Demanda prevista')
            )
            expect(data['indicator']['name']).to(
                contain(u'Demanda prevista')
            )

        with it('Returns DemandPeninsularScheduled'):
            # 545
            e = Esios(self.token)
            profile = DemandPeninsularScheduled(e)
            assert isinstance(profile, DemandPeninsularScheduled)
            data = profile.get(self.start_date, self.end_date)
            expect(data['indicator']['short_name']).to(
                equal(u'Demanda programada')
            )
            expect(data['indicator']['name']).to(
                contain(u'Demanda programada')
            )

        with it('Returns DemandPeninsularForecastDaily'):
            # 460
            e = Esios(self.token)
            profile = DemandPeninsularForecastDaily(e)
            assert isinstance(profile, DemandPeninsularForecastDaily)
            data = profile.get(self.start_date, self.end_date)
            expect(data['indicator']['short_name']).to(
                equal(u'Previsi\xf3n diaria')
            )
            expect(data['indicator']['name']).to(
                contain(u'Previsi\xf3n diaria')
            )

        with it('Returns DemandPeninsularForecastWeekly'):
            # 603
            e = Esios(self.token)
            profile = DemandPeninsularForecastWeekly(e)
            assert isinstance(profile, DemandPeninsularForecastWeekly)
            data = profile.get(self.start_date, self.end_date)
            expect(data['indicator']['short_name']).to(
                equal(u'Previsi\xf3n semanal')
            )
            expect(data['indicator']['name']).to(
                contain(u'Previsi\xf3n semanal')
            )

        with it('Returns DemandPeninsularForecastMonthly'):
            # 461
            e = Esios(self.token)
            profile = DemandPeninsularForecastMonthly(e)
            assert isinstance(profile, DemandPeninsularForecastMonthly)
            data = profile.get(self.start_date, self.end_date)
            expect(data['indicator']['short_name']).to(
                equal(u'Previsi\xf3n mensual')
            )
            expect(data['indicator']['name']).to(
                contain(u'Previsi\xf3n mensual')
            )

        with it('Returns DemandPeninsularForecastYearly'):
            # 1774
            e = Esios(self.token)
            profile = DemandPeninsularForecastYearly(e)
            assert isinstance(profile, DemandPeninsularForecastYearly)
            data = profile.get(self.start_date, self.end_date)
            expect(data['indicator']['short_name']).to(
                equal(u'Demanda anual')
            )
            expect(data['indicator']['name']).to(
                contain(u'Previsi\xf3n demanda anual')
            )

        with it('Returns DemandNonPeninsularSystemReal'):
            # 1740
            e = Esios(self.token)
            profile = DemandNonPeninsularSystemReal(e)
            assert isinstance(profile, DemandNonPeninsularSystemReal)
            data = profile.get(self.start_date, self.end_date)
            expect(data['indicator']['short_name']).to(
                equal(u'Demanda Real SNP')
            )
            expect(data['indicator']['name']).to(
                contain(u'Demanda Real SNP')
            )

        with it('Returns DemandNonPeninsularSystemRealSumGeneration'):
            # 10350
            e = Esios(self.token)
            profile = DemandNonPeninsularSystemRealSumGeneration(e)
            assert isinstance(profile, DemandNonPeninsularSystemRealSumGeneration)
            data = profile.get(self.start_date, self.end_date)
            expect(data['indicator']['short_name']).to(
                equal(u'Demanda real SNP')
            )
            expect(data['indicator']['name']).to(
                contain(u'Demanda real suma de generaci\xf3n SNP')
            )

        with it('Returns DemandNonPeninsularSystemForecasted'):
            # 1742
            e = Esios(self.token)
            profile = DemandNonPeninsularSystemForecasted(e)
            assert isinstance(profile, DemandNonPeninsularSystemForecasted)
            data = profile.get(self.start_date, self.end_date)
            expect(data['indicator']['short_name']).to(
                equal(u'Demanda prevista SNP')
            )
            expect(data['indicator']['name']).to(
                contain(u'Demanda prevista SNP')
            )

        with it('Returns DemandNonPeninsularSystemScheduled'):
            # 1741
            e = Esios(self.token)
            profile = DemandNonPeninsularSystemScheduled(e)
            assert isinstance(profile, DemandNonPeninsularSystemScheduled)
            data = profile.get(self.start_date, self.end_date)
            expect(data['indicator']['short_name']).to(
                equal(u'Demanda programada SNP')
            )
            expect(data['indicator']['name']).to(
                contain(u'Demanda programada SNP')
            )

        with it('Returns GenerationNationalWind'):
            # 2038
            e = Esios(self.token)
            profile = GenerationNationalWind(e)
            assert isinstance(profile, GenerationNationalWind)
            data = profile.get(self.start_date, self.end_date)
            expect(data['indicator']['short_name']).to(
                equal(u'Generaci\xf3n T.Real e\xf3lica nacional')
            )
            expect(data['indicator']['name']).to(
                contain(u'Generaci\xf3n T.Real e\xf3lica nacional')
            )

        with it('Returns GenerationNationalNuclear'):
            # 2039
            e = Esios(self.token)
            profile = GenerationNationalNuclear(e)
            assert isinstance(profile, GenerationNationalNuclear)
            data = profile.get(self.start_date, self.end_date)
            expect(data['indicator']['short_name']).to(
                equal(u'Generaci\xf3n T.Real nuclear nacional')
            )
            expect(data['indicator']['name']).to(
                contain(u'Generaci\xf3n T.Real nuclear nacional')
            )

        with it('Returns GenerationNationalCoal'):
            # 2040
            e = Esios(self.token)
            profile = GenerationNationalCoal(e)
            assert isinstance(profile, GenerationNationalCoal)
            data = profile.get(self.start_date, self.end_date)
            expect(data['indicator']['short_name']).to(
                equal(u'Generaci\xf3n T.Real carb\xf3n nacional')
            )
            expect(data['indicator']['name']).to(
                contain(u'Generaci\xf3n T.Real carb\xf3n nacional')
            )

        with it('Returns GenerationNationalCombinedCycle'):
            # 2041
            e = Esios(self.token)
            profile = GenerationNationalCombinedCycle(e)
            assert isinstance(profile, GenerationNationalCombinedCycle)
            data = profile.get(self.start_date, self.end_date)
            expect(data['indicator']['short_name']).to(
                equal(u'Generaci\xf3n T.Real ciclo combinado nacional')
            )
            expect(data['indicator']['name']).to(
                contain(u'Generaci\xf3n T.Real ciclo combinado nacional')
            )

        with it('Returns GenerationNationalExchanges'):
            # 553
            e = Esios(self.token)
            profile = GenerationNationalExchanges(e)
            assert isinstance(profile, GenerationNationalExchanges)
            data = profile.get(self.start_date, self.end_date)
            expect(data['indicator']['short_name']).to(
                equal(u'Intercambios')
            )
            expect(data['indicator']['name']).to(
                contain(u'Generaci\xf3n T.Real intercambios')
            )

        with it('Returns GenerationNationalSolarPhotovoltaic'):
            # 2044
            e = Esios(self.token)
            profile = GenerationNationalSolarPhotovoltaic(e)
            assert isinstance(profile, GenerationNationalSolarPhotovoltaic)
            data = profile.get(self.start_date, self.end_date)
            expect(data['indicator']['short_name']).to(
                equal(u'Generaci\xf3n T.Real solar fotovoltaica nacional')
            )
            expect(data['indicator']['name']).to(
                contain(u'Generaci\xf3n T.Real solar fotovoltaica nacional')
            )

        with it('Returns GenerationNationalSolarThermal'):
            # 2045
            e = Esios(self.token)
            profile = GenerationNationalSolarThermal(e)
            assert isinstance(profile, GenerationNationalSolarThermal)
            data = profile.get(self.start_date, self.end_date)
            expect(data['indicator']['short_name']).to(
                equal(u'Generaci\xf3n T.Real solar t\xe9rmica nacional')
            )
            expect(data['indicator']['name']).to(
                contain(u'Generaci\xf3n T.Real solar t\xe9rmica nacional')
            )

        with it('Returns GenerationNationalRenewableThermal'):
            # 2046
            e = Esios(self.token)
            profile = GenerationNationalRenewableThermal(e)
            assert isinstance(profile, GenerationNationalRenewableThermal)
            data = profile.get(self.start_date, self.end_date)
            expect(data['indicator']['short_name']).to(
                equal(u'Generaci\xf3n T.Real t\xe9rmica renovable nacional')
            )
            expect(data['indicator']['name']).to(
                contain(u'Generaci\xf3n T.Real t\xe9rmica renovable nacional')
            )

        with it('Returns GenerationNationalDiesel'):
            # 2047
            e = Esios(self.token)
            profile = GenerationNationalDiesel(e)
            assert isinstance(profile, GenerationNationalDiesel)
            data = profile.get(self.start_date, self.end_date)
            expect(data['indicator']['short_name']).to(
                equal(u'Generaci\xf3n T.Real motor diesel nacional')
            )
            expect(data['indicator']['name']).to(
                contain(u'Generaci\xf3n T.Real motor diesel nacional')
            )

        with it('Returns GenerationNationalGasTurbine'):
            # 2048
            e = Esios(self.token)
            profile = GenerationNationalGasTurbine(e)
            assert isinstance(profile, GenerationNationalGasTurbine)
            data = profile.get(self.start_date, self.end_date)
            expect(data['indicator']['short_name']).to(
                equal(u'Generaci\xf3n T.Real turbina de gas nacional')
            )
            expect(data['indicator']['name']).to(
                contain(u'Generaci\xf3n T.Real turbina de gas nacional')
            )

        with it('Returns GenerationNationalSteamTurbine'):
            # 2049
            e = Esios(self.token)
            profile = GenerationNationalSteamTurbine(e)
            assert isinstance(profile, GenerationNationalSteamTurbine)
            data = profile.get(self.start_date, self.end_date)
            expect(data['indicator']['short_name']).to(
                equal(u'Generaci\xf3n T.Real turbina de vapor nacional')
            )
            expect(data['indicator']['name']).to(
                contain(u'Generaci\xf3n T.Real turbina de vapor nacional')
            )

        with it('Returns GenerationNationalAuxiliary'):
            # 2050
            e = Esios(self.token)
            profile = GenerationNationalAuxiliary(e)
            assert isinstance(profile, GenerationNationalAuxiliary)
            data = profile.get(self.start_date, self.end_date)
            expect(data['indicator']['short_name']).to(
                equal(u'Generaci\xf3n T.Real generaci\xf3n auxiliar nacional')
            )
            expect(data['indicator']['name']).to(
                contain(u'Generaci\xf3n T.Real generaci\xf3n auxiliar nacional')
            )

        with it('Returns GenerationNationalCogenerationAndWaste'):
            # 2051
            e = Esios(self.token)
            profile = GenerationNationalCogenerationAndWaste(e)
            assert isinstance(profile, GenerationNationalCogenerationAndWaste)
            data = profile.get(self.start_date, self.end_date)
            expect(data['indicator']['short_name']).to(
                equal(u'Generaci\xf3n T.Real cogeneraci\xf3n y residuos nacional')
            )
            expect(data['indicator']['name']).to(
                contain(u'Generaci\xf3n T.Real cogeneraci\xf3n y residuos nacional')
            )

        with it('Returns GenerationNationalHydraulic'):
            # 2067
            e = Esios(self.token)
            profile = GenerationNationalHydraulic(e)
            assert isinstance(profile, GenerationNationalHydraulic)
            data = profile.get(self.start_date, self.end_date)
            expect(data['indicator']['short_name']).to(
                equal(u'Generaci\xf3n T.Real generaci\xf3n hidr\xe1ulica Nacional')
            )
            expect(data['indicator']['name']).to(
                contain(u'Generaci\xf3n T.Real generaci\xf3n hidr\xe1ulica Nacional')
            )

        with it('Returns GenerationNationalHydraulicAggregated'):
            # 2042
            e = Esios(self.token)
            profile = GenerationNationalHydraulicAggregated(e)
            assert isinstance(profile, GenerationNationalHydraulicAggregated)
            data = profile.get(self.start_date, self.end_date)
            expect(data['indicator']['short_name']).to(
                equal(u'Generaci\xf3n T.Real hidra\xfalica nacional')
            )
            expect(data['indicator']['name']).to(
                contain(u'Generaci\xf3n T.Real hidra\xfalica nacional')
            )

        with it('Returns GenerationNationalStoragePumpingTurbine'):
            # 2066
            e = Esios(self.token)
            profile = GenerationNationalStoragePumpingTurbine(e)
            assert isinstance(profile, GenerationNationalStoragePumpingTurbine)
            data = profile.get(self.start_date, self.end_date)
            expect(data['indicator']['short_name']).to(
                equal(u'Generaci\xf3n T.Real turbinaci\xf3n bombeo Nacional')
            )
            expect(data['indicator']['name']).to(
                contain(u'Generaci\xf3n T.Real turbinaci\xf3n bombeo Nacional')
            )

        with it('Returns GenerationNationalStoragePumpingConsumption'):
            # 2065
            e = Esios(self.token)
            profile = GenerationNationalStoragePumpingConsumption(e)
            assert isinstance(profile, GenerationNationalStoragePumpingConsumption)
            data = profile.get(self.start_date, self.end_date)
            expect(data['indicator']['short_name']).to(
                equal(u'Generaci\xf3n T.Real consumo bombeo Nacional')
            )
            expect(data['indicator']['name']).to(
                contain(u'Generaci\xf3n T.Real consumo bombeo Nacional')
            )

        with it('Returns GenerationNationalStorageBatteryDelivery'):
            # 2198
            e = Esios(self.token)
            profile = GenerationNationalStorageBatteryDelivery(e)
            assert isinstance(profile, GenerationNationalStorageBatteryDelivery)
            data = profile.get(self.start_date, self.end_date)
            expect(data['indicator']['short_name']).to(
                equal(u'Entrega Bater\xedas Nacional')
            )
            expect(data['indicator']['name']).to(
                contain(u'Entrega Bater\xedas Nacional')
            )

        with it('Returns GenerationNationalStorageBatteryCharging'):
            # 2199
            e = Esios(self.token)
            profile = GenerationNationalStorageBatteryCharging(e)
            assert isinstance(profile, GenerationNationalStorageBatteryCharging)
            data = profile.get(self.start_date, self.end_date)
            expect(data['indicator']['short_name']).to(
                equal(u'Carga Bater\xedas Nacional')
            )
            expect(data['indicator']['name']).to(
                contain(u'Carga Bater\xedas Nacional')
            )

        with it('Returns GenerationNationalExportAndorra'):
            # 2068
            e = Esios(self.token)
            profile = GenerationNationalExportAndorra(e)
            assert isinstance(profile, GenerationNationalExportAndorra)
            data = profile.get(self.start_date, self.end_date)
            expect(data['indicator']['short_name']).to(
                equal(u'Generaci\xf3n T.Real exportaci\xf3n Andorra')
            )
            expect(data['indicator']['name']).to(
                contain(u'Generaci\xf3n T.Real exportaci\xf3n Andorra')
            )

        with it('Returns GenerationNationalExportMorocco'):
            # 2069
            e = Esios(self.token)
            profile = GenerationNationalExportMorocco(e)
            assert isinstance(profile, GenerationNationalExportMorocco)
            data = profile.get(self.start_date, self.end_date)
            expect(data['indicator']['short_name']).to(
                equal(u'Generaci\xf3n T.Real exportaci\xf3n Marruecos')
            )
            expect(data['indicator']['name']).to(
                contain(u'Generaci\xf3n T.Real exportaci\xf3n Marruecos')
            )

        with it('Returns GenerationNationalExportPortugal'):
            # 2070
            e = Esios(self.token)
            profile = GenerationNationalExportPortugal(e)
            assert isinstance(profile, GenerationNationalExportPortugal)
            data = profile.get(self.start_date, self.end_date)
            expect(data['indicator']['short_name']).to(
                equal(u'Generaci\xf3n T.Real exportaci\xf3n Portugal')
            )
            expect(data['indicator']['name']).to(
                contain(u'Generaci\xf3n T.Real exportaci\xf3n Portugal')
            )

        with it('Returns GenerationNationalExportFrance'):
            # 2071
            e = Esios(self.token)
            profile = GenerationNationalExportFrance(e)
            assert isinstance(profile, GenerationNationalExportFrance)
            data = profile.get(self.start_date, self.end_date)
            expect(data['indicator']['short_name']).to(
                equal(u'Generaci\xf3n T.Real exportaci\xf3n Francia')
            )
            expect(data['indicator']['name']).to(
                contain(u'Generaci\xf3n T.Real exportaci\xf3n Francia')
            )

        with it('Returns GenerationNationalExportTotal'):
            # 2072
            e = Esios(self.token)
            profile = GenerationNationalExportTotal(e)
            assert isinstance(profile, GenerationNationalExportTotal)
            data = profile.get(self.start_date, self.end_date)
            expect(data['indicator']['short_name']).to(
                equal(u'Generaci\xf3n T.Real exportaci\xf3n total')
            )
            expect(data['indicator']['name']).to(
                contain(u'Generaci\xf3n T.Real exportaci\xf3n total')
            )

        with it('Returns GenerationNationalImportAndorra'):
            # 2073
            e = Esios(self.token)
            profile = GenerationNationalImportAndorra(e)
            assert isinstance(profile, GenerationNationalImportAndorra)
            data = profile.get(self.start_date, self.end_date)
            expect(data['indicator']['short_name']).to(
                equal(u'Generaci\xf3n T.Real importaci\xf3n Andorra')
            )
            expect(data['indicator']['name']).to(
                contain(u'Generaci\xf3n T.Real importaci\xf3n Andorra')
            )

        with it('Returns GenerationNationalImportMorocco'):
            # 2074
            e = Esios(self.token)
            profile = GenerationNationalImportMorocco(e)
            assert isinstance(profile, GenerationNationalImportMorocco)
            data = profile.get(self.start_date, self.end_date)
            expect(data['indicator']['short_name']).to(
                equal(u'Generaci\xf3n T.Real importaci\xf3n Marruecos')
            )
            expect(data['indicator']['name']).to(
                contain(u'Generaci\xf3n T.Real importaci\xf3n Marruecos')
            )

        with it('Returns GenerationNationalImportPortugal'):
            # 2075
            e = Esios(self.token)
            profile = GenerationNationalImportPortugal(e)
            assert isinstance(profile, GenerationNationalImportPortugal)
            data = profile.get(self.start_date, self.end_date)
            expect(data['indicator']['short_name']).to(
                equal(u'Generaci\xf3n T.Real importaci\xf3n Portugal')
            )
            expect(data['indicator']['name']).to(
                contain(u'Generaci\xf3n T.Real importaci\xf3n Portugal')
            )

        with it('Returns GenerationNationalImportFrance'):
            # 2076
            e = Esios(self.token)
            profile = GenerationNationalImportFrance(e)
            assert isinstance(profile, GenerationNationalImportFrance)
            data = profile.get(self.start_date, self.end_date)
            expect(data['indicator']['short_name']).to(
                equal(u'Generaci\xf3n T.Real importaci\xf3n Francia')
            )
            expect(data['indicator']['name']).to(
                contain(u'Generaci\xf3n T.Real importaci\xf3n Francia')
            )

        with it('Returns GenerationNationalImportTotal'):
            # 2077
            e = Esios(self.token)
            profile = GenerationNationalImportTotal(e)
            assert isinstance(profile, GenerationNationalImportTotal)
            data = profile.get(self.start_date, self.end_date)
            expect(data['indicator']['short_name']).to(
                equal(u'Generaci\xf3n T.Real importaci\xf3n total')
            )
            expect(data['indicator']['name']).to(
                contain(u'Generaci\xf3n T.Real importaci\xf3n total')
            )

        with it('Returns GenerationPeninsularWind'):
            # 551
            e = Esios(self.token)
            profile = GenerationPeninsularWind(e)
            assert isinstance(profile, GenerationPeninsularWind)
            data = profile.get(self.start_date, self.end_date)
            expect(data['indicator']['short_name']).to(
                equal(u'E\xf3lica')
            )
            expect(data['indicator']['name']).to(
                contain(u'Generaci\xf3n T.Real e\xf3lica')
            )

        with it('Returns GenerationPeninsularNuclear'):
            # 549
            e = Esios(self.token)
            profile = GenerationPeninsularNuclear(e)
            assert isinstance(profile, GenerationPeninsularNuclear)
            data = profile.get(self.start_date, self.end_date)
            expect(data['indicator']['short_name']).to(
                equal(u'Nuclear')
            )
            expect(data['indicator']['name']).to(
                contain(u'Generaci\xf3n T.Real nuclear')
            )

        with it('Returns GenerationPeninsularFuelGas'):
            # 548
            e = Esios(self.token)
            profile = GenerationPeninsularFuelGas(e)
            assert isinstance(profile, GenerationPeninsularFuelGas)
            data = profile.get(self.start_date, self.end_date)
            expect(data['indicator']['short_name']).to(
                equal(u'Fuel-gas')
            )
            expect(data['indicator']['name']).to(
                contain(u'Generaci\xf3n T.Real fuel-gas')
            )

        with it('Returns GenerationPeninsularCoal'):
            # 547
            e = Esios(self.token)
            profile = GenerationPeninsularCoal(e)
            assert isinstance(profile, GenerationPeninsularCoal)
            data = profile.get(self.start_date, self.end_date)
            expect(data['indicator']['short_name']).to(
                equal(u'Carb\xf3n')
            )
            expect(data['indicator']['name']).to(
                contain(u'Generaci\xf3n T.Real carb\xf3n')
            )

        with it('Returns GenerationPeninsularCombinedCycle'):
            # 550
            e = Esios(self.token)
            profile = GenerationPeninsularCombinedCycle(e)
            assert isinstance(profile, GenerationPeninsularCombinedCycle)
            data = profile.get(self.start_date, self.end_date)
            expect(data['indicator']['short_name']).to(
                equal(u'Ciclo combinado')
            )
            expect(data['indicator']['name']).to(
                contain(u'Generaci\xf3n T.Real C.Combinado')
            )

        with it('Returns GenerationPeninsularExchanges'):
            # 553
            e = Esios(self.token)
            profile = GenerationPeninsularExchanges(e)
            assert isinstance(profile, GenerationPeninsularExchanges)
            data = profile.get(self.start_date, self.end_date)
            expect(data['indicator']['short_name']).to(
                equal(u'Intercambios')
            )
            expect(data['indicator']['name']).to(
                contain(u'Generaci\xf3n T.Real intercambios')
            )

        with it('Returns GenerationPeninsularBalearicLink'):
            # 554
            e = Esios(self.token)
            profile = GenerationPeninsularBalearicLink(e)
            assert isinstance(profile, GenerationPeninsularBalearicLink)
            data = profile.get(self.start_date, self.end_date)
            expect(data['indicator']['short_name']).to(
                equal(u'Enlace Pen\xednsula-Baleares')
            )
            expect(data['indicator']['name']).to(
                contain(u'Generaci\xf3n T.Real enlace balear')
            )

        with it('Returns GenerationPeninsularSolarPhotovoltaic'):
            # 1295
            e = Esios(self.token)
            profile = GenerationPeninsularSolarPhotovoltaic(e)
            assert isinstance(profile, GenerationPeninsularSolarPhotovoltaic)
            data = profile.get(self.start_date, self.end_date)
            expect(data['indicator']['short_name']).to(
                equal(u'Solar fotovoltaica')
            )
            expect(data['indicator']['name']).to(
                contain(u'Solar fotovoltaica')
            )

        with it('Returns GenerationPeninsularSolarThermal'):
            # 1294
            e = Esios(self.token)
            profile = GenerationPeninsularSolarThermal(e)
            assert isinstance(profile, GenerationPeninsularSolarThermal)
            data = profile.get(self.start_date, self.end_date)
            expect(data['indicator']['short_name']).to(
                equal(u'Solar t\xe9rmica')
            )
            expect(data['indicator']['name']).to(
                contain(u'Solar t\xe9rmica')
            )

        with it('Returns GenerationPeninsularRenewableThermal'):
            # 1296
            e = Esios(self.token)
            profile = GenerationPeninsularRenewableThermal(e)
            assert isinstance(profile, GenerationPeninsularRenewableThermal)
            data = profile.get(self.start_date, self.end_date)
            expect(data['indicator']['short_name']).to(
                equal(u'T\xe9rmica renovable')
            )
            expect(data['indicator']['name']).to(
                contain(u'T\xe9rmica renovable')
            )

        with it('Returns GenerationPeninsularCogenerationAndWaste'):
            # 1297
            e = Esios(self.token)
            profile = GenerationPeninsularCogenerationAndWaste(e)
            assert isinstance(profile, GenerationPeninsularCogenerationAndWaste)
            data = profile.get(self.start_date, self.end_date)
            expect(data['indicator']['short_name']).to(
                equal(u'Cogeneraci\xf3n y resto')
            )
            expect(data['indicator']['name']).to(
                contain(u'Cogeneraci\xf3n y resto')
            )

        with it('Returns GenerationPeninsularHydraulic'):
            # 2080
            e = Esios(self.token)
            profile = GenerationPeninsularHydraulic(e)
            assert isinstance(profile, GenerationPeninsularHydraulic)
            data = profile.get(self.start_date, self.end_date)
            expect(data['indicator']['short_name']).to(
                equal(u'Generaci\xf3n T.Real generaci\xf3n hidr\xe1ulica')
            )
            expect(data['indicator']['name']).to(
                contain(u'Generaci\xf3n T.Real generaci\xf3n hidr\xe1ulica')
            )

        with it('Returns GenerationPeninsularHydraulicAggregated'):
            # 546
            e = Esios(self.token)
            profile = GenerationPeninsularHydraulicAggregated(e)
            assert isinstance(profile, GenerationPeninsularHydraulicAggregated)
            data = profile.get(self.start_date, self.end_date)
            expect(data['indicator']['short_name']).to(
                equal(u'Hidr\xe1ulica')
            )
            expect(data['indicator']['name']).to(
                contain(u'Generaci\xf3n T.Real hidr\xe1ulica')
            )

        with it('Returns GenerationPeninsularStoragePumpingTurbine'):
            # 2079
            e = Esios(self.token)
            profile = GenerationPeninsularStoragePumpingTurbine(e)
            assert isinstance(profile, GenerationPeninsularStoragePumpingTurbine)
            data = profile.get(self.start_date, self.end_date)
            expect(data['indicator']['short_name']).to(
                equal(u'Generaci\xf3n T.Real turbinaci\xf3n bombeo')
            )
            expect(data['indicator']['name']).to(
                contain(u'Generaci\xf3n T.Real turbinaci\xf3n bombeo')
            )

        with it('Returns GenerationPeninsularStoragePumpingConsumption'):
            # 2078
            e = Esios(self.token)
            profile = GenerationPeninsularStoragePumpingConsumption(e)
            assert isinstance(profile, GenerationPeninsularStoragePumpingConsumption)
            data = profile.get(self.start_date, self.end_date)
            expect(data['indicator']['short_name']).to(
                equal(u'Generaci\xf3n T.Real consumo bombeo')
            )
            expect(data['indicator']['name']).to(
                contain(u'Generaci\xf3n T.Real consumo bombeo')
            )

        with it('Returns GenerationPeninsularStorageBatteryDelivery'):
            # 2167
            e = Esios(self.token)
            profile = GenerationPeninsularStorageBatteryDelivery(e)
            assert isinstance(profile, GenerationPeninsularStorageBatteryDelivery)
            data = profile.get(self.start_date, self.end_date)
            expect(data['indicator']['short_name']).to(
                equal(u'Entrega Bater\xedas')
            )
            expect(data['indicator']['name']).to(
                contain(u'Entrega Bater\xedas')
            )

        with it('Returns GenerationPeninsularStorageBatteryCharging'):
            # 2166
            e = Esios(self.token)
            profile = GenerationPeninsularStorageBatteryCharging(e)
            assert isinstance(profile, GenerationPeninsularStorageBatteryCharging)
            data = profile.get(self.start_date, self.end_date)
            expect(data['indicator']['short_name']).to(
                equal(u'Carga Bater\xedas')
            )
            expect(data['indicator']['name']).to(
                contain(u'Carga Bater\xedas')
            )

        with it('Returns GenerationPeninsularExportAndorra'):
            # 2068
            e = Esios(self.token)
            profile = GenerationPeninsularExportAndorra(e)
            assert isinstance(profile, GenerationPeninsularExportAndorra)
            data = profile.get(self.start_date, self.end_date)
            expect(data['indicator']['short_name']).to(
                equal(u'Generaci\xf3n T.Real exportaci\xf3n Andorra')
            )
            expect(data['indicator']['name']).to(
                contain(u'Generaci\xf3n T.Real exportaci\xf3n Andorra')
            )

        with it('Returns GenerationPeninsularExportMorocco'):
            # 2069
            e = Esios(self.token)
            profile = GenerationPeninsularExportMorocco(e)
            assert isinstance(profile, GenerationPeninsularExportMorocco)
            data = profile.get(self.start_date, self.end_date)
            expect(data['indicator']['short_name']).to(
                equal(u'Generaci\xf3n T.Real exportaci\xf3n Marruecos')
            )
            expect(data['indicator']['name']).to(
                contain(u'Generaci\xf3n T.Real exportaci\xf3n Marruecos')
            )

        with it('Returns GenerationPeninsularExportPortugal'):
            # 2070
            e = Esios(self.token)
            profile = GenerationPeninsularExportPortugal(e)
            assert isinstance(profile, GenerationPeninsularExportPortugal)
            data = profile.get(self.start_date, self.end_date)
            expect(data['indicator']['short_name']).to(
                equal(u'Generaci\xf3n T.Real exportaci\xf3n Portugal')
            )
            expect(data['indicator']['name']).to(
                contain(u'Generaci\xf3n T.Real exportaci\xf3n Portugal')
            )

        with it('Returns GenerationPeninsularExportFrance'):
            # 2071
            e = Esios(self.token)
            profile = GenerationPeninsularExportFrance(e)
            assert isinstance(profile, GenerationPeninsularExportFrance)
            data = profile.get(self.start_date, self.end_date)
            expect(data['indicator']['short_name']).to(
                equal(u'Generaci\xf3n T.Real exportaci\xf3n Francia')
            )
            expect(data['indicator']['name']).to(
                contain(u'Generaci\xf3n T.Real exportaci\xf3n Francia')
            )

        with it('Returns GenerationPeninsularExportTotal'):
            # 2072
            e = Esios(self.token)
            profile = GenerationPeninsularExportTotal(e)
            assert isinstance(profile, GenerationPeninsularExportTotal)
            data = profile.get(self.start_date, self.end_date)
            expect(data['indicator']['short_name']).to(
                equal(u'Generaci\xf3n T.Real exportaci\xf3n total')
            )
            expect(data['indicator']['name']).to(
                contain(u'Generaci\xf3n T.Real exportaci\xf3n total')
            )

        with it('Returns GenerationPeninsularImportAndorra'):
            # 2073
            e = Esios(self.token)
            profile = GenerationPeninsularImportAndorra(e)
            assert isinstance(profile, GenerationPeninsularImportAndorra)
            data = profile.get(self.start_date, self.end_date)
            expect(data['indicator']['short_name']).to(
                equal(u'Generaci\xf3n T.Real importaci\xf3n Andorra')
            )
            expect(data['indicator']['name']).to(
                contain(u'Generaci\xf3n T.Real importaci\xf3n Andorra')
            )

        with it('Returns GenerationPeninsularImportMorocco'):
            # 2074
            e = Esios(self.token)
            profile = GenerationPeninsularImportMorocco(e)
            assert isinstance(profile, GenerationPeninsularImportMorocco)
            data = profile.get(self.start_date, self.end_date)
            expect(data['indicator']['short_name']).to(
                equal(u'Generaci\xf3n T.Real importaci\xf3n Marruecos')
            )
            expect(data['indicator']['name']).to(
                contain(u'Generaci\xf3n T.Real importaci\xf3n Marruecos')
            )

        with it('Returns GenerationPeninsularImportPortugal'):
            # 2075
            e = Esios(self.token)
            profile = GenerationPeninsularImportPortugal(e)
            assert isinstance(profile, GenerationPeninsularImportPortugal)
            data = profile.get(self.start_date, self.end_date)
            expect(data['indicator']['short_name']).to(
                equal(u'Generaci\xf3n T.Real importaci\xf3n Portugal')
            )
            expect(data['indicator']['name']).to(
                contain(u'Generaci\xf3n T.Real importaci\xf3n Portugal')
            )

        with it('Returns GenerationPeninsularImportFrance'):
            # 2076
            e = Esios(self.token)
            profile = GenerationPeninsularImportFrance(e)
            assert isinstance(profile, GenerationPeninsularImportFrance)
            data = profile.get(self.start_date, self.end_date)
            expect(data['indicator']['short_name']).to(
                equal(u'Generaci\xf3n T.Real importaci\xf3n Francia')
            )
            expect(data['indicator']['name']).to(
                contain(u'Generaci\xf3n T.Real importaci\xf3n Francia')
            )

        with it('Returns GenerationPeninsularImportTotal'):
            # 2077
            e = Esios(self.token)
            profile = GenerationPeninsularImportTotal(e)
            assert isinstance(profile, GenerationPeninsularImportTotal)
            data = profile.get(self.start_date, self.end_date)
            expect(data['indicator']['short_name']).to(
                equal(u'Generaci\xf3n T.Real importaci\xf3n total')
            )
            expect(data['indicator']['name']).to(
                contain(u'Generaci\xf3n T.Real importaci\xf3n total')
            )

        with it('Returns GenerationPeninsularSolarAggregatedOutdated'):
            # 552
            e = Esios(self.token)
            profile = GenerationPeninsularSolarAggregatedOutdated(e)
            assert isinstance(profile, GenerationPeninsularSolarAggregatedOutdated)
            data = profile.get(self.start_date, self.end_date)
            expect(data['indicator']['short_name']).to(
                equal(u'Solar')
            )
            expect(data['indicator']['name']).to(
                contain(u'Generaci\xf3n T.Real solar')
            )

        with it('Returns GenerationPeninsularSolarAggregated'):
            # 10206
            e = Esios(self.token)
            profile = GenerationPeninsularSolarAggregated(e)
            assert isinstance(profile, GenerationPeninsularSolarAggregated)
            data = profile.get(self.start_date, self.end_date)
            expect(data['indicator']['short_name']).to(
                equal(u'Solar')
            )
            expect(data['indicator']['name']).to(
                contain(u'Solar')
            )

        with it('Returns GenerationNonPeninsularSystemWind'):
            # 1745
            e = Esios(self.token)
            profile = GenerationNonPeninsularSystemWind(e)
            assert isinstance(profile, GenerationNonPeninsularSystemWind)
            data = profile.get(self.start_date, self.end_date)
            expect(data['indicator']['short_name']).to(
                equal(u'E\xf3lica SNP')
            )
            expect(data['indicator']['name']).to(
                contain(u'Generaci\xf3n T.Real e\xf3lica SNP')
            )

        with it('Returns GenerationNonPeninsularSystemCoal'):
            # 1750
            e = Esios(self.token)
            profile = GenerationNonPeninsularSystemCoal(e)
            assert isinstance(profile, GenerationNonPeninsularSystemCoal)
            data = profile.get(self.start_date, self.end_date)
            expect(data['indicator']['short_name']).to(
                equal(u'Carb\xf3n SNP')
            )
            expect(data['indicator']['name']).to(
                contain(u'Generaci\xf3n T.Real carb\xf3n SNP')
            )

        with it('Returns GenerationNonPeninsularSystemCombinedCycle'):
            # 1746
            e = Esios(self.token)
            profile = GenerationNonPeninsularSystemCombinedCycle(e)
            assert isinstance(profile, GenerationNonPeninsularSystemCombinedCycle)
            data = profile.get(self.start_date, self.end_date)
            expect(data['indicator']['short_name']).to(
                equal(u'Ciclo combinado SNP')
            )
            expect(data['indicator']['name']).to(
                contain(u'Generaci\xf3n T.Real ciclo combinado SNP')
            )

        with it('Returns GenerationNonPeninsularSystemBalearicLink'):
            # 1751
            e = Esios(self.token)
            profile = GenerationNonPeninsularSystemBalearicLink(e)
            assert isinstance(profile, GenerationNonPeninsularSystemBalearicLink)
            data = profile.get(self.start_date, self.end_date)
            expect(data['indicator']['short_name']).to(
                equal(u'Enlace balear SNP')
            )
            expect(data['indicator']['name']).to(
                contain(u'Generaci\xf3n T.Real enlace balear SNP')
            )

        with it('Returns GenerationNonPeninsularSystemSolarPhotovoltaic'):
            # 1748
            e = Esios(self.token)
            profile = GenerationNonPeninsularSystemSolarPhotovoltaic(e)
            assert isinstance(profile, GenerationNonPeninsularSystemSolarPhotovoltaic)
            data = profile.get(self.start_date, self.end_date)
            expect(data['indicator']['short_name']).to(
                equal(u'Solar fotovoltaica SNP')
            )
            expect(data['indicator']['name']).to(
                contain(u'Generaci\xf3n T.Real solar fotovoltaica SNP')
            )

        with it('Returns GenerationNonPeninsularSystemDiesel'):
            # 1743
            e = Esios(self.token)
            profile = GenerationNonPeninsularSystemDiesel(e)
            assert isinstance(profile, GenerationNonPeninsularSystemDiesel)
            data = profile.get(self.start_date, self.end_date)
            expect(data['indicator']['short_name']).to(
                equal(u'Motores di\xe9sel SNP')
            )
            expect(data['indicator']['name']).to(
                contain(u'Generaci\xf3n T.Real motores di\xe9sel SNP')
            )

        with it('Returns GenerationNonPeninsularSystemGasTurbine'):
            # 1744
            e = Esios(self.token)
            profile = GenerationNonPeninsularSystemGasTurbine(e)
            assert isinstance(profile, GenerationNonPeninsularSystemGasTurbine)
            data = profile.get(self.start_date, self.end_date)
            expect(data['indicator']['short_name']).to(
                equal(u'Turbina de gas SNP')
            )
            expect(data['indicator']['name']).to(
                contain(u'Generaci\xf3n T.Real turbina de gas SNP')
            )


# class GenerationNonPeninsularSystemSteamTurbine(Indicator):
#     path = 'indicators/1747'
#
#
# class GenerationNonPeninsularSystemAuxiliary(Indicator):
#     path = 'indicators/1754'
#
#
# class GenerationNonPeninsularSystemCogenerationAndWaste(Indicator):
#     path = 'indicators/1755'
#
#
# class GenerationNonPeninsularSystemHydraulic(Indicator):
#     path = 'indicators/2083'
#
#
# class GenerationNonPeninsularSystemHydraulicAggregated(Indicator):
#     """
#     Represents peninsular-level hydraulic energy indicators, including:
#     - Pumping turbine output
#     - Pumping energy consumption
#     - Hydraulic generation
#     Plus or minus some error.
#     """
#     path = 'indicators/1749'
#
#
# class GenerationNonPeninsularSystemStoragePumpingTurbine(Indicator):
#     path = 'indicators/2082'
#
#
# class GenerationNonPeninsularSystemStoragePumpingConsumption(Indicator):
#     path = 'indicators/2081'
#
#
# class GenerationNonPeninsularSystemStorageBatteryDelivery(Indicator):
#     path = 'indicators/2169'
#
#
# class GenerationNonPeninsularSystemStorageBatteryCharging(Indicator):
#     path = 'indicators/2168'
#
#
# class GenerationWindForecast(Indicator):
#     path = 'indicators/541'
#
#
# class GenerationSolarPhotovoltaicForecast(Indicator):
#     path = 'indicators/542'
#
#
# class GenerationSolarThermalForecast(Indicator):
#     path = 'indicators/543'
#
#
# class GenerationSolarAggregatedForecast(Indicator):
#     path = 'indicators/10034'