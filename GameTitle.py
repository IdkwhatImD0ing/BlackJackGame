'''
Created on 6 February 2019; Last edited on 4 March 2019

@author: Bill Zhang
'''
from TitleScreen import title
import settings


def main():
    settings.init()  #Loads all the variables require for this game

    program = title()

    program.window.mainloop(
    )  #Launches the mainloop of the title select screen


if __name__ == "__main__":
    main()
