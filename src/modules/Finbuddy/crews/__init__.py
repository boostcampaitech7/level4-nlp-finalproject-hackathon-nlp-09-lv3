
from .table_crew import TableCrew
from .image_crew import ImageCrew
from .context_crew import ContextCrew
from .final_crew import FinalCrew
def get_table_crew():
    return TableCrew().table_crew()

def get_image_crew():
    return ImageCrew().image_crew()

def get_context_crew():
    return ContextCrew().context_crew()

def get_final_crew():
    return FinalCrew().final_crew()