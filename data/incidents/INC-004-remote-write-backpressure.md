# INC-004: Remote write queue filled and samples were dropped

## Metadata
- Incident ID: INC-004
- Date: 2026-06-04
- Severity: P1
- Service: prometheus-server
- Component: remote-write
- Category: remote-storage
- Status: Resolved
- Related Logs: data/logs/remote_write_backpressure.log
- Related Design Docs: data/design_docs/prometheus_remote_write.md
- Related Code Areas: storage/remote/

## Summary
Prometheus remote write fell behind because the remote endpoint returned HTTP 429 responses. The queue reached capacity and samples were dropped.

## User Impact
Downstream long-term storage missed samples. Some historical dashboards showed gaps.

## Symptoms
- Remote endpoint returned HTTP 429.
- Remote write queue length increased.
- Samples were dropped after the queue became full.
- Highest sent timestamp lagged behind current time.

## Timeline
- 14:20 UTC: Remote write queue manager started.
- 14:21 UTC: Remote endpoint returned HTTP 429.
- 14:22 UTC: Queue length approached capacity.
- 14:22 UTC: Samples were dropped.
- 14:30 UTC: Remote endpoint capacity was increased.

## Root Cause
The remote storage receiver was rate-limiting Prometheus due to insufficient ingestion capacity.

## Resolution
Scaled the remote write receiver and temporarily reduced sample volume by dropping high-cardinality metrics.

## Preventive Actions
- Monitor remote write queue length.
- Alert on dropped samples.
- Control high-cardinality metrics.
- Use capacity planning for remote storage.

## Useful Queries
- `prometheus_remote_storage_samples_failed_total`
- `prometheus_remote_storage_samples_dropped_total`
- `prometheus_remote_storage_queue_highest_sent_timestamp_seconds`

## Related Files
- data/logs/remote_write_backpressure.log
- data/design_docs/prometheus_remote_write.md
- data/code_repo/prometheus/storage/remote/
