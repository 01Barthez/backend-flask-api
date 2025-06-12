# Meal Tracker - Troubleshooting Guide

## Authentication Issues

### Problem: Unable to Login

- **Symptoms**: 401 Unauthorized, Login Failure
- **Possible Causes**:
  1. Incorrect credentials
  2. Expired JWT token
  3. Password hashing mismatch

#### Troubleshooting Steps

```bash
# Check logs
docker-compose logs app

# Verify credentials
# Ensure password meets complexity requirements
# Reset password if necessary
```

### Problem: JWT Token Issues

- **Symptoms**: Repeated authentication failures
- **Solutions**:
  1. Regenerate JWT secret
  2. Check token expiration settings
  3. Verify secret key configuration

## Database Connection Problems

### Problem: Connection Refused

- **Symptoms**:
  - Database unavailable
  - Connection timeout
- **Troubleshooting**:

```bash
# Check database container status
docker-compose ps db

# Verify connection string
# Ensure correct credentials in .env
# Check network configuration
```

### Problem: Migration Failures

- **Symptoms**:
  - Database schema errors
  - Migration conflicts
- **Solutions**:

```bash
# Reset migrations
flask db stamp head
flask db migrate
flask db upgrade

# Force migration
flask db upgrade --sql
```

## Performance Issues

### Slow Query Detection

- Use database monitoring tools
- Analyze query execution plans
- Add database indexes

### Memory Consumption

- Monitor container resources
- Optimize SQLAlchemy queries
- Implement connection pooling

## Security Troubleshooting

### Potential Vulnerabilities

- Regularly update dependencies
- Run security scans
- Use `safety` for dependency checks

```bash
# Dependency security check
safety check
```

## Logging & Debugging

### Comprehensive Logging

- Enable debug mode
- Capture detailed error logs
- Use structured logging

### Debug Configuration

```python
# In main.py or configuration
app.config['DEBUG'] = True
app.config['SQLALCHEMY_ECHO'] = True
```

## Network & Containerization

### Docker Network Issues

- Verify docker network configuration
- Check port mappings
- Ensure container intercommunication

```bash
# Inspect docker networks
docker network ls
docker network inspect backend-flask-api_default
```

## Common Error Scenarios

### 500 Internal Server Error

- Check application logs
- Validate input data
- Review recent code changes

### 403 Forbidden

- Verify JWT permissions
- Check user role configurations
- Validate token scopes

## Recommended Diagnostic Workflow

1. Identify Error Symptoms
2. Check Logs
3. Reproduce in Controlled Environment
4. Isolate Component
5. Apply Targeted Fix
6. Verify Resolution

## Emergency Recovery

### Complete Reset

```bash
# Stop all services
docker-compose down -v

# Rebuild from scratch
docker-compose up --build
```

## Monitoring Tools

- Prometheus
- Grafana
- ELK Stack
- Sentry Error Tracking

## Best Practices

- Regular updates
- Comprehensive logging
- Proactive monitoring
- Security patch management
