# Contract Guard Monitoring Setup

This guide explains how to set up monitoring for the Contract Guard application using Prometheus and Grafana.

## Components

1. **Prometheus**: Metrics collection and storage
2. **Grafana**: Metrics visualization and dashboards
3. **Custom Metrics**: Application-specific metrics

## Setup Instructions

### 1. Install Prometheus

```bash
# Download Prometheus
wget https://github.com/prometheus/prometheus/releases/download/v2.45.0/prometheus-2.45.0.linux-amd64.tar.gz
tar xvfz prometheus-*.tar.gz
cd prometheus-*

# Start Prometheus
./prometheus --config.file=prometheus.yml
```

### 2. Install Grafana

```bash
# Download Grafana
wget https://dl.grafana.com/oss/release/grafana_9.5.2_amd64.deb
sudo dpkg -i grafana_9.5.2_amd64.deb

# Start Grafana
sudo systemctl start grafana-server
```

### 3. Configure Prometheus

Create `prometheus.yml`:

```yaml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'contract-guard'
    static_configs:
      - targets: ['localhost:5000']
    metrics_path: '/metrics'
```

### 4. Add Metrics to Backend

Add the following to your Flask application:

```python
from prometheus_client import Counter, Histogram, generate_latest
from flask import Response

# Define metrics
REQUEST_COUNT = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status']
)

REQUEST_LATENCY = Histogram(
    'http_request_duration_seconds',
    'HTTP request latency',
    ['method', 'endpoint']
)

FILE_PROCESSING_TIME = Histogram(
    'file_processing_seconds',
    'Time spent processing files',
    ['file_type']
)

OPENAI_API_CALLS = Counter(
    'openai_api_calls_total',
    'Total OpenAI API calls',
    ['endpoint', 'status']
)

# Add metrics endpoint
@app.route('/metrics')
def metrics():
    return Response(generate_latest(), mimetype='text/plain')
```

### 5. Import Grafana Dashboard

1. Open Grafana (http://localhost:3000)
2. Add Prometheus as a data source
3. Import the dashboard JSON from `monitoring/grafana-dashboard.json`

## Key Metrics to Monitor

1. **Application Metrics**
   - Request count and latency
   - File processing time
   - OpenAI API calls and latency
   - Error rates

2. **System Metrics**
   - CPU usage
   - Memory usage
   - Disk I/O
   - Network traffic

3. **Business Metrics**
   - Number of contracts processed
   - Average risk level distribution
   - Most common clause types
   - User query patterns

## Alerting Setup

### 1. Configure Alert Rules

Create `alert.rules`:

```yaml
groups:
- name: contract-guard
  rules:
  - alert: HighErrorRate
    expr: rate(http_requests_total{status=~"5.."}[5m]) > 0.1
    for: 5m
    labels:
      severity: critical
    annotations:
      summary: High error rate detected
      description: Error rate is above 10% for 5 minutes

  - alert: SlowResponseTime
    expr: http_request_duration_seconds{quantile="0.9"} > 2
    for: 5m
    labels:
      severity: warning
    annotations:
      summary: Slow response time
      description: 90th percentile of response time is above 2 seconds
```

### 2. Configure Alert Notifications

In Grafana:
1. Go to Alerting > Notification channels
2. Add your preferred notification channel (Email, Slack, etc.)
3. Configure alert rules to use the notification channel

## Monitoring Best Practices

1. **Set up Logging**
   - Use structured logging
   - Include request IDs
   - Log all errors with context

2. **Regular Maintenance**
   - Review and update dashboards
   - Adjust alert thresholds
   - Clean up old metrics

3. **Performance Optimization**
   - Monitor memory usage
   - Track API response times
   - Identify bottlenecks

## Troubleshooting

1. **Metrics Not Showing**
   - Check Prometheus targets
   - Verify metrics endpoint
   - Check network connectivity

2. **High Latency**
   - Check system resources
   - Review API response times
   - Monitor database performance

3. **Missing Data**
   - Check retention policies
   - Verify scrape intervals
   - Review log files

## Additional Resources

- [Prometheus Documentation](https://prometheus.io/docs/)
- [Grafana Documentation](https://grafana.com/docs/)
- [Flask Monitoring Best Practices](https://flask.palletsprojects.com/en/2.0.x/patterns/monitoring/) 