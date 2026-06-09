# INC-002: Prometheus configuration reload failed due to YAML syntax error

## Metadata
- Incident ID: INC-002
- Date: 2026-06-02
- Severity: P3
- Service: prometheus-server
- Component: config
- Category: configuration
- Status: Resolved
- Related Logs: data/logs/config_reload_failure.log
- Related Design Docs: data/design_docs/prometheus_service_discovery.md
- Related Code Areas: config/, cmd/prometheus/

## Summary
A Prometheus reload request failed because the configuration file contained invalid YAML syntax at line 37.

## User Impact
New scrape configuration changes were not applied. Prometheus continued running with the previously valid configuration.

## Symptoms
- Reload request was received.
- Config parsing failed.
- Logs showed `yaml: line 37: did not find expected key`.
- Previous configuration remained active.

## Timeline
- 09:00 UTC: Prometheus started with valid configuration.
- 09:30 UTC: Reload request received.
- 09:30 UTC: Config reload failed.
- 09:35 UTC: Configuration was corrected and validated.

## Root Cause
A malformed indentation in `prometheus.yml` caused YAML parsing failure.

## Resolution
Fixed the YAML indentation and validated the configuration using promtool before reloading.

## Preventive Actions
- Validate config in CI before deployment.
- Run `promtool check config` before reload.
- Add pre-commit YAML linting.
- Keep previous valid config as fallback.

## Useful Queries
Not applicable. This was a configuration load failure.

## Related Files
- data/logs/config_reload_failure.log
- data/code_repo/prometheus/config/
- data/code_repo/prometheus/cmd/prometheus/
