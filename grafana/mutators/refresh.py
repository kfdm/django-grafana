from grafana.mutators import Mutator


class Refresh(Mutator):
    """
    Default Refresh

    Set default Refresh to 5 minutes
    """

    def mutate(self, data):
        data["refresh"] = "5m"
        return data
