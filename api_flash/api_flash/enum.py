from enum import Enum
#this is real position of table data role precreate
class type_user(Enum):
    DOYEN = 0
    VICE_DOYEN = 1
    AGENT = 2
    ENSEIGNANT = 3
    AUTEUR = 4
    ETUDIANT = 5


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
