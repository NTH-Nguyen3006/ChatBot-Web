from .generate_image import generateImage
from ..services import *

def callback_func(target: str, args: dict = None):
    generate_arg_list = []
    for arg, value in args.items():
        if isinstance(value, int): 
            generate_arg_list.append(f'{arg} = {int(value)}')
        elif isinstance(value, str):
            generate_arg_list.append(f'{arg} = "{value}"')
        else:
            generate_arg_list.append(f'{arg} = {value}')

    result_set = {}
    call_function_str = f'result = {target}({", ".join(generate_arg_list)})'
    exec(call_function_str, {f'{target}': eval(target)}, result_set)
    return result_set.get("result")