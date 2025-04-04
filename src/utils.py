# Esta função era auxiliar e já não é mais usada. Mesmo assim vou deixar aqui porque pode vir a ser precisa
def checkIfString(string):
    return string.startswith(" ") or (string.endswith(":") or string.endswith(" ") or len(string.split(" ")) > 1)

def print_funcs(functions):
    funcs_code = ""
    for func in functions.items():
        func_vm_array = func[1][1]
        funcs_code += "\n" + "\n".join(func_vm_array) + "\n" + "\n"
    return funcs_code

def get_nth_element_dict(dict: dict, nth, typ):
    i = 0
    for element in dict.keys():
        if i == nth:
            return (dict[element] if typ == 0 else element)
    return -1

def get_name_from_pusha(instructions):
    name = ""
    for instruction in instructions:
        if instruction.startswith("PUSHA"):
            splitted_inst = instruction.split(" ")
            name = splitted_inst[1]
    return name