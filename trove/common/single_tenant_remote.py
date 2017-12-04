# Copyright (c) 2014 Hewlett-Packard Development Company, L.P.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from trove.common import cfg
from trove.common.remote import normalize_url

from cinderclient.v2 import client as CinderClient
from neutronclient.v2_0 import client as NeutronClient
from novaclient.client import Client as NovaClient

CONF = cfg.CONF

"""
trove.conf
...

The following should be set in the trove CONF file for this
single_tenant_remote config to work correctly.

nova_proxy_admin_user =
nova_proxy_admin_pass =
nova_proxy_admin_tenant_name =
trove_auth_url =
nova_compute_service_type =
nova_compute_url =
cinder_service_type =
os_region_name =

remote_nova_client = \
 trove.common.single_tenant_remote.nova_client_trove_admin
remote_cinder_client = \
 trove.common.single_tenant_remote.cinder_client_trove_admin
remote_neutron_client = \
 trove.common.single_tenant_remote.neutron_client_trove_admin
...

"""


def nova_client_trove_admin(context, region_name=None, password=None):
    """
    Returns a nova client object with the trove admin credentials

    All parameters are ignored since all the required informations are
    taken from CONF. The parameters are there just to be able to replace
    trove.common.nova_client.

    :param context
    :param region_name
    :param password
    :return novaclient: novaclient with trove admin credentials
    :rtype: novaclient.Client
    """

    client = NovaClient(CONF.nova_client_version,
                        username=CONF.nova_proxy_admin_user,
                        password=CONF.nova_proxy_admin_pass,
                        project_name=CONF.nova_proxy_admin_tenant_name,
                        auth_url=CONF.trove_auth_url,
                        service_type=CONF.nova_compute_service_type,
                        region_name=CONF.os_region_name,
                        insecure=CONF.nova_api_insecure)

    if CONF.nova_compute_url and CONF.nova_proxy_admin_tenant_id:
        client.client.endpoint_override = "%s/%s/" % (
            normalize_url(compute_url),
            CONF.nova_proxy_admin_tenant_id)

    return client


def cinder_client_trove_admin(context, region_name=None):
    """
    Returns a cinder client object with the trove admin credentials

    All parameters are ignored since all the required informations are
    taken from CONF. The parameters are there just to be able to replace
    trove.common.cinder_client.

    :param context
    :param region_name
    :return cinderclient: cinderclient with trove admin credentials
    """
    client = CinderClient.Client(CONF.nova_proxy_admin_user,
                                 CONF.nova_proxy_admin_pass,
                                 project_id=CONF.nova_proxy_admin_tenant_name,
                                 auth_url=CONF.trove_auth_url,
                                 service_type=CONF.cinder_service_type,
                                 region_name=CONF.os_region_name,
                                 insecure=CONF.cinder_api_insecure)

    if CONF.cinder_url and CONF.nova_proxy_admin_tenant_id:
        client.client.management_url = "%s/%s/" % (
            normalize_url(CONF.cinder_url), CONF.nova_proxy_admin_tenant_id)

    return client


def neutron_client_trove_admin(context, region_name=None):
    """
    Returns a neutron client object with the trove admin credentials

    All parameters are ignored since all the required informations are
    taken from CONF. The parameters are there just to be able to replace
    trove.common.neutron_client.

    :param context
    :param region_name
    :return neutronclient: neutronclient with trove admin credentials
    """
    client = NeutronClient.Client(
        username=CONF.nova_proxy_admin_user,
        password=CONF.nova_proxy_admin_pass,
        tenant_name=CONF.nova_proxy_admin_tenant_name,
        auth_url=CONF.trove_auth_url,
        service_type=CONF.neutron_service_type,
        region_name=CONF.os_region_name,
        insecure=CONF.neutron_api_insecure)

    if CONF.neutron_url:
        client.management_url = CONF.neutron_url

    return client
