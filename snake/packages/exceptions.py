class GameOver(Exception):

    def __init__(self,message: str) -> None:
        self._message = message
    
    def __str__(self):
        return f"Game over! {self._message}"
