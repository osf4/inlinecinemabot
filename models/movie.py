from dataclasses import dataclass


@dataclass(kw_only = True)
class Movie:
    title: str
    preview_url: str

    duration: str
    format: str
    sessions: str
    
    description: str