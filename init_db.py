from sqlalchemy import create_engine
from app.models import Base
from app.settings import settings


engine = create_engine(settings.get_database_url(), echo=True)

Base.metadata.create_all(engine)

