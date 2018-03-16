from admin_helpers import *
from allmodels import *
from terrainapp.admin.RunAdmin import RunAdmin

import util

class BestRunAdmin(RunAdmin):
    list_display='id myuser myrace mystart myend mytime myspeed place created_tz'.split()

    def mytime(self, obj):
        exi=BestRun.objects.filter(race=obj.race, user=obj.user)
        return '%0.3f'%(obj.raceMilliseconds*1.0/1000)

    def myspeed(self, obj):
        if not obj.speed:
            obj.save()
        return '%0.1f studs/sec'%obj.speed

    myspeed.admin_order_field='-speed'

    adminify(mytime, myspeed)

