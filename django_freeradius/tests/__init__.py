import os

from django.core.management import call_command


class CreateRadiusObjectsMixin(object):
    def _get_extra_fields(self, **kwargs):
        # For adding mandatory extra fields
        options = dict()
        options.update(**kwargs)
        return options

    def _create_radius_check(self, **kwargs):
        options = {}
        options.update(self._get_extra_fields())
        options.update(kwargs)
        rc = self.radius_check_model(**options)
        rc.full_clean()
        rc.save()
        return rc

    def _create_radius_accounting(self, **kwargs):
        options = {}
        options.update(self._get_extra_fields())
        options.update(kwargs)
        ra = self.radius_accounting_model.objects.create(**options)
        return ra

    def _create_radius_reply(self, **kwargs):
        options = {}
        options.update(self._get_extra_fields())
        options.update(kwargs)
        rr = self.radius_reply_model(**options)
        rr.full_clean()
        rr.save()
        return rr

    def _create_nas(self, **kwargs):
        options = {}
        options.update(self._get_extra_fields())
        options.update(kwargs)
        n = self.nas_model(**options)
        n.full_clean()
        n.save()
        return n

    def _create_radius_group(self, **kwargs):
        options = dict(name='test',
                       description='test')
        options.update(self._get_extra_fields())
        options.update(kwargs)
        rg = self.radius_group_model(**options)
        rg.full_clean()
        rg.save()
        return rg

    def _create_radius_groupcheck(self, **kwargs):
        options = {}
        options.update(self._get_extra_fields())
        options.update(kwargs)
        c = self.radius_groupcheck_model(**options)
        c.full_clean()
        c.save()
        return c

    def _create_radius_groupreply(self, **kwargs):
        options = {}
        options.update(self._get_extra_fields())
        options.update(kwargs)
        r = self.radius_groupreply_model(**options)
        r.full_clean()
        r.save()
        return r

    def _create_radius_usergroup(self, **kwargs):
        options = {}
        options.update(self._get_extra_fields())
        options.update(kwargs)
        ug = self.radius_usergroup_model(**options)
        ug.full_clean()
        ug.save()
        return ug

    def _create_radius_postauth(self, **kwargs):
        options = {}
        options.update(self._get_extra_fields())
        options.update(kwargs)
        rp = self.radius_postauth_model(**options)
        rp.full_clean()
        rp.save()
        return rp

    def _create_radius_batch(self, **kwargs):
        options = {}
        options.update(self._get_extra_fields())
        options.update(kwargs)
        rb = self.radius_batch_model.objects.create(**options)
        return rb

    def _create_user(self, **kwargs):
        options = {}
        options.update(self._get_extra_fields())
        options.update(kwargs)
        u = self.user_model.objects.create_user(**kwargs)
        return u


class ApiParamsMixin(object):
    def _get_extra_params(self, **kwargs):
        # For adding mandatory extra fields
        options = {}
        options.update(**kwargs)
        return options

    def _get_postauth_params(self, **kwargs):
        params = {'username': 'molly',
                  'password': 'barbar',
                  'reply': 'Access-Accept',
                  'called_station_id': '00-11-22-33-44-55:hostname',
                  'calling_station_id': '00:26:b9:20:5f:10'}
        params.update(self._get_extra_params())
        params.update(kwargs)
        return params

    def _get_accounting_params(self, **kwargs):
        kwargs.update(self._get_extra_params())
        return kwargs


class FileMixin(object):
    def _get_path(self, file):
        d = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(d, file)


class CallCommandMixin(object):
    def _call_command(self, command, **kwargs):
        call_command(command, **kwargs)
