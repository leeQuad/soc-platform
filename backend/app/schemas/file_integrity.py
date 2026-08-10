from pydantic import BaseModel


class FileIntegrityResult(BaseModel):
    new_files: list[str]
    changed_files: list[str]
    deleted_files: list[str]