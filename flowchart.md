## Sistema Bancário

### Workflow do Sistema Bancário POO

```mermaid
graph
A[Digita CPF] --> B(CPF cadastrado?)
B --Não --> C(Cadastrar Usuario e criar conta)
B --Sim--> D{Rhombus}
C --> D(Login)
D --> E(Escolhe conta)
E --> F(Menu de Operações)
F --> G(Sacar)
G -- Verifica valor desejado, saldo limite saques e valor diarios --> J(Efetiva saque)
F --> H(Extrato)
H --> K(Gera Extrato)
F --> I(Depositar)
I -- Verifica valor --> L(Efetiva Deposito)
F --> Q(Sai do sistema)
F --> N(Criar nova conta)
F --> M(Ver contas ativas)