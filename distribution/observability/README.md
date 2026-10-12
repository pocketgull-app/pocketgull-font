# PocketGull Typography for Observability (Grafana, Datadog & Prometheus)

Eliminates horizontal number flutter during live streaming and ensures operators never confuse `0` with `O` or `1` with `l` during critical system alerts.

## 1-Line Drop-in for Grafana

Add to your Grafana reverse-proxy stylesheet, Custom CSS plugin, or browser userscript:

```css
@import url("https://cdn.jsdelivr.net/gh/pocketgull-app/pocketgull-font@3.1.0/fonts.css");

.panel-content, [role="gridcell"], .logs-row {
  font-family: 'PocketGull Mono', monospace !important;
  font-feature-settings: "tnum" 1, "zero" 1, "cv05" 1, "ss02" 1 !important;
  font-variant-numeric: tabular-nums slashed-zero !important;
}
```

## Benefits for SREs & NOC Operators
* **Zero Number Flutter**: Tabular numerals keep decimal points aligned in high-frequency trading and CPU telemetry streams.
* **Instant Disambiguation**: Cross-slashed `Z` vs `2`, curved foot `l` vs `1` vs `I`, slashed zero `0̸` vs `O`.
