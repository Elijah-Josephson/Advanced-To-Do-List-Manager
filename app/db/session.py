from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('postgresql+psycopg://todo_user:todo_pass@localhost:5432/todolist_db')
Session = sessionmaker(bind = engine)