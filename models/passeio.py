from models.models import Model

class Passeio(Model):
    def oferecerPasseio(self):
        v=0
        ponto = self.get(ponto = self.ponto)
        teste0 = Model(tabela='pontos_turisticos')
        teste1 = teste0.get(name=self.ponto)
        if len(teste1) != 0:
            for i in range(len(ponto)):
                if ponto[i][3] == self.data:
                    v=1
            if v==0:
                self.save()
                return True
            else:
                return False
        else:
            return False