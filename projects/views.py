# projects/views.py

from django.db.models import get_model
from django.views.generic import ListView, DetailView, ArchiveIndexView

from projects.settings import PROJECT_MODEL, PROJECT_PAGINATE_BY

project_model = get_model(*PROJECT_MODEL.split('.'))

class ProjectDetailView(DetailView):
    queryset = project_model._default_manager.live()

class ProjectListView(ListView):
    queryset = project_model._default_manager.live()
    context_object_name="project_list",
    paginate_by = PROJECT_PAGINATE_BY
    template = '/projects/project_list.html'

class ProjectSizeAscListView(ProjectListView):
    queryset = project_model._default_manager.live().size_asc()

class ProjectSizeDescListView(ProjectListView):
    queryset = project_model._default_manager.live().size_desc()

class ProjectDateListView(ProjectListView):
    queryset = project_model._default_manager.live()

class ProjectCurrentListView(ProjectListView):
    queryset = project_model._default_manager.live().current()

class ProjectCompletedListView(ProjectListView):
    queryset = project_model._default_manager.live().completed()