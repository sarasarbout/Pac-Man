from typing import Any
import json

class ParsingError(Exception):
    """Custom exception for configuration parsing errors."""

    ...

def is_int(value: Any) -> bool:
    pass

class ConfigParser:
    def read_file(self, path_file: str) -> str:
        try:
            with open(path_file, "r") as f:
                content = f.read()
            if not content:
                raise ParsingError("file is empty")
            return content
        except FileNotFoundError:
            print(f"{path_file} doesn't exist!")

    def strip_comments(self, content: str) -> str:
        cleaned_content = ""
        lines = content.split("\n")
        for line in lines:
            cleaned_line = line.split("#", 1)[0].strip()
            if cleaned_line == "":
                continue
            cleaned_content += cleaned_line
        return cleaned_content

    def parse_json(self, text: str) -> dict[str, Any]:
        return json.loads(text)

    def check_keys(self, data: dict[str, Any]) -> None:
        pass

    def check_values(self, key: str, value: Any) -> bool:
        pass

    def check_level(self, index: int, raw: Any) -> dict[str, Any]:
        pass


    def default_level(self, index: int) -> dict[str, Any]:
        pass


    def normalize_levels(self, levels: list[dict[str, Any]]) -> list[dict[str, Any]]:
        pass


    def build_default(self) -> dict[str, Any]:
        pass

    def parse(self, path_file: str) -> dict[str, Any]:
        pass
    #the pipeline




    
    
        
    



