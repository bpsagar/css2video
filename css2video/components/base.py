import copy


class BaseComponent(object):
    """A base component for other CSS components

    Public attributes:
        - Dict: Dictionary form of the component
    """

    def __init__(self, Dict):
        super(BaseComponent, self).__init__()
        self.Dict = Dict

    @classmethod
    def from_dict(cls, Dict):
        """Creates a component from dictionary"""
        return cls(Dict=Dict)

    def to_dict(self):
        """Returns the dictionary form of the component"""
        return self.Dict

    def duplicate(self):
        """Returns a duplicate of this component"""
        return self.__class__(Dict=copy.deepcopy(self.Dict))
