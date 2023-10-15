import random

# In this script, we simulate the behaviors of the mining pool in risk-free strategy.
# In an attack instance, the private branch would replace public branch as new canonical chain.
# So we count the number of blocks of adversary and honest validators in the original and new canonical chain to quantify our attack's extra fee and payout

feelist = []
rewardlist = []

feelist_1 = []
rewardlist_1 = []

# LE
def LE(private_branch, public_branch):
    private_primary_count = 0
    for block in private_branch:
        if block['block_type'] == 'primary':
            private_primary_count += 1

    private_secondary_count = 0
    public_primary_count = 0
    public_secondary_count = 0

    for block in private_branch:
        if block['block_type'] == 'secondary':
            private_secondary_count += 1

    for block in public_branch:
        if block['block_type'] == 'primary':
            public_primary_count += 1

    for block in public_branch:
        if block['block_type'] == 'secondary':
            public_secondary_count += 1

    if private_primary_count > public_primary_count:
        return 1
    elif private_primary_count == public_primary_count and private_secondary_count > public_secondary_count:
        return 1
    elif private_primary_count == public_primary_count and private_secondary_count == public_secondary_count:
        return 0
    else:
        return -1

def receiveBlock(flaghonestpri, flaghonestsec):
    if flaghonestpri:
        return "primary"
    elif flaghonestsec:
        return "secondary"
    return "empty"

def countNumberBlocks(blockchains, countadvblocks, counthonblocks):
    # count adv/hon original number of blocks in the canonical chain
    chainlen = len(blockchains)

    for i in range(chainlen):

        blocklist1 = blockchains[i]

        flagadvsec1 = False
        flaghonestpri1 = False
        flagadvpri1 = False
        flaghonestsec1 = False
        # in one slot, whether honest/adv validators propose at least one primary block or one secondary block.
        for block in blocklist1:
            if (block['block_type'] == "secondary") and (block['node_type'] == "adv"):
                flagadvsec1 = True
            if (block['block_type'] == "primary") and (block['node_type'] == "adv"):
                flagadvpri1 = True
            if (block['block_type'] == "primary") and (block['node_type'] == "honest"):
                flaghonestpri1 = True
            if (block['block_type'] == "secondary") and (block['node_type'] == "honest"):
                flaghonestsec1 = True


        # count the number of blocks of adv and honest respectively when the attack is not run.
        if (flagadvpri1 and not flaghonestpri1):
            countadvblocks = countadvblocks + 1
        if (not flagadvpri1 and flaghonestpri1):
            counthonblocks = counthonblocks + 1
        if (not flagadvpri1 and not flaghonestpri1):
            if (flagadvsec1):
                countadvblocks = countadvblocks + 1
            elif flaghonestsec1:
                counthonblocks = counthonblocks + 1
        if (flagadvpri1 and flaghonestpri1):
            counthonblocks = counthonblocks + 1 / 2
            countadvblocks = countadvblocks + 1 / 2
    return countadvblocks, counthonblocks

for j in range(1,11):

    n = 297  # number of validators
    c = 1 / 4
    m = 240000  # slots of 100 epoches

    # blockchains containing blocks in every slot
    blockchains = []
    p = 1 - (1 - c) ** (1 / n)

    # adversary stake
    print(j)
    t = j/30*n

    for i in range(m):
        current_blocks = []  # blocks in current slot

        # primary leadership selection
        primary = set()
        for j in range(n):
            if random.uniform(0, 1) < p:
                primary.add(j)

        # secondary leadership selection
        secondary = random.randint(0, n-1)

        # belongs to adv or honest?
        for node in primary:
            block_type = "primary"
            if node < t:
                node_type = "adv"
            else:
                node_type = "honest"
            current_blocks.append({'block_type': block_type, 'node_type': node_type})

        block_type = "secondary"
        if secondary < t:
            node_type = "adv"
        else:
            node_type = "honest"
        current_blocks.append({'block_type': block_type, 'node_type': node_type})

        # put blocks in current slot in blockchain
        blockchains.append(current_blocks)
    blockchains_clone = blockchains.copy()
    count = 0

    countoriadvblocks = 0
    countorihonblocks = 0

    chainlen = len(blockchains)
    lastpepeindex = -1

    # count adv/hon original number of blocks in the canonical chain
    for i in range(chainlen-3):

        blocklist1 = blockchains[i]

        flagadvsec1 = False
        flaghonestpri1 = False
        flagadvpri1 = False
        flaghonestsec1 = False

        # in one slot, whether honest/adv validators propose at least one primary block or one secondary block.
        for block in blocklist1:
            if (block['block_type'] == "secondary") and (block['node_type'] == "adv"):
                flagadvsec1 = True
            if (block['block_type'] == "primary") and (block['node_type'] == "adv"):
                flagadvpri1 = True
            if (block['block_type'] == "primary") and (block['node_type'] == "honest"):
                flaghonestpri1 = True
            if (block['block_type'] == "secondary") and (block['node_type'] == "honest"):
                flaghonestsec1 = True

        # count the number of blocks of adv and honest respectively when the attack is not run.
        if(flagadvpri1 and not flaghonestpri1):
            countoriadvblocks = countoriadvblocks + 1
        if(not flagadvpri1 and flaghonestpri1):
            countorihonblocks = countorihonblocks + 1
        if(not flagadvpri1 and not flaghonestpri1):
            if(flagadvsec1):
                countoriadvblocks = countoriadvblocks + 1
            elif flaghonestsec1:
                countorihonblocks = countorihonblocks + 1
        if(flagadvpri1 and flaghonestpri1):
            countorihonblocks = countorihonblocks + 1/2
            countoriadvblocks = countoriadvblocks + 1/2

    # when attack is running.
    for i in range(chainlen-3):

        # blocks in slot_i, slot_{i+1}, slot_{i+2}, slot_{i+3}
        blocklist1 = blockchains[i]
        blocklist2 = blockchains[i+1]
        blocklist3 = blockchains[i+2]
        blocklist4 = blockchains[i + 3]
        flagadvsec1 = False
        flaghonestpri1 = False
        flagadvpri1 = False
        flaghonestsec1 = False

        flagadvsec2 = False
        flagadvpri2 = False
        flaghonestpri2 = False
        flaghonestsec2 = False

        flagadvpri3 = False
        flaghonestpri3 = False
        flagadvsec3 = False
        flaghonestsec3 = False
        flaghonestfirst3 = False

        flagadvpri4 = False
        flaghonestpri4 = False
        flagadvsec4 = False
        flaghonestsec4 = False

        # in one slot, whether honest/adv validators propose at least one primary block or one secondary block.
        for block in blocklist1:
            if (block['block_type'] == "secondary") and (block['node_type'] == "adv"):
                flagadvsec1 = True
            if (block['block_type'] == "primary") and (block['node_type'] == "adv"):
                flagadvpri1 = True
            if (block['block_type'] == "primary") and (block['node_type'] == "honest"):
                flaghonestpri1 = True
            if (block['block_type'] == "secondary") and (block['node_type'] == "honest"):
                flaghonestsec1 = True
        for block in blocklist2:
            if (block['block_type'] == "secondary") and (block['node_type'] == "adv"):
                flagadvsec2 = True
            if (block['block_type'] == "secondary") and (block['node_type'] == "honest"):
                flaghonestsec2 = True
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
            if (block['block_type'] == "secondary") and (block['node_type'] == "honest"):
                flaghonestsec4 = True


        # for simplicity, we detect the pattern of adversarial blocks such as "primary-primary-empty" scenario to trigger our selfish mining attack.
        # "primary-primary-empty" falls into the scenario of risk-free strategy.

        if(flagadvpri1 and flagadvpri2 and not flagadvpri3 and flaghonestsec3):
            lastpepeindex = i + 2

            a = i
            b = i+1

            # attack is triggered. the private branch is withheld.
            # riskfree(a, b, blockchains)

            # construct the private branch with blocks of the mining pool
            privatebranch = []
            privatebranch.append({'block_type': "primary", 'node_type': "adv"})
            privatebranch.append({'block_type': "primary", 'node_type': "adv"})
            # in slot_1.
            # returns "primary", "secondary" or "empty"
            receivedBlock = receiveBlock(flaghonestpri1, flaghonestsec1)

            # construct the public branch with real sub-branch
            publicbranch = []
            # real sub-branch
            publicbranch.append({'block_type': receivedBlock, 'node_type': "honest"})

            # place a virtual primary block of slot_2 in public branch
            publicbranch.append({'block_type': "primary", 'node_type': "honest"})
            # use LE function with private branch and public branch as input to determine whether to release private branch in slot_{\beta-1}(slot_1)
            resultLE = LE(private_branch=privatebranch, public_branch=publicbranch)

            # continue to withhold private branch to slot_\beta
            # use Pred function to determine whether extend the private branch to maximize the extra revenue.
            if resultLE:
                # in slot2
                receivedBlock2 = receiveBlock(flaghonestpri2, flaghonestsec2)
                # the block of public branch in slot_2 is replaced as real block
                publicbranch.pop()
                publicbranch.append({'block_type': receivedBlock2, 'node_type': "honest"})

                # intend to expand the private branch and public branch to slot_3
                # the mining pool is not eligible to propose any block in slot_3.
                privatebranch.append({'block_type': "empty", 'node_type': "adv"})
                # construct virtual public branch, assume that the honest validators propose at least one primary block in slot_3
                publicbranch.append({'block_type': "primary", 'node_type': "honest"})
                resultLE2 = LE(private_branch=privatebranch, public_branch=publicbranch)
                # extend the private branch to slot_3 and continue to withhold the private branch
                # extend beta to slot_3 and becomes the canonical chain.
                if resultLE2 == 1:
                    b = i+2
                    block_slot1 = []
                    block_slot1.append(privatebranch[0])
                    blockchains_clone[i] = block_slot1

                    block_slot2 = []
                    block_slot2.append(privatebranch[1])
                    blockchains_clone[i+1] = block_slot2

                    block_slot3 = []
                    block_slot3.append(privatebranch[2])

                    blockchains_clone[i+2] = block_slot3
                # not extend beta and release private branch in slot_2 or extend beta but release in beta-1
                # released at slot_2 and becomes the canonical chain
                else:
                    b = i+1
                    block_slot1 = []
                    block_slot1.append(privatebranch[0])
                    blockchains_clone[i] = block_slot1
                    block_slot2 = []
                    block_slot2.append(privatebranch[1])
                    blockchains_clone[i + 1] = block_slot2

            # release private branch early. not continue to withhold private branch to slot_\beta
            # private branch becomes the canonical chain.
            else:
                # release in slot_1
                b=i+1
                block_slot1 = []
                block_slot1.append(privatebranch[0])
                blockchains_clone[i] = block_slot1
                block_slot2 = []
                block_slot2.append(privatebranch[1])
                blockchains_clone[i + 1] = block_slot2

    counthonblocks_newCanonicalChain = 0
    countadvblocks_newCanonicalChain = 0

    countadvblocks_newCanonicalChain, counthonblocks_newCanonicalChain = countNumberBlocks(blockchains_clone, countadvblocks=countadvblocks_newCanonicalChain,counthonblocks=counthonblocks_newCanonicalChain)

    # fee
    print("fee: ", countorihonblocks - counthonblocks_newCanonicalChain)
    feelist_1.append(countorihonblocks - counthonblocks_newCanonicalChain)
    # reward
    ori = countoriadvblocks/(countoriadvblocks+countorihonblocks)
    print("reward: ", (countadvblocks_newCanonicalChain/(countadvblocks_newCanonicalChain+counthonblocks_newCanonicalChain) - ori)/ori)

    rewardlist.append((countadvblocks_newCanonicalChain/(countadvblocks_newCanonicalChain+counthonblocks_newCanonicalChain) - ori)/ori)
print(feelist_1)
print(rewardlist)
