from pydantic import BaseModel, Field
from typing import Dict, List

class ModuleStructure(BaseModel):
    module: str = Field(..., alias="module", description="The name of the module")
    description: str = Field(..., alias="Description", description="Detailed description")
    submodules: Dict[str, str] = Field(..., alias="Submodules", description="Key-value pair of submodule name and description")

class ExtractionResult(BaseModel):
    hierarchy: List[ModuleStructure]