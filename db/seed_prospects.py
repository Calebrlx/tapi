import requests

# API URL for the database
API_URL = "http://10.0.0.25:8000/prospects/"

# List of prospects
prospects = [
    "78of76", "abeinginsand", "absentminded-potato", "absoluteocellibehavior",
    "akiridraws", "amitybrightlights", "an-aura-about-you", "apmanda",
    "artemiseternal", "asexualerror", "asthecrowtries", "aviradasa", "babynium",
    "batvillainz", "blackberryjambaby", "blankbullet5", "bluegummiebears",
    "bonesmt", "bookmuncherss", "botanicaloddity", "brendia-t-stuff",
    "brownbearbutch", "bumblebeebarista", "bumblestheopossum", "canolaaoil",
    "carolina117", "catchandelier", "chaoticgoodthief", "charlies-webster",
    "clay-sicles", "cleokuns", "clown-college-honor-roll", "comicallysmallcereals",
    "cootiekitten", "creativeheartfinds", "cryapie", "crypticcripple", "cybercervine",
    "cytherea", "daemonmage", "dailyartjaneone", "dame-umbra",
    "definitelynotsecretaccount", "dew-ontherocks", "dgp-men", "diceshamingisafreeaction",
    "dirtforworm", "discordarchitect", "doctor-aqua-the-awesome", "domihime",
    "dragoonofficial", "drdrizzey", "dreamer-in-a-far-away-land", "drizzledover",
    "eatcrayonsalways", "edgier-than-a-diamond", "electriclauv", "emdrawalot",
    "erintough-blog", "estellijelli", "ev-cupcake", "eye-motive", "fionamanita",
    "floweringspringgardenz", "flowrfemme", "free-laughter", "fu3g0n3gr0",
    "gayghostrights", "glinnmelethril", "goat-carr", "gobstoppr", "goldenhaloyunan",
    "goobersplat", "goosemagician", "hazelthewolfo", "heart-stars", "hedgehology",
    "hejkatie", "hellomynameiscytherea", "hellsinger-sides", "helo", "honeyandbee",
    "horrorpodcastslover", "humoriffic", "i-3at-s0ap", "i-like-your-funny-hat",
    "i-think-im-asleep", "iisbirb", "interplanetaryfox", "intrepidenigma",
    "irreputablyyours", "isthisamew", "izzythedemigod", "jack-of-lanterns",
    "januaryavis", "jinxthechaotic", "jup1tersparx", "juyuu", "k1rafr0mplut0",
    "koszmarnybudyn", "la-criatura", "ladycelery", "lazyprincessnightmare",
    "learningourlovelanguage", "leaves-and-inks", "lewinterwolf", "lil-grimlynn",
    "liminalspaceintercom", "littlealienproducts", "littleworks", "lou-ofc",
    "lucyseraph14-blog", "lupinemonstrosity", "mahaliamaverick", "manonslayme",
    "marushou13", "mathair-thiomanta", "megaemanueleme", "metalgodawful",
    "metalheddie", "missscully-velvet", "monnichi-blog-aka-legend-of-sora",
    "moondream249", "my-friends-call-me-bug", "mylunajewel", "n0c-tilucent",
    "night-fa11", "nintendocrowbro", "nmykena-springtrap", "noicechimmedoge",
    "noodledragon", "obi-mom-kenobi", "odetokeons", "oflorelei", "ooctoopussi",
    "pandansca", "paperbirdbouquet", "patinedgold", "petcicada", "pigeontakeover",
    "questionforgotten", "r-chivist", "randxartz", "reblogalanaartdream",
    "reddstardust", "rennethen", "renzilla-exists", "reptilebug", "rkherman",
    "rockstarfreddybby", "rvensong", "schneakyverene", "secretcherimaybe",
    "sevilai", "sexinahammock", "shortcircuitthegreat", "shyflameweasel",
    "simplebasichuman-blog", "skyeoak", "smaller-than-a-cryptid", "smooshedrice",
    "snakeunderyourboot", "softwafflo", "solar-plant-princess", "somebodykeepstakingmyusername",
    "someonelikemehere", "southerngothspell", "spacestarberrymain", "spickerzocker",
    "spycopoth", "starvingartstudent", "such-a-downer", "sugarnspiceartworks",
    "sunblocks", "surpriseimbored", "sxndrxsuniverse", "tangentialdrone",
    "teafromthemicrowave", "teddytoroa", "theabstruseanon", "theartistofhumanorigin",
    "theradiopixie", "therealjamcracker", "therogueduchess", "thesedoomdays",
    "thisurltotallysucks", "thumpersdae", "tiffanybutts", "trulymonochrome",
    "uselessmoth", "vandyrix", "victorydoll", "watergh0st", "webedragons",
    "weblackbell", "what-am-i-d0ing", "where-the-fireflies-are", "woolmaiden",
    "xblood-kittenx", "xylo-slongium", "yeehawnk", "yourcoffeeguru",
    "yousuckflounderlemming", "yuumei-art", "zaiqukaj", "zollaris", "zombie-ki",
    "zombie-lemon"
]

def add_prospect(slug):
    response = requests.post(API_URL, json={"slug": slug})
    if response.status_code == 200:
        print(f"Successfully added: {slug}")
    else:
        print(f"Failed to add: {slug}, Status Code: {response.status_code}")

if __name__ == "__main__":
    for prospect in prospects:
        add_prospect(prospect)