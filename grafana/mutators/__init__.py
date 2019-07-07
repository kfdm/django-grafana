from pkg_resources import working_set
from django.utils.functional import cached_property


class Mutator:
    @property
    def model(self):
        return self.__class__.__module__

    @cached_property
    def name(self):
        try:
            return self.__doc__.strip().split("\n", 1)[0].strip()
        except AttributeError:
            return self.__class__

    @cached_property
    def help(self):
        try:
            return self.__doc__.strip().split("\n", 1)[1].strip()
        except AttributeError:
            return "No Help"

    @classmethod
    def drivers(cls, whitelist=None):
        for entry in working_set.iter_entry_points("grafana.mutator"):
            if whitelist and entry.module_name not in whitelist:
                continue
            yield entry.module_name, entry.load()()
