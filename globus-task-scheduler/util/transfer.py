"""
Create a Globus transfer from one endpoint to another
"""
import os

import globus_sdk

CLIENT = os.environ['GLOBUS_PORTAL_CLIENT']
REFRESH_TOKEN = os.environ['GLOBUS_PORTAL_REFRESH_TOKEN']


class Transfer(object):

    def __init__(self, refresh_token=None):
        self.refresh_token = REFRESH_TOKEN if refresh_token is None else refresh_token

    @classmethod
    def new_refresh_token(cls,):
        c = globus_sdk.NativeAppAuthClient(CLIENT)
        c.oauth2_start_flow(refresh_tokens=True)
        print(f'Please go to this URL and login: {c.oauth2_get_authorize_url()}')
        auth_code = input('Please enter the code here: ').strip()
        tr = c.oauth2_exchange_code_for_tokens(auth_code)
        return cls(refresh_token=tr.by_resource_server['transfer.api.globus.org']['refresh_token'])

    @property
    def client(self,):
        return globus_sdk.NativeAppAuthClient(CLIENT,)

    @property
    def authorizer(self,):
        return globus_sdk.RefreshTokenAuthorizer(self.refresh_token, self.client)

    @property
    def transfer_client(self,):
        return globus_sdk.TransferClient(authorizer=self.authorizer)

    @property
    def endpoints(self,):
        return [e for e in self.transfer_client.endpoint_search(filter_scope='my-endpoints')]

    def get_endpoint_name_from_id(self, idx):
        name = [e['display_name'] for e in self.endpoints if e['id']==idx]
        if len(name) == 0:
            raise ValueError(f'No endpoint with id {idx}')
        else:
            return name[0]

    def transfer_data(self, source_id, target_id, items):
        tc = self.transfer_client
        td = globus_sdk.TransferData(tc, source_id, target_id)
        for i in items:
            recursive = i.get('recursive', False)
            td.add_item(i['source'], i['target'], recursive=recursive)
        return tc.submit_transfer(td)
