"""Interpret an explicitly supplied snapshot; never discover or query a runtime."""
from datetime import datetime, timezone
from .contracts import Invalid, keys, text


def instant(value):
    if not isinstance(value, str):
        raise Invalid('Timestamp must be an ISO string with timezone')
    try:
        parsed = datetime.fromisoformat(value.replace('Z', '+00:00'))
        if parsed.tzinfo is None:
            raise ValueError()
        return parsed.astimezone(timezone.utc)
    except (ValueError, OverflowError) as exc:
        raise Invalid('Timestamp must be an ISO string with timezone') from exc


def diagnose(snapshot, as_of):
    keys(snapshot, ('schema_version', 'observed_at', 'target', 'checks', 'services'), 'snapshot')
    if type(snapshot['schema_version']) is not int or snapshot['schema_version'] != 1:
        raise Invalid('Unsupported snapshot schema_version')
    observed, now = instant(snapshot['observed_at']), instant(as_of)
    if observed > now:
        raise Invalid('Observation cannot be in the future')
    target = snapshot['target']
    keys(target, ('expected', 'observed'), 'target')
    text(target['expected'], 'expected target')
    if target['observed'] is not None:
        text(target['observed'], 'observed target')
    checks = snapshot['checks']
    names = ('mode_loaded', 'skill_loaded', 'docs_query', 'runtime_query', 'extraction')
    keys(checks, names, 'checks')
    if any(v not in ('passed', 'failed', 'unverified') for v in checks.values()):
        raise Invalid('Checks must be passed, failed or unverified')
    services = snapshot['services']
    if not isinstance(services, list) or len(services) > 100:
        raise Invalid('services must be a list of at most 100 entries')
    findings = []
    def add(check, status, message):
        findings.append({'check': check, 'status': status, 'message': message})
    age = (now - observed).total_seconds()
    add('freshness', 'unverified' if age > 86400 else 'passed',
        'Snapshot older than 24 hours; recollect before relying on it.' if age > 86400 else 'Snapshot within 24 hours; this tool did not verify its source.')
    actual = target['observed']
    add('target', 'unverified' if actual is None else 'passed' if actual == target['expected'] else 'failed',
        'Compare the observed target with the intended target before runtime changes.')
    for name in names:
        add(name, checks[name], 'Supplied observation; retain the corresponding tool call or run evidence.')
    if not services:
        add('services', 'unverified', 'No service observations supplied.')
    seen = set()
    for service in services:
        keys(service, ('name', 'role', 'state', 'exit_code', 'health', 'restarts_before', 'restarts_after'), 'service')
        name = service['name']
        text(name, 'service name')
        if name in seen:
            raise Invalid('Duplicate service name')
        seen.add(name)
        if service['role'] not in ('init', 'daemon') or service['state'] not in ('running', 'exited', 'restarting', 'missing'):
            raise Invalid('Unknown service role/state')
        if service['health'] not in ('healthy', 'unhealthy', 'starting', 'none'):
            raise Invalid('Unknown health value')
        code = service['exit_code']
        if code is not None and (type(code) is not int or not 0 <= code <= 255):
            raise Invalid('exit_code: null or integer 0..255')
        counts = [service['restarts_before'], service['restarts_after']]
        if any(v is not None and (type(v) is not int or v < 0) for v in counts):
            raise Invalid('Restart counts must be nonnegative integers or null')
        if all(v is not None for v in counts) and counts[1] < counts[0]:
            raise Invalid('Restart counter decreased; recollect one container instance')
        status, message = 'unverified', 'Insufficient evidence for the declared service role.'
        if service['role'] == 'init':
            if service['state'] == 'exited' and code is not None:
                status = 'passed' if code == 0 else 'failed'
                message = 'Initialization exit code checked; an exited initializer can be successful.'
            elif service['state'] in ('missing', 'restarting'):
                status = 'failed'
        else:
            if service['state'] != 'running' or service['health'] == 'unhealthy':
                status, message = 'failed', 'Daemon is absent, stopped, restarting or unhealthy.'
            elif all(v is not None for v in counts) and counts[1] > counts[0]:
                status, message = 'failed', 'Restart count increased during the observation interval.'
            elif service['health'] == 'healthy' and all(v is not None for v in counts):
                status, message = 'passed', 'Healthy daemon with stable observed restart count.'
        add('service:' + name, status, message)
    overall = 'failed' if any(f['status'] == 'failed' for f in findings) else 'unverified' if any(f['status'] == 'unverified' for f in findings) else 'passed'
    return {'status': overall, 'basis': 'supplied snapshot only; no runtime or network access',
            'observed_at': snapshot['observed_at'], 'as_of': as_of, 'findings': findings}
