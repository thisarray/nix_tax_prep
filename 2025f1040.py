"""Form 1040 U.S. Individual Income Tax Return 2025."""

import form

class Federal(form.Form):
    def __init__(self):
        super().__init__(__doc__)

        # Standard deduction
        self['12e'] = 15750

    def calculate(self):
        """Update the form lines with 1040 calculations."""
        # Add lines 1a through 1h.
        self['1z'] = self['1a'] + self['1b'] + self['1c'] + self['1d'] + self['1e'] + self['1f'] + self['1g'] + self['1h']
        # Total income. Add lines 1z, 2b, 3b, 4b, 5b, 6b, 7a, and 8.
        self[9] = self['1z'] + self['2b'] + self['3b'] + self['4b'] + self['5b'] + self['6b'] + self['7a'] + self[8]
        # Adjusted gross income. Subtract line 10 from line 9.
        self['11a'] = self[9] - self[10]
        # Amount from line 11a (adjusted gross income).
        self['11b'] = self['11a']

        # Add lines 12e, 13a, and 13b.
        self[14] = self['12e'] + self['13a'] + self['13b']

        # Taxable income. Subtract line 14 from line 11b.
        # If zero or less, enter -0-.
        self[15] = self['11b'] - self[14]
        if self[15] <= 0:
            self[15] = 0

        # Add lines 16 and 17.
        self[18] = self[16] + self[17]

        # Add lines 19 and 20.
        self[21] = self[19] + self[20]

        # Subtract line 21 from line 18. If zero or less, enter -0-.
        self[22] = self[18] - self[21]
        if self[22] <= 0:
            self[22] = 0

        # Total tax. Add lines 22 and 23.
        self[24] = self[22] + self[23]

        # Add lines 25a through 25c.
        self['25d'] = self['25a'] + self['25b'] + self['25c']

        # Add lines 27a, 28, 29, 30, and 31.
        # These are your total other payments and refundable credits.
        self[32] = self['27a'] + self[28] + self[29] + self[30] + self[31]

        # Total payments. Add lines 25d, 26, and 32.
        self[33] = self['25d'] + self[26] + self[32]

        # If line 33 is more than line 24, subtract line 24 from line 33.
        # This is the amount you overpaid.
        if self[33] > self[24]:
            self[34] = self[33] - self[24]

        # Amount you owe. Subtract line 33 from line 24.
        self[37] = self[24] - self[33]

if __name__ == '__main__':
    federal = Federal()
    federal.print()
