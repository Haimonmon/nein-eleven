class BitGridLogics:
    """ Collision logics """
    def __init__(self):
        self.cell_coordinates = []

    def _get_cell_coordinates(self, offset_x: int, offset_y: int) -> None: 
        """ Gets all cell coordinates storing set of x and y coordinates """
        for row in range(self.row):
            for column in range(self.columns):
                x = offset_x + column * self.cell_size
                y = offset_y + row * self.cell_size
                self.cell_coordinates.append((x, y))
    
    