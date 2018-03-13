import math
from . import terrainutil
import util

import django.utils
django.utils.timezone.activate('America/Juneau')

from django.db import models
APP='terrainapp'

class BaseModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    def clink(self, text=None,wrap=True,skip_btn=False,klasses=None, tooltip=None):
        if skip_btn:
            klass=''
        else:
            klass='btn btn-default'
        if klasses:
            klass+=' '.join(klasses)
        if wrap:
            wrap=''
        else:
            wrap=' nb'
        if not text:
            text=self
        if not tooltip:
            tooltip=''

        return u'<a class="%s%s" title="%s" href="../../%s/%s/?id=%d">%s</a>'%(klass, wrap, tooltip, APP, self.__class__.__name__.lower(), self.id, text)

    class Meta:
        app_label=APP
        abstract=True

class RequestSource(BaseModel):
    ip=models.CharField(max_length=100)
    success_count=models.IntegerField(default=0)
    failure_count=models.IntegerField(default=0)

    class Meta:
        app_label='terrainapp'
        db_table='requestsource'

    def __str__(self):
        return 'Source:%s successes: %d failures: %d'%(self.ip, self.success_count, self.failure_count)

class UserSource(BaseModel): #this is the summary of every time a user joined from this IP.
    user=models.ForeignKey('RobloxUser', related_name='usersources')
    source=models.ForeignKey('RequestSource', related_name='usersources')
    first=models.BooleanField(default=0) #whether the user started the server.
    count=models.IntegerField(default=0)

    class Meta:
        app_label='terrainapp'
        db_table='usersource'

    def __str__(self):
        return '%s joined from ip %s %d times.'%(self.user, self.source.ip, self.count)

class Day(BaseModel):
    #day=models.IntegerField() #e.g. 17 = 1970 jan 1st + 17 days
    daystr=models.CharField(max_length=50) # Jan 18, 1970

    class Meta:
        app_label='terrainapp'
        db_table='day'

    def __str__(self):
        return '%s has power %s on %s'%(self.user, self.power, self.daystr)

class UserPower(BaseModel):
    user=models.ForeignKey('RobloxUser', related_name='userpowers')
    power=models.ForeignKey('Power', related_name='userpowers')
    day=models.ForeignKey('Day', related_name='userpowers')

    class Meta:
        app_label='terrainapp'
        db_table='userpower'

    def __str__(self):
        return '%s has power %s on %s'%(self.user, self.power.name, self.day)

class Power(BaseModel):
    name=models.CharField(max_length=50)

    class Meta:
        app_label='terrainapp'
        db_table='power'

    def __str__(self):
        return 'power: %s'%(self.name)


class FailedSecurityAttempt(BaseModel):
    source=models.ForeignKey('RequestSource', related_name='failures')
    params=models.CharField(max_length=250, blank=True, null=True)

    class Meta:
        app_label='terrainapp'
        db_table='failedsecurityattempt'

    def __str__(self):
        return '%s failed at %s'%(self.source, self.created)

#~ class UserStats(BaseModel):
    #~ user=models.ForeignKey('User', related_name='stats')
    #~ finds=models.IntegerField()
    #~ wrs=models.IntegerField()
    #~ topTens=models.IntegerField()

    #~ class Meta:
        #~ app_label='terrainapp'
        #~ db_table='userstats'

class RobloxUser(BaseModel):
    userId=models.IntegerField(unique=True) #blank=True, null=True
    username=models.CharField(max_length=30)
    banLevel=models.IntegerField(default=0) #0==safe, 1=ban, 2=bad ban

    #ban = no chat
    #superban = no chat, slow runspeed muahaha.
    def setBanLevel(self, banLevel):
        if self.banLevel!=banLevel:
            self.banLevel=banLevel
            self.save()

    class Meta:
        app_label='terrainapp'
        db_table='robloxuser'

    def __str__(self):
        bantext=''
        if self.banLevel:
            bantext='%s'%str(self.banLevel)
        return '%s%s'%(self.username or str(self.userId), bantext)

class GameJoin(BaseModel):
    user=models.ForeignKey('RobloxUser', related_name='joins')

    class Meta:
        app_label='terrainapp'
        db_table='gamejoin'

    def __str__(self):
        return '%s joined game.'%self.user.username

class UserDied(BaseModel):
    user=models.ForeignKey('RobloxUser', related_name='deaths')
    x=models.FloatField(blank=True, null=True)
    y=models.FloatField(blank=True, null=True)
    z=models.FloatField(blank=True, null=True)

    class Meta:
        app_label='terrainapp'
        db_table='userdied'

    def __str__(self):
        return '%s died in game at %0.0f, %0.0f, %0.0f.'%(self.user.username, self.x, self.y, self.z)

class UserQuit(BaseModel):
    user=models.ForeignKey('RobloxUser', related_name='quits')
    x=models.FloatField(blank=True, null=True)
    y=models.FloatField(blank=True, null=True)
    z=models.FloatField(blank=True, null=True)

    class Meta:
        app_label='terrainapp'
        db_table='userquit'

    def __str__(self):
        return '%s quit in game at %0.0f, %0.0f, %0.0f.'%(self.user.username, self.x, self.y, self.z)

class UserReset(BaseModel):
    user=models.ForeignKey('RobloxUser', related_name='resets')
    x=models.FloatField(blank=True, null=True)
    y=models.FloatField(blank=True, null=True)
    z=models.FloatField(blank=True, null=True)

    class Meta:
        app_label='terrainapp'
        db_table='userreset'

    def __str__(self):
        return '%s reset in game at %0.0f, %0.0f, %0.0f.'%(self.user.username, self.x, self.y, self.z)


class GameLeave(BaseModel):
    user=models.ForeignKey('RobloxUser', related_name='leaves')

    class Meta:
        app_label='terrainapp'
        db_table='gameleave'

    def __str__(self):
        return '%s left game.'%self.user.username

class Sign(BaseModel):
    signId=models.IntegerField()
    name=models.CharField(max_length=50)
    x=models.FloatField(blank=True, null=True)
    y=models.FloatField(blank=True, null=True)
    z=models.FloatField(blank=True, null=True)

    calcFinds=models.IntegerField(default=0) #calculated values for total finds.
    calcNearest=models.ForeignKey('Sign', related_name='nearest_to', default=None, null=True)

    class Meta:
        app_label='terrainapp'
        db_table='sign'

    def __unicode__(self):
        return 'Sign %d (%s)'%(self.signId, self.name)

    def __str__(self):
        return '%s'%(self.name)

    def findNearestSign(self, others):
        bestDistance=None
        for o in others:
            if o.id==self.id:continue
            dist=Sign.getDistance(self, o)
            if bestDistance==None or dist<bestDistance:
                bestDistance=dist
                bestOther=o
        return bestOther

    def getDistance(self, other):
        return math.pow(((self.x-other.x)**2+(self.y-other.y)**2+(self.z-other.z)**2), 1/2)

class Find(BaseModel):
    sign=models.ForeignKey('Sign', related_name='finds')
    user=models.ForeignKey('RobloxUser', related_name='finds')

    class Meta:
        app_label='terrainapp'
        db_table='find'

    def __str__(self):
        return '%s found %s'%(self.user.username, self.sign.name)

class Race(BaseModel):
    start=models.ForeignKey('Sign', related_name='starts')
    end=models.ForeignKey('Sign', related_name='ends')
    distance=models.IntegerField(default=0)

    class Meta:
        app_label='terrainapp'
        db_table='race'

    def calculateDistance(self):
        if self.start and self.end:
            self.distance=terrainutil.getDistance(self.start, self.end)

    def __str__(self):
        return '%s => %s (%0.0f)'%(self.start.name, self.end.name, self.distance)

    def save(self, *args, **kwargs):
        if not self.distance:
            self.calculateDistance()
        super(Race, self).save(*args, **kwargs)

class Run(BaseModel):
    race=models.ForeignKey('Race', related_name='runs')
    user=models.ForeignKey('RobloxUser', related_name='runs', db_index=True)
    place=models.IntegerField(default=0)
    speed=models.FloatField(default=0)

    raceMilliseconds=models.IntegerField() #run time in milliseconds

    class Meta:
        app_label='terrainapp'
        db_table='run'

    def __str__(self):
        return '%s ran the race from %s to %s in %f'%(self.user.username, self.race.start.name, self.race.end.name, self.raceMilliseconds/1000)

    def save(self, *args, **kwargs):
        self.speed=self.race.distance/1.0/self.raceMilliseconds*1000
        super(Run, self).save(*args, **kwargs)

class BestRun(BaseModel): #an individual user's best run of a certain race.  This is how we generate user-distinct top 10
    race=models.ForeignKey('Race', related_name='bestruns')
    user=models.ForeignKey('RobloxUser', related_name='bestruns')
    place=models.IntegerField(blank=True, null=True) #global place for this race.
    raceMilliseconds=models.IntegerField() #run time in milliseconds
    speed=models.FloatField(default=0)

    class Meta:
        app_label='terrainapp'
        db_table='bestrun'

    def __str__(self):
        placeText=self.place and '[place: %d]'%self.place
        return '%s\'s bestrun of the race from %s to %s took: %f%s'%(self.user.username, self.race.start.name, self.race.end.name, self.raceMilliseconds/1000, placeText)

    def save(self, *args, **kwargs):
        self.speed=self.race.distance/1.0/self.raceMilliseconds*1000
        super(BestRun, self).save(*args, **kwargs)

class Message(BaseModel):
    user=models.ForeignKey('RobloxUser', related_name='messages')
    text=models.CharField(max_length=200)
    read=models.BooleanField(default=False)

    class Meta:
        app_label='terrainapp'
        db_table='message'

    def __str__(self):
        return 'Message %s=>%s'%(self.user, self.text)

class GameServerError(BaseModel):
    code=models.CharField(max_length=100)
    data=models.CharField(max_length=500)
    message=models.CharField(max_length=500)
    requestsource=models.ForeignKey('RequestSource', related_name='gameservererrors', blank=True, null=True)

    class Meta:
        app_label='terrainapp'
        db_table='gameservererror'

    def __str__(self):
        return '%s:%s:%s'%(self.code or '',self.data or '',self.message or '')

class ChatMessage(BaseModel):
    user=models.ForeignKey('RobloxUser', related_name='chatmessages')
    rawtext=models.CharField(max_length=500)
    filteredtext=models.CharField(max_length=500)
    requestsource=models.ForeignKey('RequestSource', related_name='chatmessages')

    class Meta:
        app_label='terrainapp'
        db_table='chatmessage'

    def __str__(self):
        fil=''
        if self.rawtext!=self.filteredtext:
            fil=' => '+self.filteredtext
        return '%s sent %s%s'%(self.user.username, self.rawtext, fil)

class RaceEvent(BaseModel):
    name=models.CharField(max_length=100, default='')
    description=models.CharField(max_length=1000, default='')
    race=models.ForeignKey('Race', related_name='events')
    startdate=models.DateTimeField()
    enddate=models.DateTimeField()
    badge=models.ForeignKey('Badge', related_name='events')

    class Meta:
        app_label='terrainapp'
        db_table='raceevent'

    def __str__(self):
        return 'event: %s. Race: %s and get badge: %s.  Start:%s End:%s. %s'%(self.name, self.race, self.badge.name, util.safeDateAsString(self.startdate), util.safeDateAsString(self.enddate), self.description)

class Badge(BaseModel):
    name=models.CharField(max_length=200)
    assetId=models.IntegerField() #the roblox assetId

    class Meta:
        app_label='terrainapp'
        db_table='badge'

    def __str__(self):
        return 'badge: %s (%d)'%(self.name, self.assetId)

#more stuff like find best 10 etc.
