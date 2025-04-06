PYTHON := python
SRC_DIR := src
IN_DIR := in

all: 1 2 3 4 5 exprArit function procedure testeFor testeIf testeWhile variaveis

1:
	$(PYTHON) $(SRC_DIR)/main.py "$(IN_DIR)/Exemplo1.txt"

2:
	$(PYTHON) $(SRC_DIR)/main.py "$(IN_DIR)/Exemplo2.txt"

3:
	$(PYTHON) $(SRC_DIR)/main.py "$(IN_DIR)/Exemplo3.txt"

4:
	$(PYTHON) $(SRC_DIR)/main.py "$(IN_DIR)/Exemplo4.txt"

5:
	$(PYTHON) $(SRC_DIR)/main.py "$(IN_DIR)/Exemplo5.txt"

exprArit:
	$(PYTHON) $(SRC_DIR)/main.py "$(IN_DIR)/Expr_Arit.txt"

function:
	$(PYTHON) $(SRC_DIR)/main.py "$(IN_DIR)/Function.txt"

procedure:
	$(PYTHON) $(SRC_DIR)/main.py "$(IN_DIR)/Procedure.txt"

testeFor:
	$(PYTHON) $(SRC_DIR)/main.py "$(IN_DIR)/TesteFor.txt"

testeIf:
	$(PYTHON) $(SRC_DIR)/main.py "$(IN_DIR)/TesteIF.txt"

testeWhile:
	$(PYTHON) $(SRC_DIR)/main.py "$(IN_DIR)/TesteWhile.txt"

variaveis:
	$(PYTHON) $(SRC_DIR)/main.py "$(IN_DIR)/Variaveis.txt"