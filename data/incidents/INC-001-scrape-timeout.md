# INC-001: Kubernetes pod target repeatedly failed scraping

## Metadata
- Incident ID: INC-001
- Date: 2026-06-01
- Severity: P2
- Service: prometheus-server
- Component: scrape
- Category: target-scraping
- Status: Resolved
- Related Logs: data/logs/scrape_timeout.log
- Related Design Docs: data/design_docs/prometheus_scrape_lifecycle.md
- Related Code Areas: scrape/

## Summary
Prometheus marked a Kubernetes pod target as down after repeated scrape failures. The target endpoint returned timeout errors and intermittent HTTP 503 responses.

## User Impact
Metrics from the affected pod were missing, causing dashboards and alerts for that pod to become unreliable.

## Symptoms
- Target `http://10.42.1.15:9100/metrics` showed as down.
- Logs showed `context deadline exceeded`.
- Logs also showed HTTP 503 responses from the metrics endpoint.

## Timeline
- 10:15 UTC: Scrape manager started.
- 10:16 UTC: First timeout observed.
- 10:17 UTC: Repeated timeout observed.
- 10:18 UTC: Target marked down.

## Root Cause
The target application was overloaded and could not respond to Prometheus scrape requests within the configured scrape timeout.

## Resolution
The application was restarted and scrape timeout was temporarily increased for the affected job.

## Preventive Actions
- Add alert for repeated scrape timeout.
- Monitor target endpoint latency.
- Tune scrape timeout only for slow exporters.
- Investigate application-side metrics endpoint performance.

## Useful Queries
- `up{job="kubernetes-pods"}`
- `scrape_duration_seconds{job="kubernetes-pods"}`
- `scrape_samples_scraped{job="kubernetes-pods"}`

## Related Files
- data/logs/scrape_timeout.log
- data/design_docs/prometheus_scrape_lifecycle.md
- data/code_repo/prometheus/scrape/
