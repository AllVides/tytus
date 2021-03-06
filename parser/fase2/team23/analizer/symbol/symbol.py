class Symbol:
    """
    Esta clase representa los simbolos que producen los resultados
    de las diferentes ejecuciones (execute()) de las instrucciones y
    expresiones.
    """

    def __init__(self, value, type_, row, column, col_creada, cons) -> None:
        self.value = value
        self.type = type_
        self.row = row
        self.column = column
        self.col_creada = col_creada
        self.cons = cons

