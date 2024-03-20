from API.models import Business
import re


def clean_string(string):
    """
        Removes unwanted characters from the string. Only retains: letters, numbers, spaces and hyphens
        Replace all spaces with hyphens
        :param string:
        :return: str
    """
    pattern = r'[^a-zA-Z0-9\s-]'

    # Use re.sub() to replace matched characters with the replacement character
    new_string = re.sub(pattern, "", string)

    return new_string.strip().replace(" ", "-").lower()


def slugify(business_name):
    """
        Takes the business name to create a unique slug from
        :param business_name:
        :return: Slugified business name
    """
    slug = clean_string(business_name)
    same_business = Business.query.filter_by(slug=slug).first()

    if not same_business:
        return slug

    all_businesses = Business.query.all()
    number_of_businesses = len(all_businesses)
    slug = f"{slug}-{number_of_businesses}"
    return slug

