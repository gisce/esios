from datetime import datetime

from libsaas import http, parsers
from libsaas.services import base


class Indicator(base.RESTResource):
    path = 'indicators'

    @base.apimethod
    def get(self, start_date, end_date):
        assert isinstance(start_date, datetime)
        assert isinstance(end_date, datetime)
        if start_date.tzinfo is None:
            raise Exception('Start date must have time zone')
        if end_date.tzinfo is None:
            raise Exception('End date must have time zone')
        time_trunc = 'hour'
        start_date = start_date.isoformat()
        end_date = end_date.isoformat()
        params = base.get_params(
            ('start_date', 'end_date', 'time_trunc'), locals()
        )
        request = http.Request('GET', self.get_url(), params)
        return request, parsers.parse_json


class ProfilePVPC(Indicator):
    pass


class ProfilePVPC20A(ProfilePVPC):
    path = 'indicators/526'


class ProfilePVPC20DHA(ProfilePVPC):
    path = 'indicators/527'


class ProfilePVPC20DHS(ProfilePVPC):
    path = 'indicators/528'


class PriceSpotIntradaily1(Indicator):
    path = 'indicators/612'


class PriceSpotIntradaily2(Indicator):
    path = 'indicators/613'


class PriceSpotIntradaily3(Indicator):
    path = 'indicators/614'


class PriceSpotIntradaily4(Indicator):
    path = 'indicators/615'


class PriceSpotIntradaily5(Indicator):
    path = 'indicators/616'


class PriceSpotIntradaily6(Indicator):
    path = 'indicators/617'


class PriceSpotIntradaily7(Indicator):
    path = 'indicators/618'


class PriceChargeBiasToUp(Indicator):
    path = 'indicators/686'


class PriceChargeBiasToDown(Indicator):
    path = 'indicators/687'


class ChargeBiasHigherProduction(Indicator):
    path = 'indicators/726'


class ChargeBiasLowerProduction(Indicator):
    path = 'indicators/727'


class ProfilePVPC20TD(ProfilePVPC):
    path = 'indicators/1006'


class PricePVPC(Indicator):
    pass


class PricePVPC20A(ProfilePVPC):
    path = 'indicators/1013'


class PricePVPC20DHA(ProfilePVPC):
    path = 'indicators/1014'


class PricePVPC20DHS(ProfilePVPC):
    path = 'indicators/1015'


class PricePVPC20TD(ProfilePVPC):
    path = 'indicators/1001'


class LinkBalanceMorocco(Indicator):
    path = 'indicators/10209'


class pmd_snp(Indicator):
    path = 'indicators/573'


class pmh_pmm_free(Indicator):
    path = 'indicators/792'


class pmh_pbf_free_RT3(Indicator):
    path = 'indicators/793'


class pmh_tiempo_real_free_RT6(Indicator):
    path = 'indicators/794'


class pmh_intradiario_free_RT4(Indicator):
    path = 'indicators/796'


class pmh_res_pot_sub_free_PS3(Indicator):
    path = 'indicators/797'


class pmh_bs_free_BS3(Indicator):
    path = 'indicators/798'


class mhpMeasuredDeviationsFree(Indicator):
    path = 'indicators/799'


class pmh_saldo_desv_free_EXD(Indicator):
    path = 'indicators/800'


class mhpPO146BalanceFree(Indicator):
    path = 'indicators/802'


class mhpFalloNominacionUPGFree(Indicator):
    path = 'indicators/803'


class mhpDailyMarket(Indicator):
    path = 'indicators/805'


class mhpPBF(Indicator):
    path = 'indicators/806'


class mhpRealTimeRestrictions(Indicator):
    path = 'indicators/807'


class mhpIntraDailyMarket(Indicator):
    path = 'indicators/808'


class mhpIntradailyMarketRestrictions(Indicator):
    path = 'indicators/809'


class mhpAdditionalPowerReservation(Indicator):
    path = 'indicators/810'


class mhpSecondaryBand(Indicator):
    path = 'indicators/811'


class mhpMeasuredDsv(Indicator):
    path = 'indicators/812'


class mhpDesviationsBalance(Indicator):
    path = 'indicators/813'


class mhpCapPayments(Indicator):
    path = 'indicators/814'


class mhpPO146Balance(Indicator):
    path = 'indicators/815'


class mhpUpgNomination(Indicator):
    path = 'indicators/816'


class PriceMedioAnualMercadoDiario(Indicator):
    path = 'indicators/961'


class mhpInterruptibilityServiceFree(Indicator):
    path = 'indicators/1276'


class mhpInterruptibilityService(Indicator):
    path = 'indicators/1277'


class mhpPowerFactorControlFree(Indicator):
    path = 'indicators/1285'


class mhpPowerFactorControl(Indicator):
    path = 'indicators/1286'


class mhpEnergyBalanceFree(Indicator):
    path = 'indicators/1366'


class mhpEnergyBalanceInc(Indicator):
    path = 'indicators/1368'


class PriceEnergiaExcedentariaAutoconsumCompensacioSimplificada(Indicator):
    path = 'indicators/1739'


class PriceMedioHorarioMAJ3total(Indicator):
    path = 'indicators/1901'


class PriceMedioHorarioMAJ3nocur(Indicator):
    path = 'indicators/1902'


class PriceMedioHorarioMAJ3cur(Indicator):
    path = 'indicators/1903'


class PriceMedioHorarioAJOStotal(Indicator):
    path = 'indicators/1904'


class PriceMedioHorarioAJOSnocur(Indicator):
    path = 'indicators/1905'


class PriceMedioHorarioAJOScur(Indicator):
    path = 'indicators/1906'
