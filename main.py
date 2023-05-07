import time
import concurrent.futures

from scrapeIt import *

# def do_something(seconds):
#     print(f'Sleeping {seconds} second(s)...')
#     time.sleep(seconds)
#     return f'Done Sleeping...{seconds}'


if __name__ == '__main__':

    img_url = ["https://cdn.discordapp.com/attachments/1070930778780868658/1103512206240382986/image.png",
               "https://cdn.discordapp.com/attachments/1070930778780868658/1103513651727577108/image.png",
               "https://cdn.discordapp.com/attachments/1070930778780868658/1103500447190356039/image.png",
               "https://media.discordapp.net/attachments/1070930778780868658/1103500407864574103/image.png",
               "https://cdn.discordapp.com/attachments/1070930778780868658/1103500333654745128/image.png",
               "https://cdn.discordapp.com/attachments/1070930778780868658/1103499317874020422/image.png",
               "https://media.discordapp.net/attachments/1069726036041945098/1104847976620363887/image.png?width=230&height=169",
               "https://media.discordapp.net/attachments/1069726036041945098/1103442611852820490/Screenshot_139.png?width=294&height=422",
               "https://cdn.discordapp.com/attachments/1069726036041945098/1092386889715171458/image.png",
               "https://cdn.discordapp.com/attachments/1069726036041945098/1096733105978613800/image.png",
               "https://cdn.discordapp.com/attachments/1076623943760347136/1078684006700290138/image.png",
               "https://media.discordapp.net/attachments/1076623943760347136/1095317173393698836/Screenshot_113.png?width=405&height=422",
               "https://media.discordapp.net/attachments/1076623943760347136/1103500673389183097/image.png?width=392&height=422",
               "https://media.discordapp.net/attachments/1070930778780868658/1103500333654745128/image.png?width=230&height=422",
               "https://media.discordapp.net/attachments/1076623943760347136/1103500139936632853/image.png?width=447&height=317",
               "https://media.discordapp.net/attachments/1076623943760347136/1103498722274459649/image.png?width=295&height=422",

               ]
    start = time.perf_counter()

    print('threading working on it...')
    process_links(img_url)



    # start = time.perf_counter()
    # with concurrent.futures.ProcessPoolExecutor() as executor:
#
    #     print(f'process pool working on it...')
    #     future = [executor.submit(get_usernames, url) for url in img_url]
    #     for f in concurrent.futures.as_completed(future):
    #         print(f)




        # map method - iterates in order of the list
        # results = executor.map(get_usernames, img_url)
        # for result in results:
        #     print(results)

    finish = time.perf_counter()

    print(f'Finished in {round(finish-start, 2)} second(s)')

    