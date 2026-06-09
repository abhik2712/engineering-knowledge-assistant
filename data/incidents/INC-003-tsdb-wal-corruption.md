# INC-003: Prometheus startup failed due to TSDB WAL corruption

## Metadata
- Incident ID: INC-003
- Date: 2026-06-03
- Severity: P1
- Service: prometheus-server
- Component: tsdb
- Category: storage
- Status: Resolved
- Related Logs: data/logs/tsdb_wal_corruption.log
- Related Design Docs: data/design_docs/prometheus_tsdb_storage.md
- Related Code Areas: tsdb/

## Summary
Prometheus failed to start because the local TSDB detected corruption in a WAL segment.

## User Impact
Prometheus was unavailable and could not scrape targets, evaluate rules, or serve queries.

## Symptoms
- Startup aborted.
- Logs showed `WAL segment corruption detected`.
- Logs showed `unexpected checksum`.
- Local storage open operation failed.

## Timeline
- 02:10 UTC: Prometheus startup initiated.
- 02:10 UTC: TSDB storage opening started.
- 02:10 UTC: WAL corruption detected.
- 02:10 UTC: Prometheus startup aborted.

## Root Cause
A previous unclean shutdown caused partial WAL segment corruption.

## Resolution
The corrupted WAL segment was isolated, storage repair was performed, and Prometheus was restarted.

## Preventive Actions
- Ensure graceful shutdown.
- Use reliable persistent volumes.
- Monitor disk health and filesystem errors.
- Keep remote write or backup strategy for critical metrics.

## Useful Queries
Not applicable because the server failed during startup.

## Related Files
- data/logs/tsdb_wal_corruption.log
- data/design_docs/prometheus_tsdb_storage.md
- data/code_repo/prometheus/tsdb/
