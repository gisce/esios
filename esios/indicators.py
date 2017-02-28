from datetime import datetime

from libsaas import http, parsers
from libsaas.services import base


class Indicator(base.RESTResource):
    path = 'indicators'


class DateRangeIndicator(Indicator):
    @base.apimethod
    def get(self, start_date, end_date):
        assert isinstance(start_date, datetime)
        assert isinstance(end_date, datetime)
        if start_date.tzinfo is None:
            raise Exception('Start date must have time zone')
        if end_date.tzinfo is None:
            raise Exception('End date must have time zone')
        time_trunc = self.time_trunc
        start_date = start_date.isoformat()
        end_date = end_date.isoformat()
        params = base.get_params(
            ('start_date', 'end_date', 'time_trunc'), locals()
        )
        request = http.Request('GET', self.get_url(), params)
        return request, parsers.parse_json


class ProfilePVPC(DateRangeIndicator):
    time_trunc = 'hour'


class PricePVPC(DateRangeIndicator):
    time_trunc = 'hour'


class PriceSPOT(DateRangeIndicator):
    time_trunc = 'hour'


class ProfilePVPC20A(ProfilePVPC):
    path = 'indicators/526'


class ProfilePVPC20DHA(ProfilePVPC):
    path = 'indicators/527'


class ProfilePVPC20DHS(ProfilePVPC):
    path = 'indicators/528'


class PricePVPC20A(PricePVPC):
    path = 'indicators/1013'


class PricePVPC20DHA(PricePVPC):
    path = 'indicators/1014'


class PricePVPC20DHS(PricePVPC):
    path = 'indicators/1015'


class PriceSPOTDaily(PriceSPOT):
    path = 'indicators/600'


class PriceSPOTIntraday1(PriceSPOT):
    path = 'indicators/612'


class PriceSPOTIntraday2(PriceSPOT):
    path = 'indicators/613'


class PriceSPOTIntraday3(PriceSPOT):
    path = 'indicators/614'


class PriceSPOTIntraday4(PriceSPOT):
    path = 'indicators/615'


class PriceSPOTIntraday5(PriceSPOT):
    path = 'indicators/616'


class PriceSPOTIntraday6(PriceSPOT):
    path = 'indicators/617'


class PriceSPOTIntraday7(PriceSPOT):
    path = 'indicators/618'
