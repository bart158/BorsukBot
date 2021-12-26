import discord
from discord.ext import commands

import logging
import requests
import json
import random
import os
import shelve
from dotenv import load_dotenv

load_dotenv()


TOKEN = os.getenv("DISCORD_API_KEY")
COOKIE = {'steamLoginSecure': os.getenv("STEAM_COOKIE")}

description = 'Python Discord Bot'

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

bot = commands.Bot(command_prefix = '?', description=description)
unacceptable_words = ["słaby", "zły", "bez krwi i kości", "bublowaty",
"chałowaty", "chałowy", "denny", "do bani", "do chrzanu", "do kitu", "do luftu", "do niczego",
"du dupy", "dziadowski", "funta kłaków niewart", "kiepskawy", "kiepski", "kijowy", "kulawy",
"lichy", "lipny", "mało wart", "marny", "mierny", "nędzny", "nic nie wart", "niedobry", "nieklawy",
"nietęgi", "niewiele wart", "niewydarzony", "nijaki", "obciachowy", "od siedmiu boleści",
"ordynarny", "płytki", "pod zdechłym psem", "podły", "pośledni", "przeciętny", "ramotowaty", "słaby",
"mętny", "syfiasty", "szmatławy", "tandetny", "trzech groszy niewart", "zakichany", "zasmarkany",
"złamanego szeląga niewart", "żałosny", "cały w nerwach", "cięty jak osa", "gniewliwy", "gniewny",
"nabuzowany", "podekscytowany", "podenerwowany", "podirytowany", "podminowany", "podniecony", "podrażniony",
"poirytowany", "poruszony", "przejęty", "rozdrażniony", "rozeźlony", "rozgniewany", "rozgorączkowany", "rozindyczony",
"rozjątrzony", "rozjuszony", "rozsierdzony", "rozsrożony", "roztrzęsiony", "rozwścieczony", "rozwścieklony", "rozzłoszczony",
"spieniony", "spięty", "straszny", "wkurzony", "wnerwiony", "wpieniony", "wściekły", "wzburzony", "zagniewany", "zaniepokojony",
"zapieniony", "zbulwersowany", "zdenerwowany", "zgorszony", "zirytowany", "niespokojny", "ożywiony", "rozbity", "rozdygotany",
"rozemocjowany", "rozklekotany", "rozlatany", "wstrząśnięty", "zemocjowany", "bezecny", "drański", "fałszywy", "haniebny", "jaszczurczy",
"karygodny", "łachudrowaty", "łajdacki", "naganny", "niecny", "nieetyczny", "niegodny", "niegodziwy", "nieprzyzwoity", "nieszlachetny",
"nikczemny", "obłudny", "obmierzły", "obrzydliwy", "odpychający", "odrażający", "odstręczający", "ohydny", "okropny", "parszywy", "paskudny",
"perfidny", "plugawy", "podławy", "potworny", "przeokropny", "skandaliczny", "sparszywiały", "szatański", "szelmowski", "szkaradny", "szubrawy",
"szujowaty", "świniowaty", "wężowy", "wredny", "wszawy", "występny", "złośliwy", "znikczemniały", "żmijowaty", "dziki", "kipiący gniewem",
"Nie swój", "oburzony", "pogniewany", "rozszalały", "zacietrzewiony", "zniecierpliwiony", "rozhisteryzowany", "arcygroźny",
"bazyliszkowaty", "bazyliszkowy", "cyniczny", "czarci", "czartowski", "demoniczny", "diabelny", "diabelski", "diabli", "diaboliczny", "groźny",
"infernalny", "lisi", "lucyferyczny", "makabryczny", "makiaweliczny", "mefistofeliczny", "mefistofelowy", "nieprzyjazny",
"niesamowity", "piekielny", "przeraźliwy", "przerażający", "przewrotny", "srogi", "straszliwy", "surowy", "szalbierczy",
"szalbierski", "szyderczy", "upiorny", "wrogi", "z piekła rodem", "zastraszający", "z nerwami na wierzchu", "gangrenowaty",
"grzeszny", "łotrowski", "niechlubny", "niehonorowy", "niemoralny", "nieprawy", "niesławny", "niewybredny", "świński", "wyrodny",
"zdrożny", "zwarzony", "brzydki", "fatalny", "francowaty", "koszmarkowaty", "koszmarny", "nieładny", "niżej wszelkiej krytyki",
"poniżej wszelkiej krytyki", "potworkowaty", "szpetny", "wstrętny", "nabzdyczony", "cięty", "zjeżony", "mydłkowaty", "omierzły",
"przebrzydły", "nieludzki", "opłakany", "porażający", "rozpaczliwy", "szokujący", "widmowy", "zakazany", "zatrważający", "karczemny",
"antypatyczny", "chłodny", "cierpki", "godny pożałowania", "godny ubolewania", "gorzki", "jędzowaty", "kwaśny", "naprzykrzony",
"niemiły", "nieprzyjemny", "niesłodki", "niesympatyczny", "nieuprzejmy", "nieznośny", "nieżyczliwy", "opryskliwy", "oschły",
"przykry", "szorstki", "upierdliwy", "uprzykrzony", "wiedźmowaty", "wydrowaty", "zołzowaty", "tragiczny", "alarmistyczny",
"alarmujący", "apokaliptyczny", "czarny", "fatalistyczny", "grobowy", "kapitulancki", "karawaniarski", "kasandryczny",
"katastroficzny", "niefortunny", "niepokojący", "niepomyślny", "pogrzebowy", "ponury", "przygnębiający", "złowieszczy", "złowrogi",
"złowróżbny", "żałobny", "dramatyczny", "hiobowy", "panikarski", "pesymistyczny", "posępny", "wizyjny", "cholerny", "kolosalny", "nadzwyczajny",
"niemożliwy", "nieopisany", "niepojęty", "niesłychany", "niezwykły", "ogromny", "okrutny", "pioruński", "szalony", "wyjątkowy", "hańbiący",
"niski", "uwłaczający", "nadąsany", "najeżony", "obrażony", "jowiszowy", "marsowy", "sataniczny", "bezwstydny", "nieuczciwy", "Belzebub", "bies", "Boruta",
"czart", "czort", "demon", "demon zła", "diabeł", "kaduk", "książę ciemności", "kusiciel", "kusy", "licho", "Lucyfer", "Lucyper", "mefisto", "moc nieczysta",
"moc piekielna", "nieczysty duch", "Rokita", "siła nieczysta", "syn ciemności", "szatan", "upadły anioł", "wódz złych duchów", "złe",
"złośliwy duch", "zły duch", "błędny", "inadekwatny", "mylny", "nie na miejscu", "nieadekwatny", "niedobrany", "niekompatybilny", "nienależyty",
"nieodpowiedni", "niepoprawny", "nieprawidłowy", "nieprzystający", "nieprzystawalny", "nieprzystojny", "niestosowny", "nietrafny", "niewczesny",
"niewłaściwy", "niezdatny", "niezręczny", "opaczny", "lodowaty", "niechętny", "niekoleżeński", "niełaskawy", "nieobłaskawiony", "nieprzychylny", "polemiczny",
"przeciwny", "przeczący", "uprzedzony", "wrogo nastawiony", "zimny", "gorszący", "beznadziejny", "katastrofalny", "krytyczny", "chmurny", "depresyjny",
"nieszczęśliwy", "pechowy", "pochmurny", "smutny", "antagonistyczny", "nienawistny", "nieprzyjacielski", "opozycyjny", "przeciwstawny", "sprzeczny",
"wraży", "antychryst", "władca piekła", "amatorski", "dyletancki", "niefachowy", "nieporadny", "nieprofesjonalny", "nieskładny", "niesolidny",
"nieudany", "nieudolny", "nieumiejętny", "niewprawny", "niewyrobiony", "niezdarny", "niezgrabny", "niefartowny", "niewesoły", "zasmucający", "mizerny",
"pożal się Boże", "naburmuszony", "nadęty", "naindyczony", "napuszony", "nastroszony", "niezadowolony", "odęty", "chybiony", "nietrafiony",
"pseudoartystyczny", "zawzięty", "napięty", "brudny", "dwulicowy", "nieczysty", "niedozwolony", "nielojalny", "niesprawiedliwy", "nieszczery",
"oszukańczy", "podejrzany", "szemrany", "zakłamany", "załgany", "aberracyjny", "nieprzepisowy", "patologiczny", "wadliwy", "nieużyty", "kaleki", "niecelny",
"poroniony", "zgubny", "kontestacyjny", "kontestatorski", "negatywny", "pejoratywny", "ujemny", "horrendalny", "gromowładny", "piorunujący", "zabójczy",
"defetystyczny", "niechętny czemuś", "niechętny komuś", "rozsierdzony rozzłoszczony", "wściekły na coś", "wściekły na kogoś", "koślawy",
"nieprawdziwy", "omyłkowy", "pomyłkowy", "przeinaczony", "przekłamany", "przekręcony", "wypaczony", "zafałszowany", "niekorzystny", "niepochlebny",
"niechwalebny", "niedopuszczalny", "oburzający", "żenujący", "feralny", "niekompetentny", "karcący", "marsowaty", "oziębły", "przytłaczający", "deficytowy",
"niedochodowy", "nieekonomiczny", "nieintratny", "nieopłacalny", "niepopłatny", "nierentowny", "niewydajny", "niewydolny", "niezyskowny", "wysokodeficytowy",
"bezwartościowy", "byle jaki", "wstrząsający", "zaperzony", "nasrożony", "niebezpieczny", "podstępny", "szkodliwy", "zdegenerowany", "zdemoralizowany",
"zepsuty", "budzący grozę", "mrożący krew w żyłach", "chmurnawy", "kłopotliwy", "niepocieszający", "przygniatający", "smutnawy", "zniechęcający", "agresywny",
"pełen złej woli", "złego usposobienia", "niedostateczny", "felerny", "nieszczęsny", "demoralizujący", "niezdrowy", "bolesny", "ciężki", "dotkliwy", "drastyczny",
"krzywdzący", "w afekcie", "ciemny", "nie wzbudzający zaufania", "przestępczy", "niedoskonały", "niepełnowartościowy", "ułomny", "złej jakości", "destrukcyjny",
"nierad", "rozgoryczony", "zgorzkniały", "nieugięty", "nieustępliwy", "zacięty", "zajadły", "indolentny", "niedouczony", "nieobowiązkowy", "nierzetelny",
"niesumienny", "źle pracujący", "nerwowy", "niecierpliwy", "nieopanowany", "zaminowany", "denerwujący", "drażniący", "uciążliwy", "nieczynny", "niesprawny",
"popsuty", "uszkodzony", "wybrakowany", "zdefektowany", "amoralny", "bez serca", "cwaniacki", "mroczny", "wyklęty", "wykolejony", "źle usposobiony",
"zasługujący na naganę", "mdły", "niejadalny", "niesmaczny", "niestrawny", "niezjadliwy", "kiepskiej jakości", "gwałtowny", "zaciekły", "zapamiętały",
"morderczy", "pieski", "pożałowania godny", "psi", "nie do przyjęcia", "nie nadający się", "nieakceptowalny", "przynoszący straty", "nie najlepszy", "niedostosowany",
"niewychowany", "cienki", "pozagatunkowy", "zawodny", "bardzo zły", "kompromitujący", "śmiertelny", "zjadliwy" ]


@bot.event
async def on_ready():
    print("The bot is now ready for use")
    print("----------------------------")
    my_activity = discord.Game(name = "at your mum\'s 💦")
    await bot.change_presence(activity=my_activity, status=discord.Status.online)

@bot.command()
async def hello(ctx):
    await ctx.send("world")

@bot.command()
async def popuś(ctx):
    await ctx.send("Popuś! Popuś!")

@bot.event
async def on_message(message):
    message_lower_case = message.content.lower()
    if message.author == bot.user:
        return
    
    if message.content.startswith('debil'):
        await message.channel.send('twoja stara')
    if message.content.startswith('bajo jajo'):
        await message.channel.send('ja ci dam bajo jajo')
    if message.content.startswith('helikopter helikopter'):
        await message.channel.send('Para kofer, para kofer')
    if message.content.startswith('despacito'):
        await message.channel.send('quiero respirar tu cuello despacito')
    if message.content.startswith('Wesołych Świąt'):
        await message.channel.send('Nawzajem')
    if message_lower_case.find('trans') >= 0:
        await message.channel.send('Trans rights are human rights')
    if message.author.name == 'GGMW':
        insults = ['Jesteś useless na bocie!', 'Jesteś useless na topie!', 'Jesteś useless w lesie!',
        'Kochasz grać w drewutnię!', 'Masz większe ego niż Tymek lufę!', 'Jesteś fanboyem anime!', 'https://i.ibb.co/0Vzcpt9/Screenshot-2021-12-25-163816.png']
        await message.reply(random.choice(insults))
    if(message_lower_case.find("popuś") >= 0):
        credit_score_counter_popus = 0
        for i in unacceptable_words:
            if message_lower_case.find(i) >= 0:
                credit_score_counter_popus += 1
        if credit_score_counter_popus > 0:
            if credit_score_counter_popus == 1:
                await message.reply("Obraziłeś Króla Popsona! Twój wynik kredytu społecznego został obniżony o " + str(credit_score_counter_popus) + " punkt.")
            elif credit_score_counter_popus > 1 and credit_score_counter_popus < 5:
                await message.reply("Obraziłeś Króla Popsona! Twój wynik kredytu społecznego został obniżony o " + str(credit_score_counter_popus) + " punkty.")
            else:
                await message.reply("Obraziłeś Króla Popsona! Twój wynik kredytu społecznego został obniżony o " + str(credit_score_counter_popus) + " punktów.")
            author_id = str(message.author.id)
            if not os.path.exists(os.path.join("data", "credit_score")):
                os.makedirs(os.path.join("data", "credit_score"))
            credit_score = shelve.open(os.path.join("data", "credit_score", "credit_score"))
            if author_id in credit_score:
                credit_score[author_id] -= credit_score_counter_popus
            else:
                credit_score[author_id] = 0
                credit_score[author_id] -= credit_score_counter_popus
            if credit_score[author_id] < -10:
                await message.channel.send("Użytkownik @" + message.author.name + " ma wynik kredytu społecznego poniżej -10!")

    await bot.process_commands(message)



@bot.command()
async def pullsteamprice(ctx, *arg):
    joining_word = ' '
    weapon_name = joining_word.join(arg)
    weapon_name_url = weapon_name
    weapon_name_url.replace(' ', '%20')
    response = requests.get('https://steamcommunity.com/market/priceoverview/?appid=730&market_hash_name=' + weapon_name_url + '&currency=6',  cookies=COOKIE)
    json_response = response.json()
    print(json_response)
    await ctx.send("Najniższa cena " + weapon_name + " na rynku to: " + json_response['lowest_price'])
    await ctx.send("Na rynku jest " + json_response['volume'] + ' ' + weapon_name)


@bot.event
async def on_member_join(member):
    channel = bot.get_channel(652821241144541194)
    await channel.send("No siema")

@bot.event
async def on_member_remove(member):
    channel = bot.get_channel(652821241144541194)
    await channel.send("Żegnam")

bot.run(TOKEN)