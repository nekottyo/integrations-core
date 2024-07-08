# (C) Datadog, Inc. 2024-present
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)

MOCKED_PROMETHEUS_METRICS = [
    "fly_io.instance.cpu",
    "fly_io.instance.disk.io_in_progress",
    "fly_io.instance.disk.reads_completed",
    "fly_io.instance.disk.reads_merged",
    "fly_io.instance.disk.sectors_read",
    "fly_io.instance.disk.sectors_written",
    "fly_io.instance.disk.time_io",
    "fly_io.instance.disk.time_io_weighted",
    "fly_io.instance.disk.time_reading",
    "fly_io.instance.disk.time_writing",
    "fly_io.instance.disk.writes_completed",
    "fly_io.instance.disk.writes_merged",
    "fly_io.instance.filefd.allocated",
    "fly_io.instance.filefd.max",
    "fly_io.instance.filesystem.block_size",
    "fly_io.instance.filesystem.blocks",
    "fly_io.instance.filesystem.blocks_avail",
    "fly_io.instance.filesystem.blocks_free",
    "fly_io.instance.load.avg",
    "fly_io.instance.memory.active",
    "fly_io.instance.memory.buffers",
    "fly_io.instance.memory.cached",
    "fly_io.instance.memory.dirty",
    "fly_io.instance.memory.inactive",
    "fly_io.instance.memory.mem_available",
    "fly_io.instance.memory.mem_free",
    "fly_io.instance.memory.mem_total",
    "fly_io.instance.memory.shmem",
    "fly_io.instance.memory.slab",
    "fly_io.instance.memory.swap_cached",
    "fly_io.instance.memory.swap_free",
    "fly_io.instance.memory.swap_total",
    "fly_io.instance.memory.vmalloc_chunk",
    "fly_io.instance.memory.vmalloc_total",
    "fly_io.instance.memory.vmalloc_used",
    "fly_io.instance.memory.writeback",
    "fly_io.instance.net.recv_bytes",
    "fly_io.instance.net.recv_compressed",
    "fly_io.instance.net.recv_drop",
    "fly_io.instance.net.recv_errs",
    "fly_io.instance.net.recv_fifo",
    "fly_io.instance.net.recv_frame",
    "fly_io.instance.net.recv_multicast",
    "fly_io.instance.net.recv_packets",
    "fly_io.instance.net.sent_bytes",
    "fly_io.instance.net.sent_carrier",
    "fly_io.instance.net.sent_colls",
    "fly_io.instance.net.sent_compressed",
    "fly_io.instance.net.sent_drop",
    "fly_io.instance.net.sent_errs",
    "fly_io.instance.net.sent_fifo",
    "fly_io.instance.net.sent_packets",
    "fly_io.instance.up",
    "fly_io.instance.memory.pressure_full",
    "fly_io.instance.memory.pressure_some",
]

ALL_REST_METRICS = ['fly_io.app.count', 'fly_io.machine.count', 'fly_io.machines_api.up']

APP_UP_METRICS = [
    {
        'name': 'fly_io.app.count',
        'count': 1,
        'value': 1,
        'tags': [
            'app_name:example-app-1',
            'app_id:o7vx1kl85749k3f1',
            'app_network:default',
            'app_status:deployed',
            'fly_org:test',
        ],
    },
    {
        'name': 'fly_io.app.count',
        'count': 1,
        'value': 1,
        'tags': [
            'app_name:example-app-4',
            'app_id:z4k69d4wp2n5js93',
            'app_network:default',
            'app_status:deployed',
            'fly_org:test',
        ],
    },
    {
        'name': 'fly_io.app.count',
        'count': 1,
        'value': 1,
        'tags': [
            'app_name:example-app-2',
            'app_id:4840jpkjkxo1ei63',
            'app_network:default',
            'app_status:deployed',
            'fly_org:test',
        ],
    },
    {
        'name': 'fly_io.app.count',
        'count': 1,
        'value': 1,
        'tags': [
            'app_name:example-app-3',
            'app_id:zg90akwdv84qvd47',
            'app_network:default',
            'app_status:deployed',
            'fly_org:test',
        ],
    },
]

MACHINE_COUNT_METRICS = [
    {
        'name': 'fly_io.machine.count',
        'count': 1,
        'value': 1,
        'tags': [
            'app_id:o7vx1kl85749k3f1',
            'app_name:example-app-1',
            'fly_org:test',
            'fly_platform_version:v2',
            'instance_id:POSJ7Y49KSI6PG1H7KPKJN5IK',
            'machine_region:ewr',
        ],
    },
    {
        'name': 'fly_io.machine.count',
        'count': 1,
        'value': 1,
        'tags': [
            'app_id:o7vx1kl85749k3f1',
            'app_name:example-app-1',
            'fly_org:test',
            'fly_platform_version:v2',
            'instance_id:01AP4Y49KSI6PG1H7KPKJN5GF',
            'machine_region:ewr',
        ],
    },
]
