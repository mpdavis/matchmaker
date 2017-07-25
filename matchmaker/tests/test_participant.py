
from ..participant import Participant

import pytest

class TestParticipant(object):
    
    def test_matches(self):
        
        # given
        seller = Participant(type='seller', id='id', geography_ids=[1, 2, 3], industry_ids=[4, 5, 6])
        
        buyer_exact = Participant(type='buyer', id='id_exact', geography_ids=[1, 2, 3], industry_ids=[4, 5, 6])
        buyer_nonmatching = Participant(type='buyer', id='id_nonmatching', geography_ids=[1, 4, 5], industry_ids=[])
        buyer_barely_matched = Participant(type='buyer', id='id_barely_matched', geography_ids=[1], industry_ids=[4])
        
        # when
        seller.match([buyer_exact, buyer_nonmatching, buyer_barely_matched])

        # then
        assert seller.matches == {buyer_exact: 6, buyer_barely_matched: -2}
    
    def test_matches_ranked(self):
        
        # given
        seller = Participant(type='seller', id='id_test', geography_ids=[1, 2, 3, 4], industry_ids=[4, 5, 6])
        
        buyer_exact = Participant(type='buyer', id='id_exact', geography_ids=[1, 2, 3], industry_ids=[4, 5, 6])
        buyer_nonmatching = Participant(type='buyer', id='id_nonmatching', geography_ids=[1, 4, 5], industry_ids=[])
        buyer_barely_matched = Participant(type='buyer', id='id_barely_matched', geography_ids=[1], industry_ids=[4])
        
        # when
        seller.match([buyer_exact, buyer_nonmatching, buyer_barely_matched])

        # then
        assert seller.get_matches_ranked() == [buyer_exact, buyer_barely_matched]
