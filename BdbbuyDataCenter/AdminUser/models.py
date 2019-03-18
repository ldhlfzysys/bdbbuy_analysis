from django.db import models

# Create your models here.
from Tools.model_util import CModel



class Adminuser(CModel):
    name = models.CharField(max_length=50, blank=True, null=True)
    password = models.CharField(max_length=50, blank=True, null=True)
    boss = models.IntegerField(blank=True, null=True)
    driver = models.IntegerField(blank=True, null=True)
    store_manager = models.IntegerField()
    sale_manager = models.IntegerField(blank=True, null=True)
    sale_manager7 = models.IntegerField(blank=True, null=True)
    auth = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'adminuser'

    def toInfoJson(self):
        return {
            "id": self.id,
            "name": self.name
        }

    @classmethod
    def getDriverList(cls):
        return Adminuser.objects.filter(driver=1)

    @classmethod
    def getUserNameById(cls, user_id):
        name = ''
        admin_q = Adminuser.objects.filter(id=user_id)
        if len(admin_q) > 0:
            name = admin_q[0].name
        return name

