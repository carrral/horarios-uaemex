

class Materia:

    def __init__(self,cve,nom):
        self.cve = cve
        self.nom = nom

    def get_attr_list(self):
        return [self.cve,self.nom]
