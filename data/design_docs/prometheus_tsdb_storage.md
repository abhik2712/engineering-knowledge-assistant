# Prometheus TSDB Storage

## Purpose
This document explains Prometheus local storage at a high level.

## Overview
Prometheus stores scraped samples in a local time-series database called TSDB. The storage layer is responsible for appending samples, maintaining write-ahead logs, compacting blocks, and serving queries.

Local storage is optimized for time-series workloads. Samples are first written to the WAL for durability and later compacted into blocks.

## Key Components
- Head Block: In-memory and recent samples.
- WAL: Write-ahead log used for durability.
- Blocks: Persisted chunks and indexes for historical data.
- Compaction: Merges smaller blocks into larger blocks.
- Retention: Removes old blocks based on time or size limits.

## Flow
1. Scrape manager collects samples.
2. Samples are appended to TSDB head.
3. WAL records sample data for recovery.
4. Periodically, head data is cut into persistent blocks.
5. Compaction merges blocks.
6. Queries read from head and persisted blocks.

## Common Failures
- WAL corruption.
- Disk full.
- Permission issue on storage path.
- Slow disk causing ingestion lag.
- Excessive cardinality causing high memory usage.
- Retention misconfiguration.

## Operational Signals
- TSDB startup logs.
- WAL replay duration.
- Disk usage.
- Head series count.
- Compaction duration.
- Query latency.

## Related Code Areas
- `tsdb/`
- `storage/`
