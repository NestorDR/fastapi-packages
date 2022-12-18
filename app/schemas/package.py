# -*- coding: utf-8 -*-

# --- Third Party Libraries ---
# pydantic: library which provides data validation and settings management using Python type hinting.
from pydantic import BaseModel


# Create Models
# The use of Pydantic allows defines request payload models and response models in Python Class object notation.
# Having models variants for the same entity helps to fit the required data context.

# Response models
class Package(BaseModel):
    id: int
    name: str
    version: str
    status: str


# Request payload models
class PackageCreate(BaseModel):
    name: str
    version: str


class PackageUpdate(PackageCreate):
    status_id: int
