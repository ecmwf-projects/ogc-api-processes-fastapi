# Copyright 2022, European Union.

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License


class OGCProcessesApiError(Exception):
    """Generic API error."""

    pass


class ConflictError(OGCProcessesApiError):
    """Database conflict."""

    pass


class NotFoundError(OGCProcessesApiError):
    """Resource not found."""

    pass


class ForeignKeyError(OGCProcessesApiError):
    """Foreign key error (process does not exist)."""

    pass


class DatabaseError(OGCProcessesApiError):
    """Generic database errors."""

    pass


class InvalidQueryParameter(OGCProcessesApiError):
    """Error for unknown or invalid query parameters.
    Used to capture errors that should respond according to
    http://docs.opengeospatial.org/is/17-069r3/17-069r3.html#query_parameters
    """

    pass
