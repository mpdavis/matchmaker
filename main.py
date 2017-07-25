
from matchmaker.file_loader import load_file

from matchmaker.matcher import Matcher
from matchmaker.matcher import SellerToBuyerGeographyMatcher
from matchmaker.matcher import SellerToBuyerIndustryMatcher

def main():
    """
    Main entry point for the application.
    """
    
    data = load_file("./data/sample_data.json")
    
    matcher = Matcher(data)
    
    for seller in matcher.get_matches():
        seller.print_matches()


if __name__ == "__main__":
    main()
