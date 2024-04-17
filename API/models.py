from API import db
from datetime import datetime


# Junction table for many-to-many relationship between Service and appointment
businesses_clients_association = db.Table(
    'businesses_clients_association',
    db.Column('business_id', db.Integer, db.ForeignKey('businesses.id')),
    db.Column('client_id', db.Integer, db.ForeignKey('clients.id'))
)


# Business services Junction Table
class ServicesBusinessesAssociation(db.Model):
    """
        Junction Table
    """
    __tablename__ = "services_businesses_association"

    id = db.Column(db.Integer, primary_key=True)
    business_id = db.Column(db.Integer, db.ForeignKey('businesses.id'))
    service_id = db.Column(db.Integer, db.ForeignKey('services.id'))
    price = db.Column(db.Integer)


class Business(db.Model):
    """Businesses/Service providers table"""
    __tablename__ = "businesses"

    id = db.Column(db.Integer, primary_key=True)
    business_name = db.Column(db.String(50), nullable=False)
    category = db.Column(db.String(15), nullable=False)
    slug = db.Column(db.String(100), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    phone = db.Column(db.String(15), nullable=False, unique=True)
    city = db.Column(db.String(30), nullable=False)
    location = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text, nullable=True)
    password = db.Column(db.String(250), nullable=False)
    google_map = db.Column(db.String(300), nullable=True)
    active = db.Column(db.Boolean, default=False)
    verified = db.Column(db.Boolean, default=False)
    join_date = db.Column(db.DateTime, default=datetime.utcnow)
    updated_on = db.Column(db.DateTime)
    # profile Image link with cloudinary.
    profile_img = db.Column(db.String, nullable=True)
    services = db.relationship("Service", secondary='services_businesses_association',  backref="businesses",
                               lazy="dynamic"
                               )
    inventory = db.relationship("Inventory", backref="business", lazy="dynamic", cascade='all, delete-orphan')
    expense_accounts = db.relationship("ExpenseAccount", backref="business", lazy="dynamic", cascade='all, '
                                                                                                     'delete-orphan')
    notifications = db.relationship("BusinessNotification", backref="business", lazy="dynamic", cascade='all, '
                                                                                                        'delete-orphan')
    staff = db.relationship("Staff", backref="business", lazy="dynamic", cascade="all, delete-orphan")
    sales = db.relationship("Sale", backref="business", lazy="dynamic", cascade="all, delete-orphan")
    appointments = db.relationship("Appointment", backref="business", lazy="dynamic", cascade="all, delete-orphan")
    clients = db.relationship('Client', secondary='businesses_clients_association', backref='service_providers')

    def __repr__(self):
        return f"Business({self.business_name}, {self.slug})"


class Service(db.Model):
    """Services offered by the business"""
    __tablename__ = "services"

    id = db.Column(db.Integer, primary_key=True)
    service = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    sales = db.relationship("Sale", backref="service", lazy="dynamic")
    appointments = db.relationship("Appointment", backref="service", lazy="dynamic")

    def __str__(self):
        return f"Services({self.service})"


class Sale(db.Model):
    """Business Sales"""
    __tablename__ = "sales"

    id = db.Column(db.Integer, primary_key=True)
    payment_method = db.Column(db.String(30), nullable=False)
    description = db.Column(db.Text, nullable=True)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    business_id = db.Column(db.Integer, db.ForeignKey("businesses.id"))
    service_id = db.Column(db.Integer, db.ForeignKey("services.id", ondelete='SET NULL'))

    def __repr__(self):
        return f"Sales({self.date_created}, {self.payment_method})"


class ExpenseAccount(db.Model):
    """Business Expense accounts"""
    __tablename__ = "expenseaccounts"

    id = db.Column(db.Integer, primary_key=True)
    account_name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text)
    business_id = db.Column(db.Integer, db.ForeignKey("businesses.id"))
    expense = db.relationship("Expense", backref="account", lazy="dynamic")

    def __repr__(self):
        return f"ExpenseAccount({self.account_name})"


class Expense(db.Model):
    """Businesses Expenses"""
    __tablename__ = "expenses"

    id = db.Column(db.Integer, primary_key=True)
    expense = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    modified_at = db.Column(db.DateTime)
    expense_account = db.Column(db.Integer, db.ForeignKey("expenseaccounts.id", ondelete='SET NULL'))

    def __repr__(self):
        return f"Expense({self.expense})"


class BusinessNotification(db.Model):
    """Notifications sent to the businesses"""
    __tablename__ = "business_notifications"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    message = db.Column(db.Text, nullable=False)
    read = db.Column(db.Boolean, default=False)
    sent_at = db.Column(db.DateTime, default=datetime.utcnow)
    business_id = db.Column(db.Integer, db.ForeignKey("businesses.id"))

    def __repr__(self):
        return f"Notification({self.title})"


class Staff(db.Model):
    """Staff members"""
    __tablename__ = "staff"

    id = db.Column(db.Integer, primary_key=True)
    f_name = db.Column(db.String(20), nullable=False)
    l_name = db.Column(db.String(20), nullable=False)
    phone = db.Column(db.String(15), nullable=False, unique=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    role = db.Column(db.String(20), nullable=False)
    public_id = db.Column(db.String(15), nullable=False, unique=True)
    employer_id = db.Column(db.Integer, db.ForeignKey("businesses.id"))

    def __repr__(self):
        return f"Staff({self.f_name}, {self.l_name})"


class Inventory(db.Model):
    """Business Inventory"""
    __tablename__ = "inventory"

    id = db.Column(db.Integer, primary_key=True)
    product = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(20), nullable=False, default="Normal")
    updated_at = db.Column(db.DateTime)
    business_id = db.Column(db.Integer, db.ForeignKey("businesses.id"))

    def __repr__(self):
        return f"Inventory({self.product}, {self.status})"


class Rating(db.Model):
    """Business Ratings"""
    __tablename__ = "ratings"

    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)
    rated_at = db.Column(db.DateTime, default=datetime.utcnow)
    business_id = db.Column(db.Integer, db.ForeignKey("businesses.id"))

    def __repr__(self):
        return f"Rating({self.rating})"


# ------------------------------------------------------------- CLIENTS ---------------------------------------------


class Client(db.Model):
    """Clients table"""
    __tablename__ = "clients"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    phone = db.Column(db.String(15), nullable=False, unique=True)
    password = db.Column(db.String(300), nullable=False)
    verified = db.Column(db.Boolean, default=False)
    queued_for_deletion = db.Column(db.Boolean, default=False)
    otp = db.Column(db.String(200), nullable=True)
    otp_expiration = db.Column(db.DateTime, nullable=True)
    join_date = db.Column(db.DateTime, default=datetime.utcnow)
    notifications = db.relationship("ClientNotification", backref="client", lazy="dynamic", cascade="all, "
                                                                                                    "delete-orphan")
    reviews = db.relationship("Review", backref="client", lazy="dynamic", cascade="all, delete-orphan")
    appointments = db.relationship("Appointment", backref="client", lazy="dynamic")

    def __repr__(self):
        return f"Client({self.name}, {self.phone})"


class ClientNotification(db.Model):
    """Notifications sent to Clients"""
    __tablename__ = "clientsnotitications"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    message = db.Column(db.Text, nullable=False)
    sent_at = db.Column(db.DateTime, default=datetime.utcnow)
    client_id = db.Column(db.Integer, db.ForeignKey("clients.id"))

    def __repr__(self):
        return f"Notification({self.title})"


class ClientDeleted(db.Model):
    """
        Clients deleted or queued for deletion
    """
    __tablename__ = "clientsdeleted"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50))
    phone = db.Column(db.String(20))
    delete_reason = db.Column(db.Text)
    request_date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"ClientDeleted({self.email}, {self.phone})"


# ----------------------------------------------- SHARED --------------------------------------------


class Review(db.Model):
    """Customer Reviews"""
    __tablename__ = "reviews"

    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.Text, nullable=True)
    reviewed_at = db.Column(db.DateTime, default=datetime.utcnow)
    client_id = db.Column(db.Integer, db.ForeignKey("clients.id"))
    business_id = db.Column(db.Integer, db.ForeignKey("businesses.id"))

    def __repr__(self):
        return f"Review({self.message})"


class Appointment(db.Model):
    """Appointments table"""
    __tablename__ = "appointments"

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    completed = db.Column(db.Boolean, default=False)
    cancelled = db.Column(db.Boolean, default=False)
    comment = db.Column(db.Text, nullable=True)
    create_at = db.Column(db.DateTime, default=datetime.utcnow)
    business_id = db.Column(db.Integer, db.ForeignKey("businesses.id"))
    staff_id = db.Column(db.Integer, db.ForeignKey("staff.id", ondelete='SET NULL'))
    client_id = db.Column(db.Integer, db.ForeignKey("clients.id", ondelete='SET NULL'))
    service_id = db.Column(db.Integer, db.ForeignKey("services.id", ondelete='SET NULL'))

    def __repr__(self):
        return f"Appointment({self.date}, {self.time}, {self.comment})"
