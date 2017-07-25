

class Participant(object):
    """
    Participant represents an entity in the matching system.
    
    A Participant isn't strictly concerned with whether it is a seller or a
    buyer, but only how it matches and ranks other participants. This would
    allow for matching for more than just the purpose of selling a business.
    For example, we could match sellers by geography_ids for the purpose of
    networking events.
    """

    geography_weight = 1
    industry_weight = 1
    
    def __init__(self, item=None, geography_weight=None, industry_weight=None, *args, **kwargs):
        
        if item == None:
            item = {}
        
        self.matches = {}
        
        self.type = item.get('type', kwargs.get('type'))
        self._id = item.get('id', kwargs.get('id'))
        
        details = item.get('details', {})
        self.geography_ids = set(details.get('geography_ids', kwargs.get('geography_ids')))
        self.industry_ids = set(details.get('industry_ids', kwargs.get('industry_ids')))
        
        if geography_weight:
            self.geography_weight = geography_weight
        
        if industry_weight:
            self.industry_weight = industry_weight

    def __str__(self):
        return "[type=%s id=%s geography_ids=%s industry_ids=%s]" % (self.type, self._id, self.geography_ids, self.industry_ids)
    
    def __repr__(self):
        return self._id
    
    def match(self, possible_matches, geography_weight=None, industry_weight=None):
        """
        Match the participant to a set of possible other participants.
        
        Each match is weighted based on the geography_weight and industry_weight.
        
        The formula for the final weight of a match is:
        
            ((number of geography_id matches - geography_id misses) * geography_weight) + ((number of industry_id matches - industry_id misses) * industry_weight)
        
        Each id match between the buyer and the seller counts for one point.
        Each id that the seller has that the buyer is missing is docked one
        point. That total is then weighted individually by the type of id to
        allow for biases toward industry or geography. 
        
        The default weight for both properties is `1`, which gives equal
        consideration to each property. If we want to weigh one property greater
        than the other, it is trvial to increase the weight for that property
        equal to the ratio we want the final weight to be. Increasing one weight
        to `2` will weigh it twice as much. Increasing it to `10` will weight it
        ten times as much.
        
        Decreasing a weight to `0` will ignore it in rankings, but at least one
        match on each property is still required.
        """
        
        if geography_weight:
            self.geography_weight = geography_weight
        
        if industry_weight:
            self.industry_weight = industry_weight
        
        for possible_match in possible_matches:
            
            # Always check for at least one geography_id match
            if self.geography_ids.isdisjoint(possible_match.geography_ids):
                continue
            
            # Always check for at least one industry_id match
            if self.industry_ids.isdisjoint(possible_match.industry_ids):
                continue
            
            self.matches[possible_match] = self.weigh_match(possible_match)
    
    def get_matches_ranked(self):
        """
        Get all of the matches for the current participant, ranked by their
        weight.
        """
        return sorted(self.matches, key=self.matches.get, reverse=True)
        
    def print_matches(self):
        """
        Helper for printing the participant, and an indented list of all of it's
        matches.
        """
        print('')
        print(self)
        for match in self.get_matches_ranked():
            print("\t%s: %s" % (self.weigh_match(match), match))
            
    def weigh_match(self, match):
        """
        Weigh a single match with the current weights.
        """
        return self._weigh_geography(match) + self._weigh_industry(match)
        
    def _weigh_geography(self, match):
        matches = len(self.geography_ids.intersection(match.geography_ids))
        misses = len(self.geography_ids.symmetric_difference(match.geography_ids))
        base_weight = matches - misses
        return base_weight * self.geography_weight
    
    def _weigh_industry(self, match):
        matches = len(self.geography_ids.intersection(match.geography_ids))
        misses = len(self.geography_ids.symmetric_difference(match.geography_ids))
        base_weight = matches - misses
        return base_weight * self.industry_weight
