# Monitoring & Maintenance Plan
## Latency thresholds
- Target < 2s (Day 1 budget); alert if p95 > 2.5s (Day 6 measured p95 = 2.29s)
## Uptime target
- 99% during office hours
## Refresh schedule
- ChromaDB: weekly or on new CSV
## Backup
- knowledge_base.db + CRM sheet: daily export
## Security review
- Monthly re-run of Day 6 injection suite; quarterly key rotation
