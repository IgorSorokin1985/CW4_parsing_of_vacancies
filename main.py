import datetime
from src.utils import Userinput
from src.classes import SuperJobAPI

#if __name__ == "__main__":
#    userinput = Userinput()
#    userinput()

sj = SuperJobAPI()
sj.get_vacancies()
#sj.get_areas()