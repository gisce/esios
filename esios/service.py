import json

from libsaas import http
from libsaas.services import base

from esios import indicators
from esios import archives

class Esios(base.Resource):
    """e.sios Service API.
    :param token: token to access the API
    """
    def __init__(self, token):
        self.token = token
        self.apiroot = 'https://api.esios.ree.es'
        self.version = 'v2'
        self.add_filter(self.use_json)
        self.add_filter(self.accepted_version)
        self.add_filter(self.add_token)

    def use_json(self, request):
        if request.method.upper() not in http.URLENCODE_METHODS:
            request.headers['Content-Type'] = 'application/json'
            request.params = json.dumps(request.params)

    def add_token(self, request):
        request.headers['Authorization'] = 'Token token="{0}"'.format(self.token)

    def accepted_version(self, request):
        request.headers['Accept'] = (
            'appliaction/json; application/vnd.esios-api-{0}+json'
        ).format(self.version)

    def get_url(self):
        return self.apiroot

    @base.resource(indicators.ProfilePVPC20A)
    def profile_pvpc_20A(self):
        """Get the profiles to invoice PVPC for 2.0A
        """
        return indicators.ProfilePVPC20A(self)

    @base.resource(indicators.ProfilePVPC20DHA)
    def profile_pvpc_20DHA(self):
        """Get the profiles to invoice PVPC for 2.0DHA
        """
        return indicators.ProfilePVPC20DHA(self)

    @base.resource(indicators.ProfilePVPC20DHS)
    def profile_pvpc_20DHS(self):
        """Get the profiles to invoice PVPC for 2.0DHS
        """
        return indicators.ProfilePVPC20DHS(self)

    @base.resource(indicators.LinkBalanceMorocco)
    def link_balance_morocco(self):
        """Morocco interconnection balance real time measurements."""
        return indicators.LinkBalanceMorocco(self)

    @base.resource(archives.Liquicomun)
    def liquicomun(self):
        """Get the liquicomun zip file
        """
        return archives.Liquicomun(self)

    @base.resource(archives.A1_liquicomun)
    def A1_liquicomun(self):
        """Get the liquicomun zip file
        """
        return archives.A1_liquicomun(self)

    @base.resource(archives.A2_liquicomun)
    def A2_liquicomun(self):
        """Get the liquicomun zip file
        """
        return archives.A2_liquicomun(self)

    @base.resource(archives.C2_liquicomun)
    def C2_liquicomun(self):
        """Get the liquicomun zip file
        """
        return archives.C2_liquicomun(self)
