from shellmancer import db
from collections import namedtuple, defaultdict
from shellmancer.models import SinglePlayerCampaign

class PrimaryAttribute:
    """
    
    """

class Construct:
    """
    Base Class for all Constructs, which are institutions, people, places, and circumstance with
    a similar approach to measurement and adjustment making.
    """
    PrimaryAttributes = ('meat', 'leet', 'street')
    AttributeThresholds = namedtuple("AttributeThresholds", *PrimaryAttributes)
    AttributeBottleNecks = namedtuple("AttributeBottleNecks", *PrimaryAttributes)
    SkillSynergy = defaultdict(list)

    def __init__(self, attrs: str, ):
        pass
