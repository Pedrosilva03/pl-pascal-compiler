from pascalLexer import lexer
#from pascalYacc import parse_input
import sys

def main(args):
    inputFile = args[1]

    with open(inputFile, 'r') as file:
        code = file.read()

    # Análise léxica do código Forth
    lexer.input(code)
    
    # Tokenize
    for token in lexer:
        print(token)

    # Análise sintática do código Forth e geração de código
    #vm_code = parse_input(code)
    
    #with open(f'../out/{inputFile}.txt', 'w') as file:
    #    file.write(vm_code)

if __name__ == "__main__":
    main(sys.argv)