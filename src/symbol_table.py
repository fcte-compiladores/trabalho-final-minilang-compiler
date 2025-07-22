class Symbol:
    def __init__(self, name, type, value=None):
        self.name = name
        self.type = type
        self.value = value

    def __repr__(self):
        return f"<Symbol: {self.name}, Type: {self.type}, Value: {self.value}>"

class SymbolTable:
    def __init__(self, parent=None):
        self.symbols = {}
        self.parent = parent

    def define(self, symbol):
        if symbol.name in self.symbols:
            raise Exception(f"Símbolo '{symbol.name}' já definido neste escopo.")
        self.symbols[symbol.name] = symbol

    def resolve(self, name):
        symbol = self.symbols.get(name)
        if symbol:
            return symbol
        if self.parent:
            return self.parent.resolve(name)
        return None

    def __repr__(self):
        return f"<SymbolTable: {self.symbols.keys()}, Parent: {self.parent is not None}>"


