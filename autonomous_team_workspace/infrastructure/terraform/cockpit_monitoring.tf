# 🏗️ COCKPIT MONITORING TERRAFORM CONFIGURATION
# Autonomous Team Production Monitoring

terraform {
  required_providers {
    scaleway = {
      source  = "scaleway/scaleway"
      version = ">= 2.0.0"
    }
  }
}

provider "scaleway" {
  project_id = "c5d299b8-8462-40fb-b5ae-32a8808bf394"
  region     = "fr-par"
  zone       = "fr-par-1"
}

# 📊 COCKPIT DATA SOURCES
data "scaleway_cockpit_data_source" "metrics" {
  project_id = "c5d299b8-8462-40fb-b5ae-32a8808bf394"
  name       = "Scaleway Metrics"
}

data "scaleway_cockpit_data_source" "logs" {
  project_id = "c5d299b8-8462-40fb-b5ae-32a8808bf394"
  name       = "Scaleway Logs"
}

# 🚨 ALERT MANAGER CONFIGURATION
resource "scaleway_cockpit_alert_manager" "autonomous_team_alerts" {
  project_id = "c5d299b8-8462-40fb-b5ae-32a8808bf394"
  
  # Enable alert manager
  enabled = true
  
  # Configure alert rules
  rule {
    name        = "Autonomous Team Container Down"
    description = "Alert when autonomous team container is down"
    condition   = "up{job=\"scaleway-container\"} == 0"
    for         = "5m"
    severity    = "critical"
    
    labels = {
      team      = "autonomous-team"
      component = "container"
      service   = "api"
    }
    
    annotations = {
      summary     = "Autonomous Team container is down"
      description = "Container {{ $labels.instance }} has been down for more than 5 minutes"
      runbook_url = "https://github.com/klogins-hash/autonomous-team/blob/main/docs/troubleshooting.md"
    }
  }
  
  rule {
    name        = "High API Error Rate"
    description = "Alert when API error rate exceeds 5%"
    condition   = "rate(http_requests_total{job=\"scaleway-container\",status=~\"5..\"}[5m]) / rate(http_requests_total{job=\"scaleway-container\"}[5m]) > 0.05"
    for         = "2m"
    severity    = "warning"
    
    labels = {
      team      = "autonomous-team"
      component = "api"
      metric    = "error_rate"
    }
    
    annotations = {
      summary     = "High API error rate detected"
      description = "Error rate is {{ $value | humanizePercentage }} for {{ $labels.instance }}"
    }
  }
  
  rule {
    name        = "Slow API Response Time"
    description = "Alert when API response time exceeds 5 seconds"
    condition   = "histogram_quantile(0.95, rate(http_request_duration_seconds_bucket{job=\"scaleway-container\"}[5m])) > 5"
    for         = "3m"
    severity    = "warning"
    
    labels = {
      team      = "autonomous-team"
      component = "api"
      metric    = "response_time"
    }
    
    annotations = {
      summary     = "Slow API response time"
      description = "95th percentile response time is {{ $value }}s for {{ $labels.instance }}"
    }
  }
  
  rule {
    name        = "Database Connection Issues"
    description = "Alert when database connections fail"
    condition   = "up{job=\"scaleway-rdb\"} == 0"
    for         = "1m"
    severity    = "critical"
    
    labels = {
      team      = "autonomous-team"
      component = "database"
      service   = "postgresql"
    }
    
    annotations = {
      summary     = "Database connection failure"
      description = "PostgreSQL database {{ $labels.instance }} is not responding"
    }
  }
  
  rule {
    name        = "Redis Cache Issues"
    description = "Alert when Redis cache is down"
    condition   = "up{job=\"scaleway-redis\"} == 0"
    for         = "1m"
    severity    = "warning"
    
    labels = {
      team      = "autonomous-team"
      component = "cache"
      service   = "redis"
    }
    
    annotations = {
      summary     = "Redis cache is down"
      description = "Redis cluster {{ $labels.instance }} is not responding"
    }
  }
}

# 📞 CONTACT POINTS FOR NOTIFICATIONS
resource "scaleway_cockpit_contact_point" "email_alerts" {
  project_id = "c5d299b8-8462-40fb-b5ae-32a8808bf394"
  name       = "autonomous-team-email"
  
  email {
    to = ["team@autonomous-team.com"]
  }
}

resource "scaleway_cockpit_contact_point" "slack_alerts" {
  project_id = "c5d299b8-8462-40fb-b5ae-32a8808bf394"
  name       = "autonomous-team-slack"
  
  slack {
    webhook_url = var.slack_webhook_url
    channel     = "#autonomous-team-alerts"
    title       = "Autonomous Team Alert"
    text        = "{{ range .Alerts }}{{ .Annotations.summary }}{{ end }}"
  }
}

# 🔔 NOTIFICATION POLICIES
resource "scaleway_cockpit_notification_policy" "critical_alerts" {
  project_id     = "c5d299b8-8462-40fb-b5ae-32a8808bf394"
  name           = "critical-alerts"
  receiver       = scaleway_cockpit_contact_point.email_alerts.name
  group_by       = ["alertname", "team", "component"]
  group_wait     = "30s"
  group_interval = "5m"
  repeat_interval = "1h"
  
  matchers {
    name  = "severity"
    value = "critical"
  }
}

resource "scaleway_cockpit_notification_policy" "warning_alerts" {
  project_id     = "c5d299b8-8462-40fb-b5ae-32a8808bf394"
  name           = "warning-alerts"
  receiver       = scaleway_cockpit_contact_point.slack_alerts.name
  group_by       = ["alertname", "team", "component"]
  group_wait     = "1m"
  group_interval = "10m"
  repeat_interval = "3h"
  
  matchers {
    name  = "severity"
    value = "warning"
  }
}

# 📊 GRAFANA USER MANAGEMENT
resource "scaleway_cockpit_grafana_user" "monitoring_agent" {
  project_id = "c5d299b8-8462-40fb-b5ae-32a8808bf394"
  login      = "monitoring-agent"
  role       = "editor"
}

resource "scaleway_cockpit_grafana_user" "readonly_user" {
  project_id = "c5d299b8-8462-40fb-b5ae-32a8808bf394"
  login      = "readonly-viewer"
  role       = "viewer"
}

# 🎯 CUSTOM DASHBOARDS
resource "scaleway_cockpit_dashboard" "autonomous_team_overview" {
  project_id = "c5d299b8-8462-40fb-b5ae-32a8808bf394"
  name       = "autonomous-team-overview"
  description = "Autonomous Team Production Overview Dashboard"
  
  dashboard_config = jsonencode({
    title = "Autonomous Team Production Overview"
    tags = ["autonomous-team", "production"]
    timezone = "browser"
    panels = [
      {
        title = "Container Health Status"
        type = "stat"
        targets = [
          {
            expr = "up{job=\"scaleway-container\"}"
            legendFormat = "{{ instance }}"
          }
        ]
        fieldConfig = {
          defaults = {
            thresholds = {
              steps = [
                { color = "red", value = 0 },
                { color = "green", value = 1 }
              ]
            }
            mappings = [
              { options = { "0" = { text = "DOWN", color = "red" } }, type = "value" },
              { options = { "1" = { text = "UP", color = "green" } }, type = "value" }
            ]
          }
        }
      },
      {
        title = "API Request Rate"
        type = "graph"
        targets = [
          {
            expr = "rate(http_requests_total{job=\"scaleway-container\"}[5m])"
            legendFormat = "{{ method }} {{ endpoint }}"
          }
        ]
      },
      {
        title = "API Response Time"
        type = "graph"
        targets = [
          {
            expr = "histogram_quantile(0.95, rate(http_request_duration_seconds_bucket{job=\"scaleway-container\"}[5m]))"
            legendFormat = "95th percentile"
          },
          {
            expr = "histogram_quantile(0.50, rate(http_request_duration_seconds_bucket{job=\"scaleway-container\"}[5m]))"
            legendFormat = "50th percentile"
          }
        ]
      },
      {
        title = "Error Rate"
        type = "graph"
        targets = [
          {
            expr = "rate(http_requests_total{job=\"scaleway-container\",status=~\"5..\"}[5m]) / rate(http_requests_total{job=\"scaleway-container\"}[5m])"
            legendFormat = "Error Rate"
          }
        ]
      },
      {
        title = "Database Connections"
        type = "graph"
        targets = [
          {
            expr = "pg_stat_database_numbackends{job=\"scaleway-rdb\"}"
            legendFormat = "{{ instance }}"
          }
        ]
      },
      {
        title = "Redis Memory Usage"
        type = "graph"
        targets = [
          {
            expr = "redis_memory_used_bytes{job=\"scaleway-redis\"}"
            legendFormat = "{{ instance }}"
          }
        ]
      }
    ]
    time = {
      from = "now-1h"
      to = "now"
    }
    refresh = "30s"
  })
}

# 🔍 MANAGED ALERTS FOR CONTAINER MONITORING
resource "scaleway_cockpit_managed_alert" "container_health" {
  project_id = "c5d299b8-8462-40fb-b5ae-32a8808bf394"
  name       = "autonomous-team-container-health"
  scope      = "container"
  
  # Container-specific monitoring
  container_monitoring = {
    namespace_id = "af8c35dc-3d68-4fbf-ab0b-a84c0f99d967"
    container_name = "autonomous-team-fixed-api"
    
    health_check = {
      enabled = true
      path    = "/health"
      port    = 8080
      interval = "30s"
      timeout  = "10s"
      retries  = 3
    }
    
    resource_limits = {
      cpu_threshold    = 80
      memory_threshold = 85
    }
  }
}

# 📈 USAGE MONITORING
resource "scaleway_cockpit_usage_overview" "monitoring" {
  project_id = "c5d299b8-8462-40fb-b5ae-32a8808bf394"
  
  # Enable comprehensive usage tracking
  enable_metrics = true
  enable_logs    = true
  
  # Set up retention policies
  metrics_retention = "31d"
  logs_retention    = "7d"
}

# 🔧 OUTPUTS FOR MONITORING ACCESS
output "cockpit_dashboards" {
  description = "Cockpit dashboard URLs"
  value = {
    container_metrics    = "https://c5d299b8-8462-40fb-b5ae-32a8808bf394.dashboard.cockpit.fr-par.scw.cloud/d/scw-serverless-containers-overview/serverless-containers-overview"
    container_logs       = "https://c5d299b8-8462-40fb-b5ae-32a8808bf394.dashboard.cockpit.fr-par.scw.cloud/d/scw-serverless-containers-logs/serverless-containers-logs"
    autonomous_team_dashboard = "https://c5d299b8-8462-40fb-b5ae-32a8808bf394.dashboard.cockpit.fr-par.scw.cloud/d/autonomous-team-overview/autonomous-team-overview"
  }
}

output "grafana_access" {
  description = "Grafana access credentials"
  value = {
    url      = "https://c5d299b8-8462-40fb-b5ae-32a8808bf394.grafana.cockpit.fr-par.scw.cloud"
    users = {
      monitoring_agent = scaleway_cockpit_grafana_user.monitoring_agent.login
      readonly_viewer  = scaleway_cockpit_grafana_user.readonly_user.login
    }
  }
  sensitive = true
}

output "alert_endpoints" {
  description = "Alert configuration endpoints"
  value = {
    alert_manager_url = "https://c5d299b8-8462-40fb-b5ae-32a8808bf394.alerts.cockpit.fr-par.scw.cloud"
    metrics_endpoint   = data.scaleway_cockpit_data_source.metrics.url
    logs_endpoint      = data.scaleway_cockpit_data_source.logs.url
  }
}
