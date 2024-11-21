from typing import Annotated

from pydantic import BaseModel, ConfigDict, StringConstraints

# Helper type for non-empty strings
NonEmptyString = Annotated[str, StringConstraints(strict=True, min_length=1)]


# Helper Base Model for types parsed from the Stash API (GraphQL)
class BaseModelWithExactAttributes(BaseModel):
    model_config = ConfigDict(extra="forbid")
