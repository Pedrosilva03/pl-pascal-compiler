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

As expressões são uma das bases deste projeto. 

## Read and write

### Read

O read tem dois casos, um geral e um para arrays. Devido a alguns detalhes nas instruções, foi necessário diferenciar os dois casos.

Dependendo da variável destino, é feita a conversão de string para inteiro ou para float. Após isso é feito um store na variável destino.

Para o caso dos arrays, o local de destino já está especificado nas instruções de acesso ao array, pelo que basta fazer STORE 0.

### Write

O write consegue lidar com diversos tipos de argumentos:

- Argumentos literais
- Variáveis
- Expressões
- Chamadas de funções

## Condições

## Loops

Os loops seguem a mesma lógica: Verificação de uma condição e o respetivo jump de saída no caso em que a condição não é mais respeitada.

Cada loop tem um identificador que é universal e que é incrementado a cada loop criado, garantindo assim que cada loop é único.

Cada loop tem alguns detalhes que os diferenciam

### For loop

O ciclo for verifica a condição e faz um cálculo (normalmente uma variável de controlo)

A estrutura é a seguinte:

- Inicializa a variável de controlo: statement
- Label: FOR(ID)
- Condição: Se a condição for falsa, ativa a instrução JZ que leva ao fim do ciclo.
- - As palavras TO e DOWNTO indicam se a condição deve verificar se a variável de controlo é menor ou maior que o objetivo.
- Corpo do ciclo: Statements
- Incremento da variável de controlo: Soma ou subtrai, dependendo do tipo de ciclo, e atualiza a variável de controlo
- Salto para nova iteração: JUMP
- Label de fim de ciclo: ENDFOR

### While loop

O ciclo while verifica a condição mas, ao contrário do ciclo for, não efetua nenhum cálculo.

A estrutura é a seguinte:

- Label: WHILE(ID)
- Condição: Se a condição for falsa, ativa a instrução JZ que leva ao fim do ciclo.
- Corpo do ciclo: Statements
- Salto para nova iteração: JUMP
- Label de fim de ciclo: ENDWHILE

### Repeat until loop

O ciclo repeat until é a mesma coisa que o ciclo while mas o corpo vem antes da condição. Isso significa que o ciclo vai sempre correr pelo menos uma vez.

A estrutura é a seguinte:

- Label: REPEAT(ID)
- Corpo do ciclo: Statements
- Condição: A condição é seguida de um NOT visto que o ciclo só corre se a condição for falsa.
- Salto para nova iteração: JUMP
- Label de fim de ciclo: ENDREPEAT

## Funções e Procedures

O código VM das funções e procedures é gerado e guardado temporariamente. Devido à forma como a VM lê o código, as funções devem ser definidas depois do código principal, mas como em pascal as funções aparecem antes, o código precisa de ser guardado e utilizado depois.

Utilizamos um dicionário para guardar estas informações. Cada posição do dicionário guarda os argumentos que uma função recebe e o código VM. Ao ser chamada, é feita uma atribuição dos valores passados como argumento às variáveis da função.

## Acesso a arrays