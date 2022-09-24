from enum import IntEnum

class AlexState(IntEnum):
    """ Possible Alex Exo States"""
    Init = 0       
    InitSitting   = 1 
    LeftForward   = 2
    RightForward  = 3 
    Standing      = 4
    Sitting       = 5  
    SittingDown   = 6  
    StandingUp    = 7
    StepFirstL    = 8
    StepFirstR    = 9   
    StepLastL     = 10
    StepLastR     = 11
    StepL         = 12        
    StepR         = 13
    BackStepR     = 14
    BackStepL     = 15
    Error         = 16
    @staticmethod
    def isStationaryState(state):
        return state in [AlexState.Error, AlexState.Init, AlexState.LeftForward,\
            AlexState.RightForward, AlexState.Standing, AlexState.Sitting]
    



class Intent(IntEnum):
    NORMALWALK = 0
    FTTG = 10
    BKSTEP = 9
    SITDOWN = 1
