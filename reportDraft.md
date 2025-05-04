# Analise sintática (Gramática)

Ver o parser out

# Analise semantica (Transformacao de codigo)

O programa percorre as diferentes producoes e gera código máquina linha a linha.

Normalmente um programa pascal está dividido em 4 partes sendo que algumas podem ser opcionais: um header que representa o nome do programa, uma secção onde funções e procedures são definidas, uma zona para declaração de variaveis e o corpo do programa principal

As partes opcionais são aglomeradas numa regra "block". Esta regra leva em atenção todas a possibilidades de estrutura que um programa pode ter. Garantido que é possível compilar vários tipos de programas, desde o mais simples: 

- Programas com apenas com um body

Até aos programas mais complexos:

- Programas com funções, procedures e declarações de variáveis

Todos os programas vão ter as instruções "START" e "STOP" como primeira e última instrução.

## Variáveis

As variáveis são definidas dentro do bloco "var" do programa pascal. O programa reconhece a declaração do bloco analisa os nomes das variáveis e os tipos. O programa suporta a declaração de variáveis:

```txt
a, b, c: integer
```

Criamos um dicionário variáveis que guarda o nome das variáveis associado ao seu tipo (nome --> tipo). As variáveis são guardadas no dicionário na ordem que foram encontradas pelo parser. Este método é vantajoso porque desta forma é possível obter a posição de cada variável e utilizar essa posição na stack com a instrução "STOREG x". O programa deteta variáveis com declaração dupla e avisa ao compilar.

Para além disso temos um dicionário de variáveis às quais foram atribuidos valores, sendo este apenas usado para detetar variáveis que podem não ter valor, simulando um compilador real.

## Identificadores

Todos os nomes de variáveis e funções são vistos como IDENTIFIERS aos olhos do compilador. Os acessos a estes elementos é feito sempre com PUSHG e STOREG

## Body

O body representa um bloco de código principal dentro de um begin..end. Estes blocos podem se referir ao código principal do programa ou ao código de uma função. O body é definido por diversos statements.

## Statements

Os statements representam uma linha de código principal. Este elemento engloba a maior parte das instruções que podem ser definidas.

- writeln
- assignment
- procedure_call
- cond_if
- while_loop
- for_loop
- repeat_loop
- readln

Estas instruções serão explicadas em detalhe abaixo.

## Assignments

Este elemento representa todos os statements do tipo

```
alguma_coisa := outra_coisa
```

Os assignments suportam, atribuição de valores literais, outras variáveis, valores de arrays, resultados de funções, expressões algébricas, entre outros.

Regra geral as atribuições são feitas fazendo um PUSHG do valor source e um STOREG para o destino.

## Expressões

## Read and write

### Read

O read tem dois casos, um geral e um para arrays. 

### Write

## Condições

## Loops

### For loop

### While loop

### Repeat until loop

## Funções e Procedures

O código VM das funções e procedures é gerado e guardado temporariamente. Devido à forma como a VM lê o código, as funções devem ser definidas depois do código principal, mas como em pascal as funções aparecem antes, o código precisa de ser guardado e utilizado depois.

Utilizamos um dicionário para guardar estas informações. Cada posição do dicionário guarda os argumentos que uma função recebe e o código VM. Ao ser chamada, é feita uma atribuição dos valores passados como argumento às variáveis da função.

## Acesso a arrays