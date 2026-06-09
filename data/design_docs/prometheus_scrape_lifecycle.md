# Prometheus Scrape Lifecycle

## Purpose
This document explains how Prometheus collects metrics from configured or discovered targets.

## Overview
Prometheus follows a pull-based model. Instead of applications pushing metrics directly to Prometheus, Prometheus periodically sends HTTP requests to target endpoints and scrapes metrics from them.

A scrape job is configured through `scrape_config`. Each scrape job defines which targets to scrape, how frequently to scrape them, and how to apply labels or relabeling rules. Targets may be configured statically or discovered dynamically using service discovery.

## Key Components
- Scrape Manager: Coordinates scrape pools.
- Scrape Pool: Represents a group of targets for a job.
- Target: A metrics endpoint, usually exposed over HTTP.
- Service Discovery: Provides target groups dynamically.
- Relabeling: Rewrites or filters target labels before scraping.

## Flow
1. Prometheus loads the configuration.
2. Service discovery finds target groups.
3. Relabeling transforms discovered labels.
4. Scrape pools are created or updated.
5. Prometheus periodically sends HTTP requests to each target's metrics endpoint.
6. Scraped samples are parsed and appended to local TSDB.
7. Failed scrapes mark the target as down and update the `up` metric.

## Common Failures
- Target endpoint is unreachable.
- Scrape request times out.
- Target returns HTTP 500 or 503.
- Metrics format is invalid.
- Relabeling drops the target unexpectedly.
- Scrape interval or timeout is misconfigured.

## Operational Signals
Useful signals include:
- `up`
- `scrape_duration_seconds`
- `scrape_samples_scraped`
- `scrape_samples_post_metric_relabeling`
- target health page

## Related Code Areas
- `scrape/`
- `discovery/`
- `config/`
