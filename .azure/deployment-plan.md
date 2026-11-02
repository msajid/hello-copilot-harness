# Application Insights Monitoring Plan

## Status
Complete

## Scope
Instrument the existing Python console application for Azure Monitor / Application Insights, expose the connection string through the existing dotenv-based configuration pattern, and document local and hosted configuration. The user confirmed local development as the hosting target.

## Decisions
- Use Microsoft's currently recommended Python OpenTelemetry distro, `microsoft-opentelemetry`.
- Use `APPLICATIONINSIGHTS_CONNECTION_STRING`, the environment-variable name recognized by the distro. Keep it optional for local runs without Application Insights.
- Name the application logger `hello_copilot_harness`, following Python logger naming conventions for this project.
- Do not create Azure resources or deployment infrastructure as part of this change.
- Hosting target: Local development. For hosted deployments, use the same environment variable in the hosting platform; no host-specific resources or infrastructure are included.

## Documentation
- [Enable OpenTelemetry in Application Insights](https://learn.microsoft.com/en-us/azure/azure-monitor/app/opentelemetry-enable?tabs=python)
- [Microsoft Learn Python API reference](https://learn.microsoft.com/en-us/python/api/azure-monitor-opentelemetry/azure.monitor.opentelemetry?view=azure-python)

## Implementation
- [x] Add the Microsoft OpenTelemetry distro dependency
- [x] Initialize the distro before application libraries, using the named logger
- [x] Add an optional connection-string placeholder to `.env.example`
- [x] Document setup, hosted configuration, and telemetry behavior in `README.md`
- [x] Validate using the repository's available lint and test commands
