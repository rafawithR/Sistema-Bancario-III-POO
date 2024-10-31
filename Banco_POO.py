import abc
from datetime import datetime as dt

DATA = dt.now()

class Transacao(abc.ABC):
    def valor(self):
        pass
    
    def registrar(self):
        pass


class Cliente:
    def __init__(self,endereco: str):
        self._endereco = endereco
        self._contas = []

    def trasacao(conta, transacao):
        pass

    def adiciona_conta(self, conta):
        self._contas.append(conta)


class Pessoa_fisica(Cliente):
    def __init__(self,endereco: str, cpf: str, nome: str, data_nascimento: str):
        super().__init__(endereco)
        self._cpf = cpf
        self._nome = nome
        self._data_nascimento = data_nascimento

    @property
    def nome(self):
        return self._nome

    @property
    def endereco(self):
        return self._endereco

    @property
    def cpf(self):
        return self._cpf


class Conta:
    all_contas = []

    def __init__(self, cliente: Cliente, numero: int, saldo: float= 0,agencia: str='0001' ):
        self._cliente = cliente
        self._saldo = saldo
        self._historico = []
        self._numero = numero
        self._agencia = agencia

    @property
    def saldo(self):
        return self._saldo
    
    @property
    def extrato(self):
        extrato_bancario = '''
############ EXTRATO ############

'''
        for atividade in self._historico:
            extrato_bancario += atividade + '\n'
        extrato_bancario += '\n' + 'Saldo: R$' + str(self.saldo) + '\n' + '#################################\n'
        return extrato_bancario

    @property
    def numero(self):
        return self._numero
    
    @property
    def cliente(self):
        return self._cliente

    @classmethod
    def nova_conta(cls,cliente, numero):
        n_conta = cls(cliente,numero)
        cls.all_contas.append(n_conta)
        return cls(cliente,numero) 

    @staticmethod
    def pegar_numero_nova_conta():
        numeros_utilizados = []
        for conta in Conta.all_contas:
            numeros_utilizados.append(conta.numero)
        if len(numeros_utilizados) == 0:
            return 1
        else:
            return numeros_utilizados[-1] +1

    def __str__(self) -> str:
        return f"Cliente: {self.cliente}, Conta: {self.numero}"


class Conta_Corrente(Conta):
    def __init__(self, cliente: Cliente, numero: int, saldo: float= 0,agencia: str='0001'):
        super().__init__(cliente, numero, saldo, agencia)
        self._limite_valor_saque = 500.00
        self._limite_saques = 3

    def sacar(self, valor: float):
        if valor > self.saldo:
            print('Saldo não disponível')
            return False
        elif self._limite_saques == 0:
            print('Você já excedeu o limite de saques hoje!')
            return False
        elif self._limite_valor_saque < valor <= 0:
            print('Este valor não pode ser sacado')
            return False
        else:
            self._saldo -= valor
            self._limite_saques -= 1
            return True

    def depositar(self,valor: float):
        if valor <= 0:
            print('Esse valor não pode ser depositado')
            return False
        else:
            self._saldo += valor
            return True

    def adicionar_transacao(self,transacao):
        self._historico.append(transacao)


class Saque(Transacao):
    
    def __init__(self,valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(valor):
       retirada = f'''Saque    {DATA.day}/{DATA.month}/{DATA.year} -R${valor:.2f}'''
       return retirada


class Deposito(Transacao):

    def __init__(self,valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(valor):
       entrada = f'''Depósito    {DATA.day}/{DATA.month}/{DATA.year}  R${valor:.2f}'''
       return entrada


def cadastrar_cliente(cpf_novo_usuario):
    cpf = cpf_novo_usuario
    primeiro_nome = input('Digite seu Primeiro Nome: ')
    sobrenome = input('Digite seu Sobrenome: ')
    nascimento_dia = input('Digite o DIA do seu Nascimento (ex: 03): ')
    nascimento_mes = input('Digite o MÊS do seu Nascimento (ex: 02): ')
    nascimento_ano = input('Digite o ANO do seu Nascimento (ex: 1989): ')
    logradouro = input('Digite seu logradouro: ')
    numero = input('Digite o número da sua residência: ')
    bairro = input('Digite o bairro: ')
    cidade = input('Digite a cidade: ')
    estado = input('Digite a sigla do estado: ')
    nome_completo= f'{primeiro_nome} {sobrenome}'.capitalize()
    data_nascimento = f'{nascimento_dia}/{nascimento_mes}/{nascimento_ano}'
    endereco = f'{logradouro.capitalize()},{numero}-{bairro.capitalize()}-{cidade.capitalize()}/{estado.upper()}'.capitalize()
    cliente = Pessoa_fisica(endereco,cpf,nome_completo,data_nascimento)
    conta_nova = Conta_Corrente.nova_conta(cliente,Conta.pegar_numero_nova_conta())
    return cliente, conta_nova


def listar_contas_ativas(cpf_usuario):
    contas_usuario = []
    for conta in Conta_Corrente.all_contas:
        if conta.cliente.cpf == cpf_usuario:
            contas_usuario.append(conta)
    return contas_usuario


def escolher_conta_ativa(numero_da_conta, lista_contas):
    for conta_ativa in lista_contas:
        if str(conta_ativa.numero) == numero_da_conta:
            return conta_ativa
        else:
            return 'Conta não existente. Verifique o número de conta escolhido!'        


def menu_inicial():
    global DATA
    
    while True:

        print(f'''
################################# MENU ##################################

Data: {DATA.day}/{DATA.month}/{DATA.year}  
Hora: {DATA.ctime()[10:16]}

Para iniciarmos, por favor digite seu CPF (somente os números):

''')
        cpf_usuario=input(' ')
        contas_usuario = listar_contas_ativas(cpf_usuario)
        if contas_usuario:
            print(f'''
Olá, {contas_usuario[0].cliente.nome}! Bom ter você de volta!

Estas são suas contas ativas:
                  ''')
            for conta_ativa in contas_usuario:
                print(f'Número conta: {conta_ativa.numero}   Saldo: R${conta_ativa.saldo}')
            conta_escolhida = input('Digite o NÚMERO da conta que você deseja acessar: ')
            escolha = escolher_conta_ativa(conta_escolhida,contas_usuario)
            if isinstance(escolha,Conta_Corrente):
                menu_cliente_ativo(escolha)
                break
            else:
                print(escolha)

        else:
            print('Parece que você ainda não tem cadastro com a gente! Vamos criar uma conta...'+'\n')
            nova_conta = cadastrar_cliente(cpf_usuario)
            menu_cliente_ativo(nova_conta[1])
            break


def menu_cliente_ativo(conta):
    global DATA
    
    if DATA.hour < 12:
        turno = 'Bom dia'
    elif 12 <= DATA.hour <= 18:
        turno = 'Boa tarde'
    else:
        turno = 'Boa noite'

    while True:

        print(f'''
################################# MENU ##################################

Data: {DATA.day}/{DATA.month}/{DATA.year}  
Hora: {DATA.ctime()[10:16]}


{turno}, {conta.cliente.nome}! O que você gostaria de fazer?


[1] - Saque
[2] - Deposito
[3] - Extrato
[4] - Criar nova conta
[5] - Ver contas
[0] - Sair

    ''')

        opcao=str(input('Digite aqui o número da opção escolhida: '))
        if opcao == '1':
            valor = float(input('Quanto você deseja sacar? '))
            if conta.sacar(valor):
                conta.adicionar_transacao(Saque.registrar(valor))
                print(f'Saque de R${valor} realizado com sucesso!')
        elif opcao == '2':
            valor = float(input('Quanto você deseja depositar? '))
            if conta.depositar(valor):
                conta.adicionar_transacao(Deposito.registrar(valor))
                print(f'Depósito de R${valor} realizado com sucesso!')
        elif opcao == '3':
            print(conta.extrato)
        elif opcao == '4':
            decisao_cliente = input('Tem certeza que deseja criar uma nova conta [S] / [N]? ')
            if decisao_cliente.lower() == 's':
                Conta_Corrente.nova_conta(conta.cliente,Conta.pegar_numero_nova_conta())
                print('Conta criada com sucesso!')
            else:
                print('Ok! Vamos voltar ao menu principal.')
        elif opcao == '5':
            print(f'''
Contas Ativas de {conta.cliente.nome}:

                      ''')
            for item in listar_contas_ativas(conta.cliente.cpf):
                
                print (f'  Número da conta:   {item.numero}')
        elif opcao == '0':
            decisao_cliente = input('Tem certeza que deseja sair [S] / [N]? ')
            if decisao_cliente.lower() == 's':
                print(f'''

{conta.cliente.nome}, obrigado por escolher nosso banco! {turno} e volte sempre!

''')    
                break
            else:
                pass

if __name__ == '__main__':
    menu_inicial()