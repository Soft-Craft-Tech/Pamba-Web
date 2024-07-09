from datetime import timedelta, datetime, date, time
from API.models import Staff, Appointment, Service
from werkzeug.utils import secure_filename
import secrets
import os
from PIL import Image
import cloudinary
import cloudinary.uploader

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}


def allowed_file(filename):
    """
        Checks id file uploaded of an allowed filetype
        :param filename:
        :return: Boolean
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def save_response_image(image):
    """
        Takes in an image, renames the image and saves the image to directory
    :param image: Image
    :return: Saved image name
    """
    random_hex = secrets.token_hex(7)
    filename = secure_filename(image.filename)
    _, f_ext = os.path.splitext(filename)
    image_filename = random_hex + f_ext
    if not os.path.exists("./clients"):
        os.mkdir("./clients")
    picture_path = os.path.join('clients', image_filename)
    # Resize image with pillow
    image = Image.open(image)
    resized_image = image.resize((400, 350))
    resized_image.save(picture_path)

    # Handle Cloudinary upload
    cloudinary.config(
        cloud_name=os.getenv("CLOUDINARY_NAME"),
        api_key=os.getenv("CLOUDINARY_API_KEY"),
        api_secret=os.getenv("CLOUDINARY_API_SECRET"),  # Click 'View Credentials' below to copy your API secret
        secure=True,
        asset_folder="pamba-web"
    )

    upload_result = cloudinary.uploader.upload(picture_path)
    image_url = upload_result.get("secure_url")

    os.remove(picture_path)
    return image_url


def add_decimal_hours_to_time(base_time: time, decimal_hours: float) -> time:
    """
        Add time give hours in decimals
        :param base_time: Initial time
        :param decimal_hours: Hour to be added
        :return: New Time
    """
    # Convert decimal hours to hours and minutes
    hours: int = int(decimal_hours)
    minutes: int = int((decimal_hours - hours) * 60)

    # Create a timedelta object with the calculated hours and minutes
    time_delta: timedelta = timedelta(hours=hours, minutes=minutes)

    # Add the timedelta to the base time
    new_time: time = (datetime.combine(date.today(), base_time) + time_delta).time()

    return new_time


def check_staff_availability(staff: Staff, service: Service, appointment_date: date, appointment_time: time) -> bool:
    """
        Check if a certain staff member is available for an appointment.
        :param staff: Staff object.
        :param service: Service being Booked.
        :param appointment_date: Appointment Date.
        :param appointment_time: Time of the appointment.
        :return:
    """
    overlap: bool = False

    # Check if the staff is booked at the selected time slot
    current_date: date = datetime.now().date()
    upcoming_staffs_appointments: list = staff.appointments \
        .filter(Appointment.date >= current_date, ~Appointment.cancelled).all()
    for appointment in upcoming_staffs_appointments:
        if appointment.date == appointment_date:  # Rethink this part #025
            appointment_duration: float = appointment.service.estimated_service_time
            appointment_start: datetime = datetime.combine(appointment.date, appointment.time)
            appointment_end: datetime = appointment_start + timedelta(minutes=int(float(appointment_duration) * 60))

            new_appointment_duration: float = service.estimated_service_time
            new_appointment_start: datetime = datetime.combine(appointment_date, appointment_time)
            new_appointment_end: datetime = new_appointment_start + timedelta(minutes=int(float(new_appointment_duration) * 60))

            # Check overlapping appointments
            overlap = (new_appointment_start < appointment_end) and (new_appointment_end > appointment_start)

            # Check if the start and end times of the old interval fall within the new interval
            overlap |= (appointment_start >= new_appointment_start and appointment_end <= new_appointment_end)

            # Check if the start time of the new interval falls within the old interval's time range
            overlap |= (appointment_start <= new_appointment_start < appointment_end)
            if overlap:
                break
    return overlap

