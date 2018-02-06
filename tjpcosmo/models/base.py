"""
All theory models must be subclasses of this Model superclass.


"""
import pathlib
import warnings
from ..theory_results import TheoryResults



model_registry = {}

class BasePredictor:
    def __init__(self, config, metadata):
        self.config = config
        self.metadata = metadata

class BaseModel:
    predictor_class = None
    theory_results_class = None
    data_class = None
    metadata_class = None


    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        name = cls.name if hasattr(cls, 'name') else cls.__name__
        name = name.lower()
        print(f"Register {name}")
        model_registry[name] = cls


    """
    This is the superclass for all Models, which represent the part of the
    likelihood function that generate mean theory predictions from parameters.

    This is just the skeleton - there are various more complete designs in the sandbox.
    Delete this notice after implementing them!

    """

    def __init__(self, config, data_info, likelihood_class):
        """
        Instantiate the model from a dictionary of options.

        Subclasses usually override this to do their own instantiation.
        They should call this parent method first.
        """
        self.config=config
        self.data = self.data_class.load(data_info)
        self.metadata = self.extract_metadata(data_info)
        self.predictor = self.predictor_class(config, self.metadata)
        self.likelihood = likelihood_class(self.data)

    @staticmethod
    def from_name(name):
        return model_registry[name]

    def extract_metadata(self, data_info):
        pass

    def run(self, parameters):
        theory_results = self.predictor.run(parameters)
        like = self.likelihood.run(theory_results)
        return like, theory_results

    def likelihood(self, parameters):
        return self.run[0]



