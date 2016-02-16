__author__ = 'AChen'

def flatten1(lst):
    if isinstance(lst, int):
        return lst
    else:
        result = []
        for lst_i in lst:
            # result = [result, flatten1(lst_i)]
            result_list = flatten1(lst_i)
            if isinstance(result_list, int):
                result.append(result_list)
            else:
                for i in range(len(result_list)):
                    result.append(result_list.pop(0))
        return result

def flatten2(lst):
    if isinstance(lst, int):
        return [lst]
    else:
        result = []
        for lst_i in lst:
            result.extend(flatten2(lst_i))
        return result

if __name__ == '__main__':
    print(flatten2([[1, 5, 7], [[4]], 0, [-4, [6], [7, [8], 8]]]))
