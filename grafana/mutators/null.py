from grafana.mutators import Mutator


class Null(Mutator):
    name = "Default Zero"

    def mutate(self, data):
        data.setdefault("rows", [])
        data.setdefault("panels", {})
        for row in data["rows"]:
            row.setdefault("panels", [])
            for panel in row["panels"]:
                panel["nullPointMode"] = "null"
        for panel in data["panels"]:
            panel["nullPointMode"] = "null"
        return data
