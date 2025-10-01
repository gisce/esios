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

    with fcontext('Generation-Demand Components'):
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


# class DemandPeninsularForecastYearly(Indicator):
#     """
#     From december to december next year. In kWh.
#     """
#     path = 'indicators/1774'
#
#
# class DemandNonPeninsularSystemReal(Indicator):
#     path = 'indicators/1740'
#
#
# class DemandNonPeninsularSystemRealSumGeneration(Indicator):
#     path = 'indicators/10350'
#
#
# class DemandNonPeninsularSystemForecasted(Indicator):
#     path = 'indicators/1742'
#
#
# class DemandNonPeninsularSystemScheduled(Indicator):
#     path = 'indicators/1741'
#
#
# # national generation of electricity (in kW)
# class GenerationNationalWind(Indicator):
#     path = 'indicators/2038'
#
#
# class GenerationNationalNuclear(Indicator):
#     path = 'indicators/2039'
#
#
# class GenerationNationalCoal(Indicator):
#     path = 'indicators/2040'
#
#
# class GenerationNationalCombinedCycle(Indicator):
#     path = 'indicators/2041'
#
#
# class GenerationNationalExchanges(Indicator):
#     path = 'indicators/553'
#
#
# class GenerationNationalSolarPhotovoltaic(Indicator):
#     path = 'indicators/2044'
#
#
# class GenerationNationalSolarThermal(Indicator):
#     path = 'indicators/2045'
#
#
# class GenerationNationalRenewableThermal(Indicator):
#     path = 'indicators/2046'
#
#
# class GenerationNationalDiesel(Indicator):
#     path = 'indicators/2047'
#
#
# class GenerationNationalGasTurbine(Indicator):
#     path = 'indicators/2048'
#
#
# class GenerationNationalSteamTurbine(Indicator):
#     path = 'indicators/2049'
#
#
# class GenerationNationalAuxiliary(Indicator):
#     path = 'indicators/2050'
#
#
# class GenerationNationalCogenerationAndWaste(Indicator):
#     path = 'indicators/2051'
#
#
# class GenerationNationalHydraulic(Indicator):
#     path = 'indicators/2067'
#
#
# class GenerationNationalHydraulicAggregated(Indicator):
#     """
#     Represents national-level hydraulic energy indicators, including:
#     - Pumping turbine output
#     - Pumping energy consumption
#     - Hydraulic generation
#     Plus or minus some error.
#     """
#     path = 'indicators/2042'
#
#
# class GenerationNationalStoragePumpingTurbine(Indicator):
#     path = 'indicators/2066'
#
#
# class GenerationNationalStoragePumpingConsumption(Indicator):
#     path = 'indicators/2065'
#
#
# class GenerationNationalStorageBatteryDelivery(Indicator):
#     path = 'indicators/2198'
#
#
# class GenerationNationalStorageBatteryCharging(Indicator):
#     path = 'indicators/2199'
#
#
# class GenerationNationalExportAndorra(Indicator):
#     path = 'indicators/2068'
#
#
# class GenerationNationalExportMorocco(Indicator):
#     path = 'indicators/2069'
#
#
# class GenerationNationalExportPortugal(Indicator):
#     path = 'indicators/2070'
#
#
# class GenerationNationalExportFrance(Indicator):
#     path = 'indicators/2071'
#
#
# class GenerationNationalExportTotal(Indicator):
#     path = 'indicators/2072'
#
#
# class GenerationNationalImportAndorra(Indicator):
#     path = 'indicators/2073'
#
#
# class GenerationNationalImportMorocco(Indicator):
#     path = 'indicators/2074'
#
#
# class GenerationNationalImportPortugal(Indicator):
#     path = 'indicators/2075'
#
#
# class GenerationNationalImportFrance(Indicator):
#     path = 'indicators/2076'
#
#
# class GenerationNationalImportTotal(Indicator):
#     path = 'indicators/2077'
#
#
# # peninsular generation of electricity (in kW)
# class GenerationPeninsularWind(Indicator):
#     path = 'indicators/551'
#
#
# class GenerationPeninsularNuclear(Indicator):
#     path = 'indicators/549'
#
#
# class GenerationPeninsularFuelGas(Indicator):
#     path = 'indicators/548'
#
#
# class GenerationPeninsularCoal(Indicator):
#     path = 'indicators/547'
#
#
# class GenerationPeninsularCombinedCycle(Indicator):
#     path = 'indicators/550'
#
#
# class GenerationPeninsularExchanges(Indicator):
#     path = 'indicators/553'
#
#
# class GenerationPeninsularBalearicLink(Indicator):
#     path = 'indicators/554'
#
#
# class GenerationPeninsularSolarPhotovoltaic(Indicator):
#     """
#     Contains data since 02/06/2015 21:00 (spain tz).
#     """
#     path = 'indicators/1295'
#
#
# class GenerationPeninsularSolarThermal(Indicator):
#     """
#     Contains data since 02/06/2015 21:00 (spain tz).
#     """
#     path = 'indicators/1294'
#
#
# class GenerationPeninsularRenewableThermal(Indicator):
#     path = 'indicators/1296'
#
#
# class GenerationPeninsularCogenerationAndWaste(Indicator):
#     path = 'indicators/1297'
#
#
# class GenerationPeninsularHydraulic(Indicator):
#     path = 'indicators/2080'
#
#
# class GenerationPeninsularHydraulicAggregated(Indicator):
#     """
#     Represents peninsular-level hydraulic energy indicators, including:
#     - Pumping turbine output
#     - Pumping energy consumption
#     - Hydraulic generation
#     Plus or minus some error.
#     """
#     path = 'indicators/546'
#
#
# class GenerationPeninsularStoragePumpingTurbine(Indicator):
#     path = 'indicators/2079'
#
#
# class GenerationPeninsularStoragePumpingConsumption(Indicator):
#     path = 'indicators/2078'
#
#
# class GenerationPeninsularStorageBatteryDelivery(Indicator):
#     path = 'indicators/2167'
#
#
# class GenerationPeninsularStorageBatteryCharging(Indicator):
#     path = 'indicators/2166'
#
#
# class GenerationPeninsularExportAndorra(Indicator):
#     path = 'indicators/2068'
#
#
# class GenerationPeninsularExportMorocco(Indicator):
#     path = 'indicators/2069'
#
#
# class GenerationPeninsularExportPortugal(Indicator):
#     path = 'indicators/2070'
#
#
# class GenerationPeninsularExportFrance(Indicator):
#     path = 'indicators/2071'
#
#
# class GenerationPeninsularExportTotal(Indicator):
#     path = 'indicators/2072'
#
#
# class GenerationPeninsularImportAndorra(Indicator):
#     path = 'indicators/2073'
#
#
# class GenerationPeninsularImportMorocco(Indicator):
#     path = 'indicators/2074'
#
#
# class GenerationPeninsularImportPortugal(Indicator):
#     path = 'indicators/2075'
#
#
# class GenerationPeninsularImportFrance(Indicator):
#     path = 'indicators/2076'
#
#
# class GenerationPeninsularImportTotal(Indicator):
#     path = 'indicators/2077'
#
#
# class GenerationPeninsularSolarAggregatedOutdated(Indicator):
#     """
#     Contains data until 02/06/2015 20:50 (spain tz).
#     Solar thermal + solar photovoltaic
#     """
#     path = 'indicators/552'
#
#
# class GenerationPeninsularSolarAggregated(Indicator):
#     """
#     Contains data since 02/06/2015 21:00 (spain tz).
#     Solar thermal + solar photovoltaic
#     """
#     path = 'indicators/10206'
#
#
# # non peninsular systems (SNP) (separated by region) (in kW)
# class GenerationNonPeninsularSystemWind(Indicator):
#     path = 'indicators/1745'
#
#
# class GenerationNonPeninsularSystemCoal(Indicator):
#     path = 'indicators/1750'
#
#
# class GenerationNonPeninsularSystemCombinedCycle(Indicator):
#     path = 'indicators/1746'
#
#
# class GenerationNonPeninsularSystemBalearicLink(Indicator):
#     path = 'indicators/1751'
#
#
# class GenerationNonPeninsularSystemSolarPhotovoltaic(Indicator):
#     path = 'indicators/1748'
#
#
# class GenerationNonPeninsularSystemDiesel(Indicator):
#     path = 'indicators/1743'
#
#
# class GenerationNonPeninsularSystemGasTurbine(Indicator):
#     path = 'indicators/1744'
#
#
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