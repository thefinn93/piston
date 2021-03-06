"""
This file is part of Piston.

Piston is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Piston is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Piston.  If not, see <http://www.gnu.org/licenses/>.
"""


from piston.exceptions import PistonException


class ConfigurationException(PistonException):
    """A given configuration file is invalid."""
    pass


class ConfigurationMissingKeysException(ConfigurationException):
    """The provided config is missing required keys."""

    pass


class InsecureRedirectException(ConfigurationException):
    """The provided redirect URL is not over https."""

    pass
