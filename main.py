import time
import concurrent.futures

from scrapeIt import *

def do_something(seconds):
    print(f'Sleeping {seconds} second(s)...')
    time.sleep(seconds)
    return f'Done Sleeping...{seconds}'


if __name__ == '__main__':
     
    img_url = ["https://cdn.discordapp.com/attachments/1070930778780868658/1103512206240382986/image.png",
               "https://cdn.discordapp.com/attachments/1070930778780868658/1103512206240382986/image.png",
               "https://cdn.discordapp.com/attachments/1070930778780868658/1103513651727577108/image.png",
               "https://cdn.discordapp.com/attachments/1070930778780868658/1103500447190356039/image.png",
               "https://media.discordapp.net/attachments/1070930778780868658/1103500407864574103/image.png",
               "https://cdn.discordapp.com/attachments/1070930778780868658/1103500333654745128/image.png",
               "https://cdn.discordapp.com/attachments/1070930778780868658/1103499317874020422/image.png"]
    
    print('working on it...')

    
    start = time.perf_counter()

    with concurrent.futures.ProcessPoolExecutor() as executor:
        # get_usernames(img_url)
        
        # as_completed - in order it is completed
        # future = [executor.submit(get_usernames, url) for url in img_url]
        # for f in concurrent.futures.as_completed(future):
        #     print(f)




        # map method - iterates in order of the list
        results = executor.map(get_usernames, img_url)
        for result in results:
            print(results)

    finish = time.perf_counter()

    print(f'Finished in {round(finish-start, 2)} second(s)')

    