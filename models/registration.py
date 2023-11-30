from constants.constants import StatusConstants


class Registration:
    def __init__(self, email, course_offering_id):
        self.email = email
        self.course_offering_id = course_offering_id
        self.status = StatusConstants.ACCEPTED