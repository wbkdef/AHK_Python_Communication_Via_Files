
from datetime import date, timedelta
import random
import easygui
import math
import re

from flexible_logger import log
from decorators import pre_process_inputs
from machine_learning_lib import random_round



# ---------------------------------- REVIEW SCHEDULE STRINGS --------------------------------------

def _get_todo_date(date):
    return "t" + "{:%y%m%d}".format(date)
    # https://docs.python.org/3.5/library/datetime.html#strftime-strptime-behavior

def get_review_schedule_basic(start_gap, mult, priority_tags='True'):
    start_gap = int(start_gap)
    mult = float(mult)
    priority_tags = {'True':True, 'False':False}[priority_tags]

    rts = ReviewsTimeStepper(start_gap, mult)
    if priority_tags:
        spg = SearchPriorityGetter()
    else:
        spg = SearchPriorityGetterDummy()
    return _get_review_schedule_general(rts, spg)


def _get_review_schedule_general(reviews_time_stepper, search_priority_getter=None, start_date=None, max_num_dates=20):
    td = date.today()
    if start_date is None:
        curr_date = td
    else:
        curr_date = start_date
    if search_priority_getter is None:
        search_priority_getter = SearchPriorityGetter()
    todo_dates = ""
    num_date = 0
    twenty_yrs = td.replace(td.year + 20)
    while curr_date < twenty_yrs and num_date < max_num_dates:
        step = reviews_time_stepper.get_next_days_step()
        curr_date += timedelta(step)
        if todo_dates != '':
            todo_dates += search_priority_getter.get_priority_tag(step, left_padding=' ')
        num_date += 1
        todo_dates += " " + _get_todo_date(curr_date)
    todo_dates += " " + search_priority_getter.get_finishing_priority_tag() + reviews_time_stepper.get_end_tag()
    return todo_dates


class ReviewsTimeStepper:
    def __init__(self, start_days_gap=1, mult=2, randomize=True):
        self.days_gap = start_days_gap
        self.mult = mult
        self.randomize = randomize

    def get_next_days_step(self):
        step = self.days_gap
        self._update_days_gap()
        return step

    def _update_days_gap(self):
        self.days_gap *= self.mult
        self.days_gap =  random_round(self.days_gap)
        if self.randomize:
            self._perturb_gap()

    def _perturb_gap(self):
        if self.days_gap <= 2:
            return
        self.days_gap += random.randint(-1, 1)

    def get_end_tag(self):
        return " rm%s" % self.mult

class SearchPriorityGetterDummy:
    def get_priority_tag(self, next_gap, left_padding=''):
        return ''

    def get_finishing_priority_tag(self):
        return ''

class SearchPriorityGetter:
    def __init__(self):
        self.thresholds_and_tags = [
            (8, "tp1"),
            (25, "tp2"),
            (125, "tp3"),
            (625, "tp4"),
            (3000, "tp5"),
            (15000, "tp6"),
        ]

    def get_priority_tag(self, next_gap, left_padding=''):
        if len(self.thresholds_and_tags) == 0 or next_gap <= self.thresholds_and_tags[0][0]:
            return ''
        theshold, tag = self.thresholds_and_tags.pop(0)
        return left_padding + tag

    def get_finishing_priority_tag(self):
        return self.get_priority_tag(1000000)




# if __name__ == '__main__':
#     rs = get_review_schedule_basic('5', '3', 'False')
#     print("\n\n--- rs: ---\n", rs, "\n------------\n")
#
#     rts = ReviewsTimeStepper()
#     spg = SearchPriorityGetter()
#     rs = _get_review_schedule_general(rts, spg)
#     print("\n\n--- rs: ---\n", rs, "\n------------\n")














# ---------------------------------- SEARCH STRINGS ---------------------------------------------

# Get search strings for Evernote
def _make_last_digit_all_values_less_last_digit_joined(s, join_with=' '):
    vals = _make_last_digit_all_values_less_last_digit(s)
    string = join_with.join(vals)
    return string

def _make_last_digit_all_values_less_last_digit(s):
    s_template = s[:-1] + '%s'
    s_end = int(s[-1:])
    vals = [s_template%i for i in range(s_end)]
    return vals

def get_search_str_evernote(date_shift=0):
    search_str = _get_search_str_non_regex(date_shift, ' ')
    return 'any: ' + search_str

def get_search_str_onenote(date_shift=0):
    search_str = _get_search_str_non_regex(date_shift, ' OR ')
    search_str = re.sub(r'OR\s*OR', 'OR', search_str)
    # log(search_str, 1)
    return search_str

def _make_last_digit_of_str_one_less(s):
    s_start = s[:-1]
    s_end = int(s[-1:])
    if s_end == 0:
        return None
    else:
        return s_start + str(s_end-1)

@pre_process_inputs(int)
def get_search_str_excel(code, todo_date=None):
    log("in get_search_str_excel, code is %s" % (code), 5)
    if todo_date == None:
        todo_date = _get_todo_date(date.today())
    log("in get_search_str_excel, code is %s, todo_date is %s" % (code, todo_date), 5)

    if code == 1:
        log("in if", 5)
        result = todo_date
    elif code == 2:
        log("in elif", 5)
        result = _make_last_digit_of_str_one_less(todo_date)
    else:
        log("in else", 5)
        result = _make_last_digit_of_str_one_less(todo_date[:2-code])
    log("in get_search_str_excel, code is %s, result is %s" % (code, result), 5)
    return result

# __A:  It's missing the decorator so the input is converted to an integer!
# __Q:  Fix this  t160328 t160330 t160403 t160409 tp1 t160419 t160505 t160528 tp2 t160701 t160822 t161108 t170304 tp3 t170824 t180511 t190604 t210108 tp4 t230604 t270110 t320606 t400716 tp5 rm1.5
def deliberate_practice_get_search_str_excel(code, todo_date=None):
    if todo_date == None:
        todo_date = _get_todo_date(date.today())
    if code == 1:
        result = todo_date
    elif code == 2:
        result = _make_last_digit_of_str_one_less(todo_date)
    else:
        result = _make_last_digit_of_str_one_less(todo_date[:2-code])
    return result


def _get_search_str_non_regex(date_shift, joiner):
    search_substrs = _get_search_dates_non_regex(date_shift, joiner)
    search_str = joiner.join(search_substrs)
    return search_str


def _get_search_dates_non_regex(date_shift, join_with):
    date_shift = int(date_shift)
    last_date = date.today() + timedelta(date_shift)
    todo_date = _get_todo_date(last_date)
    yrs = _make_last_digit_all_values_less_last_digit(todo_date[:3])
    search_substrs = [yrs[-1]]  # Only go back to the previous year
    for sub_date in [todo_date[:i] for i in range(4, 8)]:
        search_substrs.append(_make_last_digit_all_values_less_last_digit_joined(sub_date, join_with))
    search_substrs.append(todo_date)
    return search_substrs


# Get search strings for Sublime/PyCharm

def _make_given_digit_all_values_less_than_current_val_regex(s, index):
    s_start = s[:index]
    s_end = s[index:][1:]
    s_val_to_regex = int(s[index])
    if s_val_to_regex == 0:
        return None
    elif s_val_to_regex == 1:
        regex = str('0')
    else:
        regex = '[0-%s]' % (s_val_to_regex-1)
    combined = s_start + regex + '\d' * len(s_end)
    return combined

def _get_priority_restrictions_regex(max_priority):
    """Returns something like:
    ((?!.*tp)|(?=.*tp[0-2]))"""
    return "((?!.*tp)|(?=.*tp[0-%s]))" % max_priority

def _get_search_str_regex_main_body(join_with, last_date):
    """Returns something like:
    (t1[0-5]\d\d\d\d|t160[0-2]\d\d|t16030\d|t16031[0-3])"""
    todo_date = _get_todo_date(last_date + timedelta(1))
    # yrs = _make_last_digit_all_values_less_last_digit(todo_date[:3])
    # search_substrs = [yrs[-1]] #Only go back to the previous year
    search_substrs = []
    for i in range(2, 7):
        regexed_date_i = _make_given_digit_all_values_less_than_current_val_regex(todo_date, i)
        if regexed_date_i is not None:
            search_substrs.append(regexed_date_i)
    # search_substrs.append(todo_date)
    search_str = join_with.join(search_substrs)
    search_str = "(%s)" % search_str
    return search_str

def _get_search_str_regex(max_priority=None, peek_next_day=True, last_date=date.today(), join_with='|'):  # implement max_priority todo_2016_02_19
    """Returns something like:
    ((t1[0-5]\d\d\d\d|t160[0-2]\d\d|t16030\d|t16031[0-3])((?!.*tp)|(?=.*tp[0-2]))|t160314(?!.*tp))"""
    next_day = last_date + timedelta(1)
    # easygui.msgbox('_get_search_str_regex')
    search_str = _get_search_str_regex_main_body(join_with, last_date)
    if max_priority is not None:
        search_str += _get_priority_restrictions_regex(max_priority)
    if peek_next_day:
        next_day = _get_todo_date(next_day)
        next_day_no_priority = next_day + "(?!.*tp)"
        search_str = '(%s|%s)' % (search_str, next_day_no_priority)
    # easygui.msgbox('search_str is ' + search_str)
    return search_str

def get_search_str_sublime(peek='True', max_priority=1):
    # easygui.msgbox('get_search_str_sublime ')
    max_priority = int(max_priority)
    # date_shift = int(date_shift)
    peek = {'True':True, 'False':False}[peek]
    # last_date = date.today() + timedelta(date_shift)
    return _get_search_str_regex(max_priority, peek)

# def get_search_str_sublime(date_shift=0, max_priority=None):
#     max_priority = int(max_priority)
#     date_shift = int(date_shift)
#     last_date = date.today() + timedelta(date_shift)
#     return _get_search_str_regex(max_priority, last_date)

# OLD2016-03-13
# def _get_search_str_regex(max_priority=None, last_date=date.today(), join_with='|'):  # implement max_priority todo_2016_02_19
#     # if last_date is None:
#     #     last_date = date.today()
#     todo_date = _get_todo_date(last_date)
#     yrs = _make_last_digit_all_values_less_last_digit(todo_date[:3])
#     search_substrs = [yrs[-1]] #Only go back to the previous year
#     for i in range(1, 7):
#         regexed_date_i = _make_given_digit_all_values_less_than_current_val_regex(todo_date, i)
#         if regexed_date_i is not None:
#             search_substrs.append(regexed_date_i)
#     search_substrs.append(todo_date)
#     search_str = join_with.join(search_substrs)
#     search_str = "(%s)" % search_str
#     if max_priority is not None:
#         search_str += _get_priority_restrictions_regex(max_priority)
#     return search_str

# if __name__ == '__main__':
#     re3 = _make_given_digit_all_values_less_than_current_val_regex('t60214', 3)
#     re4 = _make_given_digit_all_values_less_than_current_val_regex('t60214', 4)
#     print("\n\n--- re3, re4: ---\n", re3, re4, "\n------------\n")
#     last_digit_all_values = get_search_str_sublime()
#     print("\n\n--- last_digit_all_values: ---\n", last_digit_all_values, "\n------------\n")





# ---------------------------------- TODO DATE STRINGS ---------------------------------------------

class TodoDate:
    def __init__(self):
        self.todo_date = date.today()
        self.increment_mode = "days"
        self.last_increment = 1

    DAYS = "days"
    WEEKS = "weeks"
    MONTHS = "months"
    BEG_OF_MONTHS = "beg_of_months"
    QUARTERS = "quarters"
    YEARS = "years"
    REVIEW = "review"
    SEARCH = "search"
    MODES = {DAYS, WEEKS, MONTHS, BEG_OF_MONTHS, QUARTERS, YEARS, REVIEW, SEARCH}

    def reset_to_defaults(self):
        self.todo_date = date.today()
        self.increment_mode = "days"
        self.last_increment = 1

    def set_increment_mode(self, mode):
        if mode not in TodoDate.MODES:
            easygui.msgbox("invalide mode passed to method set_increment_mode: %s" % mode)
            return
        self.increment_mode = mode

    def _increment_by_days(self, n): self.todo_date += timedelta(n)
    def _go_forward_to_day_of_month_or_last_day_of_month(self, day):
        self.todo_date.replace(day=min(day, 28))
        while self.todo_date.day < day:
            self.todo_date += timedelta(1)
            if self.todo_date.day == 1:
                self.todo_date -= timedelta(1)
                return
    def _increment_by_months(self, n):
        day = self.todo_date.day
        self._increment_by_beg_of_months(n)
        self._go_forward_to_day_of_month_or_last_day_of_month(day)
    def _increment_by_beg_of_months(self, n):
        month = self.todo_date.month + n
        year = self.todo_date.year
        all_months = year * 12 + month  # check
        year, month = year + (month - 1) // 12, (month - 1) % 12 + 1
        assert all_months == year * 12 + month  # check
        self.todo_date = date(year, month, 1)

    def repeat_prev_increment(self, repeats=1):
        repeats = int(repeats)
        dates = ''.join([self.increment_and_get_todo_date(self.last_increment) for n in range(repeats)])
        if repeats > 1:
            dates += ' every%s%s' % (self.last_increment, self.increment_mode)
        return dates

    def increment_and_get_todo_date(self, i):
        i = int(i)
        if self.increment_mode in TodoDate.DAYS: self._increment_by_days(i)
        if self.increment_mode == TodoDate.WEEKS: self._increment_by_days(i * 7)
        if self.increment_mode == TodoDate.MONTHS: self._increment_by_months(i)
        if self.increment_mode == TodoDate.BEG_OF_MONTHS: self._increment_by_beg_of_months(i)
        if self.increment_mode == TodoDate.QUARTERS: self._increment_by_months(i * 3)
        if self.increment_mode == TodoDate.YEARS: self._increment_by_months(i * 12)
        self.last_increment = i
        return self.get_todo_date()

    def get_todo_date(self):
        return " " + _get_todo_date(self.todo_date)

todo_date = TodoDate()

if __name__ == '__main__':
    print("\n\n--- todo_date.get_todo_date(): ---\n", todo_date.get_todo_date(), "\n------------\n")
    print("\n\n--- todo_date.increment_and_get_todo_date(3): ---\n", todo_date.increment_and_get_todo_date(3), "\n------------\n")
    # todo_date.set_increment_mode_months()
    # print("\n\n--- todo_date.increment_and_get_todo_date(2): ---\n", todo_date.increment_and_get_todo_date(2), "\n------------\n")
# _get_review_schedule_general()


  # t160305 Make questions on what I learned in this file!