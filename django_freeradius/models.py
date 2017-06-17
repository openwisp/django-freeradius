from .base.models import (AbstractNas, AbstractRadiusAccounting,
                          AbstractRadiusCheck, AbstractRadiusGroup,
                          AbstractRadiusGroupCheck, AbstractRadiusGroupReply,
                          AbstractRadiusGroupUsers,
                          AbstractRadiusPostAuthentication,
                          AbstractRadiusReply, AbstractRadiusUserGroup)
import swapper

class RadiusGroup(AbstractRadiusGroup):

     class Meta:
       swappable = swapper.swappable_setting('django_freeradius', 'RadiusGroup')


class RadiusGroupUsers(AbstractRadiusGroupUsers):

    class Meta:
      swappable = swapper.swappable_setting('django_freeradius', 'RadiusGroupUsers')


class RadiusCheck(AbstractRadiusCheck):

    class Meta:
      swappable = swapper.swappable_setting('django_freeradius', 'RadiusCheck')


class RadiusAccounting(AbstractRadiusAccounting):

    class Meta:
      swappable = swapper.swappable_setting('django_freeradius', 'RadiusAccounting')


class RadiusReply(AbstractRadiusReply):

    class Meta:
      swappable = swapper.swappable_setting('django_freeradius', 'RadiusReply')


class Nas(AbstractNas):

    class Meta:
      swappable = swapper.swappable_setting('django_freeradius', 'Nas')


class RadiusGroupCheck(AbstractRadiusGroupCheck):

    class Meta:
      swappable = swapper.swappable_setting('django_freeradius', 'RadiusGroupCheck')


class RadiusGroupReply(AbstractRadiusGroupReply):

    class Meta:
      swappable = swapper.swappable_setting('django_freeradius', 'RadiusGroupReply')


class RadiusPostAuthentication(AbstractRadiusPostAuthentication):

    class Meta:
      swappable = swapper.swappable_setting('django_freeradius', 'RadiusPostAuthentication')


class RadiusUserGroup(AbstractRadiusUserGroup):

    class Meta:
      swappable = swapper.swappable_setting('django_freeradius', 'RadiusUserGroup')
