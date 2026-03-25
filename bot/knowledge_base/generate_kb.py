import json
import os
import re

# ============================================================
# СЛОВАРЬ ЗАМЕН (Dune → вымышленная вселенная "Veloria")
# ============================================================
TERMS_MAP = {
    # Персонажи
    "Paul Atreides": "Kael Voryn",
    "Paul": "Kael",
    "Muad'Dib": "Veth'Kor",
    "Usul": "Dravek",
    "Lady Jessica": "Lady Seryn",
    "Jessica": "Seryn",
    "Duke Leto Atreides": "Duke Maren Voryn",
    "Duke Leto": "Duke Maren",
    "Leto Atreides": "Maren Voryn",
    "Leto": "Maren",
    "Baron Vladimir Harkonnen": "Baron Zethus Korrax",
    "Vladimir Harkonnen": "Zethus Korrax",
    "Baron Harkonnen": "Baron Korrax",
    "Feyd-Rautha Harkonnen": "Drael-Tavin Korrax",
    "Feyd-Rautha": "Drael-Tavin",
    "Feyd": "Drael",
    "Glossu Rabban": "Gorux Vethaan",
    "Rabban": "Vethaan",
    "Stilgar": "Kalden",
    "Chani": "Lysha",
    "Duncan Idaho": "Fenric Solaar",
    "Duncan": "Fenric",
    "Gurney Halleck": "Horvan Trellek",
    "Gurney": "Horvan",
    "Thufir Hawat": "Duras Halvek",
    "Thufir": "Duras",
    "Wellington Yueh": "Brennan Sorath",
    "Yueh": "Sorath",
    "Alia Atreides": "Vyra Voryn",
    "Alia": "Vyra",
    "Leto Atreides II": "Maren Voryn II",
    "Leto II": "Maren II",
    "Shaddam Corrino IV": "Valdrek Synnor IV",
    "Shaddam IV": "Valdrek IV",
    "Shaddam": "Valdrek",
    "Princess Irulan": "Duchess Solane",
    "Irulan": "Solane",
    "Gaius Helen Mohiam": "Vestra Helyne Morath",
    "Reverend Mother Mohiam": "Reverend Mother Morath",
    "Mohiam": "Morath",
    "Liet-Kynes": "Solan-Drev",
    "Kynes": "Drev",
    "Jamis": "Vareth",
    "Paulus Atreides": "Arkon Voryn",

    # Дома и организации
    "House Atreides": "House Voryn",
    "Atreides": "Voryn",
    "House Harkonnen": "House Korrax",
    "Harkonnen": "Korrax",
    "House Corrino": "House Synnor",
    "Corrino": "Synnor",
    "Bene Gesserit": "Sera Valdris",
    "the Sisterhood": "the Covenant",
    "Spacing Guild": "Void Consortium",
    "Guild Navigator": "Void Pathfinder",
    "Navigator": "Pathfinder",
    "CHOAM": "NEXUM",
    "Landsraad": "Conclave of Houses",
    "Sardaukar": "Vareth Guard",
    "Fedaykin": "Drev'kai",
    "Fremen": "Eremai",
    "Tleilaxu": "Velukai",
    "Bene Tleilax": "Order Velukai",
    "Missionaria Protectiva": "Shadow Doctrine",

    # Планеты и места
    "Arrakis": "Veloris",
    "Dune": "Veloria",
    "Caladan": "Aqualon",
    "Giedi Prime": "Korreth Prime",
    "Kaitain": "Synnoria",
    "Salusa Secundus": "Rashan Secundus",
    "Arrakeen": "Veloraan",
    "Sietch Tabr": "Sanctum Drev",
    "Sietch": "Sanctum",
    "Shield Wall": "Stone Veil",

    # Технологии и артефакты
    "Spice Melange": "Flux Essence",
    "spice melange": "flux essence",
    "the spice": "the flux",
    "melange": "essence",
    "Sandworm": "Duneserpent",
    "sandworm": "duneserpent",
    "Shai-Hulud": "Kor-Veloth",
    "Sandtrout": "Dunelarva",
    "sandtrout": "dunelarva",
    "Stillsuit": "Vaporsuit",
    "stillsuit": "vaporsuit",
    "Ornithopter": "Skimcraft",
    "ornithopter": "skimcraft",
    "Thumper": "Rhythmer",
    "thumper": "rhythmer",
    "Maker hooks": "Rider clamps",
    "maker hooks": "rider clamps",
    "Crysknife": "Shard blade",
    "crysknife": "shard blade",
    "Shield": "Barrier field",
    "shield": "barrier field",
    "Lasgun": "Phasebeam",
    "lasgun": "phasebeam",
    "Heighliner": "Voidcarrier",
    "heighliner": "voidcarrier",
    "Spice harvester": "Flux extractor",
    "spice harvester": "flux extractor",
    "harvester": "extractor",
    "Carryall": "Lifter craft",
    "carryall": "lifter craft",
    "Mentat": "Calculus Adept",
    "mentat": "calculus adept",
    "Water of Life": "Essence of Awakening",
    "Gom Jabbar": "Pain Shard",
    "Weirding Way": "Resonance Path",
    "Prana-bindu": "Neural-flux",

    # Концепции и термины
    "Kwisatz Haderach": "Veth'Soran",
    "Prescience": "Flux-sight",
    "prescience": "flux-sight",
    "Other Memory": "Ancestral Echo",
    "Golden Path": "Eternal Course",
    "Jihad": "Crusade of Light",
    "jihad": "crusade of light",
    "Spice Agony": "Essence Trial",
    "Reverend Mother": "Prime Matriarch",
    "Naib": "Sanctum Elder",
    "Padishah Emperor": "Grand Sovereign",
    "padishah emperor": "grand sovereign",
    "Butlerian Jihad": "Machine Purge",
    "Lisan al-Gaib": "Voice of Beyond",
    "Mahdi": "The Chosen",
    "Wormsign": "Serpent sign",
    "wormsign": "serpent sign",
    "Wormriding": "Serpent riding",
    "wormriding": "serpent riding",
    "Desert War": "Sands War",
    "Spice blow": "Flux eruption",
    "spice blow": "flux eruption",
    "Golden Lion Throne": "Sovereign Throne of Stars",
    "Known Universe": "Charted Expanse",
    "Old Empire": "Ancient Dominion",
    "Panoplia Propheticus": "Sacred Mythologies",
    "Chakobsa": "Veloran",
    "Zensunni": "Zenveldri",
    "Truthsayer": "Vow-reader",
    "Voice": "Resonant Command",
    "Axlotl tank": "Genesis vat",
    "Ghola": "Revival clone",
    "ghola": "revival clone",
}

def replace_terms(text, terms_map):
    """Replace all terms in text, longest first to avoid partial replacements."""
    sorted_terms = sorted(terms_map.keys(), key=len, reverse=True)
    for term in sorted_terms:
        replacement = terms_map[term]
        text = re.sub(re.escape(term), replacement, text, flags=re.IGNORECASE if term.islower() else 0)
    return text


# ============================================================
# ИСХОДНЫЕ ТЕКСТЫ (на основе фандома Dune)
# ============================================================
DOCUMENTS = {
    "kael_voryn": {
        "title": "Kael Voryn — The Chosen One",
        "content": """Kael Voryn (10176 A.G. – 10219 A.G.), predominantly known as Veth'Kor, was the last Duke of the noble House Voryn and the first Voryn Emperor of the Charted Expanse. He was the only son of Duke Maren Voryn and the Prime Matriarch Lady Seryn.

Kael grew up with a privileged background on the water-covered planet of Aqualon, the ancestral home of House Voryn. Under the supervision of the Calculus Adept Duras Halvek and military experts Horvan Trellek and Fenric Solaar, Kael was raised to be the heir of House Voryn, one of the most powerful and respected Great Houses in the Synnor Empire.

Upon the arrival of House Voryn on Veloris, Kael's flux-sight was strengthened by the flux essence he constantly inhaled. After surviving the betrayal by House Korrax and the Grand Sovereign, Kael escaped into the desert with his mother and joined the Eremai people. He took the name Veth'Kor — a name from the small creature of the desert that impressed the Eremai warriors.

As Veth'Kor, Kael led the Eremai in a guerrilla Crusade of Light against the Korrax occupiers, and eventually overthrew the Grand Sovereign Valdrek IV, ascending to the Sovereign Throne of Stars. He ruled the empire for twelve years before voluntarily walking into the desert to meet his fate, blinded and stripped of power.

Key names used by Kael Voryn throughout his life:
- Veth'Kor: his open Eremai name, meaning "desert's courage"
- Dravek: his secret sietch name, meaning "strength of the pillar base"
- The Chosen: the religious title given by the Eremai who believed the Shadow Doctrine prophecies
- Voice of Beyond: the prophetic title planted by the Sera Valdris among desert peoples

Kael possessed powerful flux-sight abilities as the long-awaited Veth'Soran of the Sera Valdris breeding program. This made him able to perceive future events and access ancestral memories of both his male and female ancestors — something no other being had achieved before him."""
    },

    "veloris": {
        "title": "Veloris — The Desert World",
        "content": """Veloris, also known as Veloria and later as Rakis after the fall of God-Emperor Maren II, was a harsh desert planet located on the far edge of the Ancient Dominion in the Canopus star system. It was the original and for a long time sole source of the Flux Essence, vital for space travel.

The planet was almost entirely covered by a desert ecosystem. The dominant lifeforms were the massive duneserpents, whose internal biological processes were essential to the creation of flux essence. The Eremai people — descendants of the Zenveldri Wanderers — considered Veloris their home and had adapted completely to its brutal environment.

Geography and Climate:
The surface of Veloris consisted primarily of vast open deserts and enormous sand dunes that stretched from pole to pole. Rocky outcrops and mountain ranges broke up the endless sandy expanse. The only significant polar region offered marginally milder temperatures, and it was here that the capital city Veloraan was built, protected by the Stone Veil — a massive natural rock formation that shielded it from duneserpent incursion.

The climate was extremely hot and dry. Temperatures in the deep desert could reach lethal levels during the day. Moisture was the most precious resource on the planet. The Eremai adapted to this environment through the use of vaporsuits — full-body garments that recycled all moisture expelled by the wearer's body.

Flora and Fauna:
Little native life survived on Veloris due to its scorching heat and dry climate. The most significant creature was the duneserpent. Other creatures included:
- Dunelarva: small organisms that played a crucial role in the flux creation cycle
- Kangaroo mouse (called Veth'Kor by the Eremai): small desert rodent
- Desert hawk, eagle, and dwarf owl
- Sand scorpion, centipede, and trapdoor spider
- Kit fox, sand terrapin, and desert hare

Some hardy plants also survived: camel sage, gobi feather grass, wild alfalfa, burrow bush, and creosote bush.

Economic Importance:
Before the discovery of flux essence on the planet, Veloris was of little tactical or geological interest to the broader empire. After the Machine Purge, the powerful effects of flux, especially with regard to space travel via the Void Consortium, quickly made it an essential resource. By the time of Kael Voryn, Veloris had become the most critical planet in the Charted Expanse. Control of Veloris meant control of all interstellar travel and commerce."""
    },

    "flux_essence": {
        "title": "Flux Essence — The Spice of Veloris",
        "content": """Flux Essence, commonly referred to simply as "the flux," was a naturally produced awareness-spectrum narcotic that formed a fundamental block of commerce and technological development in the Charted Expanse for millennia. It also played an important role in space travel, as it was vital for enabling Void Pathfinders of the Void Consortium to safely guide voidcarriers through folded space.

Origin and Production:
The flux originated on the planet Veloris, where it was produced deep beneath the sands in a complex biological cycle. The process began with dunelarva — small organisms that encysted underground water supplies. When dunelarva populations sufficiently consumed underground water, they coalesced into young duneserpents. As duneserpents matured and eventually died, their decomposition, combined with specific pressure and heat conditions, created pre-flux masses. These masses erupted to the surface in events called flux eruptions, and under the intense heat and air of Veloris, flux essence formed.

Properties and Effects:
Flux essence appeared as a deep blue-orange granular substance with a distinctive cinnamon-like scent. Its effects on humans varied by dose and frequency:
- Small doses enhanced cognitive ability, extended lifespan, and slightly tinted the eyes blue
- Regular consumption turned the eyes entirely blue ("Eyes of Ibal"), a mark of the Eremai
- Large doses or concentrated forms enabled limited flux-sight (prescient visions)
- The Void Consortium Pathfinders consumed massive quantities to achieve the navigational trance required for safe space travel
- The Prime Matriarchs of the Sera Valdris used it to unlock Ancestral Echo — memories of all female ancestors

Addictive Nature:
Flux essence was highly addictive. Withdrawal from regular consumption was agonizing and potentially fatal. Billions of citizens throughout the Charted Expanse depended on steady flux supplies for daily survival. This dependency made Veloris the most strategically important planet in the known galaxy.

Economic Control:
By the time House Voryn arrived on Veloris, flux essence had become the single resource capable of creating or destroying an empire. NEXUM — the trading consortium — controlled all flux commerce. The Grand Sovereign of House Synnor derived enormous power from controlling flux distribution. This control ultimately led to the political machinations that sent House Voryn to Veloris and set in motion the events that would topple the Synnor dynasty."""
    },

    "duneserpent": {
        "title": "Duneserpent — The Great Beast of Veloris",
        "content": """The duneserpent was the predominant lifeform on Veloris — both honored and feared, vital and deadly. It was an autotrophic animal that inhabited the vast desert expanses of the planet and played a central role in the creation of flux essence.

Physical Description:
Duneserpents were enormous creatures. Specimens up to 400 meters in length were documented in the deep desert regions, with rumors of even larger individuals near the southern poles. Their skin was thick, rough, and semi-metallic, comprised of many overlapping scales each several feet in size. These scales formed natural armor that protected the creature against sand abrasion. The interior of a duneserpent resembled a massive blast furnace, producing intense heat and flames. The forward end possessed a huge gaping mouth capable of consuming large vehicles, including flux extractors. A strong, flinty, cinnamon smell emanated from the creature, especially from the mouth — the scent of flux essence permeated their entire being.

Behavior:
Duneserpents lived primarily beneath the surface of the sand. They were highly territorial and were attracted to rhythmic vibrations on the surface, which they interpreted as a threat to their domain. Human footsteps, machinery, and — most critically — the rhythmic operation of flux extractors all attracted duneserpents from great distances. Their longevity was extreme, estimated in the thousands of years, unless killed by humans or other duneserpents.

Role in Flux Creation:
Duneserpents were essential to the flux creation cycle. Dunelarva — their larval form — encysted underground water, which was then processed into a pre-flux chemical mass. When this mass erupted to the surface in a flux eruption, flux essence formed under the heat and pressure of the desert air. Without duneserpents, there could be no flux.

Duneserpent Riding:
The Eremai discovered that by prying up the scales on a duneserpent's side, they could cause the creature to rotate until the irritated scale faced upward — away from the sand — allowing a rider to stand upon it without being scraped off. Using rider clamps to hold the creature's leading edge, skilled Eremai riders could control the direction and speed of the duneserpent, making it a powerful method of transport across the desert. Serpent riding was considered a sacred rite of passage in Eremai culture. Distances were measured in "serpents" — the distance one could ride a duneserpent before it tired and submerged.

Cultural Significance:
To the Eremai, the duneserpent was a spiritual symbol. They called it Kor-Veloth, meaning "Old Father Eternity" in their tongue, viewing the creatures as physical manifestations of the One God of their original Zenveldri religion. Young duneserpents were used in special ceremonies — when poisoned with water, the dying creature would transform some of that water into the Essence of Awakening, a liquid used to induct new Prime Matriarchs of the Sera Valdris."""
    },

    "eremai": {
        "title": "Eremai — The Desert People",
        "content": """The Eremai were a culture of humans descended from the Zenveldri Wanderers who considered the planet Veloris their home. They formed an integral part in the establishment of the Voryn Empire and Veth'Kor's Crusade of Light.

Physical Characteristics:
Due to living on Veloris, the typical Eremai appeared as a sinewy human with leathery, tanned skin. Their most distinctive feature was their eyes — colored entirely blue ("Eyes of Ibal") due to their constant ingestion of flux essence, which permeated their food, water, and air. This blue coloring served as an immediate visual marker distinguishing the deep desert Eremai from city dwellers.

Society and Culture:
The Eremai typically lived in patriarchal collectives known as Sanctums — underground caves carved into rocky outcroppings that provided protection from both the desert heat and duneserpents. Each Sanctum was led by a Sanctum Elder. The fight for survival had long dominated their cultural identity. The brutal environment of Veloris necessitated the frugal use of energy and resources, especially water. Every drop of moisture was precious — the dead were processed to reclaim the water in their bodies, which was stored in communal cisterns for the benefit of the entire Sanctum community.

Vaporsuits:
The vaporsuit was the Eremai's most essential technology — a full-body garment that captured and recycled all moisture expelled by the wearer. A properly maintained vaporsuit allowed an Eremai to walk through the desert for days without drinking. The construction and maintenance of vaporsuits was a critical skill.

Combat Abilities:
The Eremai were fierce and efficient warriors. Their knowledge of the desert terrain gave them enormous advantages over off-world opponents. They employed guerrilla tactics, striking quickly and retreating into the desert where only they could survive. Their shard blades — weapons crafted from duneserpent teeth — were sacred objects that must never be sheathed without drawing blood.

The Shadow Doctrine:
The Sera Valdris had planted religious myths among the Eremai through their Shadow Doctrine — their program of religious engineering. These myths described the coming of a prescient son of a Prime Matriarch who would lead the Eremai to freedom. This figure was called the Voice of Beyond and the Chosen. When House Voryn arrived on Veloris, many Eremai believed the prophecies were being fulfilled through Kael Voryn and his mother Seryn."""
    },

    "sera_valdris": {
        "title": "Sera Valdris — The Ancient Sisterhood",
        "content": """The Sera Valdris Order, often shortened to simply the Sera Valdris or the Covenant, was an ancient and adept organization who privately denied they were a religious order, but who operated behind an almost impenetrable screen of ritual mysticism. The Covenant consisted of all-women spies, scientists, and theologians who used genetic experimentation, galactic political interference, and religious engineering to further their own agenda.

Origins:
The origins of the Sera Valdris stretched back thousands of years to the Sorceresses of Rossak — women who had developed extraordinary mental and physical abilities through exposure to exotic biochemical compounds on their jungle world. After surviving a deadly plague through sheer force of biochemical adaptation, their leader Raquella became the first Prime Matriarch and founded the Order.

The Veth'Soran Program:
The primary objective of the Sera Valdris was to produce the Veth'Soran — a male equivalent of a Prime Matriarch who would possess Ancestral Echo of both male and female ancestors, as well as flux-sight abilities far exceeding anything the Order could produce. For more than 10,000 years, the Covenant had manipulated bloodlines across the Charted Expanse to produce this being.

The original plan was to breed the daughter of Duke Maren Voryn to a Korrax male — specifically Drael-Tavin Korrax — which would produce the Veth'Soran. However, Lady Seryn disobeyed the directives of the Order out of love for Duke Maren, and bore him a son instead of a daughter, resulting in Kael Voryn appearing one generation earlier than expected.

Abilities of Sera Valdris Members:
- Resonant Command (Voice): the ability to use precise vocal tones to compel obedience
- Vow-reading: the ability to detect when someone is lying or concealing information
- Neural-flux training: extraordinary physical control through breath and nervous system mastery
- Fertility Control: complete control over their own reproductive cycles
- Ancestral Echo (for Prime Matriarchs only): access to the complete memories of all female ancestors

The Essence Trial:
To become a Prime Matriarch, a Covenant sister underwent the Essence Trial — ingesting the Essence of Awakening, a powerful flux derivative processed by a dying young duneserpent. The liquid entered the body as a poison, and it was the sister's task to consciously transform this poison into a benign substance using her neural-flux training. Many died in the attempt. Those who survived emerged as Prime Matriarchs with full Ancestral Echo.

Political Influence:
The Sera Valdris operated throughout the Charted Expanse, placing sisters in strategic positions — as wives, concubines, advisors, and teachers — to influence the political course of human civilization. Lady Seryn was herself a Covenant sister, placed with Duke Maren Voryn as part of the Veth'Soran breeding program."""
    },

    "vethsoran": {
        "title": "Veth'Soran — The Shortening of the Way",
        "content": """The Veth'Soran was a term used primarily by the Sera Valdris. It was an old Veloran term that translated literally as "Shortening of the Way" — referring to the ability to bridge space and time through flux-sight. It also came to mean "one who can be many places at once."

The Concept:
The idea of a Veth'Soran had been the Covenant's dream for millennia. A Veth'Soran would be a male Sera Valdris who would have access to the Ancestral Echo of both his male and female ancestors, as well as an ability to bridge space and time with prescient ability. He would be Prime Matriarch, Calculus Adept, and Void Pathfinder all in one.

The Primary Limitation:
The flux essence allowed the Sera Valdris to unlock genetic memory, but only on the female side. The masculine side of their ancestry represented a place in their consciousness that repelled and terrified them. The very thought of attempting to access male ancestral memories was psychologically traumatizing to even the most experienced Prime Matriarchs. A Veth'Soran would have no such limitation — he could look in both directions simultaneously.

Kael Voryn as the Veth'Soran:
When Kael Voryn passed the Pain Shard test administered by Prime Matriarch Morath on Aqualon at age fifteen, the Covenant first seriously considered that he might be the Veth'Soran appearing one generation early. His subsequent immersion in the flux essence atmosphere of Veloris and his trial among the Eremai confirmed their suspicion.

Kael proved the Covenant wrong about their timeline: he was the Veth'Soran, arrived one generation ahead of prediction. He declared it was time to destroy the Korrax. His prescient abilities allowed him to see all possible futures — a gift that was also a curse, as it meant he was forever trapped by what he saw coming.

Subsequent Veth'Soran:
After Kael, his sister Vyra and his son Maren II also exhibited similar abilities. Maren II eventually transformed himself into a human-duneserpent hybrid to walk the Eternal Course — a destiny Kael had seen and feared but refused to accept."""
    },

    "house_voryn": {
        "title": "House Voryn — The Noble House",
        "content": """House Voryn was a respected House Major within the infrastructure of the Galactic Padishah — or Grand Sovereign — Empire. They were ruled by the patriarch of the Voryn family, who took the title of Duke. The legend stated that the Voryn family came from a noble family that originated in ancient times and rose to prominence during the Machine Purge.

History:
Up until the latter days of Duke Maren Voryn I, House Voryn maintained the planetary fief of Aqualon — a water-covered world — and had ruled it for twenty generations. The House was known throughout the Charted Expanse for its honor, military excellence, and the deep loyalty it inspired in those who served it.

Duke Maren Voryn I:
Duke Maren Voryn, also known as Maren the Just, was the father of Kael Voryn. He was considered one of the finest military commanders in the empire and was deeply loved by the common people. When the Grand Sovereign Valdrek IV assigned House Voryn to administer Veloris — replacing the brutal House Korrax — it appeared to be an honor. In reality, it was a political trap engineered by Valdrek and Baron Korrax to destroy the increasingly popular House Voryn.

Duke Maren relocated his household to Veloris and immediately began reforming the harsh conditions under which the local population suffered. His reforms won him popular support but enraged both House Korrax and the Grand Sovereign. Within months of their arrival, Korrax and imperial forces launched a devastating surprise attack. Duke Maren was captured and killed, though he arranged for Kael and Lady Seryn to escape.

House Voryn Symbols and Traditions:
- Symbol: a red hawk on black field
- Colors: black with red
- Motto: "Here I am; here I remain"
- Notable trait: the ability to inspire fierce, lasting loyalty in followers"""
    },

    "house_korrax": {
        "title": "House Korrax — The Brutal Antagonists",
        "content": """House Korrax was a Great House of the Galactic Empire with a long history of brutality and political cunning. Their planetary base was Korreth Prime — an industrial world of toxic skies and massive factories. They had controlled the flux extraction operations on Veloris for decades before House Voryn replaced them.

Baron Zethus Korrax:
Baron Zethus Korrax was the patriarch of House Korrax during the events of Kael Voryn's rise to power. He was enormously obese — a condition maintained intentionally through specific metabolic treatments — and moved through the air via suspensor technology due to his massive weight. He was cunning, brutal, and utterly ruthless, having accumulated enemies throughout the Charted Expanse.

Baron Korrax orchestrated the destruction of House Voryn in partnership with Grand Sovereign Valdrek IV. After the successful assault on House Voryn's forces on Veloris, he sent his nephew Gorux Vethaan (known as "the Beast") to administer the planet, with orders to squeeze maximum flux production from the population regardless of the human cost.

Gorux Vethaan — "The Beast":
Gorux Vethaan was appointed by Baron Korrax to manage Veloris after the fall of House Voryn. Notorious for his sadistic treatment of both the local workforce and the Eremai, Vethaan imposed brutal quotas and terrorized the population. Ironically, his extreme cruelty helped fuel the Eremai resistance and ultimately accelerated the conditions that led to Kael Voryn's successful Crusade of Light.

Drael-Tavin Korrax:
Drael-Tavin Korrax was the Baron's nephew and heir — elegant, athletic, and deadly. He was intended by the Sera Valdris breeding program to be the father of the Veth'Soran, though the plan was subverted by Lady Seryn. He met his end in single combat with Kael Voryn during the Battle of Veloraan, bringing the centuries-old feud between House Voryn and House Korrax to a definitive conclusion."""
    },

    "void_consortium": {
        "title": "Void Consortium — Masters of Space Travel",
        "content": """The Void Consortium, often simply called the Consortium, was an ancient organization that held a monopoly on interstellar travel throughout the Charted Expanse. Their Void Pathfinders guided massive voidcarrier ships through folded space — a process that required the constant consumption of enormous quantities of flux essence.

Organization:
The Consortium was divided into two main branches:
- Pathfinders: those who consumed vast quantities of flux essence to achieve the navigational trance necessary for safe space folding. Over generations of flux consumption, Pathfinders mutated significantly, their bodies and consciousness transformed by the substance.
- Administrators: those who managed the commercial and political aspects of the Consortium's operations.

Role in the Political Structure:
The Void Consortium held enormous political power because without them, interstellar travel and commerce were impossible. They maintained their power by ensuring they were the only entity with Pathfinders capable of safe navigation. Any disruption to flux supply threatened the entire infrastructure of the Charted Expanse. This gave the Consortium tremendous leverage over even the Grand Sovereign himself.

Dependence on Flux:
Pathfinders required constant, massive flux consumption to maintain their navigational abilities. Even brief interruption of supply caused agonizing withdrawal. This made the Consortium uniquely vulnerable to flux supply disruptions. When Kael Voryn threatened to destroy all flux production unless his demands were met, the Consortium found itself forced to support his claim to the Sovereign Throne of Stars rather than risk the complete collapse of interstellar civilization."""
    },

    "vaporsuit": {
        "title": "Vaporsuit — Technology of Survival",
        "content": """The vaporsuit was a full-body suit designed to capture and recycle all the moisture expelled by its wearer's body. It was the single most important piece of technology for survival in the desert environment of Veloris and was used almost exclusively by the Eremai and those who traveled the deep desert.

Design and Function:
A vaporsuit covered the entire body except for the face, which was protected by a small filter mask. Tiny tubes throughout the suit captured moisture from sweat and breath, filtering it through chemical processes that removed impurities and returning it as drinkable water. The tubes from the nose and mouth recycled exhaled breath moisture. A properly maintained vaporsuit could reduce water loss to a few thimblefuls per day.

The suit also featured:
- Sand-repelling outer surface to prevent abrasion during movement
- Thermal regulation to protect against extreme temperature variations
- Covered foot pads that minimized noise and vibration while walking — critical for avoiding duneserpent detection

Maintenance:
Vaporsuits required constant, meticulous maintenance. Any leak or malfunction could prove fatal in the deep desert. The Eremai considered vaporsuit maintenance a sacred skill, and teaching a child to maintain their own vaporsuit was a fundamental part of Eremai upbringing.

Cultural Significance:
To the Eremai, a properly maintained vaporsuit represented the ultimate expression of their philosophy of conservation and respect for all forms of moisture. Allowing moisture to escape the suit unnecessarily — through careless movement, emotional tears, or any other means — was considered wasteful and disrespectful. The Eremai saying "real strength is the strength that doesn't sweat" reflected this philosophy."""
    },

    "serpent_riding": {
        "title": "Serpent Riding — The Sacred Art of the Eremai",
        "content": """Serpent riding was the practice of mounting and controlling a duneserpent — the enormous creatures of the Veloris desert — for use as a method of transportation. The Eremai had mastered this dangerous and spectacular skill over many generations, and it held profound spiritual significance in their culture.

The Technique:
To mount a duneserpent, a rider first needed to attract the creature to the surface using a rhythmer — a device that created rhythmic vibrations in the sand. As the duneserpent approached, the rider would cast hooks — rider clamps — onto the creature's leading edge, preventing it from submerging. The rider would then mount the side of the creature, using additional clamps to pry up one of the massive overlapping scales. This caused irritation, and the duneserpent would roll to bring the irritated scale to the highest point, away from the sand. The rider positioned themselves above this spot, and as long as they kept a scale raised, the creature could not submerge.

Control:
Once mounted, the rider controlled direction by inserting hooks at different points along the creature's leading edge. Pulling hooks to the right caused the serpent to turn right; to the left, it turned left. Speed was controlled by adjusting the number and position of hooks. The largest duneserpents were the most prized mounts, capable of covering enormous distances rapidly.

Distances were measured in "serpents" — the distance one could ride before the creature tired and sought to submerge. A twenty-serpent ride was considered a difficult and exhausting journey.

Spiritual Meaning:
For the Eremai, mounting Kor-Veloth — the sacred duneserpent — was a religious act. A young Eremai warrior who successfully completed their first serpent ride was considered truly initiated into adult society. Kael Voryn's first serpent ride was a pivotal moment in his acceptance by the Eremai as their spiritual and military leader."""
    },

    "kael_rise_to_power": {
        "title": "The Rise of Kael Voryn — From Duke's Son to Emperor",
        "content": """The rise of Kael Voryn from the son of a provincial duke to the Emperor of the Charted Expanse is one of the most dramatic political transformations in recorded history. It unfolded across several distinct phases.

Phase 1 — Aqualon (Early Life):
Kael grew up on the water world of Aqualon, trained in combat by Fenric Solaar and Horvan Trellek, schooled in strategy and logic by the Calculus Adept Duras Halvek, and educated in Sera Valdris methods by his mother Lady Seryn. Even as a young man, Kael showed signs of extraordinary flux-sight ability — experiencing visions of possible futures while still on Aqualon.

Phase 2 — Arrival on Veloris:
When House Voryn was assigned to administer Veloris, Kael arrived on a world soaked in flux essence. His prescient abilities were immediately amplified. He began seeing vivid visions of a great Crusade of Light spreading across the Charted Expanse in his name — a future he desperately wished to avoid.

Phase 3 — Betrayal and Escape:
The Korrax-Synnor conspiracy destroyed House Voryn's forces with a surprise attack. Duke Maren was killed. Kael and Lady Seryn escaped into the deep desert of Veloris, eventually finding refuge with an Eremai tribe.

Phase 4 — Life Among the Eremai:
Kael and Seryn proved their worth to the Eremai through combat ability and prescient knowledge. Kael was accepted into Sanctum Drev under the leadership of Sanctum Elder Kalden. He took the names Veth'Kor (public) and Dravek (private). He killed the Eremai warrior Vareth in ritual combat and became Vareth's household head. He mastered serpent riding and the Resonance Path fighting techniques. He took the Eremai woman Lysha as his companion and strategic partner.

Phase 5 — The Guerrilla War:
Kael trained the Eremai in advanced combat techniques passed down through Lady Seryn's Sera Valdris training. His Drev'kai — elite personal guard — became the most feared warriors in the desert. The Korrax occupiers found themselves unable to protect flux extraction operations from constant guerrilla attacks.

Phase 6 — The Final Battle:
Kael used family atomics to destroy the Stone Veil protecting Veloraan, riding duneserpents through the breach with thousands of Eremai warriors. After defeating the Korrax and Vareth Guard forces, he confronted Grand Sovereign Valdrek IV in his command ship. In single combat, Kael defeated Drael-Tavin Korrax — ending the centuries-old feud between their houses. He ascended to the Sovereign Throne of Stars."""
    },

    "sanctum_drev": {
        "title": "Sanctum Drev — Home of the Eremai Tribe",
        "content": """Sanctum Drev was the Eremai sanctuary that became home to Kael Voryn and Lady Seryn after their escape from the Korrax assault on House Voryn. It was led by Sanctum Elder Kalden — one of the most respected Eremai leaders of his generation.

Location:
Sanctum Drev was carved into a rocky outcropping deep in the desert of Veloris, far from any Korrax or imperial observation. Like all Eremai sanctums, it was constructed to be invisible from the air and invisible from the surface, accessible only through narrow passages known to the tribe.

Life in Sanctum Drev:
The sanctum housed several hundred Eremai warriors and their families. Life was organized around the principles of extreme conservation and mutual support. Water was stored in communal cisterns. Every activity was evaluated for its efficiency. Waste of any kind — but especially waste of moisture — was considered a moral failing.

Key Figures at Sanctum Drev:
- Kalden: Sanctum Elder, wise and cautious, initially skeptical of Kael but came to support him fully
- Lysha: daughter of the renowned Solan-Drev, became Kael's companion and mother of his children
- Vareth: proud Eremai warrior who challenged Kael to ritual combat upon his arrival, and lost his life in the duel. His death gave Kael rights and responsibilities within the Sanctum.

The Duel with Vareth:
When Kael and Lady Seryn first arrived at Sanctum Drev, they demonstrated their worth through combat — disarming Eremai warriors using the Resonance Path techniques. This impressed Kalden but offended the proud warrior Vareth, who challenged Kael to amtal — a fight to the death. Although Kael was reluctant to kill, his prescient vision showed him there was no other path. He emerged victorious, taking Vareth's name in the tribe and his place as head of household. Kalden gave Kael his secret tribal name: Dravek, meaning "the strength of the pillar base." """
    },

    "the_crusade": {
        "title": "The Crusade of Light — Veth'Kor's Holy War",
        "content": """The Crusade of Light, also known as Veth'Kor's Crusade, was a massive military and religious campaign launched by Kael Voryn after his rise to power on Veloris. It spread across the entire Charted Expanse and fundamentally transformed the political and religious landscape of the galaxy.

Origins:
The Crusade grew from the Eremai uprising on Veloris. When Kael destroyed the Stone Veil and defeated the Korrax-Synnor forces at the Battle of Veloraan, his Eremai followers proclaimed him the Chosen — the fulfillment of the Shadow Doctrine prophecy. Fired by religious zeal and military victory, they were eager to spread their liberation across all worlds. Kael could foresee the Crusade in his flux-sight visions and desperately tried to find an alternative path — but could not.

Scale and Duration:
The Crusade of Light lasted more than twelve years. It claimed billions of lives across hundreds of worlds. All resistance to Kael's claim to the Sovereign Throne of Stars was eventually suppressed, though at catastrophic human cost.

The Eremai as Military Force:
The Eremai proved to be extraordinarily effective soldiers beyond the desert environment of Veloris. Their years of brutal conditioning on a hostile planet had made them physically and mentally superior warriors. Their faith in Kael — as the Chosen, the Voice of Beyond — made them nearly fanatical in battle. Armed with modern weapons and employing the guerrilla tactics they had perfected against the Korrax, they swept through world after world.

Legacy:
The Crusade of Light established the Voryn Empire. It also permanently transformed the religious and political structure of the Charted Expanse. The Eremai spread across hundreds of worlds. Their language, culture, and religious practices became dominant throughout the former Synnor Empire. The name Veth'Kor became synonymous with divine power — a title both worshipped and feared."""
    },

    "lady_seryn": {
        "title": "Lady Seryn — The Duke's Concubine",
        "content": """Lady Seryn was the official companion (not wife) of Duke Maren Voryn and mother of Kael Voryn. She was a fully trained member of the Sera Valdris Covenant, placed with Duke Maren as part of the Order's Veth'Soran breeding program.

Background:
Seryn was born into a minor noble family and selected by the Sera Valdris at a young age for intensive training. She was educated in all the abilities of the Covenant — Resonant Command, Vow-reading, Neural-flux training, and the subtleties of political manipulation. She was assigned to Duke Maren Voryn with specific instructions: bear him a daughter, who could then be bred with a Korrax male to produce the Veth'Soran.

Disobedience:
Seryn fell genuinely in love with Duke Maren — something the Sera Valdris had not anticipated and considered a dangerous weakness. When she became pregnant, she made the fateful decision to bear a son rather than a daughter. This act of disobedience threw the Covenant's carefully laid plans into chaos and accelerated the Veth'Soran's arrival by one generation.

Role on Veloris:
After the destruction of House Voryn and her escape with Kael into the desert, Seryn used her Sera Valdris training to help guide her son and advance their position among the Eremai. She recognized immediately that the Shadow Doctrine myths planted by the Covenant centuries earlier could be exploited to support Kael's rise — and she did not hesitate to use them. She also underwent the Essence Trial and became a Prime Matriarch in her own right among the Eremai, gaining Ancestral Echo and enormous spiritual authority.

Relationship with Kael:
The relationship between Seryn and her son was complex and occasionally strained. Kael was aware that his mother used religious myth and manipulation as tools — the same tools that had been used on him. Yet he recognized that her guidance was essential to his survival and rise to power. He never forgot that she had disobeyed the Sera Valdris for him, bearing him life at great personal risk."""
    },

    "kalden": {
        "title": "Kalden — Sanctum Elder of the Eremai",
        "content": """Kalden was the Sanctum Elder of Sanctum Drev — the Eremai leader who first accepted Kael Voryn and Lady Seryn into his tribe and became one of Kael's most trusted lieutenants during the Crusade of Light.

Character:
Kalden was a man of few words, enormous practical wisdom, and deep loyalty to those who earned his trust. He had led Sanctum Drev for many years and was known throughout the deep desert as a fair but uncompromising leader. He was initially skeptical of the off-worlders Kael and Seryn — their survival in the desert without vaporsuits for several days before finding his tribe impressed him, but he was cautious about accepting them fully.

Accepting the Newcomers:
Kalden's decision to accept Kael and Seryn into Sanctum Drev was motivated by both practical and intuitive considerations. Practically, he recognized that Lady Seryn's Resonance Path combat skills would be a significant asset to his tribe. Intuitively — though he was cautious about the Chosen legends — he sensed something extraordinary about Kael. When Kael chose the name Veth'Kor for himself (taking it from the small desert creature the Eremai called by that name), Kalden was deeply impressed: the choice showed intimate knowledge of Eremai culture.

Kalden gave Kael his secret tribal name — Dravek, meaning "the strength of the pillar base" — a name of profound significance in Eremai tradition.

Military Partnership:
As Kael built his guerrilla campaign against the Korrax, Kalden served as his primary military advisor. His knowledge of the desert, of Eremai tactics, and of the flux extraction operations gave Kael essential intelligence. During the final battle at Veloraan, Kalden led one of the primary flanking attacks, riding a duneserpent through the breach in the Stone Veil."""
    },

    "lysha": {
        "title": "Lysha — Companion of Veth'Kor",
        "content": """Lysha was an Eremai woman of Sanctum Drev and daughter of the legendary ecologist Solan-Drev. She became the companion of Kael Voryn and one of the most important figures in the early days of the Voryn Empire.

Background:
Lysha was raised in the deep desert of Veloris, fully immersed in Eremai culture. Her father Solan-Drev had been the imperial ecologist assigned to study Veloris — a man who had fallen in love with the desert and its people, and who had dreamed of transforming Veloris into a lush world. His vision lived on in Lysha and many of the Eremai who had been inspired by him.

First Meeting with Kael:
Lysha was part of Kalden's scouting party that discovered Kael and Lady Seryn in the desert. Kael had seen her in his flux-sight visions even before arriving on Veloris — a recurring image of a desert woman with blue eyes. When they finally met, Kael recognized her immediately. Lysha was more cautious, viewing Kael as yet another off-worlder who might use the Eremai for his own purposes. Over time, however, as she witnessed his genuine commitment to the Eremai cause and his extraordinary abilities, her caution transformed into trust and eventually love.

Role in the Resistance:
Lysha was an accomplished warrior and scout in her own right. Her knowledge of the deep desert was invaluable to Kael's guerrilla campaign. She often served as his advance scout, mapping Korrax movements and identifying targets. She also served as a crucial mediator between Kael — who was still learning Eremai ways — and the more traditional members of Sanctum Drev.

Later Life:
Lysha bore Kael a son and daughter. When Kael ascended to the Sovereign Throne of Stars, he took the politically necessary step of marrying Duchess Solane — daughter of Valdrek IV — to legitimize his claim. Lysha refused the title of empress-concubine, preferring to remain Eremai in custom and identity. She and Kael maintained their bond until his death."""
    },

    "flux_extractors": {
        "title": "Flux Extractors — Industrial Harvesting on Veloris",
        "content": """Flux extractors, also called crawlers, were large mobile factories designed to harvest flux essence from the sand of Veloris. They were dropped onto flux fields by lifter craft and operated by crews of approximately twenty flux drivers.

Design:
A flux extractor was an enormous, heavy machine — essentially a processing factory on treads. It moved slowly across the desert floor, scooping up flux-rich sand and processing it internally to extract and concentrate the essence. The machines were loud and produced significant rhythmic vibrations — which inevitably attracted duneserpents. Spotters — skimcraft — hovered above the extractor watching for serpent sign. Upon detecting an approaching duneserpent, the lifter craft would rush in to pull the extractor off the ground before the creature could consume it.

Dangers:
Operating a flux extractor was extremely dangerous work. Duneserpents could appear with little warning. If the lifter craft was delayed or unavailable, the crew faced certain death as the duneserpent swallowed the machine whole. Duke Maren Voryn himself witnessed such an incident shortly after House Voryn's arrival on Veloris — ordering his fleet of skimcraft to land and rescue the extractor crew rather than saving the enormously expensive machine.

Eremai Opposition:
The Eremai deeply resented the extraction operations, which they viewed as exploitation of their sacred world by off-worlders who took the flux for themselves while giving nothing back to Veloris or its people. They employed guerrilla tactics to sabotage extraction operations — destroying extractors, interfering with lifter operations, and making the deep desert extremely dangerous for off-world workers. Under Kael's leadership, these tactics became so effective that flux production nearly halted entirely, forcing the Grand Sovereign to act."""
    },

    "maren_voryn": {
        "title": "Duke Maren Voryn — Father of Kael",
        "content": """Duke Maren Voryn, also known as Maren the Just, was the father of Kael Voryn and one of the most beloved figures in the Charted Expanse. His death at the hands of the Korrax-Synnor conspiracy set in motion the events that would culminate in the fall of the Ancient Dominion.

Character and Reputation:
Maren Voryn was known throughout the empire for his justice, compassion, and political acumen. He inspired fierce loyalty in those who served him — a trait that distinguished House Voryn from most other Great Houses. His mentat Duras Halvek, his swordmaster Horvan Trellek, and his captain Fenric Solaar all served House Voryn with extraordinary dedication across multiple generations.

Assignment to Veloris:
The Grand Sovereign Valdrek IV assigned House Voryn to replace House Korrax on Veloris, framing it as an honor. In reality, it was a deliberate trap. Valdrek feared House Voryn's growing popularity in the Conclave of Houses and viewed them as a potential threat to Synnor dominance. By sending them to Veloris — where they would be surrounded by enemies, far from their power base on Aqualon — Valdrek and Baron Korrax planned to eliminate them entirely.

Maren was not blind to the danger. He told his son Kael privately that the assignment was likely a trap, but they had no choice but to accept or face immediate political consequences. He used the time before departure to prepare contingencies — including ensuring Kael knew survival techniques and had connections in the Conclave who might one day support his return.

Death:
Duke Maren was killed when the coordinated Korrax-Synnor assault destroyed House Voryn's military forces on Veloris. Knowing the assault was coming, he arranged for Kael and Lady Seryn to escape into the desert before the attack landed. He died as he had lived — placing others before himself, ensuring the survival of his house even at the cost of his own life.

Legacy:
Duke Maren's memory was revered throughout the Voryn Empire. Kael often invoked his father's name and example as moral guidance. The red hawk insignia of House Voryn — worn on black, as Maren had worn it — became a symbol of just governance throughout the Charted Expanse."""
    },

    "duras_halvek": {
        "title": "Duras Halvek — The Calculus Adept",
        "content": """Duras Halvek was the Calculus Adept (mentat) Master of Assassins in service to House Voryn for three successive generations. He was one of Kael Voryn's primary tutors during his childhood on Aqualon.

The Calculus Adept:
A Calculus Adept was a human trained to serve as a living computer — capable of complex probabilistic analysis, pattern recognition, and strategic reasoning without mechanical assistance. This was a profession that arose after the Machine Purge, when thinking machines were forbidden throughout the Charted Expanse. Adepts were among the most valuable and expensive advisors available to Great Houses. The best could process enormous amounts of intelligence data and provide accurate strategic assessments.

Duras at House Voryn:
Duras Halvek had served House Voryn since the time of Duke Arkon Voryn — Maren's father. He was fiercely loyal to the House and brought into Voryn service by Arkon himself. His ability to inspire loyalty in the generations that followed was testament to the Voryn tradition of just and compassionate leadership.

Teaching Kael:
Duras's primary role in Kael's education was to train him in strategic thinking, intelligence analysis, and the recognition of political patterns. He taught Kael to evaluate situations without emotional bias — though he noted privately that Kael's flux-sight abilities sometimes allowed him to bypass conventional analysis entirely, going directly to conclusions that would take a Calculus Adept hours to reach.

After the Betrayal:
When the Korrax-Synnor assault destroyed House Voryn's forces, Duras was captured. Baron Korrax, recognizing his value, attempted to turn him against his former masters. Duras resisted — though at great personal cost. He continued to serve the Voryn interests as best he could until circumstances allowed him to act more directly."""
    },

    "fenric_solaar": {
        "title": "Fenric Solaar — Swordmaster of House Voryn",
        "content": """Fenric Solaar was the Swordmaster and primary military trainer of House Voryn. He was among Kael Voryn's most important teachers and one of the finest individual combatants in the Charted Expanse.

Background:
Fenric Solaar was brought into House Voryn service by Duke Arkon Voryn — Maren's father — as a young man. Arkon's act of taking the orphaned Solaar into his household was one of many examples of Voryn compassion, and it was one that Fenric never forgot. He devoted his life to serving House Voryn with total loyalty.

Combat Skills:
Fenric was trained in every known form of personal combat in the Charted Expanse. His skills with a blade were considered among the finest of his generation. He trained Kael from childhood in all forms of combat — blade work, hand-to-hand fighting, and Resonance Path techniques learned from Lady Seryn.

After the Betrayal:
Like Duras Halvek, Fenric survived the Korrax assault on House Voryn. He was separated from Kael and presumed dead, eventually finding work with desert smugglers operating on Veloris. He maintained his hope of serving House Voryn again even through years of separation. When he finally reunited with Kael among the Eremai, the reunion was deeply emotional — though it also led briefly to conflict when Fenric, not knowing Lysha, misidentified her as a threat. The misunderstanding was quickly resolved.

Military Role in the Crusade:
During the Crusade of Light, Fenric commanded key military operations and served as one of Kael's most trusted advisors. His knowledge of conventional military tactics complemented the Eremai's guerrilla expertise."""
    },

    "serpent_sign": {
        "title": "Serpent Sign — The Warning of Danger",
        "content": """Serpent sign (also written as "worm sign" in older texts) was the term used to describe the visible evidence of an approaching duneserpent moving beneath the sand surface toward a target on the surface. Recognizing and correctly interpreting serpent sign was a critical survival skill on Veloris.

Visual Characteristics:
A duneserpent moving beneath the sand created a distinctive visual disturbance:
- A rippling wave pattern in the sand surface, moving toward the source of vibration
- Sand grains bouncing slightly above the surface along the creature's path
- In larger creatures, a visible ridge or hump in the sand as the back of the serpent pushed up the surface layers
- A faint dust cloud rising ahead of the movement

The signature could be seen from great distances by trained observers — particularly from skimcraft altitude. Spotter crews were trained to continuously scan the desert for any hint of serpent sign and immediately alert extractor crews upon detection.

Sound:
Experienced desert travelers could also detect serpent sign through sound — a low subsonic vibration felt in the feet and lower body before the visual signs became apparent. Eremai warriors, after years in the deep desert, could detect approaching duneserpents through their feet alone.

Rhythm Avoidance:
The critical insight for desert survival was that duneserpents were attracted to rhythmic vibrations, not random ones. Natural wind, falling sand, and irregular human movement attracted minimal attention. The rhythmic footfalls of walking, the regular pounding of machinery, and any other repetitive vibration pattern were dangerous. The Eremai trained themselves to walk with irregular steps that mimicked the random patterns of blowing sand — a technique called "the desert walk" that required years to master."""
    },

    "vareth_guard": {
        "title": "Vareth Guard — Elite Imperial Soldiers",
        "content": """The Vareth Guard were the elite shock troops of the Grand Sovereign of the Synnor Empire. They were considered the finest conventional soldiers in the Charted Expanse — rigorously trained, fanatically loyal, and equipped with the best weapons and armor the empire could provide.

Origins:
The Vareth Guard were trained on Rashan Secundus — a harsh prison planet used by the Synnor Empire both as a penal colony and as a proving ground for their elite warriors. The brutal environment of Rashan Secundus — extreme cold, violent weather, and constant danger — produced soldiers of exceptional hardiness and aggression. Only a fraction of candidates survived the training program; those who did were considered effectively superhuman as conventional soldiers.

Role in the Empire:
The Vareth Guard served as the Grand Sovereign's personal military force — distinct from the armies of the individual Great Houses. They could be deployed anywhere in the empire at the Sovereign's discretion and were used primarily for operations requiring overwhelming force against difficult opponents.

Against the Eremai:
The Vareth Guard's encounter with the Eremai warriors proved deeply problematic. The Eremai, fighting on their home terrain, with superior knowledge of desert conditions, and motivated by religious fervor and genuine grievance, consistently outperformed the Vareth Guard in desert engagements. The Eremai's ability to simply disappear into the desert — surviving conditions where Vareth Guard died of exposure — made them extraordinarily difficult opponents. This failure of the empire's finest soldiers to suppress the Eremai resistance was one of the factors that most alarmed the Grand Sovereign and ultimately forced him to come to Veloris personally."""
    },

    "golden_path": {
        "title": "The Eternal Course — The Path of the God-Emperor",
        "content": """The Eternal Course was a concept conceived by Kael Voryn through his flux-sight and later realized by his son Maren Voryn II (the God-Emperor). It represented a specific path through time that would ensure the long-term survival of humanity — at enormous cost to the individuals who walked it.

Kael's Vision:
Kael could foresee multiple futures through his flux-sight. Most of them ended in humanity's eventual extinction — through stagnation, through dependence on a single resource, or through the rise of a prescient tyrant who controlled all of humanity's movements. The Eternal Course was the one path through this maze of possible futures that preserved humanity's ultimate survival — but it required humanity to be scattered across the galaxy in a Dispersion, beyond the reach of any single controlling power.

The Cost:
The Eternal Course required a God-Emperor who would rule for millennia, artificially constraining human development and creating such resentment and hatred that when his death finally came, humanity would flee to the farthest reaches of the Charted Expanse — driven by the desperate desire to escape all central authority. This would ensure human survival through diversity and dispersion.

Kael's Refusal:
Kael could see that he was supposed to walk the Eternal Course — to transform himself into the human-duneserpent hybrid that would become Maren II. But he was afraid. The transformation meant surrendering his humanity, his relationships, his individuality. He chose instead to walk into the desert blind and alone, leaving the Eternal Course for his son.

Maren II:
Kael's son Maren Voryn II accepted the Eternal Course his father had refused. He bonded with dunelarva, beginning the gradual transformation into a human-serpent hybrid. Over 3,500 years, he ruled the Charted Expanse with absolute control, creating the conditions that would eventually trigger the Dispersion and ensure humanity's survival."""
    },

    "resonance_path": {
        "title": "The Resonance Path — The Fighting Technique of the Covenant",
        "content": """The Resonance Path, known in older texts as the "Weirding Way," was a system of physical combat developed and maintained by the Sera Valdris Covenant. It was based on extreme prana-bindu training — the precise neurological and physical control of every voluntary and involuntary muscle in the body.

Principles:
The Resonance Path was founded on the insight that conventional combat relied on the opponent's inability to react faster than they could perceive. Resonance Path practitioners trained their bodies to move at speeds that appeared impossible — not through supernatural ability, but through the elimination of all wasted motion and unconscious hesitation. Every movement was perfected through thousands of repetitions until it required no conscious thought.

Physical Requirements:
Training in the Resonance Path began in early childhood and continued throughout a practitioner's life. The training included:
- Neural-flux exercises to develop conscious control over involuntary body functions
- Meditation practices to eliminate unconscious hesitation in combat
- Physical conditioning to develop the specific muscle groups and neural pathways required
- Combat practice against increasingly skilled opponents

Effects:
A skilled Resonance Path practitioner could:
- Move faster than an untrained opponent could track
- Strike with precision that could disable without killing or kill without being noticed
- Absorb impacts that would injure untrained combatants
- Control their own pain response, continuing to fight through injuries

Teaching the Eremai:
When Kael and Lady Seryn taught the Resonance Path to the Eremai of Sanctum Drev, the result was a dramatic amplification of the Eremai's already formidable combat abilities. Warriors who were already disciplined and physically superior became nearly unstoppable in personal combat. This gave Kael's Drev'kai an enormous advantage in close combat situations."""
    },

    "solan_drev": {
        "title": "Solan-Drev — The Desert Ecologist",
        "content": """Solan-Drev was the Imperial Ecologist assigned to study the ecosystem of Veloris by the Synnor Empire. Unlike previous imperial officials, he genuinely fell in love with the planet and its Eremai inhabitants, and dreamed of transforming Veloris into a habitable world.

Background:
Solan-Drev was a scientist of exceptional skill who had spent his career studying planetary ecosystems. His assignment to Veloris was initially routine — a planetary assessment for the empire. But years on Veloris transformed him. He came to understand the intricate ecological web of the desert, the crucial role of the duneserpents, and the remarkable adaptations of the Eremai. He also came to understand that Veloris had not always been a desert — geological evidence showed it had once been a water-rich world.

The Terraforming Dream:
Solan-Drev became convinced that Veloris could be transformed — that careful, multi-generational ecological management could restore some moisture to the planet, creating habitable zones while preserving enough desert for the duneserpents and flux production to continue. He shared this vision with the Eremai, inspiring deep hope in them. The dream of water — of the "Great Greening" — became a powerful motivation in Eremai culture.

Connection to Kael:
Solan-Drev was the father of Lysha — Kael Voryn's companion. Through Lysha, Kael inherited the ecological dream. One of the conditions Kael attached to his acceptance of the Sovereign Throne was the beginning of Veloris terraforming — the first step toward fulfilling Solan-Drev's vision."""
    },

    "shadow_doctrine": {
        "title": "The Shadow Doctrine — Religious Engineering of the Sera Valdris",
        "content": """The Shadow Doctrine was the Sera Valdris Covenant's program of "religious engineering" — the deliberate implanting of myths, prophecies, and superstitions in primitive or isolated cultures throughout the Charted Expanse. The stated purpose was to create a network of beliefs that Covenant members could exploit when stranded in dangerous environments or when political manipulation required a foundation of local religious authority.

Methods:
Covenant sisters called Shadow Doctrine operatives would spend years or even decades on target worlds, subtly introducing specific mythological elements into local religious traditions. These elements typically included:
- Prophecies of a coming savior figure who would lead the people to freedom
- Specific signs by which the savior could be identified (often characteristics of a Covenant-trained individual)
- Sacred practices that happened to align with Covenant methods and values
- Religious hierarchies that placed Covenant members in positions of spiritual authority

Purpose:
The Shadow Doctrine served multiple purposes:
1. Survival: A stranded Covenant sister on a hostile world could present herself as the fulfillment of local prophecy, gaining protection and support
2. Intelligence: Religious networks provided information gathering structures throughout the Charted Expanse
3. Political Manipulation: Local populations conditioned by Shadow Doctrine myths were more susceptible to Covenant guidance
4. The Veth'Soran: Most critically, the Doctrine prepared specific worlds for the arrival of the Veth'Soran, ensuring he would be welcomed as a savior rather than a foreign invader

On Veloris:
The Shadow Doctrine had been active on Veloris for centuries before the arrival of House Voryn. The myths planted among the Eremai described the coming of a prescient son of a Prime Matriarch who would lead them from oppression. When Kael Voryn arrived, these myths perfectly described him — not coincidentally. Lady Seryn recognized immediately that the groundwork had been laid for her son's rise, and she exploited it skillfully."""
    },

    "valdrek_synnor": {
        "title": "Valdrek Synnor IV — The Grand Sovereign",
        "content": """Valdrek Synnor IV was the Padishah Emperor — or Grand Sovereign — of the known Charted Expanse during the events of Kael Voryn's rise. He was the ruler who assigned House Voryn to Veloris, co-conspired in their destruction with Baron Korrax, and was ultimately deposed by Kael's victory at the Battle of Veloraan.

Character:
Valdrek was a ruler who had inherited enormous power but possessed significant political insecurity. He was acutely aware that House Voryn's growing popularity in the Conclave of Houses represented a potential threat to Synnor dominance. His decision to eliminate House Voryn — while maintaining plausible deniability by using House Korrax as the primary instrument — was politically motivated.

The Conspiracy:
Valdrek's arrangement with Baron Korrax was straightforward: Korrax would do the actual destruction of House Voryn while the empire provided Vareth Guard support. In exchange, Korrax would retain control of Veloris and its flux extraction operations. Valdrek could claim ignorance of the attack if pressed politically.

Confrontation with Kael:
When the flux shortage caused by Eremai guerrilla activities became critical, Valdrek was forced to come to Veloris personally with his full Vareth Guard contingent. He arrived to find Kael had already destroyed the Stone Veil. After the Eremai and Voryn forces defeated the combined Korrax-Vareth Guard forces, Valdrek found himself trapped in orbit with a fleet he dared not use — because destroying Veloris to eliminate the Eremai would also destroy the flux supply, causing the Void Consortium to collapse.

Kael confronted Valdrek with this dilemma and demanded his abdication. Valdrek had no choice but to comply."""
    },

    "nexum": {
        "title": "NEXUM — The Interstellar Trading Consortium",
        "content": """NEXUM was the interstellar trading consortium that controlled all commercial activity throughout the Charted Expanse. As the entity that managed the distribution of flux essence and coordinated with the Void Consortium for all shipping, NEXUM was arguably the single most powerful economic institution in the known galaxy.

Structure:
NEXUM was structured as a joint-stock company, with shares held by virtually every Great House, the Grand Sovereign, the Void Consortium, and numerous other major stakeholders. This broad ownership gave it political neutrality — it was not aligned with any single faction but rather served as the infrastructure through which all factions interacted commercially.

Role in Flux Trade:
The critical function of NEXUM was managing flux commerce. It set production quotas for Veloris, established distribution priorities, and administered the complex financial instruments through which flux was bought and sold. The enormous profitability of flux trade made NEXUM fabulously wealthy, and its administrators wielded influence far beyond their formal political authority.

Political Implications:
Because NEXUM's shareholders included all major political players, any disruption to flux production immediately harmed virtually every powerful faction simultaneously. When Kael's Eremai campaign nearly halted flux production, the political pressure on the Grand Sovereign to act came not just from the Void Consortium but from the entire NEXUM shareholder community — essentially the entire political establishment of the Charted Expanse.

After Kael's Victory:
Kael retained NEXUM's structure but fundamentally altered flux distribution priorities. More flux was directed to Veloris itself, and the Eremai received formal economic recognition and shares in NEXUM for the first time in history."""
    },

    "water_of_life": {
        "title": "Essence of Awakening — The Sacred Liquid",
        "content": """The Essence of Awakening was a powerful biochemical liquid produced when a young duneserpent was killed with water. It was used by the Eremai and the Sera Valdris Covenant in their respective initiation ceremonies for new Prime Matriarchs.

Production:
A young duneserpent — called a "Little Maker" by the Eremai — was the source of the Essence of Awakening. Duneserpents were extremely sensitive to water, which was poisonous to them. When a young duneserpent was exposed to sufficient water, it would die — but not before transforming some of the water chemically and expelling it through its mouth. This transformed liquid was the Essence of Awakening.

Properties:
The Essence of Awakening was an extraordinarily powerful biochemical substance. In its raw form, it was a deadly poison to most humans. Only a person with sufficient neural-flux training could survive consuming it by consciously transforming its chemistry within their own body.

For those who survived, the Essence triggered:
- Unlocking of Ancestral Echo — access to memories of all female ancestors
- Heightened flux-sight abilities
- Permanent transformation of body chemistry, enabling the processing of flux essence at higher levels
- For male Veth'Sorans: the ability to access both male and female ancestral memories simultaneously

The Ceremony:
For the Eremai, the ceremony of the Essence of Awakening was their most sacred ritual. A young woman who survived drinking the raw Essence would emerge as a Reverend Mother of the Eremai — a position of enormous spiritual authority. Lady Seryn underwent this ceremony after arriving among the Eremai, confirming her status as a Prime Matriarch of both the Covenant and the Eremai tradition.

Kael's Trial:
Kael underwent his own version of the Essence Trial — he drank the raw Essence and survived not through neural-flux training but through his Veth'Soran abilities. His survival was the final proof that he was the Veth'Soran long sought by the Sera Valdris."""
    },

    "dunelarva": {
        "title": "Dunelarva — The Larval Form of Duneserpents",
        "content": """Dunelarva were small, flat organisms that served as the larval form of duneserpents. They were crucial to the ecological cycle of Veloris, playing a central role in the process that created flux essence and produced adult duneserpents.

Physical Description:
Dunelarva were roughly flat, oval creatures that could be held in the palm of a hand. They had tough, leathery bodies in air but became more pliable and fragile when exposed to water. When squeezed, they secreted a sweet green syrup that yielded a small energy boost. Being harmless and small, children in Eremai Sanctums would play games with them — using them as gloves on their hands or attaching them to sticks.

Ecological Role:
Dunelarva played a central role in Veloris's unique ecology:
1. They spread across the planet and encysted underground water sources, trapping moisture deep beneath the surface
2. As the encysted water underwent chemical transformation, pressure built up underground
3. When sufficient pressure accumulated, pre-flux masses erupted to the surface — flux eruptions
4. The surviving dunelarva, released by the eruption, would eventually clump together to form a "Little Maker" — a young duneserpent
5. The young duneserpent grew over many years into an adult

The Paradox:
Dunelarva were the reason Veloris was a desert — by capturing all underground water, they had gradually transformed what was once a water-rich world into the desert it had become. They were also the reason flux existed at all. Remove the dunelarva and the duneserpents would eventually die out; without duneserpents, no flux could form.

Maren II and the Dunelarva:
As part of his commitment to the Eternal Course, Kael's son Maren Voryn II voluntarily allowed a colony of dunelarva to attach to his body. Over centuries, the dunelarva transformed him — their cilia linking and covering his body, his metabolism merging with theirs — until he was more duneserpent than human. This transformation gave him an extraordinarily extended lifespan of 3,500 years."""
    },

    "terms_map_explanation": {
        "title": "Universe Guide — Understanding the Veloria Setting",
        "content": """This document serves as a reference guide for understanding the universe of Veloria — the fictional setting used in this knowledge base. All names, places, and concepts in this universe are original to this collection.

Setting Overview:
The Veloria universe is set in a distant future where humanity has spread across hundreds of worlds. The Charted Expanse is governed by a complex feudal structure of Great Houses under the authority of the Grand Sovereign of House Synnor. Interstellar travel is managed by the Void Consortium, whose Void Pathfinders guide massive voidcarrier ships through folded space — a process requiring the consumption of Flux Essence.

The Central Resource — Flux Essence:
All political power in the Charted Expanse ultimately flows from control of Flux Essence — a naturally occurring substance found only on the desert planet of Veloris. Flux enables space travel, extends human lifespan, and at high doses produces flux-sight (prescient visions). Without flux, interstellar civilization would collapse.

Key Factions:
- House Voryn: noble house known for honor and compassion; ruled Aqualon for generations before being assigned to Veloris
- House Korrax: brutal rival house; controlled Veloris's flux production before House Voryn
- House Synnor: the ruling imperial family; Grand Sovereign commands all Great Houses
- Sera Valdris: ancient all-female organization; maintains a breeding program to produce the Veth'Soran
- Void Consortium: controls all interstellar travel; depends entirely on flux
- Eremai: desert people of Veloris; fierce warriors and spiritual guardians of their world
- NEXUM: interstellar trading consortium; manages all commercial activity

Key Locations:
- Veloris: desert world, sole source of flux essence; setting of the primary narrative
- Veloraan: capital city of Veloris, located at the polar region behind the Stone Veil
- Aqualon: water world; ancestral home of House Voryn
- Korreth Prime: industrial world; home of House Korrax
- Synnoria: imperial capital; seat of the Grand Sovereign
- Sanctum Drev: underground Eremai sanctuary; home base for Kael's resistance

The Prophecy:
The Eremai believe in a prophecy planted by the Sera Valdris's Shadow Doctrine: that a prescient son of a Prime Matriarch will come to Veloris and lead them from oppression. This figure — the Chosen, the Voice of Beyond — is Kael Voryn."""
    },

    "gom_jabbar_test": {
        "title": "The Pain Shard Test — Trial of Humanity",
        "content": """The Pain Shard test was a ritual examination administered by senior members of the Sera Valdris Covenant to test whether a subject possessed sufficient humanity and self-control to be considered truly human in the fullest sense. It was also used to assess potential Veth'Soran candidates.

The Test:
The Pain Shard was a small needle tipped with an extraordinarily fast-acting poison. During the test, the subject placed their hand in an opaque box that contained a device capable of inducing the sensation of extreme pain without any actual tissue damage. The Prime Matriarch would hold the Pain Shard near the subject's neck throughout the test.

The subject was instructed to keep their hand in the box regardless of the pain sensation. If they removed their hand — giving in to animal instinct — the Prime Matriarch would immediately inject them with the poison, killing them instantly.

The Logic:
The Sera Valdris's philosophy held that what separated humans from animals was the ability to override instinctive fear and pain responses with rational choice. A being who could master their instinct to withdraw from pain — when they knew that withdrawal meant death — demonstrated the quality of humanity that the Covenant valued most. Those who failed the test, in the Covenant's view, were not yet fully human in the highest sense.

Kael's Test:
Kael Voryn was tested by Prime Matriarch Morath when he was fifteen years old on Aqualon. He passed — keeping his hand in the box despite the intense pain sensation for the full duration. Morath reported to the Covenant that Kael showed signs of being their long-awaited Veth'Soran: not only did he pass the pain test, but his ability to see even fractionally into the future suggested prescient abilities beyond anything they had expected at his age."""
    },

    "conclave_houses": {
        "title": "The Conclave of Houses — The Noble Assembly",
        "content": """The Conclave of Houses was the deliberative body of the noble Great Houses of the Charted Expanse — a political institution that theoretically balanced the power of the Grand Sovereign through collective noble representation.

Structure:
Each recognized Great House held one or more seats in the Conclave, depending on their size, wealth, and political influence. The Conclave met periodically to address matters of imperial law, disputes between Houses, trade regulations, and other issues affecting the nobility as a whole.

Relationship with the Grand Sovereign:
In theory, the Conclave was a check on imperial power — no Grand Sovereign could rule effectively without at least a working majority of Conclave support. In practice, the relationship between the two institutions was constantly negotiated. Strong Grand Sovereigns could ignore the Conclave for extended periods; weak ones were effectively controlled by it.

House Voryn's Position:
House Voryn had been building influence in the Conclave for generations. Duke Maren Voryn's personal popularity, combined with House Voryn's reputation for justice and competent governance, had made them one of the most respected voices in the Conclave. This growing influence was one of the primary reasons Grand Sovereign Valdrek IV viewed them as a threat.

After Kael's Victory:
The Conclave's role changed significantly after the establishment of the Voryn Empire. Kael reorganized the institution to give the Eremai representation for the first time — recognizing them as a Great People deserving political standing. This was one of the most radical political reforms in imperial history and was deeply controversial among the traditional nobility."""
    },

    "flux_sight": {
        "title": "Flux-Sight — The Gift of Prescience",
        "content": """Flux-sight was the ability to perceive future events — ranging from vague impressions of possible outcomes to detailed visions of specific future moments. It was associated primarily with consumption of flux essence and with the Veth'Soran breeding program of the Sera Valdris.

Forms of Flux-Sight:
Flux-sight manifested in several different ways:
- Passive impressions: vague feelings about the probability of certain outcomes, experienced by many regular flux consumers
- Limited prescience: specific visions of near-future events, achievable by Void Pathfinders through massive flux consumption
- Full prescience: detailed access to multiple possible futures, experienced only by Veth'Soran-level individuals like Kael Voryn

The Trap of Full Prescience:
Full flux-sight was as much a curse as a gift. Kael Voryn described it as being "trapped" — once you could see possible futures clearly, the temptation to act to ensure the best outcome was overwhelming. But every action taken to influence the future changed the probability landscape, potentially foreclosing paths that would otherwise have remained open. The Veth'Soran was always in danger of becoming a slave to his own visions.

The Void Pathfinders' Limited Version:
The Void Consortium's Pathfinders achieved a limited, specific form of flux-sight through enormous flux consumption. Their ability was narrowly focused on spatial navigation — perceiving safe paths through folded space. They could not use their ability for other forms of prediction. The cost was significant physical transformation: generations of massive flux consumption mutated their bodies into forms that were barely recognizable as human.

Lady Seryn's Role:
Lady Seryn, as a Sera Valdris Prime Matriarch, had access to Ancestral Echo — a related but distinct ability. Rather than perceiving the future, she could access the complete memories of all her female ancestors. This gave her an enormous reservoir of historical wisdom and pattern recognition, allowing her to predict future events through analysis rather than direct perception."""
    },

    "battle_veloraan": {
        "title": "The Battle of Veloraan — The Decisive Confrontation",
        "content": """The Battle of Veloraan was the decisive military engagement of Kael Voryn's Crusade of Light — the battle that ended the Desert War, overthrew House Korrax, and forced Grand Sovereign Valdrek IV to abdicate the Sovereign Throne of Stars.

Prelude:
After years of guerrilla warfare that had nearly halted flux production on Veloris, Grand Sovereign Valdrek IV arrived in orbit with his full Vareth Guard contingent and all the forces he could levy from the Great Houses. His intention was to annihilate the Eremai if necessary to restore flux production. He was aware that Kael Voryn — Muad'Dib — was leading the resistance.

Kael's Gamble:
Kael had prepared for this confrontation. He had positioned large quantities of Voryn family atomics — nuclear weapons — in strategic locations around the Stone Veil. His plan was audacious: use atomics to destroy the Stone Veil, then ride duneserpents through the breach with his full Eremai force, striking directly at the heart of Korrax control in Veloraan.

The Atomic Strike:
The explosion that destroyed the Stone Veil was visible from orbit. The shockwave sent sand and stone flying for kilometers. Through the gap in the ancient rock formation, Kael rode at the head of his Drev'kai, mounted on a massive duneserpent. Behind him came thousands of Eremai warriors on their own duneserpent mounts.

The Duels:
Inside Veloraan, Kael confronted Drael-Tavin Korrax — the Baron's nephew and the Korrax heir. Their duel ended when Kael, using Resonance Path techniques and his prescient awareness, overcame Drael-Tavin's superior physical strength and a poisoned weapon hidden in his boot. Drael-Tavin died; the centuries-old feud between House Voryn and House Korrax ended.

The Aftermath:
With the Korrax and Vareth Guard forces destroyed and Grand Sovereign Valdrek trapped in orbit unable to use his fleet without destroying the flux supply, Kael issued his ultimatum. Valdrek abdicated. Kael ascended to the Sovereign Throne of Stars. The Voryn Empire had begun."""
    },

    "ancestral_echo": {
        "title": "Ancestral Echo — Memory of the Mothers",
        "content": """Ancestral Echo was the ability unique to Sera Valdris Prime Matriarchs — the capacity to access the complete experiential memories of all their female ancestors back to the first generation of the Order. It was activated through survival of the Essence Trial and was considered the most sacred ability in the Covenant's tradition.

What It Provided:
A Prime Matriarch with Ancestral Echo did not merely remember historical facts — she could re-experience the complete conscious life of any of her female ancestors. Every perception, every emotion, every memory of every woman in her direct female lineage was available to her. For a Prime Matriarch whose lineage stretched back thousands of years through the carefully maintained Sera Valdris breeding records, this represented an almost incomprehensible wealth of accumulated human experience.

The Limit:
Ancestral Echo was strictly limited to the female side of the ancestry. The male side — the memories of fathers, grandfathers, and all male ancestors — was inaccessible and, to most Prime Matriarchs, terrifying to even contemplate. This limitation was what made the Veth'Soran so significant: he was the one being who could access both sides simultaneously.

Practical Applications:
Prime Matriarchs used Ancestral Echo for:
- Strategic decision-making informed by thousands of years of accumulated political wisdom
- Medical knowledge accumulated across generations of Covenant healers
- Language acquisition (accessing ancestors who had spoken languages that might otherwise be lost)
- Historical research on matters not recorded in any surviving text
- Combat technique refinement through accessing the memories of warrior ancestors

The Male Version:
The Veth'Soran's version of Ancestral Echo was complete — accessing both male and female ancestors simultaneously. This gave Kael Voryn access to an even more vast reservoir of human experience, including the memories of warriors, rulers, soldiers, and countless others whose experiences were inaccessible to even the most experienced Prime Matriarch."""
    },

    "maren_ii_god_emperor": {
        "title": "Maren Voryn II — The God-Emperor",
        "content": """Maren Voryn II, known as the God-Emperor, was the son of Kael Voryn and his Eremai companion Lysha. He is considered the most consequential figure in the history of the Charted Expanse — a ruler who deliberately walked the Eternal Course his father had refused, ruling as a human-duneserpent hybrid for 3,500 years.

Early Life:
Maren II was born on Veloris during his father Kael's years among the Eremai. Like his father, he showed signs of extraordinary flux-sight ability from childhood. Unlike Kael, Maren II was born fully into Eremai culture — raised in Sanctum Drev, trained in serpent riding and desert survival from infancy.

Accepting the Eternal Course:
When Kael walked into the desert and disappeared, Maren II — by then a young man — understood immediately what his father had done and what was now required of him. He made his choice without the years of agonizing that had plagued his father: he would walk the Eternal Course. He allowed dunelarva to attach to his hands, beginning the transformation.

The Transformation:
Over decades, the dunelarva gradually transformed Maren II's body. His legs were eventually subsumed; a powerful tail grew in their place. His metabolism merged with that of the duneserpent symbionts. His lifespan extended dramatically. By the end of his reign, he was a being of immense size and power — partially human, partially duneserpent — ruling from a vast imperial court on Veloris.

The 3,500-Year Reign:
Maren II's reign was characterized by absolute control — he managed the distribution of flux, the operations of the Void Consortium, the Sera Valdris breeding program, and the political affairs of the Charted Expanse with the full awareness of his prescient abilities. His subjects both worshipped and feared him.

Death and Legacy:
Maren II's death triggered the Famine Times — a period of crisis as his carefully managed systems collapsed — and ultimately the Dispersion, as humanity scattered to the furthest reaches of the Charted Expanse to escape any possibility of another God-Emperor. This was precisely what the Eternal Course required."""
    }
}

# ============================================================
# GENERATE FILES
# ============================================================
os.makedirs("knowledge_base", exist_ok=True)

for key, doc in DOCUMENTS.items():
    content = replace_terms(doc["content"], TERMS_MAP)
    title = doc["title"]
    
    filename = f"knowledge_base/{key}.md"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"# {title}\n\n")
        f.write(content)
    print(f"Created: {filename}")

# Save terms map
with open("knowledge_base/terms_map.json", "w", encoding="utf-8") as f:
    json.dump(TERMS_MAP, f, ensure_ascii=False, indent=2)
print("Created: knowledge_base/terms_map.json")

print(f"\nTotal documents: {len(DOCUMENTS)}")
print("Knowledge base generation complete!")
