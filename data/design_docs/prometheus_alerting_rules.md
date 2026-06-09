# Prometheus Alerting and Recording Rules

## Purpose
This document explains how Prometheus evaluates recording rules and alerting rules.

## Overview
Prometheus periodically evaluates rule groups. A recording rule precomputes a PromQL expression and stores the result as a new time series. An alerting rule evaluates a condition and tracks alert state.

Rules are evaluated using PromQL. If an expression fails due to invalid syntax, duplicate series matching, or many-to-many vector matching, the rule state may not update successfully.

## Key Components
- Rule Manager: Schedules and evaluates rule groups.
- Rule Group: A set of rules evaluated at a fixed interval.
- Recording Rule: Writes expression results as time series.
- Alerting Rule: Creates or updates alerts based on expression results.
- PromQL Engine: Executes rule expressions.

## Flow
1. Prometheus loads rule files from configuration.
2. Rule manager starts rule groups.
3. Each group is evaluated at its configured interval.
4. PromQL expression is executed.
5. Recording rule output is written to TSDB.
6. Alerting rule state is updated.
7. Active alerts are sent to Alertmanager if configured.

## Common Failures
- Invalid PromQL syntax.
- Many-to-many matching error.
- Duplicate series for matching labels.
- Query timeout during rule evaluation.
- Rule file reload failure.
- High-cardinality query causing slow evaluation.

## Operational Signals
- `prometheus_rule_evaluation_failures_total`
- `prometheus_rule_group_duration_seconds`
- `prometheus_rule_group_last_duration_seconds`
- rule manager logs

## Related Code Areas
- `rules/`
- `promql/`
- `config/`
