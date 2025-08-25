import pygame

class CantControlObject(Exception):
    """ Raised when object has no controllable object attributes """
    def __init__(self, message="Uh oh.., I Can't control this object!."):
        super().__init__(message)


def controller_validation(func):
    """ Controller validation decorator """
    def wrapper(self, *args, **kwargs):
        if not hasattr(self.object, "coordinates"):
            raise CantControlObject()
        return func(self, *args, **kwargs)
    return wrapper


class BitLogicController:
    """ The Main Controller of Tetromino's """
    def __init__(self, object: object, controller_name: str = "player1") -> None:
        self.temporary_object = object
        self.controller_name = controller_name

        self.rotation_index = 0

        self.object = None


    def control(self, events) -> None:
        # ? Temporary 
        grid_spawner_logic = self.temporary_object
        grid_spawner_logic.controller = self
        self.object = grid_spawner_logic.spawned_tetromino
        self.apply_controls(events)


    @controller_validation
    def move(self, dx: int, dy: int) -> None:
        """ changes object coordinates """
        self.object.change_coordinates([(x + dx, y + dy) for x, y in self.object.coordinates], dx = dx, dy = dy)
    

    @controller_validation
    def apply_controls(self, events) -> None:
        """ enable controlling of the object """
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.move(-1, 0)
                
                if event.key == pygame.K_RIGHT:
                    self.move(1, 0)

                if event.key == pygame.K_DOWN:
                    self.move(0, 1)

                if hasattr(self.object, "hard_drop"):
                    if event.key == pygame.K_SPACE:
                        self.object.hard_drop()

                if hasattr(self.object, "rotate"):
                    if event.key == pygame.K_x:
                        self.object.rotate("clock_wise")
                        self.rotation_index = (self.rotation_index + 1) % 4
                       
                    if event.key == pygame.K_z:
                        self.object.rotate("counter_clock_wise")
                        self.rotation_index = (self.rotation_index - 1) % 4

if __name__ == "__main__":
      pass

"""
TODO:
! 1. This class should only have one object attribute, as for temporary it will have its temporary_object due to hard detection of tetromino right now, change the temporary_object
!    to just object if solution was already found.
"""