systematic_registry = {}
import copy

class Systematic:
    params = []
    def __init__(self, name, **config):
        self.name = name
        self.config = config
        self.values = {}
        print(f"Would now create systematic {self.__class__.__name__} from config info: {config}")

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        name = cls.name if hasattr(cls, 'name') else cls.__name__
        name = name.lower()
        print(f"Register systematic {name}")
        systematic_registry[name] = cls

    @classmethod
    def from_info(cls, name, config):
        config  = config.copy()
        class_name = config.pop('type')
        if class_name is None:
            raise ValueError("Systematic is missing 'type' entry in param file")
        class_obj = systematic_registry.get(class_name.lower())
        if class_obj is None:
            raise ValueError(f"Systematic called {class_name} not known")

        systematic = class_obj(name, **config)
        return systematic

    def __call__(self, cosmo, source):
        s = source.copy()
        self.adjust_source(cosmo, s)
        return s

    def adjust_source(self, cosmo, source):
        print(f"Systematics {self.name} is NOT IMPLEMENTED!")

    def update(self, parameters):
        for param in self.params:
            v = parameters[f"{self.name}.{param}"]
            print(f"Updating value: {self.name} = {v} ")
            self.values[param] = v


class CosmologySystematic(Systematic):
    pass

class SourceSystematic(Systematic):
    pass

class OutputSystematic(Systematic):
    pass

