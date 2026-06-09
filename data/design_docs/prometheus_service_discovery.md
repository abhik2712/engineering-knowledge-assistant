# Prometheus Service Discovery

## Purpose
This document explains how Prometheus discovers scrape targets dynamically.

## Overview
In dynamic environments such as Kubernetes, targets appear and disappear frequently. Prometheus supports service discovery so that scrape targets do not always need to be listed statically.

A service discovery provider returns target groups. These target groups contain labels describing discovered objects. Prometheus then applies relabeling rules to decide which targets to keep, drop, or transform.

## Flow
1. Prometheus starts service discovery providers based on configuration.
2. Providers watch infrastructure APIs such as Kubernetes.
3. Discovered target groups are sent to the scrape manager.
4. Relabeling rules transform metadata labels into scrape labels.
5. Final targets are assigned to scrape pools.
6. Scrape manager updates active targets.

## Kubernetes Example
For Kubernetes pod discovery, Prometheus may need permission to list and watch pods. If RBAC permissions are missing, service discovery can fail and targets will not be scraped.

## Common Failures
- Missing RBAC permission.
- API server unavailable.
- Wrong namespace selector.
- Relabeling rule drops all discovered targets.
- Incorrect port or scheme label.
- High churn causing frequent target updates.

## Operational Signals
- Number of active targets.
- Discovery sync failures.
- Logs from discovery manager.
- Target page in Prometheus UI.

## Related Code Areas
- `discovery/`
- `scrape/`
- `config/`
