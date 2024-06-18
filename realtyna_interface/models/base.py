from django.db import models

class CreateHistoryModelMixin(models.Model):
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class UpdateHistoryModelMixin(models.Model):
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class BaseModel(models.Model):
    objects = models.Manager()

    @property
    def meta(self):
        return self._meta

    @property
    def instance_from_db(self):
        return self.__class__.objects.filter(pk=self.pk).first()

    @classmethod
    def get_field(cls, field):
        return cls._meta.get_field(field)

    class Meta:
        abstract = True
