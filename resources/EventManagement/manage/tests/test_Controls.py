# -*- coding: utf-8 -*-
# test_Controls.py
#

# import pytests

from manage import Controls as CTR

def test_validate_user_list(verbose=False):
    corr_val1 = "('dummy', 'Entry')"
    corr_val2 = "('dummy', 'Entry'), ('foo', 'list'), "
    lst_val1 = "'dummy', 'Entry'"
    lst_val2 = "'dummy', 'Entry', 'foo', 'bar', "
    lst_val3 = "'cat chenal', 'will tell', "

    which = ['Corrections','Corrections','Names','Places','People']
    for i,data in enumerate([corr_val1, corr_val2, lst_val1, lst_val2, lst_val3]):
        out, msg = CTR.validate_user_list(data, which[i], verbose)
        print(data, which, ':\n\t', msg, out)
        assert msg == 'OK'
        
    #new tests:
    out, msg = CTR.validate_user_list(lst_val1, 'Corrections', verbose)
    print('\nList instead of tuples for Corrections.\n', lst_val1, ':\n\t', msg, out)
    assert out is None
    out, msg = CTR.validate_user_list(corr_val1, 'Upper', verbose)
    print('Tuple instead of list for Upper.\n',corr_val1, ':\n\t', msg, out) 
    assert out is None