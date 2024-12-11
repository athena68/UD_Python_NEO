"""Represent models for near-Earth objects and their close approaches.

The `NearEarthObject` class represents a near-Earth object. Each has a unique
primary designation, an optional unique name, an optional diameter, and a flag
for whether the object is potentially hazardous.

The `CloseApproach` class represents a close approach to Earth by an NEO. Each
has an approach datetime, a nominal approach distance, and a relative approach
velocity.

A `NearEarthObject` maintains a collection of its close approaches, and a
`CloseApproach` maintains a reference to its NEO.

The functions that construct these objects use information extracted from the
data files from NASA, so these objects should be able to handle all of the
quirks of the data set, such as missing names and unknown diameters.

You'll edit this file in Task 1.
"""
from helpers import cd_to_datetime, datetime_to_str


class NearEarthObject:
    """A near-Earth object (NEO).

    An NEO encapsulates semantic and physical parameters about the object, such
    as its primary designation (required, unique), IAU name (optional), diameter
    in kilometers (optional - sometimes unknown), and whether it's marked as
    potentially hazardous to Earth.

    A `NearEarthObject` also maintains a collection of its close approaches -
    initialized to an empty collection, but eventually populated in the
    `NEODatabase` constructor.
    """
    def __init__(self, **info):
        """Create a new `NearEarthObject`.

        :param info: A dictionary of excess keyword arguments supplied to the constructor.
        """
        self.designation = info.get('designation', '')
        self.name = info.get('name') or None
        self.diameter = float(info.get('diameter')) if info.get('diameter') else float('nan')
        self.hazardous = info.get('hazardous', 'N').lower() == 'y'

        # Create an empty initial collection of linked approaches.
        self.approaches = []

    @property
    def fullname(self):
        """Return a representation of the full name of this NEO."""
        return f"{self.designation} ({self.name})" if self.name else self.designation

    def __str__(self):
        """Return `str(self)`."""
        hazardous = 'is' if self.hazardous else 'is not'
        return f"A NearEarthObject {self.fullname} with a diameter of {self.diameter:.3f} km and {hazardous} potentially hazardous."

    def __repr__(self):
        """Return `repr(self)`, a computer-readable string representation of this object."""
        return f"NearEarthObject(designation={self.designation!r}, name={self.name!r}, " \
               f"diameter={self.diameter:.3f}, hazardous={self.hazardous!r})"


class CloseApproach:
    """A close approach to Earth by an NEO.

    A `CloseApproach` encapsulates information about the NEO's close approach to
    Earth, such as the date and time (in UTC) of closest approach, the nominal
    approach distance in astronomical units, and the relative approach velocity
    in kilometers per second.

    A `CloseApproach` also maintains a reference to its `NearEarthObject` -
    initially, this information (the NEO's primary designation) is saved in a
    private attribute, but the referenced NEO is eventually replaced in the
    `NEODatabase` constructor.
    """
    def __init__(self, **info):
        """Create a new `CloseApproach`.

        :param info: A dictionary of excess keyword arguments supplied to the constructor.
        """
        self._designation = info.get('designation', '')
        self.time = cd_to_datetime(info.get('time'))
        self.distance = float(info.get('distance', 0.0))
        self.velocity = float(info.get('velocity', 0.0))

        # Create an attribute for the referenced NEO, originally None.
        self.neo = None

    @property
    def time_str(self):
        """Return a formatted representation of this `CloseApproach`'s approach time."""
        return datetime_to_str(self.time)

    def __str__(self):
        """Return `str(self)`."""
        return (f"A CloseApproach at {self.time_str}, "
                f"with a distance of {self.distance:.2f} AU "
                f"and a velocity of {self.velocity:.2f} km/s, "
                f"by NEO {self.neo.fullname if self.neo else 'unknown'}.")

    def __repr__(self):
        """Return `repr(self)`, a computer-readable string representation of this object."""
        return f"CloseApproach(time={self.time_str!r}, distance={self.distance:.2f}, " \
               f"velocity={self.velocity:.2f}, neo={self.neo!r})"