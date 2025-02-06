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

