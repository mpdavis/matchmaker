
from .participant import Participant

class Matcher(object):
    """
    Base class for matching participants to each other.
    
    `get_matches` can be overridden to easily provide different logic for
    ranking matches.
    
    By default, buyers are ranked by the total number of commonalities they
    share with the seller, given that they share at least one geography_id and
    industry_id.
    """
    
    sellers = set()
    buyers = set()
    
    def __init__(self, data):
        self._validate_data(data)
        self._parse_participants()
    
    def _validate_data(self, data):
        # TODO: Check the format of the data. For now we just check there is
        # something there.
        assert data
        self.data = data
        
    def _parse_participants(self):
        
        for item in self.data:
            
            if item.get('type') == 'seller':
                self.sellers.add(Participant(item))
            
            elif item.get('type') == 'buyer':
                self.buyers.add(Participant(item))
    
    def get_matches(self):
        for seller in self.sellers:
            seller.match(self.buyers)
        
        return self.sellers


class SellerToBuyerIndustryMatcher(Matcher):
    """
    Matches sellers to buyers, focusing on industry-based matches.
    
    Buyers are ranked by the total number of common industries they share with
    the seller, given that they share at least one geography_id and industry_id.
    
    The buyer with the best domain knowledge of the company being sold has the
    best chance of successfully moving forward with the company.
    """
    
    def get_matches(self):
        for seller in self.sellers:
            seller.match(self.buyers, geography_weight=0, industry_weight=1)
        
        return self.sellers


class SellerToBuyerGeographyMatcher(Matcher):
    """
    Matches sellers to buyers, focusing on geography-based matches.
    
    Buyers are ranked by the total number of common geography ids they share
    with the seller, given that they share at least one geography_id and industry_id.
    
    The buyer with the best local knowledge of the company being sold has the
    best chance of successfully moving forward with the company.
    """
    
    def get_matches(self):
        for seller in self.sellers:
            seller.match(self.buyers, geography_weight=1, industry_weight=0)
        
        return self.sellers
