"""Provide filters for querying close approaches and limit the number of results.

The `create_filters` function generates a collection of filters from user-specified
criteria. The `limit` function truncates the stream of results to a fixed number.
"""

def create_filters(
    date=None, start_date=None, end_date=None,
    distance_min=None, distance_max=None,
    velocity_min=None, velocity_max=None,
    diameter_min=None, diameter_max=None,
    hazardous=None
):
    """Create a collection of filters from user-specified criteria.

    Each argument corresponds to a filter for a specific attribute of a close
    approach or its associated near-Earth object.

    :param date: A specific date on which a close approach occurs.
    :param start_date: The earliest date on which a close approach can occur.
    :param end_date: The latest date on which a close approach can occur.
    :param distance_min: The minimum nominal approach distance in astronomical units.
    :param distance_max: The maximum nominal approach distance in astronomical units.
    :param velocity_min: The minimum relative approach velocity in kilometers per second.
    :param velocity_max: The maximum relative approach velocity in kilometers per second.
    :param diameter_min: The minimum diameter of the NEO in kilometers.
    :param diameter_max: The maximum diameter of the NEO in kilometers.
    :param hazardous: Whether the NEO is potentially hazardous.

    :return: A collection of filters to be applied to a query of close approaches.
    """
    filters = []

    if date:
        filters.append(lambda ca: ca.time.date() == date)
    if start_date:
        filters.append(lambda ca: ca.time.date() >= start_date)
    if end_date:
        filters.append(lambda ca: ca.time.date() <= end_date)
    if distance_min:
        filters.append(lambda ca: ca.distance >= distance_min)
    if distance_max:
        filters.append(lambda ca: ca.distance <= distance_max)
    if velocity_min:
        filters.append(lambda ca: ca.velocity >= velocity_min)
    if velocity_max:
        filters.append(lambda ca: ca.velocity <= velocity_max)
    if diameter_min:
        filters.append(lambda ca: ca.neo and ca.neo.diameter >= diameter_min)
    if diameter_max:
        filters.append(lambda ca: ca.neo and ca.neo.diameter <= diameter_max)
    if hazardous is not None:
        filters.append(lambda ca: ca.neo and ca.neo.hazardous == hazardous)

    return filters


def limit(iterator, n=None):
    """Produce a limited number of values from an iterator.

    :param iterator: An iterator of values.
    :param n: The maximum number of values to produce. If `None`, produce all values.
    :return: An iterator limited to the first `n` values.
    """
    if n is None or n <= 0:
        yield from iterator
    else:
        for i, item in enumerate(iterator):
            if i >= n:
                break
            yield item
