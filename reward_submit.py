import numpy as np
import sys
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
fig = plt.figure()
ax = Axes3D(fig)

log_print = open('reward.log', 'w')
sys.stdout = log_print
sys.stderr = log_print

print("We vary the number of validators in the mining pool from 0(0%) to 99(33.33%). ")
n=297  # number of validators
t=99  # number of Byzantine validators
t=np.arange(1,100,1)
c=1/4  # system parameter set as 1/4
p=1-(1-c)**(1/n)  # probability that a validator is selected as a primary leader
e=1/2  # We consider a slot where there is a primary leader 𝑣𝑖 from the mining pool and at least one honest primary leader. When 𝑣𝑖 sends it block simultaneously with the honest primary leader(s), 𝑒 denotes the probability that 𝑣𝑖 ’s block is received earlier than other blocks.

honpri=1-(1-p)**(n-t)  # probability that at least one honest validator is selected as the primary leader
nothonpri=1-honpri  # probability that no honest validator is selected as the primary leader
honsec=(n-t)/n   # probability that an honest validator is selected as a secondary leader
hononlysec=nothonpri*honsec  # probability that only one of all honest validators is selected as a secondary leader and none of the others are selected as leaders
honno=nothonpri*t/n  # probability that no honest validator is selected as leaders
advpri=1-(1-p)**t  # probability that at least one Byzantine validator is selected as the primary leader
notadvpri=1-advpri  # probability that no Byzantine validator is selected as the primary leader
advsec=t/n  # probability that a Byzantine validator is selected as a secondary leader
advonlysec=notadvpri*advsec  # probability that only one of all Byzantine validators is selected as a secondary leader and none of the others are selected as leaders
advno=notadvpri*(n-t)/n  # probability that no Byzantine validator is selected as leaders




ppep=advpri*advpri*advno  # probability that leadership of the mining pool assigned in 3 consecutive slots respectively is "primary-primary-empty", which is the only scenario of risk-free strategy
ppe=[0]*10  # Initialize the probability list
# Probability of 9 cases in this scenario
# In this case, honest validators are eligible to propose one secondary block in slot_1, slot_2.`
ppe[1]=hononlysec*hononlysec
# In this case, honest validators are eligible to propose at least one primary block in slot_2 and one secondary block in slot_1.
ppe[2]=hononlysec*honpri
# In this case, honest validators are eligible to propose one secondary block in slot_1 and no block in slot_2.
ppe[3]=hononlysec*honno
# In this case, honest validators are eligible to propose at least one primary block in slot_1 and one secondary block in slot_2.
ppe[4]=honpri*hononlysec
# In this case, honest validators are eligible to propose at least one primary block in slot_1, slot_2.`
ppe[5]=honpri*honpri
# In this case, honest validators are eligible to propose at least one primary block in slot_1 and no block in slot_2.
ppe[6]=honpri*honno
# In this case, honest validators are eligible to propose one secondary block in slot_2 and no block in slot_1.
ppe[7]=honno*hononlysec
# In this case, honest validators are eligible to propose at least one primary block in slot_2 and no block in slot_1.
ppe[8]=honno*honpri
# In this case, honest validators are eligible to propose no block in slot_1, slot_2.
ppe[9]=honno*honno

epoch_ppe=(2400-2)*ppep  # Expectation that leadership of the mining pool assigned in 3 consecutive slots respectively is "primary-primary-empty" in an epoch
# the extra expected number of blocks of the mining pool in the canonical chain in the only scenario of risk-free strategy
advppe_earn=ppe[2]*(1-e)+ppe[4]*(1-e)+ppe[5]*(2-2*e)+ppe[6]*(1-e)+ppe[8]*(1-e)
# the reduced expected number of blocks of honest validators in the canonical chain in the only scenario of risk-free strategy
honppe_loss=ppe[1]*1+ppe[2]*(1-e)+ppe[3]*1+ppe[4]*(1-e)+ppe[5]*(2-2*e)+ppe[6]*(1-e)+ppe[7]*1+ppe[8]*(1-e)+ppe[9]*1




psep=advpri*advonlysec*advno  # probability that leadership of the mining pool assigned in 3 consecutive slots respectively is "primary-secondary-empty", which is the first scenario of risk-taking strategy
pse=[0]*7  # Initialize the probability list
# Probability of 6 cases in this scenario
# In this case, honest validators are eligible to propose at least one primary block in slot_2 and one secondary block in slot_1.
pse[1]=honpri*hononlysec
# In this case, honest validators are eligible to propose one secondary block in slot_1 and no block in slot_2.
pse[2]=nothonpri*hononlysec
# In this case, honest validators are eligible to propose at least one primary block in slot_1, slot_2.
pse[3]=honpri*honpri
# In this case, honest validators are eligible to propose at least one primary block in slot_1 and no block in slot_2.
pse[4]=nothonpri*honpri
# In this case, honest validators are eligible to propose at least one primary block in slot_2 and no block in slot_1.
pse[5]=honpri*honno
# In this case, honest validators are eligible to propose no block in slot_1, slot_2.
pse[6]=nothonpri*honno

epoch_pse=(2400-2)*psep  # Expectation that leadership of the mining pool assigned in 3 consecutive slots respectively is "primary-secondary-empty" in an epoch
# the extra expected number of blocks of the mining pool in the canonical chain in the first scenario of risk-taking strategy
advpse_earn=pse[1]*1+pse[3]*(-e)+pse[4]*(1-e)+pse[5]*1
# the reduced expected number of blocks of honest validators in the canonical chain in the first scenario of risk-taking strategy
honpse_loss=pse[1]*1+pse[3]*(-e)+pse[4]*(1-e)+pse[5]*1+pse[6]*1




pepep=advpri*advpri*advno*advno  # probability that leadership of the mining pool assigned in 4 consecutive slots respectively is "primary-empty-primary-empty", which is the second scenario of risk-taking strategy
pepe=[0]*19  # Initialize the probability list
# Probability of 18 cases in this scenario
# In this case, honest validators are eligible to propose at least one primary block in slot_1, slot_2 and slot_3.
pepe[1]=honpri*honpri*honpri
# In this case, honest validators are eligible to propose at least one primary block in slot_1, slot_2 and one secondary block in slot_3.
pepe[2]=honpri*honpri*hononlysec
# In this case, honest validators are eligible to propose at least one primary block in slot_1, slot_2 and no block in slot_3.
pepe[3]=honpri*honpri*honno
# In this case, honest validators are eligible to propose at least one primary block in slot_1, slot_3 and one secondary block in slot_2.
pepe[4]=honpri*hononlysec*honpri
# In this case, honest validators are eligible to propose at least one primary block in slot_1 and one secondary block in slot_2, slot_3.
pepe[5]=honpri*hononlysec*hononlysec
# In this case, honest validators are eligible to propose at least one primary block in slot_1 and one secondary block in slot_2 and no block in slot_3.
pepe[6]=honpri*hononlysec*honno
# In this case, honest validators are eligible to propose at least one primary block in slot_2, slot_3 and one secondary block in slot_1.
pepe[7]=honpri*hononlysec*honpri
# In this case, honest validators are eligible to propose at least one primary block in slot_2 and one secondary block in slot_1, slot_3.
pepe[8]=honpri*hononlysec*hononlysec
# In this case, honest validators are eligible to propose at least one primary block in slot_2 and one secondary block in slot_1 and no block in slot_3.
pepe[9]=honpri*hononlysec*honno
# In this case, honest validators are eligible to propose at least one primary block in slot_3 and one secondary block in slot_1, slot_2.
pepe[10]=hononlysec*hononlysec*honpri
# In this case, honest validators are eligible to propose one secondary block in slot_1, slot_2 and slot_3.
pepe[11]=hononlysec*hononlysec*hononlysec
# In this case, honest validators are eligible to propose one secondary block in slot_1, slot_2 and no block in slot_3.
pepe[12]=hononlysec*hononlysec*honno
# In this case, honest validators are eligible to propose at least one primary block in slot_2, slot_3 and no block in slot_1.
pepe[13]=honno*honpri*honpri
# In this case, honest validators are eligible to propose at least one primary block in slot_2 and one secondary block in slot_3 and no block in slot_1.
pepe[14]=honno*honpri*hononlysec
# In this case, honest validators are eligible to propose at least one primary block in slot_2 and no block in slot_1, slot_3.
pepe[15]=honno*honpri*honno
# In this case, honest validators are eligible to propose at least one primary block in slot_3 and one secondary block in slot_2 and no block in slot_1.
pepe[16]=honno*hononlysec*honpri
# In this case, honest validators are eligible to propose one secondary block in slot_2, slot_3 and no block in slot_1.
pepe[17]=honno*hononlysec*hononlysec
# In this case, honest validators are eligible to propose one secondary block in slot_2 and no block in slot_1, slot_3.
pepe[18]=honno*hononlysec*honno

epoch_pepe=(2400-3)*pepep  # Expectation that leadership of the mining pool assigned in 4 consecutive slots respectively is "primary-empty-primary-empty" in an epoch
# the extra expected number of blocks of the mining pool in the canonical chain in the second scenario of risk-taking strategy
advpepe_earn=pepe[1]*(1-2*e)+pepe[2]*(-e)+pepe[3]*(-e)+pepe[4]*(-2*e)+pepe[5]*(1-e)+pepe[6]*(1-e)+pepe[7]*(-1-e)+pepe[10]*(1-e)+pepe[13]*(1-e)+pepe[16]*(1-e)
# the reduced expected number of blocks of honest validators in the canonical chain in the second scenario of risk-taking strategy
honpepe_loss=pepe[1]*(1-2*e)+pepe[2]*(-e)+pepe[3]*(-e)+pepe[4]*(-2*e)+pepe[5]*(2-e)+pepe[6]*(2-e)+pepe[7]*(-1-e)+pepe[8]*1+pepe[9]*1+pepe[10]*(2-e)+pepe[11]*2+pepe[12]*2+pepe[13]*(2-e)+pepe[14]*1+pepe[15]*1+pepe[16]*(2-e)+pepe[17]*2+pepe[18]*2




spep=advpri*advonlysec*advno  # probability that leadership of the mining pool assigned in 3 consecutive slots respectively is "secondary-primary-empty", which is the third scenario of risk-taking strategy
spe=[0]*7  # Initialize the probability list
# Probability of 6 cases in this scenario
# In this case, honest validators are eligible to propose at least one primary block in slot_1 and one secondary block in slot_2.
spe[1]=honpri*hononlysec
# In this case, honest validators are eligible to propose at least one primary block in slot_1, slot_2.
spe[2]=honpri*honpri
# In this case, honest validators are eligible to propose at least one primary block in slot_1 and no bloack in slot_2.
spe[3]=honpri*honno
# In this case, honest validators are eligible to propose one secondary block in slot_2 and no bloack in slot_1.
spe[4]=nothonpri*hononlysec
# In this case, honest validators are eligible to propose at least one primary block in slot_2 and no bloack in slot_1.
spe[5]=nothonpri*honpri
# In this case, honest validators are eligible to propose no block in slot_1, slot_2.
spe[6]=nothonpri*honno

epoch_spe=(2400-2)*spep# Expectation that leadership of the mining pool assigned in 3 consecutive slots respectively is "secondary-primary-empty" in an epoch
# the extra expected number of blocks of the mining pool in the canonical chain in the third scenario of risk-taking strategy
advspe_earn=spe[1]*1+spe[2]*(-e)+spe[3]*1+spe[5]*(1-e)
# the reduced expected number of blocks of honest validators in the canonical chain in the third scenario of risk-taking strategy
honspe_loss=spe[1]*1+spe[2]*(-e)+spe[3]*1+spe[5]*(1-e)+spe[6]*1




# the extra expected number of blocks of the mining pool in the canonical chain in above four scenarios during an epoch
adv_earn=advppe_earn*epoch_ppe+advpse_earn*epoch_pse+advpepe_earn*epoch_pepe+advspe_earn*epoch_spe
# the reduced expected number of blocks of honest validators in the canonical chain in above four scenarios during an epoch
hon_loss=honppe_loss*epoch_ppe+honpse_loss*epoch_pse+honpepe_loss*epoch_pepe+honspe_loss*epoch_spe

print("the original expected number of blocks of the mining pool in the canonical chain during an epoch:\n",2400*t/n)
print("the extra expected number of blocks of the mining pool in the canonical chain in above four scenarios during an epoch:\n",adv_earn)
print("the original expected number of blocks of honest validators in the canonical chain during an epoch:\n",2400*(n-t)/n)
print("the reduced expected number of blocks of honest validators in the canonical chain in above four scenarios during an epoch:\n",hon_loss)

reward_original=t/n
reward_risktaking=(2400*t/n+adv_earn)/(2400*t/n+adv_earn+2400*(n-t)/n-hon_loss)
reward_riskfree=(2400*t/n+advppe_earn*epoch_ppe)/(2400*t/n+advppe_earn*epoch_ppe+2400*(n-t)/n-honppe_loss*epoch_ppe)




# simulation results
y = [0.004554089328031868, 0.009225769124559075, 0.014596894383519318, 0.018928105800812348, 0.023246331620849502, 0.027549553846878072, 0.02942376326697499, 0.03253404759632719, 0.03577646489065644, 0.03806334410479062]
y = np.array(y)
y1 = [0.000761164345005036, 0.00117931024098175, 0.002097632856984381, 0.0033776644122341117, 0.0033407049475137575, 0.004211503979873121, 0.004894198602326772, 0.005153060220558849, 0.005555668157704805, 0.005948691640087844]
y1 = np.array(y1)
x = [1,2,3,4,5,6,7,8,9,10]
x = np.array(x)
plt.xlabel('fraction of adv stake%')
plt.ylabel('extra reward%')
# analysis results. risk-taking
plt.plot(100*t/n, 100*(reward_risktaking-reward_original)/reward_original,label='extra reward of overall attacks')
# analysis results. risk-free
plt.plot(100*t/n, 100*(reward_riskfree-reward_original)/reward_original,label = 'extra reward of risk-free attack')
# simulation results.
plt.plot(x/30*100 ,y*100,  label= 'extra reward of simulation results')
plt.plot(x/30*100 ,y1*100,  label= 'extra reward of simulation results in risk-free strategy')

plt.legend()
print('extra reward of overall attacks:\n', 100*(reward_risktaking-reward_original)/reward_original)
print('extra reward of risk-free attack:\n', 100*(reward_riskfree-reward_original)/reward_original)
print("simulation:")
for i, j in zip(x/30*100, y*100):
    print("("+str(i)+","+str(j)+")")
plt.show()