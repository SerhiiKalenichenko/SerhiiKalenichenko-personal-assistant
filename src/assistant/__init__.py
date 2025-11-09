from .models import Contact, Note
from .validators import validate_email, validate_phone
from .storage import JSONStore
from .contacts import AddressBook
from .notes import NotesRepo
from .tags import TagIndex
from .birthdays import next_birthdays
from .cli import main as cli
