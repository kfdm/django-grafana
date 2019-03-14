from pkg_resources import working_set


class Mutator:
    @property
    def model(self):
        return self.__class__.__module__

    @classmethod
    def drivers(cls, whitelist=None):
        for entry in working_set.iter_entry_points("grafana.mutator"):
            if whitelist and entry.module_name not in whitelist:
                continue
            yield entry.module_name, entry.load()()
