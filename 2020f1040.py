"""Form 1040 U.S. Individual Income Tax Return 2020."""

import form

class Federal(form.Form):
    def __init__(self):
        super(Federal, self).__init__(__doc__)

    def calculate(self):
        """Update the form lines with 1040 calculations."""
        # Total income. Add lines 1, 2b, 3b, 4b, 5b, 6b, 7, and 8.
        self[9] = self[1] + self['2b'] + self['3b'] + self['4b'] + self['5b'] + self['6b'] + self[7] + self[8]
        # Total adjustments to income. Add lines 10a and 10b.
        self['10c'] = self['10a'] + self['10b']
        # Adjusted gross income. Subtract line 10c from line 9.
        self[11] = self[9] - self['10c']

        # Standard deduction
        self[12] = 12400

        # Add lines 12 and 13.
        self[14] = self[12] + self[13]

        # Taxable income. Subtract line 14 from line 11.
        # If zero or less, enter -0-.
        self[15] = self[11] - self[14]
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

        # Add lines 27 through 31.
        # These are your total other payments and refundable credits.
        self[32] = self[27] + self[28] + self[29] + self[30] + self[31]

        # Add lines 25d, 26, and 32. These are your total payments.
        self[33] = self['25d'] + self[26] + self[32]

        # If line 33 is more than line 24, subtract line 24 from line 33.
        # This is the amount you overpaid.
        if self[33] > self[24]:
            self[34] = self[33] - self[24]

        # Subtract line 33 from line 24. This is the amount you owe now.
        self[37] = self[24] - self[33]

if __name__ == '__main__':
    federal = Federal()
    federal.print()
