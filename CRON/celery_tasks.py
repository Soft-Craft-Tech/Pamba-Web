import json
import logging

from API import db, celery
from API.models import FailedNotification
from API.lib.send_mail import (
    appointment_confirmation_email,
    send_ask_for_review_mail
)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

@celery.task
def resend_failed_notifications():
    """
    Celery task to resend failed notifications.
    """
    failed_notifications = FailedNotification.query.filter(
        FailedNotification.retry_count < FailedNotification.max_retries
    ).all()
    
    results = {'attempted': len(failed_notifications), 'success': 0, 'failed': 0}
    logger.info(f"Starting resend task: {results['attempted']} notifications to process")

    for notification in failed_notifications:
        try:
            params = json.loads(notification.message_params)
            logger.info(f"Processing notification {notification.id} of type '{notification.notification_type}' to {notification.recipient}")

            success = False

            if notification.notification_type == 'appointment_confirmation':
                success = appointment_confirmation_email(
                    params['client_name'],
                    params['date'],
                    params['time'],
                    params['business_name'],
                    params['business_address'],
                    params['latitude'],
                    params['longitude'],
                    params['place_id'],
                    notification.recipient
                )
            elif notification.notification_type == 'ask_for_review':
                success = send_ask_for_review_mail(
                    params['url'],
                    params['name'],
                    params['business_name'],
                    notification.recipient
                )

            if success:
                db.session.delete(notification)
                results['success'] += 1
                logger.info(f"Notification {notification.id} sent successfully and deleted.")
            else:
                notification.retry_count += 1
                results['failed'] += 1
                logger.warning(f"Notification {notification.id} failed to send. Retry count increased to {notification.retry_count}.")

        except Exception as e:
            notification.retry_count += 1
            notification.error_message = str(e)
            results['failed'] += 1
            logger.warning(
                f"Notification {notification.id} failed to send. "
                f"Retry count increased to {notification.retry_count}. "
                f"Error: {str(e)}"
                )   

        db.session.commit()

    logger.info(f"Resend task completed: {results}")
    return results
