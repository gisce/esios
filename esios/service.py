import json

from libsaas import http
from libsaas.services import base


from esios import indicators


class Esios(base.Resource):
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
        return indicators.ProfilePVPC20A(self)

    @base.resource(indicators.ProfilePVPC20DHA)
    def profile_pvpc_20DHA(self):
        return indicators.ProfilePVPC20DHA(self)

    @base.resource(indicators.ProfilePVPC20DHS)
    def profile_pvpc_20DHS(self):
        return indicators.ProfilePVPC20DHS(self)
