import discord
from discord.ext import commands
from discord.ext.commands import Bot
import asyncio
import time
from bs4 import BeautifulSoup
import requests
from tkinter import *

Client = discord.Client()
bot = commands.Bot(command_prefix='#')

#RETURNS THE PLAYERS CASUAL INFO
def retrievePlayerInfo(playerName, decisionVar):

    # Grabs the link using the player name
    link = 'https://r6stats.com/stats/uplay/' + playerName
    print(link)
    source = requests.get(link).text

    soup = BeautifulSoup(source, 'html.parser')

    # Sets all the variables for casual
    kills = soup.find('div', {"class": "value"})
    deaths = kills.find_next('div', {"class": "value"})
    kdRatio = deaths.find_next('div', {"class": "value"})
    hoursPlayed = kdRatio.find_next('div', {"class": "value"})
    winLossRecord = hoursPlayed.find_next('div', {"class": "value"})

    #Determine what needs to be returned for casual
    #Kills
    if decisionVar == 1:
        return kills.text
    #deaths
    elif decisionVar == 2:
        return deaths.text
    #KD
    elif decisionVar == 3:
        return kdRatio.text
    #hoursPlayed
    elif decisionVar == 4:
        return hoursPlayed.text
    #Win Loss Record
    elif decisionVar == 5:
        return winLossRecord.text
    else:
        stats = []
        stats.append(kills.text)
        stats.append(deaths.text)
        stats.append(kdRatio.text)
        stats.append(hoursPlayed.text)
        stats.append(winLossRecord.text)
        return stats

#RETURNS THE PLAYERS RANKED INFO
def retrievePlayerRankedInfo(playerName, decisionVar):
        # Grabs the link using the player name
        rankedLink = 'https://r6stats.com/stats/uplay/' + playerName + '/ranked'
        print("Ranked!" + rankedLink)
        rankedSource = requests.get(rankedLink).text

        soupRanked = BeautifulSoup(rankedSource, 'html.parser')

        # Sets all the variables for casual
        killsRanked = soupRanked.find('div', {"class": "value"})
        deathsRanked = killsRanked.find_next('div', {"class": "value"})
        kdRatioRanked = deathsRanked.find_next('div', {"class": "value"})
        hoursPlayedRanked = kdRatioRanked.find_next('div', {"class": "value"})
        winLossRecordRanked = hoursPlayedRanked.find_next('div', {"class": "value"})

        #Determine what needs to be returned for casual
        #Kills
        if decisionVar == 1:
            return killsRanked.text
        #deaths
        elif decisionVar == 2:
            return deathsRanked.text
        #KD
        elif decisionVar == 3:
            return kdRatioRanked.text
        #hoursPlayed
        elif decisionVar == 4:
            return hoursPlayedRanked.text
        #Win Loss Record
        elif decisionVar == 5:
            return winLossRecordRanked.text
        else:
            stats = []
            stats.append(killsRanked.text)
            stats.append(deathsRanked.text)
            stats.append(kdRatioRanked.text)
            stats.append(hoursPlayedRanked.text)
            stats.append(winLossRecordRanked.text)
            return stats


#BOT FUNCTIONALITY
# When bot starts up
@bot.event
async def on_ready():
    print('Ready When you are xdxd')

@bot.event
async def on_message(message):

    userId = message.author.id

    #Help
    if message.content.upper().startswith('!HELP'):
        await bot.send_message(message.channel, "!CasKills <UplayNameHere> = Amount of kills player has in casual \n" +
                                                "!CasDeaths <UplayNameHere> = Amount of deaths player has in casual\n" +
                                                "!CasKD <UplayNameHere> = The players Kill Death Ratio in casual\n" +
                                                "!CasHours <UplayNameHere> = The amount of hours the player has played in casual\n"+
                                                "!CasWinLoss <UplayNameHere> = The players Win Loss record in cas\n" +
                                                "!CasAll <UplayNameHere> = Shows all the stats for casual\n" +
                                                "!Thanks = Try it and see!")


    #Thanks Message
    if message.content.upper().startswith('!THANKS'):
        await bot.send_message(message.channel, 'Not a problem human! It is what I am programmed to do')

    #RAINBOW SIX SIEGE Commands
    #CASUAL STATS
    #KILLS
    if message.content.upper().startswith('!CASKILLS'):
        strArray = message.content.split(" ")
        if(strArray[1] == 'SS.Something'):
            bot.send_message(message.channel, "Eat my ass")
        else:
            strKills = retrievePlayerInfo(strArray[1], 1)
    await bot.send_message(message.channel, strArray[1] + "\n" + strKills + " kills in casual")
    #deaths
    if message.content.upper().startswith('!CASDEATHS'):
        strArray = message.content.split(" ")
        strDeaths = retrievePlayerInfo(strArray[1], 2)
        await bot.send_message(message.channel, strArray[1] + "\n"+ strDeaths + " deaths in casual")
    #KD Ratio
    if message.content.upper().startswith('!CASKD'):
        strArray = message.content.split(" ")
        strKD = retrievePlayerInfo(strArray[1], 3)
        await bot.send_message(message.channel, strArray[1] + "\n"+ strKD + " KD ratio in casual")
    #Hours Played
    if message.content.upper().startswith('!CASHOURS'):
        strArray = message.content.split(" ")
        strHours = retrievePlayerInfo(strArray[1], 4)
        await bot.send_message(message.channel, strArray[1] + "\n" + strHours + " hours played in casual")
    #Win Loss
    if message.content.upper().startswith('!CASWINLOSS'):
        strArray = message.content.split(" ")
        strWinLoss = retrievePlayerInfo(strArray[1], 5)
        await bot.send_message(message.channel, strArray[1] + "\n"+ strWinLoss + " win loss record in casual")
    #All stats
    if message.content.upper().startswith('!ALL'):
        strArray = message.content.split(" ")
        strAll = retrievePlayerInfo(strArray[1], 6)
        await bot.send_message(message.channel, strArray[1] + "\n"
                                                "Casual Kills: " + strAll[0] +
                                                "Casual Deaths: " + strAll[1] +
                                                "Casual KD Ratio: " + strAll[2] +
                                                "Casual Hours Played: " + strAll[3] +
                                                "Casual Win Loss Record: " + strAll[4])

    #RANKED stats
    #Kills
    if message.content.upper().startswith('!RANKEDKILLS'):
        strArray = message.content.split(" ")
        strKills = retrievePlayerRankedInfo(strArray[1], 1)
        await bot.send_message(message.channel, strArray[1] + "\n" + strKills + " kills in ranked")
    #deaths
    if message.content.upper().startswith('!RANKEDDEATHS'):
        strArray = message.content.split(" ")
        strDeaths = retrievePlayerRankedInfo(strArray[1], 2)
        await bot.send_message(message.channel, strArray[1] + "\n"+ strDeaths + " deaths in ranked")
    #KD Ratio
    if message.content.upper().startswith('!RANKEDKD'):
        strArray = message.content.split(" ")
        strKD = retrievePlayerRankedInfo(strArray[1], 3)
        await bot.send_message(message.channel, strArray[1] + "\n"+ strKD + " KD ratio in ranked")
    #Hours Played
    if message.content.upper().startswith('!RANKEDHOURS'):
        strArray = message.content.split(" ")
        strHours = retrievePlayerRankedInfo(strArray[1], 4)
        await bot.send_message(message.channel, strArray[1] + "\n" + strHours + " hours played in ranked")
    #Win Loss
    if message.content.upper().startswith('!RANKEDWINLOSS'):
        strArray = message.content.split(" ")
        strWinLoss = retrievePlayerRankedInfo(strArray[1], 5)
        await bot.send_message(message.channel, strArray[1] + "\n"+ strWinLoss + " win loss record in ranked")
    #All stats
    if message.content.upper().startswith('!RANKEDALL'):
        strArray = message.content.split(" ")
        strAll = retrievePlayerRankedInfo(strArray[1], 6)
        await bot.send_message(message.channel, strArray[1] + "\n"
                                                "Ranked Kills: " + strAll[0] +
                                                "Ranked Deaths: " + strAll[1] +
                                                "Ranked KD Ratio: " + strAll[2] +
                                                "Ranked Hours Played: " + strAll[3] +
                                                "Ranked Win Loss Record: " + strAll[4])

bot.login(process.env.BOT_TOKEN)
