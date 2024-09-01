
class EnObra:
    @classmethod
    def set(cls, obra):
        with open("./obra_actual.txt", "w", encoding="utf-8") as f:
            f.write(obra)
    
    @classmethod
    def get(cls):
        with open("./obra_actual.txt", "r", encoding="utf-8") as f:
            obra_actual = int(f.read())
        return obra_actual
    

