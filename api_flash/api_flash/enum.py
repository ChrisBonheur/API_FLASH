from enum import Enum

class type_user(Enum):
    DOYEN = 1
    AGENT = 2
    ENSEIGNANT = 3
    ETUDIANT = 4


class state_article(Enum):
    INIT = 1
    PARRUTION = 2
    PUBLICATION = 3