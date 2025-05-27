import logging
from API.models import Service, ExpenseAccount
from API import db
from sqlalchemy.orm import joinedload

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def update_profile_completion(business):
    """
    Check and update the profile completion status of a business.
    :param business: Business object
    :return: None
    """
    try:
        business = db.session.merge(business) 
        services = Service.query.options(joinedload(Service.business)).filter_by(business_id=business.id).all()
        accounts = business.expense_accounts.options(joinedload(ExpenseAccount.business)).all()
        
        if (
            bool(business.profile_img) and
            bool(business.description) and
            len(services) > 0 and
            len(accounts) > 0 and
            bool(business.weekday_opening) and
            bool(business.weekday_closing) and
            bool(business.weekend_opening) and
            bool(business.weekend_closing)
        ):
            business.profile_completed = True
        else:
            business.profile_completed = False        
        db.session.commit() 
    except Exception as e:
        logger.error(f"Failed to update profile completion for business ID: {business.id}. Error: {str(e)}")
        db.session.rollback()