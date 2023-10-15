import random

# In this script, we simulate babe, the block production mechanism, according to Polkadot's specification.
# For simplicity, we detect the scenarios that triggers the risk-free and risk-taking selfish mining according to the initiation condition.
# And in such scenario, honest validators have multiple cases for block proposal. Eventually, different cases lead to different attack results according to the strategy.
# We simply detect these cases and count the discarded blocks and extra blocks of honest validators and the mining pool according to different attack cases.

feelist = []
rewardlist = []
adversaryStake = []

for j in range(1,11):

    n = 297  # number of validators
    c = 1 / 4
    m = 240000  # slots of 100 epoches

    # blockchains stored with blocks
    blockchains = []
    p = 1 - (1 - c) ** (1 / n)

    adversaryStake.append(j/30)
    print(j, "adversary stake: ", j/30)
    t = j/30*n

    for i in range(m):
        current_block = []  # blocks in current slot

        # primary block leadership selection in current slot
        primary = set()
        for j in range(n):
            if random.uniform(0, 1) < p:
                primary.add(j)

        # secondary block leadership selection in current slot
        secondary = random.randint(0, n-1)

        # put blocks into block list of current slot
        for node in primary:
            block_type = "primary"
            if node < t:
                node_type = "adv"
            else:
                node_type = "honest"
            current_block.append({'block_type': block_type, 'node_type': node_type})

        block_type = "secondary"
        if secondary < t:
            node_type = "adv"
        else:
            node_type = "honest"
        current_block.append({'block_type': block_type, 'node_type': node_type})

        blockchains.append(current_block)

    count = 0
    countppe = 0
    countspe = 0
    countpse = 0
    countpepe = 0

    countoriadvblocks = 0
    countorihonblocks = 0

    countnewadvblocks = 0
    countnewhonblocks = 0

    counthonestlost = 0
    countadvlost = 0
    counthonestearn = 0
    countadvearn = 0

    counthonestlostpepe = 0
    countadvlostpepe = 0
    counthonestearnpepe = 0
    countadvearnpepe = 0

    chainlen = len(blockchains)
    lastpepeindex = -1
    for i in range(chainlen-3):

        blocklist1 = blockchains[i]
        blocklist2 = blockchains[i+1]
        blocklist3 = blockchains[i+2]
        blocklist4 = blockchains[i + 3]
        flagadvsec1 = False
        flaghonestpri1 = False
        flagadvpri1 = False
        # flaghonestsec1 = False

        flagadvsec2 = False
        flagadvpri2 = False
        flaghonestpri2 = False

        flagadvpri3 = False
        flaghonestpri3 = False
        flagadvsec3 = False
        flaghonestsec3 = False
        flaghonestfirst3 = False

        flagadvpri4 = False
        flaghonestpri4 = False
        flagadvsec4 = False

        for block in blocklist1:
            if (block['block_type'] == "secondary") and (block['node_type'] == "adv"):
                flagadvsec1 = True
            if (block['block_type'] == "primary") and (block['node_type'] == "adv"):
                flagadvpri1 = True
            if (block['block_type'] == "primary") and (block['node_type'] == "honest"):
                flaghonestpri1 = True
        for block in blocklist2:
            if (block['block_type'] == "secondary") and (block['node_type'] == "adv"):
                flagadvsec2 = True
            if (block['block_type'] == "primary") and (block['node_type'] == "honest"):
                flaghonestpri2 = True
            if (block['block_type'] == "primary") and (block['node_type'] == "adv"):
                flagadvpri2= True
        for block in blocklist3:
            if (block['block_type'] == "primary") and (block['node_type'] == "adv"):
                flagadvpri3 = True
            if (block['block_type'] == "primary") and (block['node_type'] == "honest"):
                flaghonestpri3 = True
            if (block['block_type'] == "secondary") and (block['node_type'] == "adv"):
                flagadvsec3 = True
            if (block['block_type'] == "secondary") and (block['node_type'] == "honest"):
                flaghonestsec3 = True
        for block in blocklist4:
            if (block['block_type'] == "secondary") and (block['node_type'] == "adv"):
                flagadvsec4 = True
            if (block['block_type'] == "primary") and (block['node_type'] == "honest"):
                flaghonestpri4 = True
            if (block['block_type'] == "primary") and (block['node_type'] == "adv"):
                flagadvpri4 = True


        if(flagadvpri1 and not flaghonestpri1):
            countoriadvblocks = countoriadvblocks + 1
        if(not flagadvpri1 and flaghonestpri1):
            countorihonblocks = countorihonblocks + 1
        if(not flagadvpri1 and not flaghonestpri1):
            if(flagadvsec1):
                countoriadvblocks = countoriadvblocks + 1
            else:
                countorihonblocks = countorihonblocks + 1
        if(flagadvpri1 and flaghonestpri1):
            countorihonblocks = countorihonblocks + 1/2
            countoriadvblocks = countoriadvblocks + 1/2

        # for simplicity, we detect the pattern of adversarial blocks such as "primary-primary-empty" scenario to trigger our selfish mining attack.
        # "primary-primary-empty" falls into the scenario of risk-free strategy.
        # adv ppe
        if(flagadvpri1 and flagadvpri2 and not flagadvpri3 and flaghonestsec3):
            lastpepeindex = i + 2

            countppe = countppe + 1
            # The honest validators are eligible to propose no primary block in slot_1 and slot_2
            if(not flaghonestpri1 and not flaghonestpri2):
                counthonestlost = counthonestlost +1
            # The honest validators are eligible to propose at least one primary block in slot_1 and no primary block in slot_2
            if(flaghonestpri1 and not flaghonestpri2):
                countadvearn = countadvearn + 1/2
                counthonestlost = counthonestlost +1/2
            # The honest validators are eligible to propose no primary block in slot_1 and at least one primary block in slot_2
            if(not flaghonestpri1 and flaghonestpri2):
                countadvearn = countadvearn + 1 / 2
                counthonestlost = counthonestlost + 1 / 2
            # The honest validators are eligible to propose at least one primary block in slot_1 and at least one primary block in slot_2
            if(flaghonestpri1  and flaghonestpri2):
                countadvearn = countadvearn + 1
                counthonestlost = counthonestlost + 1

        # first scenario of the risk-taking strategy
        # the validators in the mining pool are eligible to propose one secondary block at slot_1 and at least one primary block at slot_2 and no block at slot_3
        # spe
        if(not flagadvpri1 and flagadvsec1 and flagadvpri2 and not flagadvpri3 and flaghonestsec3):
            lastpepeindex = i + 2
            countspe = countspe + 1
            # The honest validators are eligible to propose at least one primary block in slot_1 and no primary block in slot_2
            if(flaghonestpri1) and not flaghonestpri2:
                countadvearn = countadvearn +1
                counthonestlost = counthonestlost + 1
            # The honest validators are eligible to propose at least one primary block in slot_1 and at least one primary block in slot_2
            if(flaghonestpri1 and flaghonestpri2):
                counthonestearn = counthonestearn + 1/2
                countadvlost = countadvlost + 1/2
            # The honest validators are eligible to propose no primary block in slot_1 and at least one primary block in slot_2
            if(flaghonestpri2 and not flaghonestpri1 ):
                counthonestlost = counthonestlost + 1/2
                countadvearn = countadvearn + 1/2
            # The honest validators are eligible to propose no primary block in slot_1 and no primary block and no secondary block in slot_2
            if(not flaghonestpri1 and not flaghonestpri2 and flagadvsec2):
                counthonestlost = counthonestlost + 1

        # another scenario of the risk-taking strategy. result is the same as the first scenario of the risk-taking strategy.
        # the validators in the mining pool are eligible to propose at least one primary block at slot_1 and one secondary block at slot_2 and no block at slot_3
        # pse
        if ( not flagadvpri2 and flagadvsec2 and flagadvpri1 and not flagadvpri3 and flaghonestsec3):
            lastpepeindex = i + 2

            countpse = countpse + 1
            # ep and sp
            if (flaghonestpri2) and not flaghonestpri1:
                countadvearn = countadvearn + 1
                counthonestlost = counthonestlost + 1
            # pp
            if (flaghonestpri2 and flaghonestpri1):
                counthonestearn = counthonestearn + 1 / 2
                countadvlost = countadvlost + 1 / 2
            # pe
            if (flaghonestpri1 and not flaghonestpri2):
                counthonestlost = counthonestlost + 1 / 2
                countadvearn = countadvearn + 1 / 2
            # ee
            if (not flaghonestpri2 and not flaghonestpri1 and flagadvsec1):
                counthonestlost = counthonestlost + 1

        # second scenario of the risk-taking strategy
        # pepe
        # the validators in the mining pool are eligible to propose at least one primary block at slot_1 and at least one primary block at slot_3
        if(flagadvpri1 and not flagadvpri2 and flagadvpri3 and not flagadvpri4 and not flagadvsec4 and not flagadvsec2):
            if(i>lastpepeindex):
                lastpepeindex = i+3
                countpepe = countpepe + 1
                if(flaghonestpri1 and flaghonestpri2 and flaghonestpri3):
                    countadvlost = countadvlost + 1/2
                    counthonestearn = counthonestearn + 1/2
                    countadvlostpepe = countadvlostpepe + 1 / 2
                    counthonestearnpepe = counthonestearnpepe + 1 / 2
                if (flaghonestpri1 and flaghonestpri2 and not flaghonestpri3 and flaghonestsec3):
                    countadvlost = countadvlost + 1 / 2
                    counthonestearn = counthonestearn + 1 / 2
                    countadvlostpepe = countadvlostpepe + 1 / 2
                    counthonestearnpepe = counthonestearnpepe + 1 / 2
                if (flaghonestpri1 and flaghonestpri2 and not flaghonestpri3 and not flaghonestsec3):
                    countadvlost = countadvlost + 1 / 2
                    counthonestearn = counthonestearn + 1 / 2
                    countadvlostpepe = countadvlostpepe + 1 / 2
                    counthonestearnpepe = counthonestearnpepe + 1 / 2
                #     psp
                if (flaghonestpri1 and not flaghonestpri2 and not flagadvsec2 and flaghonestpri3):
                    countadvlost = countadvlost + 1
                    counthonestearn = counthonestearn + 1
                    countadvlostpepe = countadvlostpepe + 1
                    counthonestearnpepe = counthonestearnpepe + 1

                # pss
                if (flaghonestpri1 and not flaghonestpri2 and not flagadvsec2 and not flaghonestpri3 and flaghonestsec3):
                    countadvearn = countadvearn + 1/2
                    counthonestlost = counthonestlost+1+1/2
                    countadvearnpepe = countadvearnpepe + 1 / 2
                    counthonestlostpepe = counthonestlostpepe + 1 + 1 / 2
                if (flaghonestpri1 and not flaghonestpri2 and not flagadvsec2 and not flaghonestpri3 and not flaghonestsec3):
                    countadvearn = countadvearn + 1 / 2
                    counthonestlost = counthonestlost + 1 + 1 / 2
                    countadvearnpepe = countadvearnpepe + 1 / 2
                    counthonestlostpepe = counthonestlostpepe + 1 + 1 / 2
                if (not flaghonestpri1 and not flagadvsec1 and flaghonestpri2 and flaghonestpri3):
                    countadvlost = countadvlost + 1 + 1/2
                    counthonestearn = counthonestearn + 1 + 1/2
                    countadvlostpepe = countadvlostpepe + 1 + 1 / 2
                    counthonestearnpepe = counthonestearnpepe + 1 + 1 / 2
                #     hon sps
                if (not flaghonestpri1 and not flagadvsec1 and flaghonestpri2 and not flaghonestpri3 and flaghonestsec3):
                    counthonestlost = counthonestlost + 1
                    counthonestlostpepe = counthonestlostpepe + 1
                if (not flaghonestpri1 and not flagadvsec1 and flaghonestpri2 and not flaghonestpri3 and not flaghonestsec3):
                    counthonestlost = counthonestlost + 1
                    counthonestlostpepe = counthonestlostpepe + 1
                if (not flaghonestpri1 and not flagadvsec1 and not flaghonestpri2 and not flagadvsec2 and flaghonestpri3):
                    countadvearn = countadvearn + 1 / 2
                    counthonestlost = counthonestlost + 1 + 1/2
                    countadvearnpepe = countadvearnpepe + 1 / 2
                    counthonestlostpepe = counthonestlostpepe + 1 + 1 / 2
                # sss
                if (not flaghonestpri1 and not flagadvsec1 and not flaghonestpri2 and not flagadvsec2 and not flaghonestpri3 and flaghonestsec3):
                    counthonestlost = counthonestlost + 2
                    counthonestlostpepe = counthonestlostpepe + 2
                # sse
                if (not flaghonestpri1 and not flagadvsec1 and not flaghonestpri2 and not flagadvsec2 and not flaghonestpri3 and not flaghonestsec3):
                    counthonestlost = counthonestlost + 2
                if (not flaghonestpri1 and flagadvsec1 and flaghonestpri2 and flaghonestpri3):
                    countadvearn = countadvearn + 1 / 2
                    counthonestlost = counthonestlost + 1 + 1/2
                    countadvearnpepe = countadvearnpepe + 1 / 2
                    counthonestlostpepe = counthonestlostpepe + 1 + 1 / 2
                if (not flaghonestpri1 and flagadvsec1 and flaghonestpri2 and not flaghonestpri3 and flaghonestsec3):
                    counthonestlost = counthonestlost + 1

                    counthonestlostpepe = counthonestlostpepe + 1
                if (not flaghonestpri1 and flagadvsec1 and flaghonestpri2 and not flaghonestpri3 and flagadvsec3):
                    counthonestlost = counthonestlost + 1

                    counthonestlostpepe = counthonestlostpepe + 1
                if (not flaghonestpri1 and flagadvsec1 and not flaghonestpri2 and not flagadvsec2 and flaghonestpri3):
                    countadvearn = countadvearn + 1 / 2
                    counthonestlost = counthonestlost + 1 + 1/2

                    countadvearnpepe = countadvearnpepe + 1 / 2
                    counthonestlostpepe = counthonestlostpepe + 1 + 1 / 2
                if (not flaghonestpri1 and flagadvsec1 and not flaghonestpri2 and not flagadvsec2 and not flaghonestpri3 and flaghonestsec3):
                    counthonestlost = counthonestlost + 2

                    counthonestlostpepe = counthonestlostpepe + 2
                if (not flaghonestpri1 and flagadvsec1 and not flaghonestpri2 and not flagadvsec2 and not flaghonestpri3 and not flaghonestsec3):
                    counthonestlost = counthonestlost + 2
                    counthonestlostpepe = counthonestlostpepe + 2

    # fee
    feelist.append(counthonestlost - countadvlost)

    # reward
    countnewadvblocks = countoriadvblocks + countadvearn - countadvlost
    countnewhonblocks = countorihonblocks + counthonestearn - counthonestlost
    ori = countoriadvblocks/(countoriadvblocks+countorihonblocks)
    rewardlist.append((countnewadvblocks/(countnewadvblocks+countnewhonblocks) - ori)/ori)

print("adversaryStake: ", adversaryStake)
print("extra fee quantified by the number of discarded blocks by the mining pool and the honest validators: \n", feelist)
print("extra reward quantified by the fraction of the number of the mining pool's blocks in the canonical chain: \n", rewardlist)
