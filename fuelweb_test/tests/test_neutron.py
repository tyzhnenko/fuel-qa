#    Copyright 2013 Mirantis, Inc.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.
from warnings import warn

from proboscis.asserts import assert_equal
from proboscis import test
from proboscis import SkipTest

from fuelweb_test.helpers.common import Common
from fuelweb_test.helpers.decorators import log_snapshot_after_test
from fuelweb_test.helpers import os_actions
from fuelweb_test import logger
from fuelweb_test.settings import DEPLOYMENT_MODE
from fuelweb_test.settings import NEUTRON_SEGMENT
from fuelweb_test.tests.base_test_case import SetupEnvironment
from fuelweb_test.tests.base_test_case import TestBasic


@test(enabled=False, groups=["thread_1", "neutron"])
class NeutronVlan(TestBasic):
    """NeutronVlan.

    Test disabled and move to fuel_tests suite:
        fuel_tests.test.test_neutron

    """  # TODO documentation

    @test(enabled=False,
          depends_on=[SetupEnvironment.prepare_slaves_3],
          groups=["deploy_neutron_vlan", "ha_one_controller_neutron_vlan",
                  "deployment", "nova", "nova-compute"])
    @log_snapshot_after_test
    def deploy_neutron_vlan(self):
        """Deploy cluster in ha mode with 1 controller and Neutron VLAN

        Test disabled and move to fuel_tests suite:
            fuel_tests.test.test_neutron.TestNeutronVlan

        Scenario:
            1. Create cluster
            2. Add 1 node with controller role
            3. Add 2 nodes with compute role
            4. Deploy the cluster
            5. Run network verification
            6. Run OSTF

        Duration 35m
        Snapshot deploy_neutron_vlan

        """
        # pylint: disable=W0101
        warn("Test disabled and move to fuel_tests suite", DeprecationWarning)
        raise SkipTest("Test disabled and move to fuel_tests suite")

        self.env.revert_snapshot("ready_with_3_slaves")

        cluster_id = self.fuel_web.create_cluster(
            name=self.__class__.__name__,
            mode=DEPLOYMENT_MODE,
            settings={
                "net_provider": 'neutron',
                "net_segment_type": NEUTRON_SEGMENT['vlan'],
                'tenant': 'simpleVlan',
                'user': 'simpleVlan',
                'password': 'simpleVlan'
            }
        )
        self.fuel_web.update_nodes(
            cluster_id,
            {
                'slave-01': ['controller'],
                'slave-02': ['compute'],
                'slave-03': ['compute']
            }
        )
        self.fuel_web.deploy_cluster_wait(cluster_id)

        cluster = self.fuel_web.client.get_cluster(cluster_id)
        assert_equal(str(cluster['net_provider']), 'neutron')

        self.fuel_web.verify_network(cluster_id)

        self.fuel_web.run_ostf(
            cluster_id=cluster_id)

        self.env.make_snapshot("deploy_neutron_vlan", is_make=True)


@test(enabled=False,
      groups=["neutron", "ha", "ha_neutron", "classic_provisioning"])
class NeutronGreHa(TestBasic):
    """NeutronGreHa.

    Test disabled and move to fuel_tests suite:
        fuel_tests.test.test_neutron

    """  # TODO documentation

    @test(enabled=False,
          depends_on=[SetupEnvironment.prepare_slaves_5],
          groups=["deploy_neutron_gre_ha", "ha_neutron_gre"])
    @log_snapshot_after_test
    def deploy_neutron_gre_ha(self):
        """Deploy cluster in HA mode with Neutron GRE (DEPRECATED)

        Test disabled and move to fuel_tests suite:
            fuel_tests.test.test_neutron.TestNeutronTunHa

        Scenario:
            1. Create cluster
            2. Add 3 nodes with controller role
            3. Add 2 nodes with compute role
            4. Deploy the cluster
            5. Run network verification
            6. Check Swift ring and rebalance it if needed
            7. Run OSTF

        Duration 80m
        Snapshot deploy_neutron_gre_ha

        """
        # pylint: disable=W0101
        warn("Test disabled and move to fuel_tests suite", DeprecationWarning)
        raise SkipTest("Test disabled and move to fuel_tests suite")

        self.env.revert_snapshot("ready_with_5_slaves")

        cluster_id = self.fuel_web.create_cluster(
            name=self.__class__.__name__,
            mode=DEPLOYMENT_MODE,
            settings={
                "net_provider": 'neutron',
                "net_segment_type": NEUTRON_SEGMENT['gre'],
                'tenant': 'haGre',
                'user': 'haGre',
                'password': 'haGre'
            }
        )
        self.fuel_web.update_nodes(
            cluster_id,
            {
                'slave-01': ['controller'],
                'slave-02': ['controller'],
                'slave-03': ['controller'],
                'slave-04': ['compute'],
                'slave-05': ['compute']
            }
        )
        self.fuel_web.deploy_cluster_wait(cluster_id)

        cluster = self.fuel_web.client.get_cluster(cluster_id)
        assert_equal(str(cluster['net_provider']), 'neutron')

        self.fuel_web.verify_network(cluster_id)
        devops_node = self.fuel_web.get_nailgun_primary_node(
            self.env.d_env.nodes().slaves[0])
        logger.debug("devops node name is {0}".format(devops_node.name))
        ip = self.fuel_web.get_nailgun_node_by_name(devops_node.name)['ip']
        Common.rebalance_swift_ring(ip)

        self.fuel_web.run_ostf(
            cluster_id=cluster_id,
            test_sets=['ha', 'smoke', 'sanity'])

        self.env.make_snapshot("deploy_neutron_gre_ha")


@test(enabled=False, groups=["neutron", "ha", "ha_neutron"])
class NeutronVlanHa(TestBasic):
    """NeutronVlanHa.

    Test disabled and move to fuel_tests suite:
        fuel_tests.test.test_neutron

    """  # TODO documentation

    @test(enabled=False,
          depends_on=[SetupEnvironment.prepare_slaves_5],
          groups=["deploy_neutron_vlan_ha", "neutron_vlan_ha"])
    @log_snapshot_after_test
    def deploy_neutron_vlan_ha(self):
        """Deploy cluster in HA mode with Neutron VLAN

        Test disabled and move to fuel_tests suite:
            fuel_tests.test.test_neutron.TestNeutronVlanHa

        Scenario:
            1. Create cluster
            2. Add 3 nodes with controller role
            3. Add 2 nodes with compute role
            4. Deploy the cluster
            5. Run network verification
            6. Check Swift ring and rebalance it if needed
            7. Run OSTF

        Duration 80m
        Snapshot deploy_neutron_vlan_ha

        """
        # pylint: disable=W0101
        warn("Test disabled and move to fuel_tests suite", DeprecationWarning)
        raise SkipTest("Test disabled and move to fuel_tests suite")

        self.env.revert_snapshot("ready_with_5_slaves")

        cluster_id = self.fuel_web.create_cluster(
            name=self.__class__.__name__,
            mode=DEPLOYMENT_MODE,
            settings={
                "net_provider": 'neutron',
                "net_segment_type": NEUTRON_SEGMENT['vlan']
            }
        )
        self.fuel_web.update_nodes(
            cluster_id,
            {
                'slave-01': ['controller'],
                'slave-02': ['controller'],
                'slave-03': ['controller'],
                'slave-04': ['compute'],
                'slave-05': ['compute']
            }
        )
        self.fuel_web.update_internal_network(cluster_id, '192.168.196.0/22',
                                              '192.168.196.1')
        self.fuel_web.deploy_cluster_wait(cluster_id)

        cluster = self.fuel_web.client.get_cluster(cluster_id)
        assert_equal(str(cluster['net_provider']), 'neutron')
        os_conn = os_actions.OpenStackActions(
            self.fuel_web.get_public_vip(cluster_id))
        self.fuel_web.check_fixed_network_cidr(
            cluster_id, os_conn)

        self.fuel_web.verify_network(cluster_id)
        devops_node = self.fuel_web.get_nailgun_primary_node(
            self.env.d_env.nodes().slaves[0])
        logger.debug("devops node name is {0}".format(devops_node.name))
        ip = self.fuel_web.get_nailgun_node_by_name(devops_node.name)['ip']
        Common.rebalance_swift_ring(ip)

        self.fuel_web.run_ostf(
            cluster_id=cluster_id, test_sets=['ha', 'smoke', 'sanity'])

        self.env.make_snapshot("deploy_neutron_vlan_ha")
