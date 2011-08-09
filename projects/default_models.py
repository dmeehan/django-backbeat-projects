# projects/default_models.py

"""

        Default models for the project app.
        Not loaded by syncdb unless specified in settings.
    
"""

from projects.models import ProjectBase, PhysicalProjectBase

class Project(ProjectBase):
    pass

class PhysicalProject(PhysicalProjectBase):
    pass