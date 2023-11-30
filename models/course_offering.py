import datetime

from constants.constants import StatusConstants


class CourseOffering:
    def __init__(self, course_name, instructor, date, min_employees, max_employees):
        self.course_name = course_name
        self.instructor = instructor
        self.date = datetime.datetime.strptime(date, "%d%m%Y")
        self.min_employees = int(min_employees)
        self.max_employees = int(max_employees)
        self.registrations = []
        self.status = StatusConstants.ACCEPTED

    def is_full(self):
        return len(self.registrations) == self.max_employees

    def is_canceled(self):
        return len(self.registrations) < self.min_employees

    def cancel(self):
        self.status = StatusConstants.COURSE_CANCELED