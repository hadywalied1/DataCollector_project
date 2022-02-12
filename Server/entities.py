class Base :
    def __init__(self, id, name) -> None:
        self.id = id
        self.name = name
        
class HandPowerData(Base):
    def __init__(self, right, left, leg):
        self.right = right
        self.left = left
        self.leg = leg
        
class HearingData(Base): 
    def __init__(self):
        pass
    
class WeightAndHeightData(Base) : 
    def __init__(self) -> None:
        pass
    
class HandStabilityData(Base) : 
    def __init__(self) -> None:
        pass
    
class DepthData(Base) : 
    def __init__(self) -> None:
        pass
    
class EffortMeasureData(Base) : 
    def __init__(self) -> None:
        pass
        
class ArmsData(Base) : 
    def __init__(self) -> None:
        pass
    
