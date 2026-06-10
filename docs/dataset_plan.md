# Dataset Plan

## Corpus Choice
The project uses the Prometheus open-source repository as the primary engineering corpus.

Prometheus is suitable because it includes:
- Monitoring server implementation
- Scrape configuration
- Service discovery
- PromQL query engine
- Rule evaluation
- TSDB storage
- Remote write support
- Operational documentation

## Initial Prometheus Areas to Index

| Area | Path | Reason |
|---|---|---|
| Overview | `README.md` | General system understanding |
| Docs | `docs/` | Official documentation |
| Internal architecture | `documentation/` | System architecture |
| Main server | `cmd/prometheus/` | Server startup and configuration |
| Config | `config/` | Config loading and validation |
| Scraping | `scrape/` | Target scraping lifecycle |
| Discovery | `discovery/` | Service discovery |
| Rules | `rules/` | Alerting and recording rules |
| PromQL | `promql/` | Query evaluation |
| TSDB | `tsdb/` | Local storage |
| Remote storage | `storage/remote/` | Remote write/read behavior |

## Synthetic Data to Create

### Design Docs
- `prometheus_scrape_lifecycle.md`
- `prometheus_service_discovery.md`
- `prometheus_alerting_rules.md`
- `prometheus_tsdb_storage.md`
- `prometheus_remote_write.md`

### Logs
- `scrape_timeout.log`
- `config_reload_failure.log`
- `tsdb_wal_corruption.log`
- `remote_write_backpressure.log`
- `alert_rule_evaluation_failure.log`
- `service_discovery_failure.log`

### Incidents
- `INC-001-scrape-timeout.md`
- `INC-002-config-reload-failure.md`
- `INC-003-tsdb-wal-corruption.md`
- `INC-004-remote-write-backpressure.md`
- `INC-005-alert-rule-evaluation-failure.md`
- `INC-006-service-discovery-failure.md`

## Dataset Design Principle
Each failure scenario should have:
1. One log file
2. One incident report
3. One related design doc
4. One or more related code areas

This allows the RAG system to test multi-source retrieval.
