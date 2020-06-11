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


class PricePVPC(Indicator):
    pass


class PricePVPC20A(ProfilePVPC):
    path = 'indicators/1013'


class PricePVPC20DHA(ProfilePVPC):
    path = 'indicators/1014'


class PricePVPC20DHS(ProfilePVPC):
    path = 'indicators/1015'


class LinkBalanceMorocco(Indicator):
    path = 'indicators/10209'


class mhpMeasuredDeviationsFree(Indicator):
    path = 'indicators/799'


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


class mhpAdditionalPowerReservation(Indicator):
    path = 'indicators/810'


class mhpSecondaryBand(Indicator):
    path = 'indicators/811'


class mhpDesviationsBalance(Indicator):
    path = 'indicators/813'


class mhpPO146Balance(Indicator):
    path = 'indicators/815'


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


class PriceEnergiaExcedentariaAutoconsumCompensacioSimplificada(Indicator):
    path = 'indicators/1739'
