
from django import template
from myapp.models import Review
import math
register = template.Library()


@register.simple_tag
def discount_calculation(price,discount):
    if discount == None or discount == 0:
        return price
    sellprice = price
    sellprice = price - (price * discount/100)
    return math.floor(sellprice)

@register.filter
def rupee(price):
    return f'₹{price}'

@register.filter
def calculate_average_rating(i):
    # Get all ratings for the specific course
    ratings = i.review_set.values_list('rating', flat=True)
    
    # Calculate the average rating
    average_rating = sum(ratings) / len(ratings) if ratings else 0
    
    return round(average_rating,2)

@register.filter
def calculate_average_rating_percentage(i):
    # Get all ratings for the specific course
    ratings = i.review_set.values_list('rating', flat=True)
    
    # Calculate the average rating
    average_rating = sum(ratings) / len(ratings) if ratings else 0
    # print("in stars is ...........",average_rating)
    
    # Convert average rating to percentage and round to integer
    average_rating_percentage = round((average_rating / 5) * 100)
    
    return round(average_rating_percentage,2)

@register.simple_tag
def calculate_percentage(i):
    # Get all ratings for the specific course
   
    rating_percentage = round((i / 5) * 100)
    
    return round(rating_percentage,2)

