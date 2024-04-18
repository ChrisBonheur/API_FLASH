from enum import Enum

class type_user(Enum):
    DOYEN = 1
    AGENT = 2
    ENSEIGNANT = 3
    ETUDIANT = 4


class type_inscription(Enum):
    PREINSCRIPTION_INIT = 1
    PREINSCRIPTION_VALID = 2
    INSCRIPTION_VALID = 3
    DISABLE = 4
    RADIATION = 5


class state_article(Enum):
    INIT = 1
    PARRUTION = 2
    PUBLICATION = 3
