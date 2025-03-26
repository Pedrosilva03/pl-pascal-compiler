from pascalLexer import lexer
from pascalYacc import parse_input
import sys

def main(args):
    inputFile = args[1]

    with open(inputFile, 'r') as file:
        code = file.read()

    # Análise léxica do código Pascal
    lexer.input(code)
    
    # Tokenize
    for token in lexer:
        print(token)

    # Análise sintática do código Pascal e geração de código
    vm_code = parse_input(code)
    
    if vm_code is None:
        print("Erro de análise sintática. O código não foi gerado.")
        return

    # Write the generated code to the output file
    output_file = f'../out/{inputFile.split("/")[-1]}'
    with open(output_file, 'w') as file:
        file.write(vm_code)

    print(f"Código gerado com sucesso em: {output_file}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python main.py <caminho_para_o_arquivo_de_entrada>")
    else:
        main(sys.argv)