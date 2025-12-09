from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('postgresql://postgres:secret@localhost/alembic_db')
Session = sessionmaker(bind = engine)