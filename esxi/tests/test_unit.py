# (C) Datadog, Inc. 2024-present
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)
import copy
import logging

import pytest
from mock import MagicMock
from pyVmomi import vim, vmodl

from datadog_checks.esxi import EsxiCheck


@pytest.mark.usefixtures("service_instance")
def test_esxi_metric_up(instance, dd_run_check, aggregator, caplog):
    check = EsxiCheck('esxi', {}, [instance])
    caplog.set_level(logging.DEBUG)
    dd_run_check(check)
    aggregator.assert_metric('esxi.host.can_connect', 1, count=1, tags=["esxi_url:localhost"])
    assert "Connected to ESXi host localhost: VMware ESXi 6.5.0 build-123456789" in caplog.text


def test_emits_critical_service_check_when_service_is_down(dd_run_check, aggregator, instance, caplog):
    check = EsxiCheck('esxi', {}, [instance])
    caplog.set_level(logging.WARNING)
    dd_run_check(check)

    aggregator.assert_metric('esxi.host.can_connect', value=0, tags=["esxi_url:localhost"])
    assert "Cannot connect to ESXi host" in caplog.text


@pytest.mark.usefixtures("service_instance")
def test_none_properties_data(vcsim_instance, dd_run_check, aggregator, service_instance, caplog):
    service_instance.content.propertyCollector.RetrievePropertiesEx = MagicMock(return_value=None)
    check = EsxiCheck('esxi', {}, [vcsim_instance])
    caplog.set_level(logging.WARNING)
    dd_run_check(check)

    assert "No resources found; halting check execution" in caplog.text

    base_tags = ["esxi_url:127.0.0.1:8989"]
    aggregator.assert_metric("esxi.host.can_connect", 1, count=1, tags=base_tags)
    aggregator.assert_all_metrics_covered()


@pytest.mark.usefixtures("service_instance")
def test_esxi_no_properties(vcsim_instance, dd_run_check, aggregator, service_instance, caplog):
    retrieve_result = vim.PropertyCollector.RetrieveResult(
        objects=[
            vim.ObjectContent(
                obj=vim.HostSystem(moId="host"),
                propSet=[],
            )
        ]
    )
    service_instance.content.propertyCollector.RetrievePropertiesEx = MagicMock(return_value=retrieve_result)
    check = EsxiCheck('esxi', {}, [vcsim_instance])
    caplog.set_level(logging.WARNING)
    dd_run_check(check)

    assert "No resources found; halting check execution" in caplog.text

    base_tags = ["esxi_url:127.0.0.1:8989"]
    aggregator.assert_metric("esxi.host.can_connect", 1, count=1, tags=base_tags)
    aggregator.assert_all_metrics_covered()


@pytest.mark.usefixtures("service_instance")
def test_esxi_no_hostname(vcsim_instance, dd_run_check, aggregator, service_instance, caplog):
    retrieve_result = vim.PropertyCollector.RetrieveResult(
        objects=[
            vim.ObjectContent(
                obj=vim.HostSystem(moId="host"),
                propSet=[
                    vmodl.DynamicProperty(
                        name='test',
                        val='c1',
                    ),
                ],
            )
        ]
    )
    service_instance.content.propertyCollector.RetrievePropertiesEx = MagicMock(return_value=retrieve_result)
    check = EsxiCheck('esxi', {}, [vcsim_instance])
    caplog.set_level(logging.DEBUG)
    dd_run_check(check)

    assert "No host name found for 'vim.HostSystem:host'; skipping" in caplog.text


@pytest.mark.usefixtures("service_instance")
def test_hostname_multiple_props(vcsim_instance, dd_run_check, aggregator, service_instance, caplog):
    retrieve_result = vim.PropertyCollector.RetrieveResult(
        objects=[
            vim.ObjectContent(
                obj=vim.HostSystem(moId="host"),
                propSet=[
                    vmodl.DynamicProperty(
                        name='test',
                        val='test',
                    ),
                    vmodl.DynamicProperty(
                        name='name',
                        val='hostname',
                    ),
                ],
            )
        ]
    )
    service_instance.content.propertyCollector.RetrievePropertiesEx = MagicMock(return_value=retrieve_result)
    check = EsxiCheck('esxi', {}, [vcsim_instance])
    dd_run_check(check)

    aggregator.assert_metric("esxi.cpu.usage.avg", hostname="hostname")


@pytest.mark.usefixtures("service_instance")
def test_esxi_perf_metrics(vcsim_instance, dd_run_check, aggregator, caplog):
    check = EsxiCheck('esxi', {}, [vcsim_instance])
    caplog.set_level(logging.DEBUG)
    dd_run_check(check)

    base_tags = ["esxi_url:127.0.0.1:8989"]
    aggregator.assert_metric("esxi.cpu.usage.avg", value=26, tags=base_tags, hostname="localhost.localdomain")
    aggregator.assert_metric("esxi.mem.granted.avg", value=80, tags=base_tags, hostname="localhost.localdomain")
    aggregator.assert_metric("esxi.host.can_connect", 1, count=1, tags=base_tags)

    assert "Skipping metric net.droppedRx.sum for localhost.localdomain, because the value "
    "returned by the host is negative (i.e. the metric is not yet available). values: [-1]" in caplog.text

    assert (
        "Skipping metric net.droppedRx.sum for localhost.localdomain because no value was returned by the host"
    ) in caplog.text


@pytest.mark.usefixtures("service_instance")
def test_vm_perf_metrics(vcsim_instance, dd_run_check, aggregator):
    check = EsxiCheck('esxi', {}, [vcsim_instance])
    dd_run_check(check)

    base_tags = ["esxi_url:127.0.0.1:8989"]
    aggregator.assert_metric("esxi.cpu.usage.avg", value=18, tags=base_tags, hostname="vm1")
    aggregator.assert_metric("esxi.cpu.usage.avg", value=19, tags=base_tags, hostname="vm2")
    aggregator.assert_metric("esxi.net.droppedRx.sum", value=28, tags=base_tags, hostname="vm1")


@pytest.mark.usefixtures("service_instance")
def test_external_host_tags(vcsim_instance, datadog_agent, dd_run_check):
    check = EsxiCheck('esxi', {}, [vcsim_instance])
    dd_run_check(check)
    datadog_agent.assert_external_tags(
        'localhost.localdomain',
        {
            'esxi': [
                'esxi_datacenter:dc2',
                'esxi_folder:folder_1',
                'esxi_type:host',
                'esxi_url:127.0.0.1:8989',
            ]
        },
    )
    datadog_agent.assert_external_tags(
        'vm1',
        {
            'esxi': [
                'esxi_datacenter:dc2',
                'esxi_folder:folder_1',
                'esxi_type:vm',
                'esxi_url:127.0.0.1:8989',
            ]
        },
    )
    datadog_agent.assert_external_tags(
        'vm2',
        {'esxi': ['esxi_cluster:c1', 'esxi_compute:c1', 'esxi_type:vm', 'esxi_url:127.0.0.1:8989']},
    )


@pytest.mark.usefixtures("service_instance")
def test_external_host_tags_all_resources(vcsim_instance, datadog_agent, dd_run_check, service_instance):
    retrieve_result = vim.PropertyCollector.RetrieveResult(
        objects=[
            vim.ObjectContent(
                obj=vim.VirtualMachine(moId="vm1"),
                propSet=[
                    vmodl.DynamicProperty(
                        name='runtime.host',
                        val=vim.HostSystem(moId="host"),
                    ),
                    vmodl.DynamicProperty(
                        name='name',
                        val='vm1',
                    ),
                ],
            ),
            vim.ObjectContent(
                obj=vim.HostSystem(moId="host"),
                propSet=[
                    vmodl.DynamicProperty(
                        name='parent',
                        val=vim.StoragePod(moId="pod1"),
                    ),
                    vmodl.DynamicProperty(
                        name='name',
                        val='hostname',
                    ),
                ],
            ),
            vim.ObjectContent(
                obj=vim.StoragePod(moId="pod1"),
                propSet=[
                    vmodl.DynamicProperty(
                        name='name',
                        val='pod1',
                    ),
                    vmodl.DynamicProperty(
                        name='parent',
                        val=vim.Datastore(moId="ds1"),
                    ),
                ],
            ),
            vim.ObjectContent(
                obj=vim.Datastore(moId="ds1"),
                propSet=[
                    vmodl.DynamicProperty(
                        name='name',
                        val='ds1',
                    ),
                    vmodl.DynamicProperty(
                        name='parent',
                        val=vim.ClusterComputeResource(moId="c1"),
                    ),
                ],
            ),
            vim.ObjectContent(
                obj=vim.ClusterComputeResource(moId="c1"),
                propSet=[
                    vmodl.DynamicProperty(
                        name='name',
                        val='c1',
                    ),
                    vmodl.DynamicProperty(
                        name='parent',
                        val=vim.HostServiceSystem(moId="hss"),
                    ),
                ],
            ),
            vim.ObjectContent(
                obj=vim.HostServiceSystem(moId="hss"),
                propSet=[
                    vmodl.DynamicProperty(
                        name='name',
                        val='hss',
                    )
                ],
            ),
        ]
    )
    service_instance.content.propertyCollector.RetrievePropertiesEx = MagicMock(return_value=retrieve_result)

    check = EsxiCheck('esxi', {}, [vcsim_instance])
    dd_run_check(check)
    datadog_agent.assert_external_tags(
        'hostname',
        {
            'esxi': [
                'esxi_cluster:c1',
                'esxi_compute:c1',
                'esxi_datastore:ds1',
                'esxi_datastore_cluster:pod1',
                'esxi_type:host',
                'esxi_url:127.0.0.1:8989',
            ]
        },
    )
    datadog_agent.assert_external_tags(
        'vm1',
        {
            'esxi': [
                'esxi_type:vm',
                'esxi_cluster:c1',
                'esxi_url:127.0.0.1:8989',
            ]
        },
    )


@pytest.mark.usefixtures("service_instance")
def test_use_guest_hostname(vcsim_instance, dd_run_check, aggregator):
    vcsim_instance = copy.deepcopy(vcsim_instance)
    vcsim_instance['use_guest_hostname'] = True
    check = EsxiCheck('esxi', {}, [vcsim_instance])
    dd_run_check(check)

    aggregator.assert_metric("esxi.cpu.usage.avg", value=18, hostname="testing-vm")
    aggregator.assert_metric("esxi.cpu.usage.avg", value=19, hostname="test-vm-2")
    aggregator.assert_metric("esxi.cpu.usage.avg", value=26, hostname="localhost.localdomain")


@pytest.mark.usefixtures("service_instance")
def test_report_vm_instance_metrics(aggregator, dd_run_check, vcsim_instance, service_instance):
    retrieve_result = vim.PropertyCollector.RetrieveResult(
        objects=[
            vim.ObjectContent(
                obj=vim.VirtualMachine(moId="vm1"),
                propSet=[
                    vmodl.DynamicProperty(
                        name='name',
                        val='vm1',
                    ),
                ],
            ),
        ]
    )
    service_instance.content.propertyCollector.RetrievePropertiesEx = MagicMock(return_value=retrieve_result)

    service_instance.content.perfManager.QueryPerf = MagicMock(
        side_effect=[
            [
                vim.PerformanceManager.EntityMetric(
                    entity=vim.VirtualMachine(moId="vm1"),
                    value=[
                        vim.PerformanceManager.IntSeries(
                            value=[47, 52],
                            id=vim.PerformanceManager.MetricId(counterId=1, instance='test1'),
                        )
                    ],
                ),
                vim.PerformanceManager.EntityMetric(
                    entity=vim.VirtualMachine(moId="vm1"),
                    value=[
                        vim.PerformanceManager.IntSeries(
                            value=[30, 11],
                            id=vim.PerformanceManager.MetricId(counterId=1, instance='test2'),
                        )
                    ],
                ),
                vim.PerformanceManager.EntityMetric(
                    entity=vim.VirtualMachine(moId="vm1"),
                    value=[
                        vim.PerformanceManager.IntSeries(
                            value=[47, 60],
                            id=vim.PerformanceManager.MetricId(counterId=1),
                        )
                    ],
                ),
            ],
            [],
        ]
    )
    instance = copy.deepcopy(vcsim_instance)

    instance.update(
        {
            'collect_per_instance_filters': {
                'vm': ['cpu.usage.avg'],
            }
        }
    )
    check = EsxiCheck('esxi', {}, [instance])
    dd_run_check(check)

    base_tags = ['esxi_url:127.0.0.1:8989']
    aggregator.assert_metric(
        'esxi.cpu.usage.avg',
        value=52,
        count=1,
        hostname='vm1',
        tags=base_tags + ['cpu_core:test1'],
    )
    aggregator.assert_metric(
        'esxi.cpu.usage.avg',
        value=11,
        count=1,
        hostname='vm1',
        tags=base_tags + ['cpu_core:test2'],
    )
    aggregator.assert_metric(
        'esxi.cpu.usage.avg',
        value=60,
        count=0,
        hostname='vm1',
        tags=base_tags,
    )


@pytest.mark.usefixtures("service_instance")
def test_report_instance_metrics_unknown_key(aggregator, dd_run_check, vcsim_instance, service_instance):
    retrieve_result = vim.PropertyCollector.RetrieveResult(
        objects=[
            vim.ObjectContent(
                obj=vim.VirtualMachine(moId="vm1"),
                propSet=[
                    vmodl.DynamicProperty(
                        name='name',
                        val='vm1',
                    ),
                ],
            ),
        ]
    )
    service_instance.content.propertyCollector.RetrievePropertiesEx = MagicMock(return_value=retrieve_result)

    service_instance.content.perfManager.QueryPerf = MagicMock(
        side_effect=[
            [
                vim.PerformanceManager.EntityMetric(
                    entity=vim.VirtualMachine(moId="vm1"),
                    value=[
                        vim.PerformanceManager.IntSeries(
                            value=[3, 10],
                            id=vim.PerformanceManager.MetricId(counterId=65541, instance='test1'),
                        )
                    ],
                ),
            ],
        ]
    )
    instance = copy.deepcopy(vcsim_instance)

    instance.update(
        {
            'collect_per_instance_filters': {
                'vm': ['mem.granted.avg'],
            }
        }
    )
    check = EsxiCheck('esxi', {}, [instance])
    dd_run_check(check)

    base_tags = ['esxi_url:127.0.0.1:8989']
    aggregator.assert_metric(
        'esxi.mem.granted.avg',
        value=10,
        count=1,
        hostname='vm1',
        tags=base_tags + ['instance:test1'],
    )


@pytest.mark.usefixtures("service_instance")
def test_report_instance_metrics_invalid_counter_id(aggregator, dd_run_check, vcsim_instance, service_instance, caplog):
    retrieve_result = vim.PropertyCollector.RetrieveResult(
        objects=[
            vim.ObjectContent(
                obj=vim.VirtualMachine(moId="vm1"),
                propSet=[
                    vmodl.DynamicProperty(
                        name='name',
                        val='vm1',
                    ),
                ],
            ),
        ]
    )
    service_instance.content.propertyCollector.RetrievePropertiesEx = MagicMock(return_value=retrieve_result)

    service_instance.content.perfManager.QueryPerf = MagicMock(
        side_effect=[
            [
                vim.PerformanceManager.EntityMetric(
                    entity=vim.VirtualMachine(moId="vm1"),
                    value=[
                        vim.PerformanceManager.IntSeries(
                            value=[3, 10],
                            id=vim.PerformanceManager.MetricId(counterId=500, instance='test1'),
                        )
                    ],
                ),
            ],
        ]
    )
    instance = copy.deepcopy(vcsim_instance)

    instance.update(
        {
            'collect_per_instance_filters': {
                'vm': ['cpu.usage.avg'],
            }
        }
    )
    check = EsxiCheck('esxi', {}, [instance])
    caplog.set_level(logging.DEBUG)
    dd_run_check(check)
    assert "Skipping value for counter 500, because the integration doesn't have metadata about it" in caplog.text

    aggregator.assert_metric("esxi.vm.count")
    aggregator.assert_metric("esxi.host.can_connect")
    aggregator.assert_all_metrics_covered()


@pytest.mark.usefixtures("service_instance")
def test_report_instance_metrics_invalid_metric_name_still_collect_metrics(aggregator, dd_run_check, vcsim_instance):
    instance = copy.deepcopy(vcsim_instance)

    instance.update(
        {
            'collect_per_instance_filters': {
                'vm': ['metric.name'],
            }
        }
    )
    check = EsxiCheck('esxi', {}, [instance])
    dd_run_check(check)
    base_tags = ["esxi_url:127.0.0.1:8989"]
    aggregator.assert_metric("esxi.cpu.usage.avg", value=26, tags=base_tags, hostname="localhost.localdomain")
    aggregator.assert_metric("esxi.mem.granted.avg", value=80, tags=base_tags, hostname="localhost.localdomain")
    aggregator.assert_metric("esxi.host.can_connect", 1, count=1, tags=base_tags)


@pytest.mark.usefixtures("service_instance")
def test_invalid_instance_filters(dd_run_check, vcsim_instance, caplog):
    instance = copy.deepcopy(vcsim_instance)

    instance.update(
        {
            'collect_per_instance_filters': {
                'cluster': ['cpu.usage.avg'],
            }
        }
    )
    check = EsxiCheck('esxi', {}, [instance])
    dd_run_check(check)
    assert "Ignoring metric_filter for resource 'cluster'. It should be one of 'host, vm'" in caplog.text


@pytest.mark.parametrize(
    'excluded_tags, expected_warning',
    [
        pytest.param([], None, id="No excluded tags"),
        pytest.param(['esxi_type'], None, id="type"),
        pytest.param(
            ['test'],
            "Unknown host tag `test` cannot be excluded. Available host tags are: `esxi_url`, `esxi_type`, "
            "`esxi_host`, `esxi_folder`, `esxi_cluster` `esxi_compute`, `esxi_datacenter`, and `esxi_datastore`",
            id="unknown tag",
        ),
        pytest.param(
            ['esxi_type', 'esxi_cluster', 'hello'],
            "Unknown host tag `hello` cannot be excluded. Available host tags are: `esxi_url`, `esxi_type`, "
            "`esxi_host`, `esxi_folder`, `esxi_cluster` `esxi_compute`, `esxi_datacenter`, and `esxi_datastore`",
            id="known and unknown tags together",
        ),
    ],
)
@pytest.mark.usefixtures("service_instance")
def test_excluded_host_tags(
    vcsim_instance, dd_run_check, datadog_agent, aggregator, excluded_tags, expected_warning, caplog
):
    vcsim_instance = copy.deepcopy(vcsim_instance)
    vcsim_instance['excluded_host_tags'] = excluded_tags
    check = EsxiCheck('esxi', {}, [vcsim_instance])
    caplog.set_level(logging.WARNING)
    dd_run_check(check)

    if expected_warning is not None:
        assert expected_warning in caplog.text

    host_external_tags = ['esxi_datacenter:dc2', 'esxi_folder:folder_1', 'esxi_type:host', 'esxi_url:127.0.0.1:8989']
    vm_1_external_tags = ['esxi_datacenter:dc2', 'esxi_folder:folder_1', 'esxi_type:vm', 'esxi_url:127.0.0.1:8989']
    vm_2_external_tags = ['esxi_cluster:c1', 'esxi_compute:c1', 'esxi_type:vm', 'esxi_url:127.0.0.1:8989']

    def all_tags_for_metrics(external_tags):
        # any external tags that are filtered, including esxi_url
        return [tag for tag in external_tags if any(excluded in tag for excluded in excluded_tags) or "esxi_url" in tag]

    aggregator.assert_metric(
        "esxi.cpu.usage.avg", value=18, tags=all_tags_for_metrics(vm_1_external_tags), hostname="vm1"
    )
    aggregator.assert_metric(
        "esxi.cpu.usage.avg", value=19, tags=all_tags_for_metrics(vm_2_external_tags), hostname="vm2"
    )
    aggregator.assert_metric(
        "esxi.cpu.usage.avg", value=26, tags=all_tags_for_metrics(host_external_tags), hostname="localhost.localdomain"
    )

    def all_external_tags(external_tags):
        # all external tags that are not excluded
        return [tag for tag in external_tags if not any(excluded in tag for excluded in excluded_tags)]

    datadog_agent.assert_external_tags('localhost.localdomain', {'esxi': all_external_tags(host_external_tags)})
    datadog_agent.assert_external_tags('vm1', {'esxi': all_external_tags(vm_1_external_tags)})
    datadog_agent.assert_external_tags('vm2', {'esxi': all_external_tags(vm_2_external_tags)})


@pytest.mark.usefixtures("service_instance")
def test_version_metadata(vcsim_instance, dd_run_check, datadog_agent):
    check = EsxiCheck('esxi', {}, [vcsim_instance])
    check.check_id = 'test:123'
    dd_run_check(check)

    version_metadata = {
        'version.scheme': 'semver',
        'version.major': '6',
        'version.minor': '5',
        'version.patch': '0',
        'version.build': '123456789',
        'version.raw': '6.5.0+123456789',
    }

    datadog_agent.assert_metadata('test:123', version_metadata)


@pytest.mark.usefixtures("service_instance")
def test_invalid_api_type(vcsim_instance, dd_run_check, caplog, aggregator, service_instance):
    service_instance.content.about.apiType = "VirtualCenter"
    check = EsxiCheck('esxi', {}, [vcsim_instance])

    dd_run_check(check)
    assert "localhost is not an ESXi host; please set the `host` config option to an ESXi host "
    "or use the vSphere integration to collect data from the vCenter" in caplog.text
    aggregator.assert_metric("esxi.host.can_connect", 0, tags=['esxi_url:127.0.0.1:8989'])
    aggregator.assert_all_metrics_covered()