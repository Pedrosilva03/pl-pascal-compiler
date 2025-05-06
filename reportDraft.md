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

As expressões são uma das bases deste projeto. Seguimos um formato de hierarquia, respeitando assim as prioridades das operações.

Regra geral, dados dois valores e uma operação, o código máquina gerado será sempre (primeiro valor) (segundo valor) (operação).

### Expressões booleanas

A última prioridade são as expressões booleanas. Colocar operadores lógicos em último nas prioridades permite criar expressões muito complexas que podem servir de base para condições.

Exemplo: (a + b) * c + d = a - 5 * 4

Ao colocar as expressões booleanas em último, é possível comparar expressões complexas, calculando primeiro os valores de cada lado.

#### Operadores lógicos

O nosso compilador suporta os vários operadores lógicos nativos do pascal, gerando o respetivo código máquina para cada um.

### Expressões soma e subtração

Acima das expressões booleanas aparecem as somas e subtrações. Estão abaixo na gramática, pelo que tem maior prioridade.

Exemplo: a + b = 0

Neste caso será feita a soma primeiro, e depois é que o resultado será comparado.

### Expressões multiplicação e divisão

No topo das prioridades aparecem as multiplicações e divisões. São o nível mais baixo de operações na gramática, pelo que são as primeiras a ser calculadas.

Exemplo: a + b * c

Neste caso, b * c será calculado primeiro e depois o resultado será somado. Esta operação é o equivalente a fazer a + (b * c).

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

É feita uma análise do tipo de dados que vão ser escritos de modo a determinar o tipo de write, visto que o código máquina diferencia a instrução dependendo do tipo de dados.

Para as funções, é analisado o tipo de return da função, para que se possa aplicar o tipo de WRITE correto.

## Condições

As condições suportam os vários casos de blocos de condiç~so do pascal. Dependendo se cada bloco tem uma ou mais linhas, é necessário adicionar BEGIN e END no inicio e no fim. Para além disso, as condições podem ou não ser acompanhadas de ELSE ou não. No caso do else, o programa também suporta blocos BEGIN..END ou apenas uma instrução.

Cada bloco de condição tem um identificador universal que é incrementado sempre que o compilador deteta um IF statement. Assim garante se que cada IF é único e que não há mistura de labels no código VM gerado.

A estrutura é relativamente parecida com os loops (analisada em detalhe mais tarde):

- Label: IF(ID)
- Condição: A condição vai sempre ter valor 0 ou 1, que será interpretado pela instrução JZ
- Corpo: Instruções que correm caso a condição seja verdade. No final encontra-se um salto para fora do IF, visto que o ELSE não corre se a condição for verdadeira
- Label: ELSE(ID): O identificador do ELSE é o mesmo do seu respetivo IF
- Corpo do ELSE: Instruções que correm caso a condição seja falsa.´
- Label de fim da condição: ENDIF(ID)

## Loops

Os loops seguem a mesma lógica: Verificação de uma condição e o respetivo jump de saída no caso em que a condição não é mais respeitada.

Cada loop tem um identificador que é universal e que é incrementado a cada loop criado, garantindo assim que cada loop é único.

Cada loop tem alguns detalhes que os diferenciam mas a estrutura é parecida entre eles e parecida com as condições.

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

## Arrays

O acesso a arrays é feito de forma parecida com o acesso a variáveis, sendo dividido em dois casos: 

### Acesso a arrays

O acesso a arrays é feito obtendo o índice da cabeça do array e somando o índice pretendido.

Exemplo: arr[4]

Como não existe uma instrução VM que permita, dados dois valores "a" e "b", colocar "b" no endereço "a" da stack, tivemos que criar um atalho.

Primeiramente faz-se um PUSHFP. Este push serve para colocar um endereço no topo da stack de modo a fazer operações diretamente sobre endereços. Visto que a VM é limitada e não dá para dar PUSH a endereços específicos, esta foi a melhor forma.

Neste caso, se o array estiver na posição 3 da stack, faz-se um PUSHI do índice onde está a cabeça, seguido de um PADD para somar endereços. Depois é colocado o valor do índice pretendido, voltando a fazer um PADD. O resultado final será o endereço da stack onde o elemento do array que se quer aceder se encontra.

### Acesso a strings

O acesso a strings é feito dando PUSH da string pretendida e do endereço pedido. Depois faz se um CHARAT. Esta instrução coloca na stack o código ASCII do carater na posição pretendida.

Exemplo: str[i]

- É feito um PUSHS str e PUSHG (indice de i). 
- É subtraída uma unidade do índice visto que a stack conta a partir de zero mas o pascal conta a partir de 1 (str[3] em pascal == str[2] na VM)
- Depois é feito um CHARAT.