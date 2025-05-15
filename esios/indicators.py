from datetime import datetime

from libsaas import http, parsers
from libsaas.services import base


class Indicator(base.RESTResource):
    path = 'indicators'
    time_trunc = 'hour'
    time_agg = 'sum'

    @staticmethod
    def validate_parameters(start_date, end_date, time_trunc, time_agg):
        assert isinstance(start_date, datetime), "Start date is not a datetime"
        assert isinstance(end_date, datetime), "End date is not a datetime"
        if start_date.tzinfo is None:
            raise Exception('Start date must have time zone')
        if end_date.tzinfo is None:
            raise Exception('End date must have time zone')
        assert time_trunc in [
            'five_minutes', 'ten_minutes', 'fifteen_minutes', 'hour', 'day',
            'month', 'year'
        ], "{} is not a valid parameter".format(time_trunc)
        assert time_agg in [
            'sum', 'average',
        ], "{} is not a valid parameter".format(time_agg)


    @base.apimethod
    def get(self, start_date, end_date, time_trunc=None, time_agg=None):
        """
        :param start_date: Start of the date range (ISO 8601 format).
        :param end_date: End of the date range (ISO 8601 format).
        :param time_trunc: Time granularity. Accepted values:
            'five_minutes', 'ten_minutes', 'fifteen_minutes', 'hour', 'day',
            'month', 'year'. Default is 'hour'.
        :param time_agg: Aggregation method. Accepted values: 'sum', 'average'.
            Default is 'sum'.
        :return: Parsed indicator values for the specified range and parameters.
        """
        if time_trunc is None:
            time_trunc = self.time_trunc
        if time_agg is None:
            time_agg = self.time_agg
        self.validate_parameters(start_date, end_date, time_trunc, time_agg)
        start_date = start_date.isoformat()
        end_date = end_date.isoformat()
        params = base.get_params(
            ('start_date', 'end_date', 'time_trunc', 'time_agg'), locals()
        )
        request = http.Request('GET', self.get_url(), params)
        return request, parsers.parse_json


class ProfilePVPC(Indicator):
    pass

class DemandaDiariaElectricaPeninsularPrevista(Indicator):
    path = 'indicators/460'
    time_agg = 'average'


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

class DemandaDiariaElectricaPeninsularReal(Indicator):
    path = 'indicators/1293'
    time_agg = 'average'

class mhpEnergyBalanceFree(Indicator):
    path = 'indicators/1366'

class mhpEnergyBalanceCUR(Indicator):
    path = 'indicators/1367'

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


class PriceMedioHorarioAJOMtotal(Indicator):
    path = 'indicators/1907'


class PriceMedioHorarioAJOMnocur(Indicator):
    path = 'indicators/1908'


class PriceMedioHorarioAJOMcur(Indicator):
    path = 'indicators/1909'


class PriceSRAD(Indicator):
    path = 'indicators/1930'

class PrecioMercadoDiario(Indicator):
    path = 'indicators/600'

class PrecioDesviosSubir(Indicator):
    path = 'indicators/686'

class PrecioDesviosBajar(Indicator):
    path = 'indicators/687'


# Net volume of generation-demand deviations
class GenerationDemandDeviation(Indicator):
    """
    Sum of the deviations to adjust upwards and downwards in respect to the demand
    in one hour, each one in with a sign.
    Publication: every hour with the information of the day D calculated until
    the moment.
    In kWh
    """
    path = 'indicators/1338'


# Demand of electricity (in kW)
class DemandNationalReal(Indicator):
    path = 'indicators/2037'


class DemandNationalForecasted(Indicator):
    path = 'indicators/2052'


class DemandNationalScheduled(Indicator):
    path = 'indicators/2053'


class DemandNationalForecastedForSNP(Indicator):
    """
    Demand forecasted at natinal level for non peninsular systems.
    """
    path = 'indicators/2084'


class DemandPeninsularReal(Indicator):
    path = 'indicators/1293'


class DemandPeninsularRealSumGeneration(Indicator):
    path = 'indicators/10004'


class DemandPeninsularForecasted(Indicator):
    path = 'indicators/544'


class DemandPeninsularScheduled(Indicator):
    path = 'indicators/545'


class DemandPeninsularForecastDaily(Indicator):
    """
    Forecast of the next 7 days.
    """
    path = 'indicators/460'


class DemandPeninsularForecastWeekly(Indicator):
    """
    Forecast of the next week.
    """
    path = 'indicators/603'


# kWh
class DemandPeninsularForecastMonthly(Indicator):
    """
    Forecast of the next 12 Months. In kWh.
    """
    path = 'indicators/461'


class DemandPeninsularForecastYearly(Indicator):
    """
    From december to december next year. In kWh.
    """
    path = 'indicators/1774'


class DemandNonPeninsularSystemReal(Indicator):
    path = 'indicators/1740'


class DemandNonPeninsularSystemRealSumGeneration(Indicator):
    path = 'indicators/10350'


class DemandNonPeninsularSystemForecasted(Indicator):
    path = 'indicators/1742'


class DemandNonPeninsularSystemScheduled(Indicator):
    path = 'indicators/1741'


# national generation of electricity (in kW)
class GenerationNationalWind(Indicator):
    path = 'indicators/2038'


class GenerationNationalNuclear(Indicator):
    path = 'indicators/2039'


class GenerationNationalCoal(Indicator):
    path = 'indicators/2040'


class GenerationNationalCombinedCycle(Indicator):
    path = 'indicators/2041'


class GenerationNationalExchanges(Indicator):
    path = 'indicators/553'


class GenerationNationalSolarPhotovoltaic(Indicator):
    path = 'indicators/2044'


class GenerationNationalSolarThermal(Indicator):
    path = 'indicators/2045'


class GenerationNationalRenewableThermal(Indicator):
    path = 'indicators/2046'


class GenerationNationalDiesel(Indicator):
    path = 'indicators/2047'


class GenerationNationalGasTrubine(Indicator):
    path = 'indicators/2048'


class GenerationNationalSteamTurbine(Indicator):
    path = 'indicators/2049'


class GenerationNationalAuxiliary(Indicator):
    path = 'indicators/2050'


class GenerationNationalCogenerationAndWaste(Indicator):
    path = 'indicators/2051'


class GenerationNationalHydraulic(Indicator):
    path = 'indicators/2067'


class GenerationNationalHydraulicAggregated(Indicator):
    """
    Represents national-level hydraulic energy indicators, including:
    - Pumping turbine output
    - Pumping energy consumption
    - Hydraulic generation
    Plus or minus some error.
    """
    path = 'indicators/2042'


class GenerationNationalStoragePumpingTurbine(Indicator):
    path = 'indicators/2066'


class GenerationNationalStoragePumpingConsumption(Indicator):
    path = 'indicators/2065'


class GenerationNationalStorageBatteryDelivery(Indicator):
    path = 'indicators/2198'


class GenerationNationalStorageBatteryCharging(Indicator):
    path = 'indicators/2199'


class GenerationNationalExportAndorra(Indicator):
    path = 'indicators/2068'


class GenerationNationalExportMorocco(Indicator):
    path = 'indicators/2069'


class GenerationNationalExportPortugal(Indicator):
    path = 'indicators/2070'


class GenerationNationalExportFrance(Indicator):
    path = 'indicators/2071'


class GenerationNationalExportTotal(Indicator):
    path = 'indicators/2072'


class GenerationNationalImportAndorra(Indicator):
    path = 'indicators/2073'


class GenerationNationalImportMorocco(Indicator):
    path = 'indicators/2074'


class GenerationNationalImportPortugal(Indicator):
    path = 'indicators/2075'


class GenerationNationalImportFrance(Indicator):
    path = 'indicators/2076'


class GenerationNationalImportTotal(Indicator):
    path = 'indicators/2077'


# peninsular generation of electricity (in kW)
class GenerationPeninsularWind(Indicator):
    path = 'indicators/551'


class GenerationPeninsularNuclear(Indicator):
    path = 'indicators/549'


class GenerationPeninsularFuelGas(Indicator):
    path = 'indicators/548'


class GenerationPeninsularCoal(Indicator):
    path = 'indicators/547'


class GenerationPeninsularCombinedCycle(Indicator):
    path = 'indicators/550'


class GenerationPeninsularExchanges(Indicator):
    path = 'indicators/553'


class GenerationPeninsularBalearicLink(Indicator):
    path = 'indicators/554'


class GenerationPeninsularSolarPhotovoltaic(Indicator):
    """
    Contains data since 02/06/2015 21:00 (spain tz).
    """
    path = 'indicators/1295'


class GenerationPeninsularSolarThermal(Indicator):
    """
    Contains data since 02/06/2015 21:00 (spain tz).
    """
    path = 'indicators/1294'


class GenerationPeninsularRenewableThermal(Indicator):
    path = 'indicators/1296'


class GenerationPeninsularCogenerationAndWaste(Indicator):
    path = 'indicators/1297'


class GenerationPeninsularHydraulic(Indicator):
    path = 'indicators/2080'


class GenerationPeninsularHydraulicAggregated(Indicator):
    """
    Represents peninsular-level hydraulic energy indicators, including:
    - Pumping turbine output
    - Pumping energy consumption
    - Hydraulic generation
    Plus or minus some error.
    """
    path = 'indicators/546'


class GenerationPeninsularStoragePumpingTurbine(Indicator):
    path = 'indicators/2079'


class GenerationPeninsularStoragePumpingConsumption(Indicator):
    path = 'indicators/2078'


class GenerationPeninsularStorageBatteryDelivery(Indicator):
    path = 'indicators/2167'


class GenerationPeninsularStorageBatteryCharging(Indicator):
    path = 'indicators/2166'


class GenerationPeninsularExportAndorra(Indicator):
    path = 'indicators/2068'


class GenerationPeninsularExportMorocco(Indicator):
    path = 'indicators/2069'


class GenerationPeninsularExportPortugal(Indicator):
    path = 'indicators/2070'


class GenerationPeninsularExportFrance(Indicator):
    path = 'indicators/2071'


class GenerationPeninsularExportTotal(Indicator):
    path = 'indicators/2072'


class GenerationPeninsularImportAndorra(Indicator):
    path = 'indicators/2073'


class GenerationPeninsularImportMorocco(Indicator):
    path = 'indicators/2074'


class GenerationPeninsularImportPortugal(Indicator):
    path = 'indicators/2075'


class GenerationPeninsularImportFrance(Indicator):
    path = 'indicators/2076'


class GenerationPeninsularImportTotal(Indicator):
    path = 'indicators/2077'


class GenerationPeninsularSolarAggregatedOutdated(Indicator):
    """
    Contains data until 02/06/2015 20:50 (spain tz).
    Solar thermal + solar photovoltaic
    """
    path = 'indicators/552'


class GenerationPeninsularSolarAggregated(Indicator):
    """
    Contains data since 02/06/2015 21:00 (spain tz).
    Solar thermal + solar photovoltaic
    """
    path = 'indicators/10206'


# non peninsular systems (SNP) (separated by region) (in kW)
class GenerationNonPeninsularSystemWind(Indicator):
    path = 'indicators/1745'


class GenerationNonPeninsularSystemCoal(Indicator):
    path = 'indicators/1750'


class GenerationNonPeninsularSystemCombinedCycle(Indicator):
    path = 'indicators/1746'


class GenerationNonPeninsularSystemBalearicLink(Indicator):
    path = 'indicators/1751'


class GenerationNonPeninsularSystemSolarPhotovoltaic(Indicator):
    path = 'indicators/1748'


class GenerationNonPeninsularSystemDiesel(Indicator):
    path = 'indicators/1743'


class GenerationNonPeninsularSystemGasTrubine(Indicator):
    path = 'indicators/1744'


class GenerationNonPeninsularSystemSteamTurbine(Indicator):
    path = 'indicators/1747'


class GenerationNonPeninsularSystemAuxiliary(Indicator):
    path = 'indicators/1754'


class GenerationNonPeninsularSystemCogenerationAndWaste(Indicator):
    path = 'indicators/1755'


class GenerationNonPeninsularSystemHydraulic(Indicator):
    path = 'indicators/2083'


class GenerationNonPeninsularSystemHydraulicAggregated(Indicator):
    """
    Represents peninsular-level hydraulic energy indicators, including:
    - Pumping turbine output
    - Pumping energy consumption
    - Hydraulic generation
    Plus or minus some error.
    """
    path = 'indicators/1749'


class GenerationNonPeninsularSystemStoragePumpingTurbine(Indicator):
    path = 'indicators/2082'


class GenerationNonPeninsularSystemStoragePumpingConsumption(Indicator):
    path = 'indicators/2081'


class GenerationNonPeninsularSystemStorageBatteryDelivery(Indicator):
    path = 'indicators/2169'


class GenerationNonPeninsularSystemStorageBatteryCharging(Indicator):
    path = 'indicators/2168'
