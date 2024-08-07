from nada_dsl import *
import random
from typing import List, Dict

class MathTool:
    def __init__(self, a: SecretInteger, b: SecretInteger) -> None:
        self.a = a
        self.b = b

    def max(self) -> SecretInteger:
        return (self.a < self.b).if_else(self.b, self.a)

    def min(self) -> SecretInteger:
        return (self.a > self.b).if_else(self.b, self.a)

class ConditionChecker:
    def __init__(self) -> None:
        pass

    def check_location(self, loc1: SecretInteger, loc2: SecretInteger, location_values: Dict[str, Integer]) -> SecretInteger:
        checkLocation: SecretInteger = (loc1 == loc2).if_else(Integer(0), Integer(1))
        if checkLocation == Integer(0):
            return loc1
        else:
            objOfEle: dict = random.choice(list(location_values.items()))
            return objOfEle[1]

    def check_age(self, age1: SecretInteger, age2: SecretInteger) -> SecretInteger:
        tools = MathTool(age1, age2)
        max_val: SecretInteger = tools.max()
        min_val: SecretInteger = tools.min()
        diff: SecretInteger = max_val - min_val
        is_below_5: SecretInteger = (diff < Integer(5)).if_else(Integer(1), Integer(0))
        return is_below_5

    def check_gender(self, lookingfor_gender1: SecretInteger, Actual_gender2: SecretInteger) -> SecretInteger:
        return (lookingfor_gender1 == Actual_gender2).if_else(Integer(1), Integer(0))

    def calculate_points(
        self, 
        isequalLocation: SecretInteger, 
        isSuitableAge: SecretInteger, 
        isOppositeGender: SecretInteger,
        location_int1: SecretInteger
    ) -> Integer:
        total_points: Integer = Integer(0)
        
        total_points += (isequalLocation == location_int1).if_else(Integer(30), Integer(0))
        total_points += (isSuitableAge == Integer(1)).if_else(Integer(20), Integer(0))
        total_points += (isOppositeGender == Integer(1)).if_else(Integer(50), Integer(0))
        
        return total_points

    def calculate_percentage(self, total_points: Integer, max_points: Integer) -> Integer:
        percentage: Integer = (total_points * Integer(100)) / max_points
        return percentage

def nada_main() -> List[Output]:
    Matchparty = Party(name="MatchParty")
    
    # get the location as number values List[num]
    location_int1: SecretInteger = SecretInteger(Input(name="location_int1", party=Matchparty))
    location_int2: SecretInteger = SecretInteger(Input(name="location_int2", party=Matchparty))

    # Get Age from current user and matching user
    age_int1: SecretInteger = SecretInteger(Input(name="age_int1", party=Matchparty))
    age_int2: SecretInteger = SecretInteger(Input(name="age_int2", party=Matchparty))

    # Get looking_for gender and user gender
    looking_for_gender_int: SecretInteger = SecretInteger(Input(name="looking_for_gender_int", party=Matchparty))
    Match_gender_int: SecretInteger = SecretInteger(Input(name="Match_gender_int", party=Matchparty))

    locations: List = [
        "New York", "Los Angeles", "Chicago", "Houston", "Phoenix", 
        "Philadelphia", "San Antonio", "San Diego", "Dallas", "San Jose"
    ]
    
    # Generate the dictionary with random integer values between 0 and 20
    location_values: Dict = {location: Integer(index) for index, location in enumerate(locations)}
    
    condition_checker = ConditionChecker()
    
    isequalLocation: SecretInteger = condition_checker.check_location(location_int1, location_int2, location_values)
    isSuitableAge: SecretInteger = condition_checker.check_age(age_int1, age_int2)
    isOppositeGender: SecretInteger = condition_checker.check_gender(looking_for_gender_int, Match_gender_int)
    
    total_points: Integer = condition_checker.calculate_points(isequalLocation, isSuitableAge, isOppositeGender, location_int1)
    max_points: Integer = Integer(100)
    matching_percentage: Integer = condition_checker.calculate_percentage(total_points, max_points)
    
    return [Output(matching_percentage, "MatchingPercentage", Matchparty)]
