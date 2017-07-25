
from ..file_loader import load_file
from ..matcher import Matcher
from ..matcher import SellerToBuyerGeographyMatcher
from ..matcher import SellerToBuyerIndustryMatcher

import pytest


@pytest.fixture
def data():
    return load_file("./data/sample_data.json")

class TestMatcher(object):
    
    def test_default_matcher(self, data):
        
        matcher = Matcher(data)
        
        for seller in matcher.get_matches():
            weight = -1
            for match in seller.get_matches_ranked():
                match_weight = seller.weigh_match(match)
                if weight == -1:
                    weight = match_weight
                else:
                    assert match_weight <= weight
                    weight = match_weight
    
    def test_geography_matcher(self, data):
        
        matcher = SellerToBuyerGeographyMatcher(data)
        
        for seller in matcher.get_matches():
            weight = -1
            for match in seller.get_matches_ranked():
                match_weight = seller.weigh_match(match)
                if weight == -1:
                    weight = match_weight
                else:
                    assert match_weight <= weight
                    weight = match_weight
    
    def test_industry_matcher(self, data):
        
        matcher = SellerToBuyerIndustryMatcher(data)
        
        for seller in matcher.get_matches():
            weight = -1
            for match in seller.get_matches_ranked():
                match_weight = seller.weigh_match(match)
                if weight == -1:
                    weight = match_weight
                else:
                    assert match_weight <= weight
                    weight = match_weight
