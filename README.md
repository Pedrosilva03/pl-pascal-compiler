<h1 align="center">Projeto da UC de Processamento de Linguagens - 2024/2025</h1>
<h2 align="center">Compilador de Pascal</h2>

## Definição
Compilador de Pascal Standard para uma linguagem intermédia a ser executada numa [VM](https://ewvm.epl.di.uminho.pt/) fornecida.

## Notas do projeto
A descrição completa e detalhada do projeto pode ser encontrada no [relatório](https://github.com/Pedrosilva03/pl-pascal-compiler/blob/main/doc/pl2025_projeto_gr9.pdf)

## O compilador
Este programa compila outros programas em Pascal Standard, gerando código assembly VM equivalente
- Efetua a análise léxica do programa, partindo-o em tokens
- Análise sintática e semântica
- Geração de código

Compatível com a maior parte dos casos e diferentes programas pascal
- Programas com ou sem variáveis,
- Suporte a funções e procedimentos com um ou mais argumentos,
- Ciclos, condições e expressões aritméticas complexas.

O código gerado pode ser copiado e executado na VM.
## Execução
Todos os comandos devem ser executados na raiz do projeto.

- Este programa necessita de um programa pascal passado como argumento. Este programa deve ser colocado na pasta [in](https://github.com/Pedrosilva03/pl-pascal-compiler/tree/main/in).
```console
python src/main.py "in/[nome_do_programa]"
```
- Caso haja algum erro, basta trocar o comando ```python``` por ```python3```
- Por outro lado, este programa conta com uma **Makefile**, utilizada para automatizar testes. Estes testes podem ser compilados com o comando
```console
make
```
- Caso aconteça algum erro com o comando ```python```, este pode ser trocado por ```python3``` na **Makefile**
```Makefile
PYTHON := python3
```
- Este comando executará todos os testes. Cada teste pode ser executado individualmente, indicando à frente o teste pretendido.

O resultado dos testes serão colocados na pasta [out](https://github.com/Pedrosilva03/pl-pascal-compiler/tree/main/out), com o mesmo nome do programa original.
## Conclusão
Trabalho realizado por Pedro Silva, Diogo Barros e Diogo Costa
