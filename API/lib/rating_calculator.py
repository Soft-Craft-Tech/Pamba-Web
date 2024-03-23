from collections import Counter


def calculate_ratings(ratings: list, breakdown: bool):
    """
        Calculate the average ratings and breakdown the rating into classes 1-5
        :param ratings: The list of ratings
        :param breakdown: Whether to breakdown ratings
        :return: Average rating, Ratings breakdown
    """
    ratings_list = [rating.rating for rating in ratings]
    rating_score = round(sum(ratings_list) / len(ratings_list))

    if breakdown:
        count = Counter(ratings_list)
        return rating_score, dict(count)
    else:
        return rating_score
