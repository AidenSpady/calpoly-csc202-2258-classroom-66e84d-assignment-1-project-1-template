from typing import *
from dataclasses import dataclass
import unittest
import math
import sys
sys.setrecursionlimit(10**6)

calpoly_email_addresses = ["spady@calpoly.edu"]

pi = math.pi


@dataclass(frozen=True)
class GlobeRect:
    lo_lat : float
    hi_lat : float
    west_long : float
    east_long : float
    
#globe_rect_union : TypeAlias = Union["GlobeRect",None]

@dataclass(frozen=True)
class Region:
    rect : GlobeRect #globe_rect_union
    name : str
    terrain : Union[Literal["ocean"],Literal["mountains"],Literal["forest"],Literal["other"]]
    
#region_union : TypeAlias = Union["Region",None]

@dataclass(frozen=True)
class RegionCondition:
    region : Region #region_union
    year : int
    pop : float #number of people
    ghg_rate : float #tons of CO2 equivalent per year
    



NYC : RegionCondition = RegionCondition(Region(GlobeRect(40,41,-74,-73),"New York City","other"),2025,8478000,92000000)
Tokyo : RegionCondition = RegionCondition(Region(GlobeRect(35,36,139,140),"Tokyo","other"),2025,37000000,59200000)   
Pacific : RegionCondition = RegionCondition(Region(GlobeRect(21,48,164,-133),"Pacific Ocean","ocean"),2025,0,0.0)
Cal_Poly : RegionCondition = RegionCondition(Region(GlobeRect(35.2964,35.309,-120.67,-120.652),"Cal Poly","other"),2025,22000,47114,)

example_region_conditions = [NYC,Tokyo,Pacific,Cal_Poly]

"""accepts a RegionCondition, and computes the tons of CO2-equivalent emitted per person living in the region per year"""
def emissions_per_capita(region : RegionCondition) -> float:
    if(region.pop == 0):
        raise ValueError("Population of given region is 0.")
    else:
        return (region.ghg_rate/ region.pop)

"""accepts a GlobeRect, and returns the area in sqaure kilometers"""
def area(region : GlobeRect) -> float:
    r = 6371
    dist = math.sqrt((region.west_long**2 + region.east_long**2))*111
    return 2*pi*r*math.sqrt((region.hi_lat**2 - region.lo_lat**2))*(dist/360)*(1/1.6)
    
"""accepts a RegionCondition function, and computes the tons of CO2-equivalent per square kilometer for the region"""
def emissions_per_square_km(region : RegionCondition) -> float:
    if(area(region.region.rect) == 0):
        raise ValueError("Area of given region is 0.")
    return (region.ghg_rate/area(region.region.rect))
    
"""accepts a paramater RetionConditions that is a list of type RegionCondition, then returns the name of the RegionCondition with the highest population density"""
def densest(RegionConditions : list[RegionCondition]) -> str:
    densest : RegionCondition = RegionConditions[0]
    densities : list[float] = []
    for i in RegionConditions:
        densities.append(i.pop/area(i.region.rect))
    
    for i in range(len(densities)):
        if (densities[i] > (densest.pop/area(densest.region.rect))):
            densest = RegionConditions[i]
            
    return densest.region.name

"""helper for project_condition that carries out the ocean terrain"""
def project_condition_ocean(region : RegionCondition, years :int) -> RegionCondition:
    rate : float = 0.01
    return RegionCondition(region.region,region.year + years,region.pop*(1+rate)**years,region.ghg_rate*(1+rate)**years)

"""helper for project_condition that carries out the mountains terrain"""
def project_condition_mountains(region : RegionCondition, years :int) -> RegionCondition:
    rate : float = 0.05
    return RegionCondition(region.region,region.year + years,region.pop*(1+rate)**years,region.ghg_rate*(1+rate)**years)

"""helper for project_condition that carries out the forest terrain"""
def project_condition_forest(region : RegionCondition, years :int) -> RegionCondition:
    rate : float = -0.001
    return RegionCondition(region.region,region.year + years,region.pop*(1+rate)**years,region.ghg_rate*(1+rate)**years)

"""helper for project_condition that carries out the other terrain"""
def project_condition_other(region : RegionCondition, years :int) -> RegionCondition:
    rate : float = 0.003
    return RegionCondition(region.region,region.year + years,region.pop*(1+rate)**years,region.ghg_rate*(1+rate)**years)

    
"""accepts the paramaters region of type RegionCondition and a years of type int, then returns a new RegionCondition with an applied population and emissions exponential growth rate"""
#exponential growth rate function = P(t) = p(1+r)^t
def project_condition(region : RegionCondition, years : int) -> RegionCondition:
    if(region.region.terrain == "ocean"):
       return project_condition_ocean(region,years)
   
    elif(region.region.terrain == "mountains"):
        return project_condition_mountains(region,years)
    
    elif(region.region.terrain == "forest"):
        return project_condition_forest(region,years)
    
    else:
        return project_condition_other(region,years)
    
    

# put all test cases in the "Tests" class.
class Tests(unittest.TestCase):
    def test_example_1(self):
        self.assertEqual(14,14)
    
    def test_EPC(self):
        self.assertAlmostEqual(10.85,emissions_per_capita(NYC),delta=0.01)
        self.assertAlmostEqual(1.6,emissions_per_capita(Tokyo),delta=0.01)
    
    def test_area(self):
        self.assertAlmostEqual(60,area(GlobeRect(40,41,40,41)),delta=0.01)
        self.assertAlmostEqual(520000000,area(GlobeRect(-90,90,-180,180)),delta=.01)
        
        
        
        
    def test_densest(self):
        densest_test_list_1 : list[RegionCondition] = [Tokyo,NYC,Pacific,Cal_Poly]
        densest_test_list_2 : list[RegionCondition] = [Cal_Poly,NYC]
        
        self.assertEqual("New York City", densest(densest_test_list_1))
        self.assertEqual("New York City", densest(densest_test_list_2))
    
    
    def test_project_condition_ocean(self):
        Atlantic = RegionCondition(Region(GlobeRect(1,1,1,1),"Atlantic","ocean"),2025,5,4)
        
        self.assertAlmostEqual(project_condition_ocean(Pacific,5).pop,0,delta=.01)
        self.assertAlmostEqual(project_condition_ocean(Pacific,5).ghg_rate,0,delta=.01)
        self.assertAlmostEqual(project_condition_ocean(Pacific,5).year,2030,delta=.01)
        
        self.assertAlmostEqual(project_condition_ocean(Atlantic,7).pop,5.360677,delta=.01)
        self.assertAlmostEqual(project_condition_ocean(Atlantic,7).ghg_rate,4.2885,delta=.01)
        self.assertAlmostEqual(project_condition_ocean(Atlantic,7).year,2032,delta=.01)
        
    def test_project_condition_mountains(self):
        Everest = RegionCondition(Region(GlobeRect(1,1,1,1),"Everest","mountains"),2025,800,2)
        
        K2 = RegionCondition(Region(GlobeRect(1,1,1,1),"K2","mountains"),2025,250,2)
        
        self.assertAlmostEqual(project_condition_mountains(Everest,20).pop,2122.6382,delta=.01)
        self.assertAlmostEqual(project_condition_mountains(Everest,20).ghg_rate,5.3065,delta=.01)
        self.assertAlmostEqual(project_condition_mountains(Everest,20).year,2045,delta=.01)
        
        self.assertAlmostEqual(project_condition_mountains(K2,10).pop,407.22366,delta=.01)
        self.assertAlmostEqual(project_condition_mountains(K2,10).ghg_rate,3.25779,delta=.01)
        self.assertAlmostEqual(project_condition_mountains(K2,10).year,2035,delta=.01)
        
    def test_project_condition_forest(self):
        Amazon = RegionCondition(Region(GlobeRect(1,1,1,1),"Amazon","forest"),2025,4000,0)
        
        Congo_Basin = RegionCondition(Region(GlobeRect(1,1,1,1),"Congo Basin","forest"),2025,950,7)
        
        self.assertAlmostEqual(project_condition_mountains(Amazon,30).pop,17287.7695,delta=.01)
        self.assertAlmostEqual(project_condition_mountains(Amazon,30).ghg_rate,0,delta=.01)
        self.assertAlmostEqual(project_condition_mountains(Amazon,30).year,2055,delta=.01)
        
        self.assertAlmostEqual(project_condition_mountains(Congo_Basin,16).pop,2073.7309,delta=.01)
        self.assertAlmostEqual(project_condition_mountains(Congo_Basin,16).ghg_rate,15.280122,delta=.01)
        self.assertAlmostEqual(project_condition_mountains(Congo_Basin,16).year,2041,delta=.01)
        
            
    def test_project_condition_other(self):
        self.assertAlmostEqual(project_condition_other(NYC,5).pop,8605935.3125,delta=.01)
        self.assertAlmostEqual(project_condition_other(NYC,5).ghg_rate,93388304.877,delta=.01)
        self.assertAlmostEqual(project_condition_other(NYC,5).year,2030,delta=.01)
        
        self.assertAlmostEqual(project_condition_other(Tokyo,7).pop,37784028.0701,delta=.01)
        self.assertAlmostEqual(project_condition_other(Tokyo,7).ghg_rate,60454444.9121,delta=.01)
        self.assertAlmostEqual(project_condition_other(Tokyo,7).year,2032,delta=.01)
        
    
        

if (__name__ == '__main__'):
    unittest.main()
