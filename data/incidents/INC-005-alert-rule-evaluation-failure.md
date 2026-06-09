# INC-005: Alert rule evaluation failed due to duplicate series matching

## Metadata
- Incident ID: INC-005
- Date: 2026-06-05
- Severity: P2
- Service: prometheus-server
- Component: rules
- Category: alerting
- Status: Resolved
- Related Logs: data/logs/alert_rule_evaluation_failure.log
- Related Design Docs: data/design_docs/prometheus_alerting_rules.md
- Related Code Areas: rules/, promql/

## Summary
The `HighErrorRate` alert rule failed because its PromQL expression produced duplicate matching series and many-to-many matching was not allowed.

## User Impact
The alert state was not updated, so high error rate conditions could have been missed.

## Symptoms
- Rule evaluation failed.
- Logs showed duplicate series for match group.
- Logs showed many-to-many matching error.
- Alert state was not updated.

## Timeline
- 11:00 UTC: Rule manager started.
- 11:01 UTC: First evaluation failure.
- 11:02 UTC: Repeated many-to-many matching error.
- 11:15 UTC: Rule expression was corrected.

## Root Cause
The alert expression joined two metrics without ensuring unique labels on one side of the match.

## Resolution
The PromQL expression was fixed by aggregating the right-hand side metric before the join.

## Preventive Actions
- Add promtool validation in CI.
- Add rule tests for alert expressions.
- Review label cardinality before vector matching.
- Use recording rules for complex expressions.

## Useful Queries
- `rate(http_requests_total{status=~"5.."}[5m])`
- `sum by (job) (...)`
- `prometheus_rule_evaluation_failures_total`

## Related Files
- data/logs/alert_rule_evaluation_failure.log
- data/design_docs/prometheus_alerting_rules.md
- data/code_repo/prometheus/rules/
- data/code_repo/prometheus/promql/
