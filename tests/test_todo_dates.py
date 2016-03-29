from todo_dates import get_search_str_excel

def test_get_search_str_excel():
    todo_date = 't60327'
    assert get_search_str_excel(1, todo_date) == 't60327'
    assert get_search_str_excel(2, todo_date) == 't60326'
    assert get_search_str_excel(3, todo_date) == 't6031'
    assert get_search_str_excel(4, todo_date) == 't602'
    assert get_search_str_excel(5, todo_date) == None
    assert get_search_str_excel(6, todo_date) == 't5'

    # assert get_search_str_excel(1) == 't60327'
    # assert get_search_str_excel(2) == 't60326'
    # assert get_search_str_excel(3) == 't6031'
    # assert get_search_str_excel(4) == 't602'
    # assert get_search_str_excel(5) == None
    # assert get_search_str_excel(6) == 't5'
