from .base.models import (AbstractNas, AbstractRadiusAccounting,
                          AbstractRadiusCheck, AbstractRadiusGroup,
                          AbstractRadiusGroupCheck, AbstractRadiusGroupReply,
                          AbstractRadiusGroupUsers,
                          AbstractRadiusPostAuthentication,
                          AbstractRadiusReply, AbstractRadiusUserGroup)
import swapper

class RadiusGroup(AbstractRadiusGroup):

     class Meta:
       swappable = swapper.swappable_setting('reusableapp', 'RadiusGroup')


class RadiusGroupUsers(AbstractRadiusGroupUsers):

    class Meta:
      swappable = swapper.swappable_setting('reusableapp', 'RadiusGroupUsers')


class RadiusCheck(AbstractRadiusCheck):

    class Meta:
      swappable = swapper.swappable_setting('reusableapp', 'RadiusCheck')


class RadiusAccounting(AbstractRadiusAccounting):

    class Meta:
      swappable = swapper.swappable_setting('reusableapp', 'RadiusAccounting')


class RadiusReply(AbstractRadiusReply):

    class Meta:
      swappable = swapper.swappable_setting('reusableapp', 'RadiusReply')


class Nas(AbstractNas):

    class Meta:
      swappable = swapper.swappable_setting('reusableapp', 'Nas')


class RadiusGroupCheck(AbstractRadiusGroupCheck):

    class Meta:
      swappable = swapper.swappable_setting('reusableapp', 'RadiusGroupCheck')


class RadiusGroupReply(AbstractRadiusGroupReply):

    class Meta:
      swappable = swapper.swappable_setting('reusableapp', 'RadiusGroupReply')


class RadiusPostAuthentication(AbstractRadiusPostAuthentication):

    class Meta:
      swappable = swapper.swappable_setting('reusableapp', 'RadiusPostAuthentication')


class RadiusUserGroup(AbstractRadiusUserGroup):

    class Meta:
      swappable = swapper.swappable_setting('reusableapp', 'RadiusUserGroup')
