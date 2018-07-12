# -*- coding: utf-8 -*-
"""
This module contains a BigQuery Hook, as well as a very basic PEP 249
implementation for BigQuery.
"""

import hvac
import os

from airflow.exceptions import AirflowException

from airflow.contrib.hooks.gcp_api_base_hook import GoogleCloudBaseHook
from airflow.hooks.dbapi_hook import DbApiHook
from airflow.utils.log.logging_mixin import LoggingMixin


class VaultGoogleCloudHook(GoogleCloudBaseHook, DbApiHook, LoggingMixin):
    """
    Interacts with Vault. This hook retrieves credentials from Vault.
    """
    path_part = {
        'service_account': 'key',
        'access_token': 'token'
    }

    def __init__(self, vault_conn_id):
        super(VaultGoogleCloudHook, self).__init__(conn_id=vault_conn_id)
        self._get_credentials()

    def _get_credentials(self):
        """
        Returns the Credentials object for Google API
        """
        conn = self.get_connection(self.conn_id)

        token = conn.password
        url = conn.host

        secret_type = self._get_field('secret_type')
        roleset = self._get_field('roleset')

        secret_engine_path = self._get_field('secret_engine_path')

        if secret_type == 'access_token':
            raise AirflowException('Currently only service account key is supprted!')

        client = hvac.Client(url=url, token=token)

        vault_path = os.path.join(secret_engine_path, self.path_part[secret_type], roleset)
        raise AirflowException(vault_path)

        # elif key_path:
        #     # if not scope:
        #     #     raise AirflowException('Scope should be defined when using a key file.')
        #     # scopes = [s.strip() for s in scope.split(',')]

        #     # Get credentials from a JSON file.
        #     if key_path.endswith('.json'):
        #         self.log.info('Getting connection using a JSON key file.')
        #         credentials = ServiceAccountCredentials\
        #             .from_json_keyfile_name(key_path, scopes)
        # else:
        #     scopes = [s.strip() for s in scope.split(',')]

        #     # Get credentials from JSON data provided in the UI.
        #     try:
        #         keyfile_dict = json.loads(keyfile_dict)

        #         # Depending on how the JSON was formatted, it may contain
        #         # escaped newlines. Convert those to actual newlines.
        #         keyfile_dict['private_key'] = keyfile_dict['private_key'].replace(
        #             '\\n', '\n')

        #         credentials = ServiceAccountCredentials\
        #             .from_json_keyfile_dict(keyfile_dict, scopes)
        # return credentials

    def _get_field(self, f, default=None):
        """
        Fetches a field from extras, and returns it. This is some Airflow
        magic. The google_cloud_platform hook type adds custom UI elements
        to the hook page, which allow admins to specify service_account,
        key_path, etc. They get formatted as shown below.
        """
        long_f = 'extra__vault_google_cloud_platform__{}'.format(f)
        if long_f in self.extras:
            return self.extras[long_f]
        else:
            return default
