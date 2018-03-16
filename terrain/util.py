import datetime, pytz

DATE='%Y-%m-%d'
minute=60
hour=minute*60
day=hour*24
week=day*7

def safeDateAsString(d):
    if d:
        return datetime.datetime.strftime(d,DATE)
    return 'no date set'

def describe_session_duration(remainder):
    if remainder ==0 or remainder==None:
        return 'active session'

    weeks=remainder//week
    remainder=remainder-weeks*week

    days=remainder//day
    remainder=remainder-days*day

    hours=remainder//hour
    remainder=remainder-hours*hour

    minutes=remainder//minute
    remainder=remainder-minutes*minute

    seconds=remainder

    res=''
    if weeks:
        res='%d weeks '%weeks
    if days:
        res+='%d days '%days
    if hours:
        res+='%d hours '%hours
    if minutes:
        res+='%d minutes '%minutes
    if seconds:
        res+='%d seconds'%seconds

    return res.strip()

def utcnow():
    now=datetime.datetime.utcnow().replace(tzinfo=pytz.utc)
    return now