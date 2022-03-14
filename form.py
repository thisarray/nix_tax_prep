"""Python 3 form library module."""

import collections.abc
from decimal import Decimal, InvalidOperation
import unittest

MAX_LINE_NUMBER = 1000
"""Integer arbitrary largest line number for natural sort."""

TWO_PLACES = Decimal(10) ** -2
"""Decimal constant for rounding to 2 decimal places."""

WIDTH = 79
"""Integer width of the border between the form name and its lines."""

ZERO = Decimal(0)
"""Decimal constant for zero (0)."""

class Form(collections.abc.MutableMapping):
    """A form is a mapping that indexes a value by line number."""

    def __init__(self, name):
        """Create an empty Form instance named name.

        Args:
            name: String name of the form.
        """
        if not isinstance(name, str):
            raise TypeError('name must be a non-empty string.')
        if len(name) <= 0:
            raise ValueError('name must be a non-empty string.')

        self.name = name
        """String name of the form."""

        self.backing = {}
        """Dictionary backing store delegate of the form."""

    def __str__(self):
        """Return the string name of the form."""
        return self.name

    @staticmethod
    def _line_number_to_key(line_number):
        """Return line_number converted to a valid string key in backing."""
        if isinstance(line_number, int):
            return str(line_number)
        if isinstance(line_number, str):
            if len(line_number) <= 0:
                raise ValueError('line_number cannot be an empty string.')
            return line_number
        raise TypeError('Unrecognized type for line_number.')

    @staticmethod
    def _natural_sort_key(line_number):
        """Return a tuple from line_number to sort line numbers humanly."""
        i = len(line_number)
        while i > 0:
            if line_number[:i].isdigit():
                return (int(line_number[:i]), line_number[i:])
            i -= 1
        return (MAX_LINE_NUMBER, line_number)

    def __getitem__(self, line_number):
        """Return the value on line_number in this form or ZERO."""
        key = Form._line_number_to_key(line_number)
        if key in self.backing:
            return self.backing[key]
        return ZERO

    def __setitem__(self, line_number, value):
        """Set the value on line_number in this form to value."""
        key = Form._line_number_to_key(line_number)
        if isinstance(value, bool):
            pass
        elif not isinstance(value, Decimal):
            try:
                value = Decimal(value)
            except InvalidOperation:
                pass
        self.backing[key] = value

    def __delitem__(self, line_number):
        """Delete the value on line_number from this form."""
        key = Form._line_number_to_key(line_number)
        if key in self.backing:
            del self.backing[key]

    def __iter__(self):
        """Return an iterator for the lines in this form in ascending order."""
        # Find the set of line numbers without a value set
        missing_set = set(range(1, len(self) + 1))
        for line_number in self.backing.keys():
            value = Form._natural_sort_key(line_number)[0]
            if value < MAX_LINE_NUMBER:
                missing_set.discard(value)

        # Build the list of all line numbers including those without a value
        keys = list(self.backing.keys()) + [str(i) for i in missing_set]
        keys.sort(key=Form._natural_sort_key)

        return iter(keys)

    def __len__(self):
        """Return the largest numeric line number with a value set.

        This differs from the traditional notion of length!
        """
        line_numbers = list(self.backing.keys())
        line_numbers.sort(key=Form._natural_sort_key, reverse=True)
        for line_number in line_numbers:
            value = Form._natural_sort_key(line_number)[0]
            if value < MAX_LINE_NUMBER:
                return value
        return 0

    def calculate(self):
        """Update the form with calculations."""
        pass

    def print(self):
        """Print the form name and all its lines."""
        self.calculate()

        width = max(len(key) for key in self)

        print(self.name)
        print('-' * WIDTH)
        for key in self:
            print('{key:>{width}}: {value}'.format(
                key=key, value=self[key], width=width))


class _UnitTest(unittest.TestCase):
    def test_line_number_to_key(self):
        """Test converting a line number to a valid key."""
        for value in [None, 42.0, [], {}]:
            self.assertRaises(TypeError, Form._line_number_to_key, value)
        self.assertRaises(ValueError, Form._line_number_to_key, '')
        self.assertEqual(Form._line_number_to_key(False), 'False')
        self.assertEqual(Form._line_number_to_key(True), 'True')
        self.assertEqual(Form._line_number_to_key(42), '42')
        self.assertEqual(Form._line_number_to_key('42'), '42')
        self.assertEqual(Form._line_number_to_key('42a'), '42a')
        self.assertEqual(Form._line_number_to_key('foobar'), 'foobar')

    def test_natural_sort_key(self):
        """Test the key function for natural sort."""
        self.assertEqual(Form._natural_sort_key('0'), (0, ''))
        self.assertEqual(Form._natural_sort_key('2'), (2, ''))
        self.assertEqual(Form._natural_sort_key('4'), (4, ''))
        self.assertEqual(Form._natural_sort_key('42'), (42, ''))
        self.assertEqual(Form._natural_sort_key('42a'), (42, 'a'))
        self.assertEqual(Form._natural_sort_key('42b'), (42, 'b'))
        self.assertEqual(Form._natural_sort_key('foobar'),
                         (MAX_LINE_NUMBER, 'foobar'))
        self.assertEqual(
            sorted(['foo', 'bar', '42a', '4', '42b'],
                   key=Form._natural_sort_key),
            ['4', '42a', '42b', 'bar', 'foo'])

    def test_form(self):
        """Test the Form class."""
        for value in [None, 42.0, [], {}]:
            self.assertRaises(TypeError, Form, value)
        self.assertRaises(ValueError, Form, '')

        form = Form('foobar')
        self.assertEqual(form.name, 'foobar')
        self.assertEqual(form.backing, {})
        self.assertEqual(str(form), 'foobar')
        self.assertEqual(form[42], ZERO)
        self.assertEqual(len(form), 0)

        form[42] = 'baz'
        self.assertEqual(form.backing, {'42': 'baz'})
        self.assertEqual(form[42], 'baz')
        self.assertEqual(len(form), 42)
        del form[42]
        self.assertEqual(form.backing, {})
        self.assertEqual(form[42], ZERO)
        self.assertEqual(len(form), 0)
        form[42] = 0
        self.assertEqual(form.backing, {'42': ZERO})
        self.assertEqual(form[42], ZERO)
        self.assertEqual(len(form), 42)
        for value in [13, 13.0, Decimal('13')]:
            form[42] = value
            self.assertEqual(form.backing, {'42': Decimal(13)})
            self.assertEqual(form[42], Decimal(13))
            self.assertEqual(len(form), 42)
        form[13] = True
        self.assertEqual(form.backing, {'13': True, '42': Decimal(13)})
        self.assertEqual(form[13], True)
        self.assertEqual(form[42], Decimal(13))
        self.assertEqual(len(form), 42)
        self.assertEqual(list(form), [str(i) for i in range(1, 43)])

        form['foobar'] = False
        self.assertEqual(form.backing, {'13': True, '42': Decimal(13),
                                        'foobar': False})
        self.assertEqual(form[13], True)
        self.assertEqual(form[42], Decimal(13))
        self.assertEqual(form['foobar'], False)
        self.assertEqual(len(form), 42)
        self.assertEqual(list(form),
                         [str(i) for i in range(1, 43)] + ['foobar'])

if __name__ == '__main__':
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(_UnitTest)
    unittest.TextTestRunner(verbosity=2).run(suite)
