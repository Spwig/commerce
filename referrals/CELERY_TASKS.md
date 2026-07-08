# Referral Program Celery Tasks

Automated background jobs for the referral program.

## Overview

The referral program uses Celery for asynchronous task processing and scheduled background jobs. All tasks are automatically configured via Celery Beat and run on schedule without manual intervention.

## Scheduled Tasks

### 1. Send Reward Expiry Reminders
**Task**: `referrals.send_reward_expiry_reminders`
**Schedule**: Daily at 10 AM
**Purpose**: Send email reminders to customers with rewards expiring in 7 days

**What it does:**
- Finds all issued rewards expiring exactly 7 days from now
- Sends expiration reminder emails to customers
- Provides urgency to encourage reward redemption

**Configuration:**
```python
# In referral program settings
{
    'expiry_days': 90,  # Rewards expire after 90 days (affects expiration date)
}
```

**Logs:**
```bash
# Check task execution
grep "reward expiry reminder" logs/celery.log

# Check emails sent
grep "Sent expiry reminder for reward" logs/django.log
```

---

### 2. Expire Old Rewards
**Task**: `referrals.expire_old_rewards`
**Schedule**: Daily at 1 AM
**Purpose**: Mark expired rewards as expired and clean up

**What it does:**
- Finds all rewards with `status='issued'` that are past their expiration date
- Updates status to `expired`
- Prevents expired rewards from being used

**Database Impact:**
```sql
-- Updates status for expired rewards
UPDATE referrals_referralreward
SET status = 'expired'
WHERE status = 'issued'
  AND expires_at < NOW()
  AND expires_at IS NOT NULL;
```

**Monitoring:**
```bash
# Check expiry task runs
grep "reward expiry cleanup" logs/celery.log

# Check how many expired
grep "Marked .* rewards as expired" logs/celery.log
```

---

### 3. Expire Old Attributions
**Task**: `referrals.expire_old_attributions`
**Schedule**: Daily at 2 AM
**Purpose**: Auto-reject pending attributions that are too old

**What it does:**
- Finds attributions with `status='pending'` older than review period (default 30 days)
- Marks as rejected with reason "expired"
- Prevents indefinite pending states

**Configuration:**
```python
# In referral program settings
{
    'attribution_review_period_days': 30,  # Auto-expire after 30 days pending
}
```

**Rationale:**
- Merchants should review and approve/reject attributions within 30 days
- Prevents backlog of old pending attributions
- Customers get clarity on their referral status

---

### 4. Update Referrer Stats
**Task**: `referrals.update_referrer_stats`
**Schedule**: Every 6 hours (at 12 AM, 6 AM, 12 PM, 6 PM)
**Purpose**: Recalculate aggregated statistics for referrers

**What it does:**
- Loops through all ReferralIdentity records
- Recalculates `total_conversions` (count of approved attributions)
- Recalculates `total_rewards_earned` (sum of issued/redeemed rewards)
- Updates records if values changed

**Why needed:**
- Ensures dashboard stats are accurate
- Corrects any inconsistencies from manual admin actions
- Provides fresh data for leaderboards

**Performance:**
```python
# Processes ~1000 identities per minute
# Typical execution: 10-30 seconds for 500 referrers
```

---

### 5. Fraud Check Batch Process
**Task**: `referrals.fraud_check_batch_process`
**Schedule**: Daily at 3 AM
**Purpose**: Re-evaluate high-risk pending attributions

**What it does:**
- Finds pending attributions with risk score ≥ 70 that are 24+ hours old
- Re-runs fraud validation checks
- Auto-approves if risk dropped below threshold
- Auto-rejects if risk increased to ≥ 90
- Processes 100 attributions per run

**Risk Thresholds:**
- **< 30**: Auto-approve (low risk)
- **30-70**: Manual review required
- **70-89**: High risk (flagged for re-check)
- **≥ 90**: Auto-reject (very high risk)

**Why re-check:**
- Initial checks may flag legitimate users (new accounts, unusual patterns)
- 24-hour delay allows time for additional user activity data
- Reduces false positives and improves accuracy

**Monitoring:**
```bash
# Check fraud checks
grep "fraud check batch process" logs/celery.log

# See auto-actions
grep "Auto-approved\|Auto-rejected" logs/django.log
```

---

### 6. Cleanup Old Events
**Task**: `referrals.cleanup_old_events`
**Schedule**: Weekly on Sunday at 4 AM
**Purpose**: Delete old referral event logs to prevent database bloat

**What it does:**
- Deletes `ReferralEvent` records older than retention period (default 90 days)
- Only deletes low-priority events (`view`, `share`)
- Keeps important events (`click`, `signup`, `order`) permanently

**Configuration:**
```python
# In referral program settings
{
    'event_retention_days': 90,  # Keep events for 90 days
}
```

**Rationale:**
- Referral events can grow to millions of records
- Click/signup/order events needed for analytics (kept permanently)
- View/share events less critical (deleted after 90 days)

**Performance Impact:**
```sql
-- Typical cleanup
DELETE FROM referrals_referralevent
WHERE created_at < (NOW() - INTERVAL '90 days')
  AND event_type IN ('view', 'share');

-- Result: Deletes ~10k-100k records per week
-- Execution time: 1-5 seconds
```

---

## Manual Tasks

### Process Attribution
**Task**: `referrals.process_attribution`
**Schedule**: On-demand (triggered manually or by admin action)
**Purpose**: Process a specific attribution asynchronously

**Usage:**
```python
from referrals.tasks import process_attribution

# Queue attribution processing
process_attribution.delay(attribution_id=123)
```

**What it does:**
- Runs validation on specific attribution
- Creates and issues rewards if approved
- Useful for retry after errors
- Useful for manual admin approval actions

**Retry Logic:**
- Max retries: 3
- Retry delay: 5 minutes (exponential backoff)
- Max backoff: 30 minutes

---

## Task Schedules Summary

| Task | Frequency | Time | Purpose |
|------|-----------|------|---------|
| Send Reward Expiry Reminders | Daily | 10 AM | Email reminders for expiring rewards |
| Expire Old Rewards | Daily | 1 AM | Mark expired rewards |
| Expire Old Attributions | Daily | 2 AM | Auto-reject old pending attributions |
| Update Referrer Stats | Every 6 hours | 12 AM, 6 AM, 12 PM, 6 PM | Recalculate statistics |
| Fraud Check Batch | Daily | 3 AM | Re-evaluate high-risk attributions |
| Cleanup Old Events | Weekly | Sunday 4 AM | Delete old event logs |

---

## Celery Configuration

### Starting Celery Worker

```bash
# Development
celery -A core worker -l info

# Production (with concurrency)
celery -A core worker -l info --concurrency=4
```

### Starting Celery Beat

```bash
# Development
celery -A core beat -l info

# Production (with scheduler)
celery -A core beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler
```

### Combined (Development Only)

```bash
# Worker + Beat in one process (not for production)
celery -A core worker -l info --beat
```

---

## Monitoring Tasks

### Check Task Status

```bash
# View active tasks
celery -A core inspect active

# View scheduled tasks
celery -A core inspect scheduled

# View registered tasks
celery -A core inspect registered | grep referrals
```

### Task Logs

```bash
# Celery task logs
tail -f logs/celery.log | grep referrals

# Django logs (for task execution details)
tail -f logs/django.log | grep "referral"
```

### Task Statistics

```python
# In Django shell
from celery import current_app

# Get task stats
stats = current_app.control.inspect().stats()
print(stats)

# Get scheduled tasks
scheduled = current_app.control.inspect().scheduled()
print(scheduled)
```

---

## Troubleshooting

### Task Not Running

**Problem**: Scheduled task not executing at expected time

**Solutions:**
1. Check Celery Beat is running:
   ```bash
   ps aux | grep "celery.*beat"
   ```

2. Check beat schedule configuration:
   ```python
   # In Django shell
   from django.conf import settings
   print(settings.CELERY_BEAT_SCHEDULE)
   ```

3. Check for errors in beat logs:
   ```bash
   tail -100 logs/celery.log | grep -i error
   ```

4. Restart Celery Beat:
   ```bash
   # Kill existing beat process
   pkill -f "celery.*beat"

   # Start new beat process
   celery -A core beat -l info
   ```

---

### Task Failing

**Problem**: Task executes but fails with errors

**Debug:**
1. Check task logs for exception:
   ```bash
   grep "referrals.*ERROR" logs/django.log
   ```

2. Run task manually in Django shell:
   ```python
   from referrals.tasks import send_reward_expiry_reminders
   result = send_reward_expiry_reminders()
   print(result)
   ```

3. Check task signature and arguments:
   ```python
   from celery import current_app
   task = current_app.tasks.get('referrals.send_reward_expiry_reminders')
   print(task)
   print(task.run())
   ```

---

### Task Running Slowly

**Problem**: Task takes too long to complete

**Optimization:**
1. Check database query performance:
   ```python
   # Enable query logging
   import logging
   logging.getLogger('django.db.backends').setLevel(logging.DEBUG)
   ```

2. Add database indexes if needed
3. Batch process records (limit 100-1000 per run)
4. Use `select_related()` and `prefetch_related()` for queries

---

### Too Many Pending Tasks

**Problem**: Task queue backlog growing

**Solutions:**
1. Increase worker concurrency:
   ```bash
   celery -A core worker -l info --concurrency=8
   ```

2. Add more worker instances (horizontal scaling)

3. Optimize task execution time

4. Adjust task expiration:
   ```python
   'task-name': {
       'schedule': 300.0,
       'options': {
           'expires': 240.0,  # Task expires if not picked up in 4 minutes
       }
   }
   ```

---

## Configuration Options

### Program Settings

Configure in Django admin → Referral Program → Settings:

```json
{
    "expiry_days": 90,
    "attribution_review_period_days": 30,
    "event_retention_days": 90,
    "auto_approve_threshold": 30
}
```

### Schedule Customization

To change task schedules, edit `core/settings.py`:

```python
CELERY_BEAT_SCHEDULE = {
    'send-reward-expiry-reminders': {
        'task': 'referrals.send_reward_expiry_reminders',
        'schedule': crontab(hour=8, minute=0),  # Change to 8 AM
    },
    # ... other tasks
}
```

### Crontab Examples

```python
# Every day at 10:30 AM
crontab(hour=10, minute=30)

# Every Monday at 9 AM
crontab(hour=9, minute=0, day_of_week=1)

# Every 1st of month at 2 AM
crontab(hour=2, minute=0, day_of_month=1)

# Every 6 hours
crontab(minute=0, hour='*/6')

# Multiple times per day
crontab(hour='*/4', minute=0)  # Every 4 hours
```

---

## Production Deployment

### Supervisor Configuration

Create `/etc/supervisor/conf.d/celery.conf`:

```ini
[program:celery-worker]
command=/path/to/shop_venv/bin/celery -A core worker -l info --concurrency=4
directory=/path/to/shop
user=www-data
autostart=true
autorestart=true
stderr_logfile=/var/log/celery/worker.err.log
stdout_logfile=/var/log/celery/worker.out.log

[program:celery-beat]
command=/path/to/shop_venv/bin/celery -A core beat -l info
directory=/path/to/shop
user=www-data
autostart=true
autorestart=true
stderr_logfile=/var/log/celery/beat.err.log
stdout_logfile=/var/log/celery/beat.out.log
```

### Systemd Configuration

Create `/etc/systemd/system/celery-worker.service`:

```ini
[Unit]
Description=Celery Worker
After=network.target

[Service]
Type=forking
User=www-data
Group=www-data
WorkingDirectory=/path/to/shop
ExecStart=/path/to/shop_venv/bin/celery -A core worker -l info --detach
Restart=always

[Install]
WantedBy=multi-user.target
```

Create `/etc/systemd/system/celery-beat.service`:

```ini
[Unit]
Description=Celery Beat Scheduler
After=network.target

[Service]
Type=simple
User=www-data
Group=www-data
WorkingDirectory=/path/to/shop
ExecStart=/path/to/shop_venv/bin/celery -A core beat -l info
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
systemctl enable celery-worker celery-beat
systemctl start celery-worker celery-beat
```

---

## Best Practices

1. **Monitor task execution** - Set up alerts for failed tasks
2. **Test locally first** - Run tasks manually before deploying
3. **Use task retries** - Configure max_retries for critical tasks
4. **Set task timeouts** - Prevent hung tasks from blocking workers
5. **Log everything** - Use structured logging for debugging
6. **Batch process large datasets** - Limit queries to 100-1000 records
7. **Use task expiration** - Prevent stale tasks from executing
8. **Separate critical tasks** - Use dedicated workers for important tasks
9. **Scale horizontally** - Add more workers instead of increasing concurrency
10. **Monitor queue depth** - Watch for growing backlogs

---

## Support

For issues with Celery tasks:

1. Check logs first: `logs/celery.log` and `logs/django.log`
2. Run task manually in Django shell for debugging
3. Check Celery worker and beat are running
4. Verify task is registered: `celery -A core inspect registered`
5. Check task schedule: Review `CELERY_BEAT_SCHEDULE` in settings
