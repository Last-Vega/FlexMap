from django.db import models
from django.db.models import constraints

# Create your models here.
class Options(models.Model):
    """選択肢テーブルの定義"""
    # id = models.IntegerField('ID', primary_key=True)
    vehicle = models.CharField('Option', max_length=255)
    speed = models.IntegerField('Speed')
    first_fee = models.IntegerField('FirstFee')
    over_fee = models.IntegerField('OverFee')


    def __str__(self):
        return self.id

class Spots(models.Model):
    """レンタルサービスの提供場所テーブルの定義"""
    id = models.IntegerField('ID',primary_key=True)
    provider_id = models.IntegerField('ProviderID')
    provider_name = models.CharField('ProviderName', max_length=255)
    spot_id = models.IntegerField('SpotID')
    spot_name = models.CharField('SpotName',max_length=255)
    spot_coordinateX = models.FloatField('SpotCoordinateX')
    spot_coordinateY = models.FloatField('SpotCoordinateY')
    spot_address = models.CharField('SpotAdress',max_length=255)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["provider_id","spot_id"],
                name="spots_unique"
            )
        ]