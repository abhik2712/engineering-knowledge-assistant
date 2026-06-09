# Prometheus Remote Write

## Purpose
This document explains how Prometheus sends samples to remote storage.

## Overview
Remote write allows Prometheus to send scraped samples to a remote system for long-term storage or centralized aggregation. Prometheus still scrapes targets locally, then sends samples asynchronously to configured remote write endpoints.

Remote write usually uses queues and batching. If the remote endpoint is slow or unavailable, queues can grow. If queues reach capacity, samples may be dropped.

## Key Components
- Remote Write Queue Manager: Manages outgoing samples.
- Shards: Parallel workers sending batches.
- Remote Endpoint: Receiver for remote write data.
- Retry Logic: Handles temporary send failures.
- Backpressure Handling: Limits memory usage when remote endpoint is slow.

## Flow
1. Prometheus scrapes targets.
2. Samples are appended to local TSDB.
3. Samples are sent to remote write queues.
4. Queue shards send batches to remote endpoint.
5. Failed sends are retried.
6. If the queue fills, samples may be dropped.

## Common Failures
- Remote endpoint unavailable.
- HTTP 429 rate limiting.
- HTTP 500 from remote storage.
- Queue capacity exceeded.
- Network timeout.
- High-cardinality metrics overloading remote storage.

## Operational Signals
- Remote write queue length.
- Failed samples.
- Dropped samples.
- Highest sent timestamp.
- Retry count.
- HTTP status code from remote storage.

## Related Code Areas
- `storage/remote/`
