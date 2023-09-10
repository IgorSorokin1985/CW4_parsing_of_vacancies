import datetime
import time
from src.utils import Userinput, Userinput_2
from src.classes import SuperJobAPI

if __name__ == "__main__":
    userinput = Userinput_2()
    userinput()

#search_from = datetime.datetime.now() - datetime.timedelta(days=30)
#unix_time = int(time.mktime(search_from.timetuple()))
#print(search_from)
#result = datetime.datetime.fromtimestamp(unix_time)
#print(result)


#datetime.datetime.fromtimestamp(vacancy_info_sj["date_published"])