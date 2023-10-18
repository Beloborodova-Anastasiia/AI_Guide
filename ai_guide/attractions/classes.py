class AttractionInfo:
    def __init__(self, object_name: str, location: str, content: str) -> None:
        self.object_name = object_name
        self.location = location
        self.content = content
    
    def __str__(self) -> str:
        return f'{self.object_name}, {self.location}'