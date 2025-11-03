FROM mattermost/mattermost-team-edition:10.11.5

# Create necessary directories
RUN mkdir -p /mattermost/data /mattermost/logs /mattermost/config /mattermost/plugins

# Set environment variables for Scaleway deployment
ENV MM_SERVICESETTINGS_SITE_URL=${SITE_URL}
ENV MM_SQLSETTINGS_DRIVERNAME=postgres
ENV MM_SQLSETTINGS_DATASOURCE=${DATABASE_URL}
ENV MM_ADMINSETTINGS_ENABLE_OPEN_SERVER=true
ENV MM_SERVICESETTINGS_LISTENANDADDRESS=:8080

# Expose port (Scaleway containers use port 8080 by default)
EXPOSE 8080

# Health check endpoint for Scaleway
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8080/api/v4/system/ping || exit 1

# Start Mattermost
CMD ["./bin/mattermost"]
