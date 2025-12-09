from sqlalchemy.orm import Session
from app.models.project import Project as ProjectModel

class SQLAlchemyProjectRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, name, description=""):
        proj = ProjectModel(name=name, description=description)
        self.session.add(proj)
        self.session.commit()
        self.session.refresh(proj)
        return proj

    def get_by_name(self, name):
        return self.session.query(ProjectModel).filter_by(name=name).first()

    def delete(self, name):
        proj = self.get_by_name(name)
        if proj:
            self.session.delete(proj)
            self.session.commit()
