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


class PistonException(Exception):

    status_code = 500

    def __init__(self, message=None, errors=[]):
        super(PistonException, self).__init__(message)
        self.message = message
        self.errors = errors

    def __str__(self):
        return self.message

    def __dict__(self):
        return {
            "success": False,
            "type": type(self).__name__,
            "message": self.message
        }
