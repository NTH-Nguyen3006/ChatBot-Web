from generate_image import generateImage

def callback_func(target: str, args: dict = None):
    generate_arg_string = ", ".join([f'{arg} = {value}' for arg, value in args.items()])
    for arg, value in args.items():
        generate_arg_string

    call_function_str = f'{target}({generate_arg_string})'
    print(call_function_str)
    exec(call_function_str)
    