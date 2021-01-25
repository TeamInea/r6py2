import asyncio
import discord
import random
from bs4 import BeautifulSoup
import requests
from discord.ext.commands import Bot
from discord import Game
import datetime
import time
import json
import re
import lxml.html

client = Bot(command_prefix='!')
client.remove_command("help")
start_time = time.time()

TOKEN = 'Bot Token'

stats_card_idx = ['ranked_stats', 'casual_stats', 'overall_stats', 'team_play', 'kills_breakdown', 'secure_stats', 'bomb_stats', 'hostage_stats']

stats_idx = ['time played', 'matched played', 'kills/match', 'kills', 'deaths', 'k/d ratio', 'wins', 'losses', 'w/l ratio', 'total kills', 'melee kills', 'headshots', 'headshot %']

kills_breakdown_idx = ['total kills', 'blind kills', 'melee kills', 'penetration kills', 'headshots', 'headshot %']

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) ' 'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 ' 'Safari/537.36'}

def get_stats(uuid):
    url = 'https://r6stats.com/stats/{}/'.format(uuid)
    uuids = '{}'.format(uuid)
    resp = requests.get(url, headers=headers)
    soup = BeautifulSoup(resp.text, 'lxml')
    username = soup.find('h1', class_='username').text
    profile_img = soup.find('img', class_='profile')['src']
    ranks = soup.find_all('div', class_='season-rank')
    operators = soup.find_all('div', class_='player-header__left-side')
    stat_cards = soup.find_all('div', class_='stat-card')
    update = soup.find('span', class_='last-updated__timestamp').text
    update = update.replace("less than a minute", "몇 초")
    update = update.replace("about", "약")
    update = update.replace("minutes", "분")
    update = update.replace("minute", "분")
    update = update.replace("hours", "시간")
    update = update.replace("hour", "시간")
    update = update.replace("days", "일")
    update = update.replace("day", "일")
    level = soup.find('span', class_='quick-info__value').text
    return {
        'url': url,
        'username': username,
        'uuids': uuids,
        'profile_img': profile_img,
        'rank': ''.join(sorted([rank.img['title'] for rank in ranks[:1]])),
        'update': update,
        'level': level,
        'operator': ''.join(sorted([operator.img['alt'] for operator in operators[:1]])),
        'ranked_stats': {
            stat_name: stat_value.find('span', class_='stat-count').text
            for stat_name, stat_value in zip(stats_idx, stat_cards[stats_card_idx.index('ranked_stats')]
                .find('div', class_='card__content')
                .find_all('div', class_='stat-section'))},
        'casual_stats': {
            stat_name: stat_value.find('span', class_='stat-count').text
            for stat_name, stat_value in zip(stats_idx, stat_cards[stats_card_idx.index('casual_stats')]
                .find('div', class_='card__content')
                .find_all('div', class_='stat-section'))},
        'overall_stats': {
            stat_name: stat_value.find('span', class_='stat-count').text
            for stat_name, stat_value in zip(stats_idx, stat_cards[stats_card_idx.index('overall_stats')]
                .find('div', class_='card__content')
                .find_all('div', class_='stat-section'))},
        'kills_breakdown': {
            stat_name: stat_value.find('span', class_='stat-count').text
            for stat_name, stat_value in zip(kills_breakdown_idx, stat_cards[stats_card_idx.index('kills_breakdown')]
                .find('div', class_='card__content')
                .find_all('div', class_='stat-section'))}}

async def embed_creator(context, uuid, uuids):
    stats = get_stats(uuid)
    embed = discord.Embed(title='R6S 전적 | {}의 전적'.format(stats['username'], color=0x00ff00))
    embed.set_thumbnail(url=stats['profile_img'])
    embed.add_field(name='닉네임', value='{}'.format(stats['username']), inline=True)
    embed.add_field(name='플레이어 고유 UUID', value='{}'.format(stats['uuids']), inline=False)
    embed.add_field(name='전체 플레이 타임', value='{}'.format(stats['overall_stats']['time played']), inline=True)
    embed.add_field(name='플레이어 레벨', value='{}'.format(stats['level']), inline=True)
    embed.add_field(name='선호 오퍼', value='{}'.format(stats['operator']), inline=True)
    embed.add_field(name='현 시즌 랭크', value='{}'.format(stats['rank']), inline=True)
    embed.add_field(name='랭크 플레이 타임', value='{}'.format(stats['ranked_stats']['time played']), inline=True)
    embed.add_field(name='랭크 경기당 킬 평균', value='{}'.format(stats['ranked_stats']['kills/match']), inline=True)
    embed.add_field(name='랭크 킬/데스 비율', value='{}'.format(stats['ranked_stats']['k/d ratio']), inline=True)
    embed.add_field(name='랭크 승/패 비율', value='{}'.format(stats['ranked_stats']['w/l ratio']), inline=True)
    embed.add_field(name='캐쥬얼 플레이 타임', value='{}'.format(stats['casual_stats']['time played']), inline=True)
    embed.add_field(name='캐쥬얼 경기당 킬 평균', value='{}'.format(stats['casual_stats']['kills/match']), inline=True)
    embed.add_field(name='캐쥬얼 킬/데스 비율', value='{}'.format(stats['casual_stats']['k/d ratio']), inline=True)
    embed.add_field(name='캐쥬얼 승/패 비율', value='{}'.format(stats['casual_stats']['w/l ratio']), inline=True)
    embed.add_field(name='통합 킬 횟수', value='{}'.format(stats['kills_breakdown']['total kills']), inline=True)
    embed.add_field(name='통합 근접 킬 횟수', value='{}'.format(stats['kills_breakdown']['melee kills']), inline=True)
    embed.add_field(name='통합 헤드샷 킬 횟수', value='{}'.format(stats['kills_breakdown']['headshots']), inline=True)
    embed.add_field(name='통합 헤드샷 %', value='{}'.format(stats['kills_breakdown']['headshot %']), inline=True)
    embed.set_footer(text="전적 업데이트 : {} 전".format(stats['update']))
    await client.send_message(context.message.channel, embed=embed)

async def get_uuid(context, username, platform):
    result_resp = requests.get('https://r6stats.com/search/{username}/{platform}/'.format(username=username, platform=platform), headers=headers)
    try:
        result_soup = BeautifulSoup(result_resp.text, 'lxml')
        users = result_soup.find_all('a', class_='result')
        user_uuids = []
        for user in users:
            user_uuids.append(user['href'][7:-1])
        uuids = user_uuids[0]
        await embed_creator(context, uuids, uuids)
    except:
        embed = discord.Embed(description="⚠️ 유저 {}을 찾을 수 없습니다.".format(username), color=0xe32b33)
        await client.send_message(context.message.channel, embed=embed)


async def r6sstatus(context):
    message = await client.send_message(context.message.channel, "🔎 정보를 가져오는중...")
    pcstatus = get_status('e3d5ea9e-50bd-43b7-88bf-39794f4e3d40')
    ps4status = get_status('fb4cc4c9-2063-461d-a1e8-84a7d36525fc')
    xboxonestatus = get_status('4008612d-3baf-49e4-957a-33066726a7bc')
    await r6sstatus_msg(context, pcstatus, ps4status, xboxonestatus)
    await client.delete_message(message)

async def r6sstatus_msg(context, pcstatus, ps4status, xboxonestatus):
    embed=discord.Embed(title='R6S Server 상태', color=0x00ff00)
    embed.set_thumbnail(url='https://images.discordapp.net/avatars/537957046964846602/12903120da6ad678ce65e765db209ada.png')
    embed.add_field(name="PC", value=pcstatus, inline=True)
    embed.add_field(name="PS4", value=ps4status, inline=True)
    embed.add_field(name="XBOXONE", value=xboxonestatus, inline=True)
    await client.send_message(context.message.channel, embed=embed)

def get_status(appid):
    api = 'https://game-status-api.ubisoft.com/v1/instances?appIds='
    data = ""
    url = api + appid
    resp = requests.get(url)
    if resp.status_code == 200:
        data = resp.text
        data = data.replace("[", "")
        data = data.replace("]", "")
        data = json.loads(data)
        data = data["Status"]
        return data

async def status_task():
    while True:
        await client.change_presence(game=Game(name="봇이 새롭게 탄생했어요!"))
        await asyncio.sleep(5)
        await client.change_presence(game=Game(name="!r6h : 정보&도움말"))
        await asyncio.sleep(5)
        await client.change_presence(game=Game(name="!r6v : 레식서버상태확인"))
        await asyncio.sleep(5)
        await client.change_presence(game=Game(name="{}개의 서버 / {}명의 유저가 이용중!".format(len(client.servers), len(set(client.get_all_members())))))
        await asyncio.sleep(5)

@client.command(pass_context=True)
async def r6s(context, nickname=''):
    if nickname == '':
        nickname = str(context.message.author.nick)
    else:
        nickname = nickname.lower()
    embed = discord.Embed(description="🔎 정보를 가져오는중...", color=0x00ff00)
    msg = await client.send_message(context.message.channel, embed=embed)
    platform = 'pc'
    await get_uuid(context, nickname, platform)
    await client.delete_message(msg)


@client.command(pass_context=True)
async def r6h():
    current_time = time.time()
    difference = int(round(current_time - start_time))
    uptime = str(datetime.timedelta(seconds=difference))
    embed = discord.Embed(title="R6S 전적 봇 도움말&정보", description="!r6h : 봇 도움말&정보 보기 \n!r6s : 자신의 디코 서버 닉네임의 전체 전적보기 \n!r6s <닉네임> : 전적 보기\n!r6v : 레인보우 식스 시즈 서버 상태 확인\n\nInvite : https://discordbots.org/bot/537957046964846602 \n\n\n제작자 : HardBlock \nWeb : https://zsxdc1379.com", color=0x00ff00)
    embed.set_footer(text="R6S Stats 봇을 사용중인 서버 : {}개 / 이용자수 : {}명 / 업타임 : {}".format(len(client.servers), len(set(client.get_all_members())), uptime))
    await client.say(embed=embed)

@client.command(pass_context=True)
async def r6v(context):
    await r6sstatus(context)

@client.event
async def on_ready():
    print('Logged in as:')
    print(client.user.name)
    print(client.user.id)
    print('------')
    client.loop.create_task(status_task())

client.run(TOKEN)
