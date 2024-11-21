from pydantic import BaseModel


# Use BaseModel instead of BaseModelWithExactAttributes since the stash plugin configuration may not be an exact match
class StashPluginConfig(BaseModel):
    dry_run_enabled: bool = False
    allow_rename_across_drives: bool = False
