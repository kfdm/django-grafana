from grafana.mutators import Mutator


class Null(Mutator):
    """
    Default Zero

    Reset pointers to Zero
    """

    def mutate(self, data):
        for panel in data.setdefault("panels", []):
            if panel["type"] == "row":
                for subpanel in panel.get("panels", []):
                    subpanel["nullPointMode"] = "null"
            else:
                panel["nullPointMode"] = "null"
        return data
