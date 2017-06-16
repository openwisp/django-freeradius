from .base.models import (AbstractNas, AbstractRadiusAccounting,
                          AbstractRadiusCheck, AbstractRadiusGroup,
                          AbstractRadiusGroupCheck, AbstractRadiusGroupReply,
                          AbstractRadiusGroupUsers,
                          AbstractRadiusPostAuthentication,
                          AbstractRadiusReply, AbstractRadiusUserGroup)


class RadiusGroup(AbstractRadiusGroup):
    pass


class RadiusGroupUsers(AbstractRadiusGroupUsers):
    pass


class RadiusCheck(AbstractRadiusCheck):
    pass


class RadiusAccounting(AbstractRadiusAccounting):
    pass


class RadiusReply(AbstractRadiusReply):
    pass


class Nas(AbstractNas):
    pass


class RadiusGroupCheck(AbstractRadiusGroupCheck):
    pass


class RadiusGroupReply(AbstractRadiusGroupReply):
    pass


class RadiusPostAuthentication(AbstractRadiusPostAuthentication):
    pass


class RadiusUserGroup(AbstractRadiusUserGroup):
    pass
