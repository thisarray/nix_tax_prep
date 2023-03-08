"""Form 1040 U.S. Individual Income Tax Return 2022."""

import form

class Federal(form.Form):
    def __init__(self):
        super(Federal, self).__init__(__doc__)

        # Standard deduction
        self[12] = 12950

    def calculate(self):
        """Update the form lines with 1040 calculations."""
        # Add lines 1a through 1h.
        self['1z'] = self['1a'] + self['1b'] + self['1c'] + self['1d'] + self['1e'] + self['1f'] + self['1g'] + self['1h']
        # Total income. Add lines 1z, 2b, 3b, 4b, 5b, 6b, 7, and 8.
        self[9] = self['1z'] + self['2b'] + self['3b'] + self['4b'] + self['5b'] + self['6b'] + self[7] + self[8]
        # Adjusted gross income. Subtract line 10 from line 9.
        self[11] = self[9] - self[10]

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

        # Add lines 27, 28, 29, and 31.
        # These are your total other payments and refundable credits.
        self[32] = self[27] + self[28] + self[29] + self[31]

        # Total payments. Add lines 25d, 26, and 32.
        self[33] = self['25d'] + self[26] + self[32]

        # If line 33 is more than line 24, subtract line 24 from line 33.
        # This is the amount you overpaid.
        if self[33] > self[24]:
            self[34] = self[33] - self[24]

        # Amount you owe. Subtract line 33 from line 24.
        self[37] = self[24] - self[33]

class Estimated(form.Form):
    def __init__(self, federal):
        super(Estimated, self).__init__('2023 Estimated Tax Worksheet')

        self.federal = federal
        """Form 1040 upon which this worksheet is based."""

        # Standard deduction
        self['2a'] = 13850
        self[7] = self.federal[21]
        self['12b'] = self.federal[24]

    def calculate(self):
        """Update the form lines with worksheet calculations."""
        self['2c'] = self['2a'] + self['2b']
        self[3] = self[1] - self['2c']

        self[6] = self[4] + self[5]

        self[8] = self[6] - self[7]
        if self[8] <= 0:
            self[8] = 0

        self['11a'] = self[8] + self[9] + self[10]

        # Total 2023 estimated tax
        self['11c'] = self['11a'] - self['11b']
        if self['11c'] <= 0:
            self['11c'] = 0

        self['12a'] = self['11c'] * Decimal('0.90')
        self['12c'] = min(self['12a'], self['12b'])

        self['14a'] = self['12c'] - self[13]
        self['14b'] = self['11c'] - self[13]

        self[15] = (self['14a'] / 4) - self.federal[36]

if __name__ == '__main__':
    federal = Federal()
    federal.print()
