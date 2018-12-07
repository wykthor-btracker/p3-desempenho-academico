# -*- coding: utf-8 -*-
#imports
import pdb
from datetime import datetime
import re
# pdb.set_trace()
#imports

#variables
money = re.compile("^R\$\d+[\.,]*\d*$")
#variables

#classes#

class node:
    def __init__(self):
        self.conns = list()

    def addConn(self,nextNode,relation):
        newConn = conn(self,nextNode,relation)
        otherConn = conn(nextNode,self,relation)
        nextNode.conns.append(otherConn)
        self.conns.append(newConn)

    def findConn(self,relation):
        for connInst in self.conns:
            if(connInst == relation):
                return True
        return False

    def listObjects(self,relation):
        if(not isinstance(relation,str)):
            raise Exception("{} is of type {}, expected string.".format(relation,type(relation)))
        res = []
        for conn in self.conns:
            if(conn==relation):
                res.append(conn.nodeB)
        return res

class projeto(node):
    def __init__(self,titulo,dataDeInicio,dataDeTermino,agencia,valor,objetivo,descricao):
        self.titulo = titulo
        try:
            self.dataDeInicio = datetime.strptime(dataDeInicio,"%d/%m/%y")
            self.dataDeTermino = datetime.strptime(dataDeTermino,"%d/%m/%y")
        except:
            raise Exception("{} ou {} nao estao no formato dd/mm/aa".format(dataDeInicio,dataDeTermino))
        if(self.dataDeInicio > self.dataDeTermino):
            raise Exception("Viagem no tempo detectada, {} acontece antes de {}".format(self.dataDeInicio,self.dataDeTermino))
        self.agencia = agencia
        self.valor = valor
        if(not re.match(money,valor)):
            raise Exception("{} nao esta no formato certo: R$xx.xx".format(valor))
        self.objetivo = objetivo
        self.descricao = descricao
        self.status = None
        super().__init__()

    def iniciar(self,profInst):
        if(isinstance(profInst,professor)):
            self.status = "Em elaboracao"
            self.addConn(profInst,"Coordena")

    def andar(self):
        if(self.findConn("Coordena")):
            self.status = "Em andamento"

    def concluir(self):
        if(self.findConn("Publica")):
            self.status = "Concluido"

class publicacao(node):
    def __init__(self,titulo,nomeDaConf,anoDaPubl,projeto = None):
        self.titulo = titulo
        self.nomeDaConf = nomeDaConf
        try:
            self.anoDaPubl = datetime.strptime(anoDaPubl,"%Y")
        except:
            raise Exception("{} nao esta no formato YYYY".format(anoDaPubl))
        self.projeto = projeto
        if(projeto):
            if(projeto.status != "Em andamento"):
                raise Exception("{} nao esta em andamento, esta {}".format(projeto,projeto.status))
            else:
                self.addConn(projeto,"Publica")
        super().__init__()

    def addColaborador(self,colabInst):
        self.addConn(colabInst,"Autor(a)")

    def associarProjeto(self,projInst):
        if(isinstance(projInst,projeto)):
            if(projInst.status != "Em andamento"):
                raise Exception("{} nao esta em andamento, esta {}".format(projInst,projInst.status))
            else:
                self.addConn(projInst,"Publica")

class pessoa(node):
    def __init__(self,nome,email):
        self.nome = nome
        self.email = email
        super().__init__()

    def addProjeto(self,projInst):
        if(projInst.status=="Em elaboracao"):
            self.addConn(projInst,"Participa")
        else:
            raise Exception("{} nao esta em elaboracao, esta {}".format(projInst,projInst.status))

    def show(self):
        info = ""
        info+="Nome: {}, E-mail:{}\n\n".format(self.nome,self.email)
        projetos = sorted(self.listObjects("Participa"),key=lambda proj:proj.dataDeTermino,reverse=True)
        for projeto in projetos:
            info+="Projeto: {} Status: {}\nData de termino: {}\n".format(projeto.titulo,projeto.status,projeto.dataDeTermino.strftime("%d/%m/%Y"))
        info+="\n"
        producoes = sorted(self.listObjects("Autor(a)"),key=lambda prod: prod.anoDaPubl,reverse=True)
        for producao in producoes:
            info+="Producao: {}\nAno de publicacao: {}\n\n".format(producao.titulo,producao.anoDaPubl.year)
        return info

class professor(pessoa):
    def __init__(self,nome,email):
        super().__init__(nome,email)

    def orientarAluno(self,alunoInst):
        self.addConn(alunoInst,"Orienta")

class alunoGrad(pessoa):
    def __init__(self,nome,email):
        super().__init__(nome,email)

    def addProjeto(self,projInst):
        if(not self.findConn("Participa")):
            super().addProjeto(projInst)
        else:
            raise Exception("{} ja tem um projeto ao qual esta associado.".format(self.nome))
class conn:
    def __init__(self,nodeA,nodeB,relation):
        self.nodeA = nodeA
        self.nodeB = nodeB
        self.relation = relation

    def __eq__(self,relation):
        return relation==self.relation

#classes#

#functions#
def test():
    prof = professor("Wykthor","Wykthor.g@wgvale.com")
    aluno = alunoGrad("Algo","algo@wgvale.com")
    prof.orientarAluno(aluno)
    pub = publicacao("Nome","Conf","2018")
    pub2 = publicacao("Nome2","Conf2","2017")
    pub.addColaborador(aluno)
    pub2.addColaborador(aluno)
    proj = projeto("titulo","02/01/18","01/12/18","agencia","R$20.50","objetivo","descricao")
    proj.iniciar(prof)
    aluno.addProjeto(proj)
    proj.andar()
    pub.associarProjeto(proj)
    proj.concluir()
    return(aluno)
#functions#

#main#
def main(*args, **kwargs):
    test()
    return None
#main#

if(__name__=="__main__"):
    main()
