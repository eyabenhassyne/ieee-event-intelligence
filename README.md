# IEEE Event Intelligence Platform

## Overview

The IEEE Event Intelligence Platform is a Business Intelligence and
decision-support prototype for monitoring IEEE events.

The platform consolidates authorized event data, processes it through an ETL
workflow, stores cleaned data in an analytics database, and presents KPIs
through Power BI dashboards and management reports.

## Main Objectives

- Map available IEEE event data sources
- Build a repeatable ETL workflow
- Detect and report data-quality issues
- Design a PostgreSQL dimensional model
- Define event-monitoring KPIs
- Build Power BI dashboards
- Produce technical and user documentation

## Scope

The project includes:

- CSV and Excel data imports
- Data validation and normalization
- PostgreSQL analytics database
- Fact and dimension tables
- KPI definitions
- Power BI dashboards
- Data-quality monitoring
- Reporting and documentation

## Out of Scope

The project does not include:

- Event registration
- Payment processing
- Authentication or user accounts
- Mobile application development
- Full event-management functionality
- Conference paper-management workflows

## Proposed Architecture

1. IEEE and local data sources
2. Raw and staging layers
3. ETL and data-quality processing
4. PostgreSQL analytics database
5. Power BI semantic model
6. Dashboards and decision-support reports

## Technology Stack

- Python
- pandas
- PostgreSQL
- SQL
- Power BI
- Git
- Markdown

## Project Status

Current phase: Project initialization and requirements analysis.

## Data Warehouse Design

The project uses a PostgreSQL star schema centered on one `FactEvents` row per IEEE event.

Implemented dimensions include:
- `DimDate`
- `DimCategory`
- `DimSubcategory`
- `DimCountry`
- `DimState`
- `DimLocation`
- `DimOrganizingUnit`

Audit support is modeled through:
- `audit.etl_run`
- `audit.source_file`
- `audit.data_quality_issue`

Missing attendance remains `NULL` and must not be coerced to zero. Registration, feedback, promotion, and reporting-compliance analytics are deferred unless new source data becomes available.

## Current Status

- Database schema design: implemented in SQL scripts
- Database deployment: applied to PostgreSQL

## ETL Pipeline

The ETL pipeline is designed to load reference dimensions first, resolve surrogate keys, write one fact row per IEEE event, log each ETL run, and record data-quality issues. The loader is designed to be idempotent through source-key upserts and to preserve missing attendance as `NULL`.

## Current Status

- ETL implementation: completed and run against PostgreSQL
- Database loading: complete for the current source extract, with one rejected row and documented data-quality issues
- Next phase: KPI dictionary, SQL analytical views, Power BI semantic model, and dashboards

## KPI Layer

The KPI layer documents supported event-volume, attendance, organizing-unit, category, geography, and data-quality measures that are derived from the PostgreSQL star schema and audit tables.

## Analytics Views

The analytics layer now includes reusable views for event overview, monthly summaries, category performance, organizing-unit performance, country performance, attendance quality, data-quality summary, and ETL run summary.

## Power BI Preparation

Power BI guidance now covers the star-schema model, the recommended import tables and views, DAX measures, and dashboard blueprints. Missing attendance remains blank and should not be coerced to zero.

## Current Status

- KPI dictionary: in progress
- Analytics views: created and verified
- Power BI preparation: documented
- Next manual step: Build the Power BI Desktop report from the semantic-model specification and dashboard blueprint

## Dashboard Mockups

The repository also includes static dashboard mockups and design notes for the supported Power BI report pages.

### Current Status

- Dashboard mockups: in progress
- Supported pages: executive overview, event inventory, attendance analytics, organizational units, category analysis, geographic analysis, data quality and ETL, monthly export
- Review status: approved with one navigation fix applied
- Screenshot status: pending, because browser screenshot tooling was not available in this environment
- Next manual step: translate the static mockups into the Power BI report
