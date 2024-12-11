"""A database encapsulating collections of near-Earth objects and their close approaches.

A `NEODatabase` holds an interconnected data set of NEOs and their close
approaches. It provides methods to fetch an NEO by primary designation or by
name, as well as a method to query close approaches that match a collection of
user-specified criteria.
"""


class NEODatabase:
    """A database of near-Earth objects and their close approaches.

    A `NEODatabase` contains a collection of NEOs and close approaches. It
    additionally maintains a lookup table to fetch a NEO by its primary
    designation or by its name.
    """
    def __init__(self, neos, approaches):
        """Create a new `NEODatabase`.

        :param neos: A collection of `NearEarthObject`s.
        :param approaches: A collection of `CloseApproach`es.
        """
        self._neos = {neo.designation: neo for neo in neos}
        self._approaches = approaches

        # Link approaches to their respective NEOs
        for approach in self._approaches:
            neo = self._neos.get(approach._designation)
            if neo:
                approach.neo = neo
                neo.approaches.append(approach)

    def get_neo_by_designation(self, designation):
        """Find and return an NEO by its primary designation.

        If no match is found, return `None`.

        :param designation: The primary designation of the NEO to search for.
        :return: The `NearEarthObject` with the desired primary designation, or `None`.
        """
        return self._neos.get(designation)

    def get_neo_by_name(self, name):
        """Find and return an NEO by its name.

        If no match is found, return `None`.

        :param name: The name of the NEO to search for.
        :return: The `NearEarthObject` with the desired name, or `None`.
        """
        for neo in self._neos.values():
            if neo.name == name:
                return neo
        return None

    def query(self, filters=()):
        """Query close approaches to generate those that match a collection of filters.

        This generates a stream of `CloseApproach` objects that match all of the
        provided filters.

        If no arguments are provided, generate all known close approaches.

        :param filters: A collection of filters capturing user-specified criteria.
        :return: A stream of matching `CloseApproach` objects.
        """
        for approach in self._approaches:
            if all(f(approach) for f in filters):
                yield approach
