# Import all the models, so that Base has them before being
# imported by Alembic
from ..db.database import Base  # noqa
from app.models import user,post  # noqa