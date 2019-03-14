from grafana.mutators import Mutator


class Refresh(Mutator):
    name = "Default Refresh"

    def mutate(self, data):
        data["refresh"] = "5m"
        return data
