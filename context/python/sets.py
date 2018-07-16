import pandas


class Sets():

    def __init__(self, dict_of_sets):
        self.dict_of_sets = dict_of_sets

    def as_count_matrix(self):
        '''
        >>> s = Sets({'a': {1, 2}, 'b': {2, 3}, 'c': {1}})
        >>> with pandas.option_context('display.float_format', '{:,.0f}'.format):
        ...   s.as_count_matrix()
           a  b  c
        a  2  1  1
        b  1  2  0
        c  1  0  1
        '''
        keys = self.dict_of_sets.keys()
        df = pandas.DataFrame(index=keys, columns=keys, dtype=int)
        for j in keys:
            for k in keys:
                df[j][k] = len(self.dict_of_sets[j] & self.dict_of_sets[k])
        return df

    def as_ratio_matrix(self):
        '''
        >>> s = Sets({'a': {1, 2}, 'b': {2, 3}, 'c': {1}})
        >>> s.as_ratio_matrix()
             a    b    c
        a  1.0  0.5  1.0
        b  0.5  1.0  0.0
        c  0.5  0.0  1.0
        '''
        keys = self.dict_of_sets.keys()
        df = pandas.DataFrame(index=keys, columns=keys, dtype=int)
        for j in keys:
            for k in keys:
                df[j][k] = (
                    len(self.dict_of_sets[j] & self.dict_of_sets[k]) /
                    len(self.dict_of_sets[j])
                )
        return df

    def as_columns(self):
        '''
        >>> s = Sets({'a': {1, 2}, 'b': {2, 3}, 'c': {1}})
        >>> print(s.as_columns().to_string(index=False))
        a  b  c
        1  2  1
        2  3
        '''
        keys = self.dict_of_sets.keys()
        max_len = max([len(self.dict_of_sets[k]) for k in keys])
        df = pandas.DataFrame(columns=keys)
        for k in keys:
            base = [''] * max_len
            values = [str(v) for v in self.dict_of_sets[k]]
            base[0:len(values)] = values
            df[k] = base
        return df

    def as_strings(self):
        pass