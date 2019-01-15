# -*- coding: utf-8 -*-
#imports
import engine
import pdb
from functools import reduce
#pdb.set_trace()
#imports

#variables#
mainScreen = """
 _______   _______     _______. _______ .___  ___. .______    _______ .__   __.  __    __    ______   
|       \\ |   ____|   /       ||   ____||   \\/   | |   _  \\  |   ____||  \\ |  | |  |  |  |  /  __  \\  
|  .--.  ||  |__     |   (----`|  |__   |  \\  /  | |  |_)  | |  |__   |   \\|  | |  |__|  | |  |  |  | 
|  |  |  ||   __|     \\   \\    |   __|  |  |\\/|  | |   ___/  |   __|  |  . `  | |   __   | |  |  |  | 
|  '--'  ||  |____.----)   |   |  |____ |  |  |  | |  |      |  |____ |  |\\   | |  |  |  | |  `--'  | 
|_______/ |_______|_______/    |_______||__|  |__| | _|      |_______||__| \\__| |__|  |__|  \\______/  
                                                                                                      
     ___       ______     ___       _______   _______ .___  ___.  __    ______   ______               
    /   \\     /      |   /   \\     |       \\ |   ____||   \\/   | |  |  /      | /  __  \\              
   /  ^  \\   |  ,----'  /  ^  \\    |  .--.  ||  |__   |  \\  /  | |  | |  ,----'|  |  |  |             
  /  /_\\  \\  |  |      /  /_\\  \\   |  |  |  ||   __|  |  |\\/|  | |  | |  |     |  |  |  |             
 /  _____  \\ |  `----./  _____  \\  |  '--'  ||  |____ |  |  |  | |  | |  `----.|  `--'  |             
/__/     \\__\\ \\______/__/     \\__\\ |_______/ |_______||__|  |__| |__|  \\______| \\______/   

Bem vindo ao sistema de gestão do laboratório 110110110 !
Que deseja fazer hoje?
1. Criar projeto
2. Criar publicação
3. Dar um aluno para um orientador
4. Gerenciar projeto
5. Gerenciar publicação
6. Consulta por colaborador
7. Consulta por projeto
8. Relatório do laboratório
9. Sair
"""
#variables

#classes#

#classes

#functions#

#functions

#main#
def main(*args,**kwargs):
	labo = engine.lab()
	choice = -1
	while(choice != "9"):
		print(mainScreen)	
		choice = input()
		if choice=="1":
			print("Diga o titulo, data de inicio(dd/mm/aaaa), data de término(dd/mm/aaaa), agencia financiadora, valor alocado(R$XX.XX), objetivo e descrição, separados por vírgula.")
			values = input()
			new = None
			try:
				new = engine.projeto(*values.split(","))
			except Exception as e:
				print("Opa! Algo errado: {}".format(e.args[0]))
			if(new):
				print("Pronto! Quando for procurar por ele, use {}".format(new.nome))
				labo.addConn(new,"projeto")
		elif choice=="2":
			print("Diga o título, nome da conferência, ano da publicação(aaaa):")
			values = input()
			new = None
			try:
				new = engine.publicacao(*values.split(","))#*lista passa a lista como parâmetros da função
			except Exception as e:
				print("Opa! Algo errado: {}".format(e.args[0]))
			if(new):
				print("Pronto! Quando for procurar por ele, use {}".format(new.nome))
				labo.addConn(new,"publicacao")			
		elif choice=="3":
			print("Diga o nome do aluno e do professor, separados por vírgula:")
			values = input()
			try:
				values = values.split(",")
			except:
				print("Opa! Parece que você esqueceu das vírgulas.")
				continue
			if(len(values)!=2):
				print("Opa! Faltou algo. entrada esperada: aluno,professor.")
			new = None
			aluno,professor = labo.findNode(values[0],"pessoa"),labo.findNode(values[1],"pessoa")
			if(aluno and professor):
				try:
					professor.orientarAluno(aluno)
				except:
					print("{} não é um professor! Precisa ser pra poder orientar né.".format(professor))
			elif(aluno):
				print("Professor(a) não encontrado! Se deseja cadastrá-lo, digite nome e email, seperados por vírgula:")
				prof = input()
				if(prof!=""):
					prof = prof.split(",")
					try:
						new = engine.professor(*prof)
					except Exception as e:
						print("Opa! Algo errado: {}".format(e.args[0]))	
					if(new):	
						print("Pronto!")
						new.orientarAluno(aluno)
						labo.addConn(new,"pessoa")
			elif(professor):
				print("Eita. Não achei esse aluno. Se quiser cadastrá-lo, digita nome, e-mail e a escolaridade: g para graduacao, m para mestrado, d para doutorado, separado por vírgula, e resolvo isso agora.")
				alunoInst = input() 
				try:
					if(alunoInst.split(",")[2]=="g"):
						new = engine.alunoGrad(*alunoInst.split(",")[:2])
					else:
						new = engine.pessoa(*alunoInst.split(","))
				except Exception as e:
					print("Opa! Algo errado: {}".format(e.args[0]))			
				if(new):
					print("Pronto!")
					professor.orientarAluno(new)
					labo.addConn(new,"pessoa")
			else:
				print("Opa! Esses eu não achei, se quiser cadastrá-los, coloca assim: nome do aluno, email do aluno, nível de escolaridade do aluno(g para graduação, m para mestrado, d para doutorado) nome do professor, email do professor, tudo separado por vírgula.")
				dois = input()
				newAluno,newProf = None, None
				if(dois!=""):
					dois = dois.split(",")
					aluno = dois[:3]
					prof = dois[3:]
					try:
						if(aluno[2]=="g"):
							newAluno = engine.alunoGrad(*aluno[:2])
						else:
							newAluno = engine.pessoa(*aluno[:2])
						newProf = engine.professor(*prof)
					except Exception as e:
						print("Opa! Algo errado: {}".format(e.args[0]))			
					if(newAluno and newProf):
						newProf.orientarAluno(newAluno)
						print("Pronto!")
						labo.addConn(newAluno,"pessoa")
						labo.addConn(newProf,"pessoa")
		elif choice=="4":
			print("Qual o titulo do projeto?:")
			nome = input()
			proj = labo.findNode(nome,"projeto")
			if (proj and isinstance(proj,engine.projeto)):
				if(not proj.status):
					print("Esse projeto não foi iniciado, se deseja alocar um professor e pôr o projeto em elaboração, digite o nome ou e-mail do professor.")
					prof = input()
					profInst = labo.findNode(prof,"pessoa")
					if(profInst and isinstance(profInst,engine.professor)):
						proj.iniciar(profInst)
						print("Pronto!")
					else:
						print("Professor não encontrado! Se deseja cadastrar um novo, digite nome e e-mail, separados por vírgula.")
						prof = input()
						if(prof!=""):
							prof = prof.split(",")
							try:
								new = engine.professor(*prof)
							except Exception as e:
								print("Opa! Algo errado: {}".format(e.args[0]))	
							if(new and not labo.findNode(new.nome,"pessoa")):
								print("Pronto!")
								proj.iniciar(new)
								labo.addConn(new,"pessoa")
							else:
								print("Opa! Já existe uma pessoa com esse nome, coloca mais coisa no nome e tenta de novo! sobrenome, etc.")
				elif(proj.status == "Em elaboracao"):
					print("Esse projeto está em elaboração, o que deseja fazer?\n1. Alocar um aluno para este projeto.\n2. Colocar o projeto em andamento.(Cuidado! Alocações de alunos não serão mais possíveis.)")
					innerChoice = input()
					if(innerChoice == "1"):
						print("Qual o nome do aluno?")
						aluno = labo.findNode(input(),"pessoa")
						if(aluno):
							try:
								aluno.addProjeto(proj)
							except Exception as e:
								print("Opa! Algo errado: {}".format(e.args[0]))
						else:
							print("Eita. Não achei esse aluno. Se quiser cadastrá-lo, digita nome, e-mail e a escolaridade: g para graduacao, m para mestrado, d para doutorado, separado por vírgula, e resolvo isso agora.")
							alunoInst = input() 
							try:
								if(alunoInst.split(",")[2]=="g"):
									new = engine.alunoGrad(*alunoInst.split(",")[:2])
								else:
									new = engine.pessoa(*alunoInst.split(","))
							except Exception as e:
								print("Opa! Algo errado: {}".format(e.args[0]))
							new.addProjeto(proj)
					elif(innerChoice=="2"):
						print("Ok!")
						proj.andar()
				elif(proj.status == "Em andamento"):
					print("Esse projeto está em elaboração, o que deseja fazer?\n1. Associar publicacao 2. Concluir projeto.")
					innerChoice = input()
					if(innerChoice=="1"):
						print("Qual o nome da publicacao?")
						nome = input()
						att = labo.findNode(nome,"publicacao")
						if(att):
							try:
								att.associarProjeto(proj)
								print("Pronto!")
							except Exception as e:
								print("Opa! Algo errado: {}".format(e.args[0]))
					elif(innerChoice=="2"):
						print("Ok!")
						proj.concluir()
				elif(proj.status == "Concluido"):
					print("Esse projeto está concluído! Não há mais nada a se fazer.")
		elif choice=="5":
			print("Qual o nome da publicacao?")
			pub = input()
			att = labo.findNode(pub,"publicacao")					
			if(att):
				print("Se deseja associar essa publicacao a algum projeto, digite o nome do projeto, caso contrário, digite nada.")
				innerChoice = input()
				find = labo.findNode()
				if(find):
					try:
						pub.associarProjeto(find)
						print("Pronto!")
					except Exception as e:
						print("Opa! Algo errado: {}".format(e.args[0]))
		elif choice=="6":
			print("Qual o nome OU email do colaborador?")
			colab = input()
			att = labo.findNode(colab,"pessoa")
			if(att):
				print(att.show())
			else:
				print("Eita! Não achei esse.")
		elif choice=="7":
			print("Qual o nome do projeto?")
			proj = input()
			att = labo.findNode(proj,"projeto")
			if(att):
				print(att.show())
			else:
				print("Eita! Não achei esse.")
		elif choice=="8":
			colabs = 0
			totalDeProjetos = 0
			publicacoes = 0
			orientacoes = 0
			colabs = labo.listObjects("pessoa")
			projetos = labo.listObjects("projeto")
			publicacoes = labo.listObjects("publicacao")
			orientacoes = [colab for colab in colabs if isinstance(colab,engine.professor)]
			orientacoes = reduce(lambda x,y:x+y,map(lambda x:len([val for val in x.conns if val=="Orienta"]),orientacoes))
			projetosEmElaboracao = len([proj for proj in projetos if proj.status == "Em elaboracao"])
			projetosEmAndamento = len([proj for proj in projetos if proj.status == "Em andamento"])
			projetosConcluidos = len([proj for proj in projetos if proj.status == "Concluido"])			
			print("Colaboradores: {}\nProjetos: {}\nPublicacoes: {}\nOrientacoes: {}\nProjetos em elaboração: {}\nProjetos em andamento:{}\nProjetos concluidos:{}\n".format(len(colabs),len(projetos),len(publicacoes),orientacoes,projetosEmElaboracao,projetosEmAndamento,projetosConcluidos))
		input()
	return None
#main#
if __name__ == '__main__':
	main()
