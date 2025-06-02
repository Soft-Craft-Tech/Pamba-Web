from typing import Union, Optional, Any
from sqlalchemy.exc import SQLAlchemyError

from API.models import Appointment, Service, Staff, Client, Business
from flask import Blueprint, request, jsonify
from API.lib.auth import (
    client_login_required,
    business_login_required,
    verify_api_key,
    business_verification_required)
from API.lib.data_serializer import serialize_appointment, serialize_client
from API.lib.sendSMS import send_sms
from API.lib.utils import check_staff_availability
from API import db, bcrypt
from datetime import datetime, timedelta, time, date
from API.lib.SMS_messages import reschedule_appointment_composer, new_appointment_notification_message, \
    appointment_remainder_message
from API.lib.checkBusinessClosed import check_business_closed
from API.lib.send_mail import appointment_confirmation_email, send_ask_for_review_mail

appointment_blueprint = Blueprint("appointments", __name__, url_prefix="/API/appointments")


@appointment_blueprint.route("/book", methods=["POST"])
@client_login_required
def book_appointment(client):
    """
        Book Appointment from the mobile application
        :param client: Logged in client
        :return: 200, 403, 404
    """
    try:
        payload: dict = request.get_json()

        appointment_date: date = datetime.strptime(payload.get("date"), '%d-%m-%Y')
        appointment_time: time = datetime.strptime(payload.get("time"), '%H:%M').time()
        comment: str = payload.get("comment", "").strip()
        service_id: int = payload.get("service")
        staff_id: int = payload.get("staff", "")

        if not service_id:
            return jsonify({"message": "Service ID is required."}), 400

        service: Service = Service.query.filter_by(id=service_id).first()
        if not service:
            return jsonify({"message": "Service not found"}), 404

        if not client.verified:
            return jsonify({"message": "Please, verify your account."}), 403

        if staff_id:
            staff: Staff = Staff.query.get(staff_id)
            if not staff:
                return jsonify({"message": "Staff you booked with doesn't exist"}), 404
            overlap: bool = check_staff_availability(
                staff=staff,
                appointment_date=appointment_date,
                appointment_time=appointment_time,
                service=service
            )
            if overlap:
                return jsonify({
                    "message": "The Staff you selected is already booked at this time."
                }), 400

        business: Business = service.business

        open_status = check_business_closed(appointment_time, appointment_date, business)
        if not open_status:
            return jsonify({"message": "Our premises are not open at the picked time and day"}), 400

        new_appointment: Appointment = Appointment(
            date=appointment_date,
            time=appointment_time,
            comment=comment,
            business_id=business.id,
            client_id=client.id,
            staff_id=staff_id if staff_id else None,
            service_id=service.id
        )

        # Avoid Booking multiple appointments scheduled at the same time
        appointment: Appointment = Appointment.query\
            .filter_by(date=appointment_date, time=appointment_time, client_id=client.id, cancelled=False).first()
        if appointment:
            return jsonify({"message": "You have another appointment scheduled at this time."}), 400

        db.session.add(new_appointment)
        db.session.commit()
        try:
            appointment_confirmation_email(
            client_name=client.name.split()[0],
            date=appointment_date,
            time=appointment_time,
            business_name=business.business_name,
            business_address=business.formatted_address,
            latitude=business.latitude,
            longitude=business.longitude,
            place_id=business.place_id,
            recipient=client.email
            )
        except Exception as e:
            print(f"[ERROR] Email sending failed: {e}")
            return jsonify({"message": "Booking Successful but we encountered an error sending the appointment details to your email. Please check again later",
            "appointment": serialize_appointment(appointment)
            }), 200

        appointment_message = new_appointment_notification_message(
            name=client.name.split()[0],
            time_=appointment_time.strftime("%H:%M"),
            date_=appointment_date.strftime("%d-%B-%Y"),
            service=service.service,
            business=business.business_name
        )
        try:
            send_sms(client.phone, appointment_message)
            return jsonify({
                "message": "Booking Successful",
                "appointment": serialize_appointment(appointment)
                }), 200
        except Exception as e:
            return jsonify({"message": "Booking Successful but we encountered an error sending the appointment SMS"})

    except KeyError as e:
        return jsonify({"message": f"Missing required field: {str(e)}"}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"An unexpected error occurred. Please try again later. {str(e)}"}), 400


@appointment_blueprint.route("/book/web-appointments", methods=["POST"])
@verify_api_key
def book_appointment_on_web():
    """
    Book appointment from the web without Auth
    :return: 201, 400, 404, 500
    """
    try:
        payload = request.get_json()

        try:
            appointment_date: date = datetime.strptime(payload["date"], '%d-%m-%Y').date()
            appointment_time: time = datetime.strptime(payload["time"], '%H:%M').time()
        except (ValueError, KeyError):
            return jsonify({"message": "Invalid or missing Time/Date format"}), 400

        comment: str = payload.get("comment", "").strip()
        business_id: int = payload.get("business")
        service_id: int = payload.get("service")
        staff_id: int = payload.get("staff", "")
        email: str = payload.get("email", "").strip().lower()
        phone: str = payload.get("phone", "").strip()
        name: str = payload.get("name", "").strip().title()
        notification_mode: str = payload.get("notification", "").lower()

        if not (business_id and service_id and email and phone and name and notification_mode):
            return jsonify({"message": "Missing required fields"}), 400

        today_date: date = datetime.today().date()
        current_time: time = datetime.today().time()

        if appointment_date < today_date:
            return jsonify({"message": "Can't book an appointment for a past date"}), 400
        if appointment_date == today_date and appointment_time < current_time:
            return jsonify({"message": "You can't book an appointment for a past time"}), 400

        service: Service = Service.query.get(service_id)
        if not service:
            return jsonify({"message": "The service you are booking is unavailable"}), 404

        business: Business = Business.query.get(business_id)
        if not business:
            return jsonify({"message": "Business not found"}), 404

        open_status = check_business_closed(appointment_time, appointment_date, business)
        if not open_status:
            return jsonify({"message": "Our premises are not open at the selected time and day"}), 400

        if staff_id:
            staff: Staff = Staff.query.get(staff_id)
            if not staff:
                return jsonify({"message": "Staff you booked with doesn't exist"}), 404
            overlap: bool = check_staff_availability(
                staff=staff,
                appointment_date=appointment_date,
                appointment_time=appointment_time,
                service=service
            )
            if overlap:
                return jsonify({
                    "message": "The Staff you selected is already booked at this time. "
                               "Please book with a different staff or let us assign you someone"
                }), 400

        # Database operations (client creation and appointment booking)
        try:
            client: Client = Client.query.filter_by(email=email).first()
            if not client:
                client = Client(
                    email=email,
                    phone=phone,
                    name=name
                )
                db.session.add(client)
                db.session.commit()

            appointment: Appointment = Appointment(
                date=appointment_date,
                time=appointment_time,
                comment=comment,
                notification_mode=notification_mode,
                business_id=business.id,
                staff_id=staff_id if staff_id else None,
                client_id=client.id,
                service_id=service.id
            )
            db.session.add(appointment)
            db.session.commit()

        except SQLAlchemyError as db_err:
            db.session.rollback()
            return jsonify({"message": "A database error occurred", "error": str(db_err)}), 500

        try:
            appointment_confirmation_email(
                client_name=client.name.split()[0],
                date=appointment_date,
                time=appointment_time,
                business_name=business.business_name,
                business_address=business.formatted_address,
                latitude=business.latitude,
                longitude=business.longitude,
                place_id=business.place_id,
                recipient=client.email
            )

            notification_message: str = new_appointment_notification_message(
                name=name.split()[0] if name else None,
                time_=appointment_time,
                date_=appointment_date,
                service=service.service,
                business=business.business_name
            )
            send_sms(phone=phone, message=notification_message)

        except Exception as notify_err:
            return jsonify({
                "message": "Appointment booked but notification sending failed",
                "error": str(notify_err)
            }), 200

        return jsonify({"message": "Appointment Booked Successfully"}), 201

    except Exception as e:
        return jsonify({"message": "Failed to book appointment due to unexpected error", "error": str(e)}), 400


@appointment_blueprint.route("/reschedule/<int:appointment_id>", methods=["PUT"])
@client_login_required
def reschedule_appointment(client, appointment_id):
    """
        Client reschedule appointment.
        :param client: Client
        :param appointment_id: ID of appointment being rescheduled
        :return: 200
    """
    try:
        payload: Any = request.get_json()
        appointment_date: datetime = datetime.strptime(payload["date"], '%d-%m-%Y')
        appointment_time: time = datetime.strptime(payload["time"], '%H:%M').time()
        notification_method: str = payload.get("notification", "")
        comment: str = payload.get("comment", "")
        staff_id: Union[str, int] = payload.get("staff_id", "")
        staff: Optional[Staff] = None

        appointment: Appointment = Appointment.query.get(appointment_id)

        if staff_id != "":
            staff = Staff.query.get(staff_id)
            if not staff:
                return jsonify({"message": "This staff doesn't exist"}), 404

        if not appointment:
            return jsonify({"message": "Appointment doesn't exist"}), 404

        if appointment.client_id != client.id:
            return jsonify({"message": "Not allowed"}), 403

        if appointment.completed:
            return jsonify({"message": "Appointment already completed."}), 400

        # Avoid Booking multiple appointments scheduled at the same time
        appointments_booked_same_time: Appointment = Appointment.query \
            .filter_by(date=appointment_date, time=appointment_time, client_id=client.id, cancelled=False).first()
        if appointments_booked_same_time:
            return jsonify({"message": "You have another appointment scheduled at this time."}), 400

        appointment.time = appointment_time
        appointment.date = appointment_date
        appointment.staff_id = staff.id if staff else appointment.staff_id
        appointment.comment = comment if comment != "" else appointment.comment
        appointment.notification_mode = notification_method if notification_method != "" else appointment.notification_mode
        db.session.commit()

        client: Client = appointment.client
        message: str = reschedule_appointment_composer(
            name=client.name.split()[0],
            time_=appointment_time,
            date_=appointment_date.strftime("%d-%b-%Y"),
            service=appointment.service.service,
            business=appointment.business.business_name
        )
        try:
            send_sms(appointment.client.phone, message)
            return jsonify({"message": "Appointment has been rescheduled"}), 200
        except Exception as e:
            print(f"[ERROR] Failed to send SMS: {e}")
            return jsonify({"message": "Appointment has been rescheduled, but failed to send notification SMS"}), 200
    except Exception:
        return jsonify ({"message": "Failed to reschedule due to an unexpected issue"}), 400


@appointment_blueprint.route("/cancel/<int:appointment_id>", methods=["PUT"])
@client_login_required
def cancel_appointment(client, appointment_id):
    """
        Cancel appointment
        :param client: Logged in client
        :param appointment_id: ID of the appointment being cancelled
        :return: 200, 401
    """
    try:
        payload = request.get_json()
        comment = payload["comment"]
        appointment = Appointment.query.get(appointment_id)

        if not appointment:
            return jsonify({"message": "Appointment not Found"}), 404

        if appointment.client_id != client.id:
            return jsonify({"message": "Not allowed"}), 403

        if appointment.completed:
            return jsonify({"message": "Appointment already completed."}), 400

        appointment.cancelled = True
        if comment:
            appointment.comment = comment
        db.session.commit()

        return jsonify({"message": "Cancellation Successful"}), 200
    except Exception:
        return jsonify({"message":"Failed to cancel appointment due to an unexpected issue"}), 400


@appointment_blueprint.route("/my-appointments", methods=["GET"])
@client_login_required
def my_appointments(client):
    """
        Fetch the client's appointments: Last appointment, upcoming
        :param client:
        :return:
    """
    appointments: list = Appointment.query.filter_by(client_id=client.id).order_by(Appointment.date.desc()).all()
    cancelled_appointments: list = []
    upcoming_appointments: list = []
    previous_appointments: list = []
    today: date = datetime.today().date()

    if not appointments:
        return jsonify({"message": "No appointments"}), 404

    for appointment in appointments:
        serialized_appointment = serialize_appointment(appointment)
        serialized_appointment["imgUrl"] = appointment.business.profile_img
        serialized_appointment["phone"] = appointment.business.phone
        serialized_appointment["name"] = appointment.business.business_name
        serialized_appointment["description"] = appointment.business.formatted_address
        serialized_appointment["placeId"] = appointment.business.place_id
        serialized_appointment["directions"] = f"https://www.google.com/maps/dir/?api=1&destination={appointment.business.latitude},{appointment.business.longitude}&place_id={appointment.business.place_id}"
        if appointment.cancelled:
            cancelled_appointments.append(serialized_appointment)
        if appointment.completed or today > appointment.date and not appointment.cancelled:
            previous_appointments.append(serialized_appointment)

        if not appointment.cancelled and not appointment.completed and today < appointment.date:
            upcoming_appointments.append(serialized_appointment)

    return jsonify(
        {
            "message": "Success",
            "cancelled": cancelled_appointments,
            "upcoming": upcoming_appointments,
            "previous": previous_appointments
        }
    ), 200


@appointment_blueprint.route("/assign-appointment/<int:appointment_id>", methods=["PUT"])
@business_login_required
@business_verification_required
def assign_appointment(business, appointment_id):
    """
        Assign an appointment to a member of staff to handle
        :param business: Logged-in business/owner
        :param appointment_id: Appointment being assigned
        :return: 404, 401, 400, 200
    """
    try:
        payload = request.get_json()
        staff_id = payload["staffID"]
        password = payload["password"]

        appointment = Appointment.query.get(appointment_id)
        if not appointment:
            return jsonify({"message": "Not Found"}), 404

        if not bcrypt.check_password_hash(business.password, password):
            return jsonify({"message": "Incorrect Password"}), 401

        if appointment.business_id != business.id:
            return jsonify({"message": "Not allowed"}), 403

        if appointment.cancelled:
            return jsonify({"message": "This appointment was cancelled"}), 400

        staff = Staff.query.get(staff_id)
        if not staff:
            return jsonify({"message": "Staff not found"}), 404

        if staff.employer_id != business.id:
            return jsonify({"message": "Not allowed"}), 403

        appointment.staff_id = staff.id
        return jsonify({"message": "Successful", "appointment": serialize_appointment(appointment)}), 200
    except Exception:
        return jsonify({"message": "Failed to assign appointment due to an unexpected issue"})


@appointment_blueprint.route("/business-appointments", methods=["GET"])
@business_login_required
@business_verification_required
def fetch_business_appointments(business):
    """
        Fetch all appointments booked with the logged-in business. Exc: Cancelled and Completed
        :param business: Logged-in
        :return: 200
    """
    today: datetime = datetime.today()
    appointments: list = business.appointments \
        .order_by(Appointment.date.desc(), Appointment.time.desc()) \
        .filter(~Appointment.cancelled).all()

    all_appointments: list = []

    for appointment in appointments:
        combined_datetime: datetime = datetime.combine(appointment.date, appointment.time)
        appointment_duration: int = int(float(appointment.service.estimated_service_time) * 60)
        appointment_ends: datetime = combined_datetime + timedelta(minutes=appointment_duration)
        staff: str = ""

        if appointment.staff:
            staff = appointment.staff.f_name

        serialized_appointment = serialize_appointment(appointment)
        serialized_appointment["start"] = combined_datetime.strftime("%Y-%m-%d %H:%M")
        serialized_appointment["end"] = appointment_ends.strftime("%Y-%m-%d %H:%M")
        serialized_appointment["people"] = [appointment.client.name]
        serialized_appointment["title"] = f"{appointment.service.service} by {staff if staff else 'Unassigned'}"
        serialized_appointment["calendarId"] = "past" if appointment_ends < today else "upcoming"
        all_appointments.append(serialized_appointment)

    return jsonify({"appointments": all_appointments}), 200


@appointment_blueprint.route("/end_appointment/<int:appointment_id>", methods=["PUT"])
@business_login_required
@business_verification_required
def end_appointment(business, appointment_id):
    """
        End Appointment when completed
        Trigger a notification for appointment Review.
        :param business: Logged in Business.
        :param appointment_id: ID of appointment being ended
        :return: 200, 400.
    """
    try:
        today = datetime.today()
        appointment = Appointment.query.get(appointment_id)

        if appointment.business_id != business.id:
            return jsonify({"message": "Not Allowed"}), 400

        # Can't end completed Appointment.
        if appointment.completed:
            return jsonify({"message": "Appointment already completed"}), 400

        # Can't end future appointment.
        if appointment.date > today.date() or (appointment.date == today.date() and appointment.time > today.time()):
            return jsonify({"message": "You can't end a future appointment"}), 400

        appointment.completed = True
        db.session.commit()

        try:
            send_ask_for_review_mail(
                url=f"https://www.pamba.africa/reviews/new/{appointment.id}",
                business_name=business.business_name,
                name=appointment.client.name,
                recipient=appointment.client.email
            )
            return jsonify({
                "message": "Appointment Ended. Review request sent.",
                "appointment": serialize_appointment(appointment)
            }), 200

        except Exception as e:
            print(f"[ERROR] Failed to send review email: {e}")
            return jsonify({
                "message": "Appointment ended but we encountered an error sending the review request email.",
                "appointment": serialize_appointment(appointment)
            }), 200

    except Exception:
        return jsonify({"message":"Failed to end appointment due to an unexpected issue"}), 400


@appointment_blueprint.route("/<int:appointment_id>", methods=["GET"])
def fetch_single_appointment(appointment_id):
    """
        Fetch single appointment
        :param appointment_id:
        :return:
    """
    appointment = Appointment.query.get(appointment_id)

    if not appointment:
        return jsonify({"message": "Not found"}), 404

    return jsonify({"appointment": serialize_appointment(appointment)}), 200


@appointment_blueprint.route("/send_reminder", methods=["GET"])
@verify_api_key
def send_appointment_reminder():
    """
        Send reminder for upcoming appointments
        Reminder can be sent via SMS or whatsapp
        :return:
    """
    try:
        today: date = datetime.today().date()
        appointments: list = Appointment.query.filter(
            Appointment.date == today,
            ~Appointment.cancelled,
            ~Appointment.completed
        ).all()

        unsent_reminders: int = 0

        for appointment in appointments:
            client: Client = appointment.client
            message: str = appointment_remainder_message(
                business=appointment.business.business_name,
                date_=appointment.date,
                time_=appointment.time.strftime("%H:%M"),
                name=client.name.split()[0],
                service=appointment.service.service
            )

            try:
                response = send_sms(phone=client.phone, message=message)
                if response.status_code != 200:
                    unsent_reminders += 1
            except Exception as e:
                print(f"[ERROR] Failed to send SMS for appointment ID {appointment.id}: {e}")
                unsent_reminders += 1

        return jsonify({
            "message": "Reminders processed",
            "total_appointments": len(appointments),
            "unsuccessful": unsent_reminders
        }), 200

    except Exception as e:
        print(f"[FATAL ERROR] Reminder job failed: {e}")
        return jsonify({"message": "Failed to process reminders due to an unexpected error"}), 200
