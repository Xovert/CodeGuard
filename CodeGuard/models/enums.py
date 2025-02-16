import enum 

class CourseStatus(enum.Enum):
    DRAFT = "Draft"
    PUBLISHED = "Published"
    ARCHIVED = "Archived"

class CompletionStatus(enum.Enum):
    NOT_STARTED = "Not_Started"
    STARTED = "Started"
    COMPLETE = "Complete"

    @property
    def next_status(self):
        return {
            self.NOT_STARTED: self.STARTED,
            self.STARTED: self.COMPLETE,
            self.COMPLETE: self.COMPLETE,
        }[self]

class Severity(enum.Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"
    ERROR = "ERROR"

    @classmethod
    def from_str(cls, value):
        if value == "":
            return cls.ERROR
     
        mapping = {
            "INFO": cls.LOW,   
            "WARNING": cls.MEDIUM, 
            "ERROR": cls.HIGH      
        }
        if value in mapping:
            return mapping[value]

        try:
            return cls(value)
        except ValueError:
            raise ValueError(f"Invalid severity value: {value}")