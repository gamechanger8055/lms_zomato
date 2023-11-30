from constants.constants import StatusConstants
from models.course_offering import CourseOffering
from models.registration import Registration
from datetime import datetime


class LMSService:
    def __init__(self):
        self.course_offerings = {}
        self.registrations = {}

    def add_course_offering(self, course_name, instructor, date, min_employees, max_employees):
        # date=datetime.strptime(date,"%d%m%Y")
        course_offering_id = f"OFFERING-{course_name}-{instructor}"
        course_offering = CourseOffering(course_name, instructor, date, min_employees, max_employees)
        self.course_offerings[course_offering_id]=course_offering
        return course_offering_id

    def register_for_course(self, email, course_offering_id):
        existing_registration = False
        for reg in self.registrations:
            if self.registrations[reg].email == email and self.registrations[reg].course_offering_id == course_offering_id:
                existing_registration = True
        if existing_registration:
            return None, StatusConstants.INPUT_DATA_ERROR
        course_offering = self.course_offerings[course_offering_id]
        if not course_offering or course_offering.status == StatusConstants.COURSE_CANCELED:
            return None, StatusConstants.COURSE_NOT_FOUND_ERROR
        reg = course_offering.registrations
        if course_offering.is_full():
            return None, StatusConstants.COURSE_FULL_ERROR
        registration = Registration(email, course_offering_id)
        reg.append(registration)
        course_offering.registrations = reg
        if len(course_offering.registrations) >= course_offering.min_employees:
            course_offering.status = StatusConstants.ACTIVE
        email_name = email.split("@")[0]
        course_teacher = course_offering_id.split("-")[1]
        reg = f"REG-COURSE-{email_name}-{course_teacher}"
        self.registrations[reg]=registration
        return reg, StatusConstants.ACCEPTED

    def cancel_registration(self, registration_id):

        registration = self.registrations[registration_id]
        if not registration:
            return registration_id, StatusConstants.REGISTRATION_NOT_FOUND_ERROR
        reg=registration_id.split("-")
        course_offering=None
        for course in self.course_offerings:
            course_class=self.course_offerings[course]
            if course_class.course_name==reg[3]:
                course_offering=course_class
        if any(self.course_offerings[co].status == StatusConstants.CONFIRMED for co in self.course_offerings):
            return registration_id, StatusConstants.CANCEL_REJECTED
        if not course_offering:
            return registration_id,StatusConstants.COURSE_NOT_FOUND_ERROR
        course_reg=course_offering.registrations
        course_reg.remove(registration)
        course_offering.registrations=course_reg
        del self.registrations[registration_id]

        return registration_id, StatusConstants.CANCEL_ACCEPTED

    def allot_course(self, course_offering_id):
        course_offering = self.course_offerings[course_offering_id]

        if not course_offering or course_offering.status == StatusConstants.COURSE_CANCELED:
            return course_offering_id, StatusConstants.COURSE_NOT_FOUND_ERROR

        registrations = course_offering.registrations

        if len(registrations) < course_offering.min_employees:
            course_offering.cancel()

        sorted_registrations = sorted(registrations, key=lambda x: x.email)
        status = StatusConstants.CONFIRMED if course_offering.status == StatusConstants.ACTIVE else StatusConstants.COURSE_CANCELED
        course_offering.status=status
        result = []
        for registrations in sorted_registrations:
            email_name = registrations.email.split("@")[0]
            course_desc = course_offering_id.split("-")
            course_teacher = course_desc[2]
            course_name = course_desc[1]
            course_date = course_offering.date.strftime("%d%m%Y")
            reg = f"REG-COURSE-{email_name}-{course_name} {registrations.email} {course_offering_id} {course_name} {course_teacher} {course_date}"
            result.append(reg)

        return result, status
