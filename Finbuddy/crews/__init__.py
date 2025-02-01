
from .table_crew import TableCrew
from .image_crew import ImageCrew
from .context_crew import ContextCrew

def get_table_crew():
    return TableCrew().table_crew()

def get_image_crew():
    return ImageCrew().image_crew()

def get_context_crew():
    return ContextCrew().context_crew()