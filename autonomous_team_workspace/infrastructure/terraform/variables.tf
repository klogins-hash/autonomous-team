# 📋 TERRAFORM VARIABLES FOR COCKPIT MONITORING

variable "project_id" {
  description = "Scaleway Project ID"
  type        = string
  default     = "c5d299b8-8462-40fb-b5ae-32a8808bf394"
}

variable "region" {
  description = "Scaleway Region"
  type        = string
  default     = "fr-par"
}

variable "zone" {
  description = "Scaleway Zone"
  type        = string
  default     = "fr-par-1"
}

variable "container_namespace_id" {
  description = "Container Namespace ID"
  type        = string
  default     = "af8c35dc-3d68-4fbf-ab0b-a84c0f99d967"
}

variable "container_name" {
  description = "Container Name for Monitoring"
  type        = string
  default     = "autonomous-team-fixed-api"
}

variable "slack_webhook_url" {
  description = "Slack webhook URL for notifications"
  type        = string
  default     = ""
  sensitive   = true
}

variable "alert_email" {
  description = "Email address for critical alerts"
  type        = string
  default     = "team@autonomous-team.com"
}

variable "enable_slack_alerts" {
  description = "Enable Slack notifications"
  type        = bool
  default     = false
}

variable "enable_email_alerts" {
  description = "Enable email notifications"
  type        = bool
  default     = true
}

variable "metrics_retention_days" {
  description = "Metrics retention period in days"
  type        = number
  default     = 31
}

variable "logs_retention_days" {
  description = "Logs retention period in days"
  type        = number
  default     = 7
}
