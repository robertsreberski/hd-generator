from os import path
import generator
import files
import conn
import time
import datetime

margin = {
    "GoscHotelowy": 0,
    "OpcjaPobytu": 0,
    "Hotel": 0,
    "Usluga": 0,
    "CennikUslugi": 0,
    "KartaHotelowa": 0,
    "ZamowienieUslugi": 0,
    "Pobyt": 0
}


def proceed(N, t1, t2, opcje_uslug):
    if t1 is None:
        t1 = t2 - datetime.timedelta(days=365 * 3)
    if t2 is None:
        t2 = t1 + datetime.timedelta(days=365 * 3)

    print("### Starting to generate ###\r\n")
    start_time = time.time()
    lists = generator.generuj(N=int(N), t1=t1, t2=t2, opcje_uslug=opcje_uslug)
    elapsed_time = time.time() - start_time
    print("### Generating has been finished ###")
    print("Total time to complete: {time}s\r\n".format(time=elapsed_time))

    saved = {}
    print("### Saving objects to .bulk files ###")

    for key, val in lists.items():
        n = margin[key]
        saved[key] = files.dump(key, list(val.values())[n:])
        margin[key] = len(val)

    print("### Saving objects has been finished ###")
    print("### Bulk inserting to DB ###\r\n")
    for key, filepath in saved.items():
        print("{key}... ".format(key=key), end='', flush=True)
        start_time = time.time()
        conn.execute_bulk(key, filepath)
        elapsed_time = time.time() - start_time
        print("Finished; time: {time}".format(time=elapsed_time))

    print("### Bulk insertion has been finished ###")


total_start = time.time()
print("### Generator has started ###")
input("Did you set correct db connection data in conn.py? [Click ENTER to continue]")
print("Recreating connected DB... ", end=' ', flush=True)
conn.recreate_all()
print("Finished")

print("### Preparing to generate objects ###")
N = input("How many hotel cards to generate? [Integer] ")
start = input("Set T1 date [YYYY-MM-DD]: ")
end = input("Set T2 date [YYYY-MM-DD][If not set, date will be today]: ")

if start.strip() == '':
    start_date = datetime.datetime.strptime('2012-12-12', "%Y-%m-%d").date()
else:
    start_date = datetime.datetime.strptime(start, "%Y-%m-%d").date()

if end.strip() == '':
    end_date = datetime.date.today()
else:
    end_date = datetime.datetime.strptime(end, "%Y-%m-%d").date()

if N.strip() == '':
    count = 50
else:
    count = int(N)/2
opcje = ['sprzatanie', 'restauracja', 'wydarzenia', 'rekreacja', 'sport', 'spa']
proceed(N=count, t1=None, t2=start_date, opcje_uslug=opcje)
input("\nT1 generated, press ENTER to continue to T2\n")
opcje.append('safari')
proceed(N=count, t1=start_date, t2=end_date, opcje_uslug=opcje)



print("### Generator work has been finished, goodbye ###")
total_elapsed = time.time() - total_start
print("Total time: {time}s".format(time=total_elapsed))