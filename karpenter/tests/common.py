# (C) Datadog, Inc. 2023-present
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)
import os

from datadog_checks.dev import get_docker_hostname, get_here

HERE = get_here()
HOST = get_docker_hostname()
PORT = 8000


def get_fixture_path(filename):
    return os.path.join(HERE, 'fixtures', filename)


MOCKED_INSTANCE = {
    "openmetrics_endpoint": f"http://{HOST}:{PORT}/metrics",
    'tags': ['test:tag'],
}

COMPOSE_FILE = os.path.join(HERE, 'docker', 'docker-compose.yaml')

TEST_METRICS = [
    'karpenter.build_info',
    'karpenter.certwatcher.read.certificate.count',
    'karpenter.certwatcher.read.certificate.errors.count',
    'karpenter.cloudprovider.batcher.batch.time_seconds.bucket',
    'karpenter.cloudprovider.batcher.batch.time_seconds.count',
    'karpenter.cloudprovider.batcher.batch.time_seconds.sum',
    'karpenter.cloudprovider.batcher.batch_size.bucket',
    'karpenter.cloudprovider.batcher.batch_size.count',
    'karpenter.cloudprovider.batcher.batch_size.sum',
    'karpenter.cloudprovider.duration_seconds.bucket',
    'karpenter.cloudprovider.duration_seconds.count',
    'karpenter.cloudprovider.duration_seconds.sum',
    'karpenter.cloudprovider.instance.type.cpu_cores',
    'karpenter.cloudprovider.instance.type.memory_bytes',
    'karpenter.cloudprovider.instance.type.price_estimate',
    'karpenter.cluster_state.node_count',
    'karpenter.cluster_state.synced',
    'karpenter.controller.runtime.active_workers',
    'karpenter.controller.runtime.max.concurrent_reconciles',
    'karpenter.controller.runtime.reconcile.count',
    'karpenter.controller.runtime.reconcile.time_seconds.bucket',
    'karpenter.controller.runtime.reconcile.time_seconds.count',
    'karpenter.controller.runtime.reconcile.time_seconds.sum',
    'karpenter.controller.runtime.reconcile_errors.count',
    'karpenter.deprovisioning.actions_performed.count',
    'karpenter.deprovisioning.eligible_machines',
    'karpenter.deprovisioning.evaluation.duration_seconds.bucket',
    'karpenter.deprovisioning.evaluation.duration_seconds.count',
    'karpenter.deprovisioning.evaluation.duration_seconds.sum',
    'karpenter.deprovisioning.replacement.machine.initialized_seconds.bucket',
    'karpenter.deprovisioning.replacement.machine.initialized_seconds.count',
    'karpenter.deprovisioning.replacement.machine.initialized_seconds.sum',
    'karpenter.disruption.actions_performed.count',
    'karpenter.disruption.budgets.allowed_disruptions',
    'karpenter.disruption.consolidation_timeouts.count',
    'karpenter.disruption.evaluation.duration_seconds.bucket',
    'karpenter.disruption.evaluation.duration_seconds.count',
    'karpenter.disruption.evaluation.duration_seconds.sum',
    'karpenter.disruption.nodes.disrupted.count',
    'karpenter.disruption.pods.disrupted.count',
    'karpenter.disruption.queue_depth',
    'karpenter.disruption.replacement.nodeclaim.initialized_seconds.bucket',
    'karpenter.disruption.replacement.nodeclaim.initialized_seconds.count',
    'karpenter.disruption.replacement.nodeclaim.initialized_seconds.sum',
    'karpenter.go.gc.duration_seconds.count',
    'karpenter.go.gc.duration_seconds.quantile',
    'karpenter.go.gc.duration_seconds.sum',
    'karpenter.go.memstats.alloc_bytes',
    'karpenter.go.memstats.alloc_bytes.count',
    'karpenter.go.memstats.buck.hash.sys_bytes',
    'karpenter.go.memstats.frees.count',
    'karpenter.go.memstats.gc.sys_bytes',
    'karpenter.go.memstats.heap.alloc_bytes',
    'karpenter.go.memstats.heap.idle_bytes',
    'karpenter.go.memstats.heap.inuse_bytes',
    'karpenter.go.memstats.heap.objects',
    'karpenter.go.memstats.heap.released_bytes',
    'karpenter.go.memstats.heap.sys_bytes',
    'karpenter.go.memstats.last.gc.time_seconds',
    'karpenter.go.memstats.lookups.count',
    'karpenter.go.memstats.mallocs.count',
    'karpenter.go.memstats.mcache.inuse_bytes',
    'karpenter.go.memstats.mcache.sys_bytes',
    'karpenter.go.memstats.mspan.inuse_bytes',
    'karpenter.go.memstats.mspan.sys_bytes',
    'karpenter.go.memstats.next.gc_bytes',
    'karpenter.go.memstats.other.sys_bytes',
    'karpenter.go.memstats.stack.inuse_bytes',
    'karpenter.go.memstats.stack.sys_bytes',
    'karpenter.go.memstats.sys_bytes',
    'karpenter.go_goroutines',
    'karpenter.go_info',
    'karpenter.go_threads',
    'karpenter.interruption.actions_performed.count',
    'karpenter.interruption.deleted_messages.count',
    'karpenter.interruption.message.latency.time_seconds.bucket',
    'karpenter.interruption.message.latency.time_seconds.count',
    'karpenter.interruption.message.latency.time_seconds.sum',
    'karpenter.interruption.received_messages.count',
    'karpenter.leader_election.master_status',
    'karpenter.machines_created.count',
    'karpenter.machines_initialized.count',
    'karpenter.machines_launched.count',
    'karpenter.machines_registered.count',
    'karpenter.machines_terminated.count',
    'karpenter.nodes.allocatable',
    'karpenter.nodes.eviction.queue_depth',
    'karpenter.nodes.leases_deleted.count',
    'karpenter.nodes.system_overhead',
    'karpenter.nodes.terminated.count',
    'karpenter.nodes.termination.time_seconds.count',
    'karpenter.nodes.termination.time_seconds.quantile',
    'karpenter.nodes.termination.time_seconds.sum',
    'karpenter.nodes.total.daemon_limits',
    'karpenter.nodes.total.daemon_requests',
    'karpenter.nodes.total.pod_limits',
    'karpenter.nodes.total.pod_requests',
    'karpenter.pods.startup.time_seconds.count',
    'karpenter.pods.startup.time_seconds.quantile',
    'karpenter.pods.startup.time_seconds.sum',
    'karpenter.pods.state',
    'karpenter.process.cpu_seconds.count',
    'karpenter.process.max_fds',
    'karpenter.process.open_fds',
    'karpenter.process.resident.memory_bytes',
    'karpenter.process.start.time_seconds',
    'karpenter.process.virtual.memory.max_bytes',
    'karpenter.process.virtual.memory_bytes',
    'karpenter.provisioner.limit',
    'karpenter.provisioner.scheduling.duration_seconds.bucket',
    'karpenter.provisioner.scheduling.duration_seconds.count',
    'karpenter.provisioner.scheduling.duration_seconds.sum',
    'karpenter.provisioner.scheduling.queue_depth',
    'karpenter.provisioner.scheduling.simulation.duration_seconds.bucket',
    'karpenter.provisioner.scheduling.simulation.duration_seconds.count',
    'karpenter.provisioner.scheduling.simulation.duration_seconds.sum',
    'karpenter.provisioner.usage',
    'karpenter.provisioner.usage.pct',
    'karpenter.rest.client_requests.count',
    'karpenter.workqueue.longest.running.processor_seconds',
    'karpenter.workqueue.queue.duration_seconds.bucket',
    'karpenter.workqueue.queue.duration_seconds.count',
    'karpenter.workqueue.queue.duration_seconds.sum',
    'karpenter.workqueue.unfinished.work_seconds',
    'karpenter.workqueue.work.duration_seconds.bucket',
    'karpenter.workqueue.work.duration_seconds.count',
    'karpenter.workqueue.work.duration_seconds.sum',
    'karpenter.workqueue_adds.count',
    'karpenter.workqueue_depth',
    'karpenter.workqueue_retries.count',
]

RENAMED_LABELS = [
    'go_version:go1.20.6',
    'client_host:10.100.0.1:443',
]
