# INC-006: Kubernetes service discovery failed due to RBAC permission issue

## Metadata
- Incident ID: INC-006
- Date: 2026-06-06
- Severity: P2
- Service: prometheus-server
- Component: discovery
- Category: service-discovery
- Status: Resolved
- Related Logs: data/logs/service_discovery_failure.log
- Related Design Docs: data/design_docs/prometheus_service_discovery.md
- Related Code Areas: discovery/

## Summary
Prometheus failed to discover Kubernetes pod targets because the service account lacked permission to list pods.

## User Impact
New pod targets were not discovered and therefore were not scraped.

## Symptoms
- Kubernetes service discovery sync failed.
- Logs showed RBAC permission denied.
- Error mentioned service account `system:serviceaccount:monitoring:prometheus`.
- Pod targets were missing from the target list.

## Timeline
- 08:45 UTC: Kubernetes service discovery started.
- 08:45 UTC: First RBAC failure observed.
- 08:46 UTC: Retry attempted.
- 08:47 UTC: Discovery sync failed again.
- 09:00 UTC: ClusterRole permissions were corrected.

## Root Cause
The Prometheus service account did not have permission to list pod resources at cluster scope.

## Resolution
Updated Kubernetes RBAC rules to allow the Prometheus service account to list and watch pods.

## Preventive Actions
- Validate RBAC during deployment.
- Add smoke test for service discovery.
- Monitor discovered target count.
- Alert when target count drops unexpectedly.

## Useful Queries
- `prometheus_sd_kubernetes_events_total`
- `prometheus_target_scrape_pool_targets`
- `up{job="kubernetes-pods"}`

## Related Files
- data/logs/service_discovery_failure.log
- data/design_docs/prometheus_service_discovery.md
- data/code_repo/prometheus/discovery/
