import requests, sys, random, time
from threading import Thread
from colorama import init, Fore
from queue import Queue

init()
#Colorama
RED = Fore.RED
BLUE = Fore.BLUE
GREEN = Fore.GREEN
YELLOW = Fore.YELLOW
RESET = Fore.RESET

q = Queue()

def ClownLogo():
    from colorama import init, Fore
    import sys, random, time
    init()
    clear = "\x1b[0m"
    colors = [36, 32, 34, 35, 31, 37]

    x = """

     ____     __      __                _        ____                          
    / __/_ __/ /  ___/ /__  __ _  ___ _(_)__    / __/______ ____  ___  ___ ____
   _\ \/ // / _ \/ _  / _ \/  ' \/ _ `/ / _ \  _\ \/ __/ _ `/ _ \/ _ \/ -_) __/
  /___/\_,_/_.__/\_,_/\___/_/_/_/\_,_/_/_//_/ /___/\__/\_,_/_//_/_//_/\__/_/   
                                                                             
     CS! : Escanea todos los subdominios de los sitios web que desees UwU       
    """
    for N, line in enumerate(x.split("\n")):
         sys.stdout.write("\x1b[1;%dm%s%s\n" % (random.choice(colors), line, clear))
         time.sleep(0.05)

def scan_subdomains(domain):
    global q
    while True:
        # get the subdomain from the queue
        subdomain = q.get()
        # scan the subdomain
        url = f"http://{subdomain}.{domain}"
        try:
            requests.get(url)
        except requests.ConnectionError:
            pass
        else:
            print(f"{RED}[{BLUE}+{RED}] {GREEN}Discovered subdomain:{YELLOW}", url)

        # we're done with scanning that subdomain
        q.task_done()


def main(domain, n_threads, subdomains):
    global q

    # fill the queue with all the subdomains
    for subdomain in subdomains:
        q.put(subdomain)

    for t in range(n_threads):
        # start all threads
        worker = Thread(target=scan_subdomains, args=(domain,))
        # daemon thread means a thread that will end when the main thread ends
        worker.daemon = True
        worker.start()


if __name__ == "__main__":
    import argparse
    ClownLogo()
    parser = argparse.ArgumentParser(description="Subdomain Scanner using excelent")
    parser.add_argument("domain", help="Domain to scan for subdomains without protocol (e.g without 'http://' or 'https://')")
    parser.add_argument("-l", "--wordlist", help="File that contains all subdomains to scan, line by line. Default is subdomains.txt",
                        default="subdomains.txt")
    parser.add_argument("-t", "--num-threads", help="Number of threads to use to scan the domain. Default is 10", default=10, type=int)
    
    args = parser.parse_args()
    domain = args.domain
    wordlist = args.wordlist
    num_threads = args.num_threads

    main(domain=domain, n_threads=num_threads, subdomains=open(wordlist).read().splitlines())
    q.join()