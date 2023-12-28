from django.db.models import Max


def annotate_current_price(listings):
    listings = listings.annotate(current_price=Max('bids__amount'))
    for listing in listings:
        if listing.current_price is None:
            listing.current_price = listing.starting_bid
    return listings
