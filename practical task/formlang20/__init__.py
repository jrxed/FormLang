from .counter import CounterFactory, IntWithInf


def find_max_len_of_identical_symbols_in_reg_exp(regexp, symbol):
    stack = []
    counter = CounterFactory.get_counter(symbol)
    for index, char in enumerate(regexp):
        if char in 'abc1':
            stack.append(counter(char))
        else:
            if char == '*':
                if not stack:
                    error_text = 'Input is not a correct regular expression\n'
                    error_text += regexp + '\n'
                    error_text += ' ' * index + '^' + '\n'
                    error_text += 'Operator ' + char + ' doesn\'t have enough parameters (0/1)'

                    raise ValueError(error_text)
                obj = stack.pop()
                stack.append(obj.star())

            elif char in '.+':
                if len(stack) < 2:
                    error_text = 'Input is not a correct regular expression\n'
                    error_text += regexp + '\n'
                    error_text += ' ' * index + '^' + '\n'
                    error_text += 'Operator ' + char + ' doesn\'t have enough parameters (' + str(len(stack)) + '/2)'

                    raise ValueError(error_text)

                right = stack.pop()
                left = stack.pop()

                if char == '.':
                    stack.append(left * right)
                elif char == '+':
                    stack.append(left + right)

    if len(stack) != 1:
        raise ValueError('input is not a correct regular expression')

    result = stack[0]

    return str(IntWithInf.max(*result.get_count()))
