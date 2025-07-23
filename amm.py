class AMM:
    def __init__(self, token_reserve, base_reserve, fee=0.003):
        self.xr, self.yr = token_reserve, base_reserve
        self.fee = fee

    def get_price(self, x_in, token_to_base=True):
        in_amount = x_in * (1 - self.fee)
        if token_to_base:
            return self.yr - (self.xr * self.yr) / (self.xr + in_amount)
        else:
            return self.xr - (self.xr * self.yr) / (self.yr + in_amount)

    def swap(self, x_in, token_to_base=True):
        y_out = self.get_price(x_in, token_to_base)
        if token_to_base:
            self.xr += x_in
            self.yr -= y_out
        else:
            self.yr += x_in
            self.xr -= y_out
        return y_out

    def add_liquidity(self, dx, dy):
        self.xr += dx
        self.yr += dy