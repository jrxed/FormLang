from formlang20 import find_max_len_of_identical_symbols_in_reg_exp as func


if __name__ == '__main__':
    regexp = input()
    symbol = input()

    result = func(regexp, symbol)
    print(result)
