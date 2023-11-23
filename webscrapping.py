from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
import pandas as pd

import create
import delete
from conectar import conexao, cursor

class Web:
    def __init__(self, duq=0, ter=0, qua=0, qui=0, meg=0, lqua=0, lqui=0, lmeg=0):
        self.duq = duq
        self.ter = ter
        self.qua = qua
        self.qui = qui
        self.meg = meg
        self.lqua = lqua
        self.lqui = lqui
        self.lmeg = lmeg

        self.link = 'https://asloterias.com.br/resultados-da-mega-sena-2022?ordenacao=crescente'
        self.map = {
            "numeros": {
                "xpath": "/html/body/main/div[2]/div/div/div[1]/span[$NUM$]"
            },
            "concurso": {
                "xpath": "/html/body/main/div[2]/div/div/div[1]/strong[$NUM$]"
            }
        }
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()

    def abrir_site(self):
        self.driver.get(self.link)
        sleep(2)
        global numero
        contador = 0
        jogo = []
        matriz = []
        matrix = []
        num = []
        k = 1
        cursor.execute(delete.deleteTableJogos)
        cursor.execute(create.createTableTbJogos)
        for j in range(110):
            concurso = int(
                self.driver.find_element(By.XPATH, self.map["concurso"]["xpath"].replace('$NUM$', f'{j + 4}')).text)
            print(concurso, end=' ')
            jogo.append(concurso)
            for i in range(6):
                print(self.driver.find_element(By.XPATH, self.map["numeros"]["xpath"].replace('$NUM$', f'{k}')).text,
                      end=' ')
                numero = int(
                    self.driver.find_element(By.XPATH, self.map["numeros"]["xpath"].replace('$NUM$', f'{k}')).text)
                jogo.append(numero)
                if k == 654:
                    k += 2
                else:
                    k += 1
            matriz.append(jogo)
            self.inserir(jogo[0],jogo[1],jogo[2],jogo[3],jogo[4],jogo[5],jogo[6])
            jogo = []
            print('')

        opcao = input('Imprimir matriz [S/N]: ').strip().upper()
        if opcao == 'S':
            for linha in range(len(matriz)):
                for coluna in range(7):
                    print(matriz[linha][coluna], end='\t')
                    matrix.append(matriz[linha][coluna])
                print('')



        opcaoPlan = input('Deseja gerar planilha [S/N]: ').strip().upper()
        if opcaoPlan == 'S':
            try:
                planilha = pd.DataFrame(matriz)
                planilha.to_excel('C:/Usuários/4459091780X/Desktop/Mega.xlsx')
            except:
                print('A planilha não foi gerada...')

        while True:
            qde = int(input('Digite a quantidade [6-20]: '))
            if qde > 5 and qde < 21:
                break

        for x in range(qde):
            num.append(int(input(f'Digite o {x + 1}º: ')))

        for linha in range(len(matriz)):
            for z in range(qde):
                for coluna in range(7):
                    if matriz[linha][coluna] == num[z]:
                        contador += 1
            self.contar(contador, linha)
            contador = 0
        print('-' * 30)
        print(f'Duq: \t', self.duq)
        print(f'Ter: \t', self.ter)
        print(f'Qua: \t{self.qua} e linha {self.lqua}')
        print(f'Qui: \t{self.qui} e linha {self.lqui}')
        print(f'Meg: \t{self.meg} e linha {self.lmeg}')

    def contar(self, cont, line):
        if cont == 2:
            self.duq += 1
        elif cont == 3:
            self.ter += 1
        elif cont == 4:
            self.qua += 1
            self.lqua = line
        elif cont == 5:
            self.qui += 1
            self.lqui = line
        elif cont == 6:
            self.meg += 1
            self.lmeg = line

    def inserir(self, c, n1, n2, n3, n4, n5, n6):
        try:
            insert = f'''INSERT INTO tb_jogos(conc,n1,n2,n3,n4,n5,n6)
            values('{c}','{n1}','{n2}','{n3}','{n4}','{n5}','{n6}');'''
            cursor.execute(insert)
            conexao.commit()
        except:
            print('Não foi possível inserir dados no banco.')
