class Porte:
    def __init__(self, id, libelle, isOpen):
        self.id = id
        self.libelle = libelle
        self.isOpen = isOpen

    def fromDoc(portes):
        list = []
        for porte in portes:
            list.append(Porte(
                porte['id'],
                porte['libelle'],
                porte['isOpen'])
            )
        return list

    def toDoc(self):
        return {
            "id": self.id,
            "libelle": self.libelle,
            "isOpen": self.isOpen,
        }
