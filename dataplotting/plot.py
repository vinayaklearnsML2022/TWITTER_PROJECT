# importing libraries 
import matplotlib.pyplot as plt 
from matplotlib import font_manager as fm
tamil = fm.FontProperties(fname = "D:/twitter_project/lang/NotoSerifTamil-VariableFont_wdth,wght.ttf")
                              
import seaborn as sns
import numpy as np


 # define Seaborn color palette to use 
palette_color = sns.color_palette('bright') 

# def initialisefigandaxis():
    


def plotpie(data:int,keys:str,title:str):
    # plotting data on chart 
    fig,ax = plt.subplots()
    fig.suptitle("tweet search sentiment")
    ax.pie(data, labels=keys, colors=palette_color, startangle=90,autopct='%.0f%%') 
    # displaying chart 
    ax.set_title(title)
    plt.show( )
    fig.savefig('sentiment.png',bbox_inches='tight')   # save the figure to file
    plt.close(fig)


def plotlc(tweets:int,dates:str,title:str):
    
    # plotting data on chart 
    # encoded_string = title.encode("utf-8")
    fig,ax = plt.subplots()
    fig.suptitle(title,fontproperties=tamil)
    ax.plot(dates, tweets) 
    # displaying chart 
    ax.set_title("Max Tweet Count " +str(max(tweets))+ " on " +str(dates[np.argmax(tweets)]))
    ax.set_ylim(0,max(tweets)*1.25)
    ax.axhline(max(tweets),ls="--", c="grey")
    plt.xticks(rotation=45)
    plt.show( )
    fig.savefig('tweetcount.png',bbox_inches='tight')   # save the figure to file
    plt.close(fig)
   