import math
from django.db import models
from terrainapp.basemodel import BaseModel
from constants import *

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