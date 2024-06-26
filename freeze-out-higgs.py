################################################################################################
### We have used this code in hep-ph/1911.02616, hep-ph/2102.02313 #############################
###### Please send your queries to chandaprolay@gmail.com ###################################
###########################################################################################



import math	
import numpy as np
from scipy.integrate import quad, dblquad, tplquad
from scipy.optimize import fsolve
import matplotlib.pyplot as plt

##############################################################################################
#### Defining important parameters ############
#######################################

mW = 80.385;
mZ = 91.1876;
mHiggs = 125.09;
mh = 125.09;
GammaHiggs = 1.3*10**-2;
mElec = 0.5101*10**-3;
mMu = 105.65*10**-3;
mTau = 1.7769;
mNeutrino = 2*10**-9;
mU = 2.2*10**-3;
mDown = 4.7*10**-3;
mS = 96*10**-3;
mC = 1.27;
mB = 4.18;
mT = 173.21;
mNuc = 0.93827;
mp = 0.938;
fN = 0.326;
#H0 = 100 h (6.58*10**-25) (3.086*10**19)**-1;
cdmH0GeV = 67.44*((3.086*10.0**19.0)**-1.0)*(6.58*10.0**-25.0);

s0 = (2970.0)* (1.98*10**-14)**3 ;
OmegaB =  0.022;
etaB = 0.88*10**-10;
pi = 3.14;

Mpl = 1.2211*(10**19);
gsG = 100.0; #(*number of degrees of freedom for photon Temp*)
gsD = 100.0; #(*g at decay*)
g = 2.0;
vacExp = 246.0;
v0 = 246.0;
RhoC = 8.13*(10.0)**(-47.0); #(*critical density of universe in GeV^4*)
S0 = 2.2925*(10.0)**(-38.0); #(*entropy of universe today in GeV^3*)
beta = 1.0/3.0;
BBN = 10.0**-2.0;

Tc = 10.0**5.0;
r = 0.99;
eta = 10.0**-10;
nu = 2.0/3.;
cx = 2.0;
symW = 1.0;#symmetry factor for gauge bosons W
symZ = 0.5; #symmetry factor for gauge bosons Z
Eta = 10.0**-10;
mXref1 = 10.0**3.0;

print('H0=',cdmH0GeV, ', beta=', beta)

def heaviside(x):
    if x== 0.0:
       return 1.0
    return 0.0 if x<0.0 else 1.0  
    
     
#Expression for the decay rate
def higgsToDM(k,mX):
    return (cx**2*k**2*v0**2)*((32.0*pi*mHiggs)**-1.0) \
    *((1-  (4*mX**2)*mHiggs**-2)**0.5)*heaviside(mHiggs**2.0-4.0*mX**2.0)
###################################################################    
###### Approximate expression for the annihilation rate #######    
################################################################
def p0(k, mX, rh, rf, rg):
    return ((cx**2.0*k**2.0*rf**2.0)/(16.0*pi*mX**2.0))\
    *(1.0-4.0*rf**2.0)**(1.5)/((1.0-rh**2.0)**2.0 + rg**2.0)\
    *heaviside(1.0-4.0*rf**2.0)
    
def p0a(k, mX, mf):
    return ((cx**2.0*k**2.0*(mf/(2.0*mX))**2.0)/(16.0*pi*mX**2.0))\
    *(1.0-4.0*(mf/(2.0*mX))**2.0)**(1.5)/((1.0-(mh/(2.0*mX))**2.0)**2.0 + ((mh*GammaHiggs)/(4.0*mX**2.0))**2.0)\
    *heaviside(1.0-4.0*(mf/(2.0*mX))**2.0)   
    
def p1a(k, mX, mf):    
    return ((cx**2.0*k**2.0*(mf/(2.0*mX))**2.0)/(32.0*pi*mX**2.0))\
    *(1.0-4.0*(mf/(2.0*mX))**2.0)/((1.0-(mh/(2.0*mX))**2.0)**2.0 + ((mh*GammaHiggs)/(4.0*mX**2.0))**2.0)\
    *(-1.0+7.0*(mf/(2.0*mX))**2.0+(mh/(2.0*mX))**2.0*(1.0-10.0*(mf/(2.0*mX))**2)+3.0*(mf/(2.0*mX))**2.0\
    *((mh/(2.0*mX))**4 + ((mh*GammaHiggs)/(4.0*mX**2.0))**2))/((1 - (mh/(2.0*mX))**2)**2 + ((mh*GammaHiggs)/(4.0*mX**2.0))**2)\
    *heaviside(1.0-4.0*(mf/(2.0*mX))**2.0)  
    
def q0a(k,sym,mX,mV):
    return ((cx**2.0*sym*k**2.0)/(32.0*pi*mX**2.0))*(1.0-4.0*(mV/(2.0*mX))**2.0)**0.5\
    *(1.0-4.0*(mV/(2.0*mX))**2.0+12.0*(mh/(2.0*mX))**4.0)/((1.0-(mh/(2.0*mX))**2.0)**2.0 + ((mh*GammaHiggs)/(4.0*mX**2.0))**2.0)\
    *heaviside(1.0-4.0*(mV/(2.0*mX))**2.0)
    
def fact1(mX,mV):
    return -1.0+14.0*(mV/(2.0*mX))**2.0-76.0*(mV/(2.0*mX))**4.0+168.0*(mV/(2.0*mX))**6.0
    -(12.0*(mh/(2.0*mX))**2.0*((mV/(2.0*mX))**2.0-8.0*(mV/(2.0*mX))**4.0+20.0*(mV/(2.0*mX))**6.0)) + \
    ((mh/(2.0*mX))**4.0+((mh*GammaHiggs)/(4.0*mX**2.0))**2.0)*(1.0-2.0*(mV/(2.0*mX))**2.0-20.0*(mV/(2.0*mX))**4.0-72.0*(mV/(2.0*mX))**6.0)    
    
def q1a(k,sym,mX,mV):
    return ((cx**2.0*sym*k**2.0)/(32.0*pi*mX**2.0))*(1.0-4.0*(mV/(2.0*mX))**2.0)**0.5\
    *fact1(mX,mV)/((1.0-(mh/(2.0*mX))**2.0)**2.0 + ((mh*GammaHiggs)/(4.0*mX**2.0))**2.0)\
    *heaviside(1.0-4.0*(mV/(2.0*mX))**2.0)    
    
def r0a(k,sym,mX):
    return ((cx**2.0*sym*k**2.0)/(64.0*pi*mX**2.0))*(1.0-4.0*(mh/(2.0*mX))**2.0)**0.5\
    *heaviside(1.0-4.0*(mh/(2.0*mX))**2.0)
    
def r1a(k,sym,mX):
    return ((cx**2.0*sym*k**2.0)/(256.0*pi*mX**2.0))*(-1.0+6.0*(mh/(2.0*mX))**2.0)\
    *(1.0-4.0*(mh/(2.0*mX))**2.0)**-0.5*heaviside(1.0-4.0*(mh/(2.0*mX))**2.0)    
    
    
print (higgsToDM(10.0**-3.0,10.0**1.0),np.real(higgsToDM(10.0**-3.0,10.0**3.0)))  
print ('p0=',p0(10**-3, mXref1, (mHiggs/(2.0*mXref1)), (mB/(2.0*mXref1)), (mHiggs*GammaHiggs)/(4.0*mXref1**2.0)), p0a(10**-3.0, mXref1, mB), ',q0=',q0a(10.0**-3.0,symZ,mXref1,mZ),', r0=',r0a(10.0**-3.0,1.0,mXref1))
print('p1=',p1a(10.0**-3.0,mXref1,mB), ',q1=',q1a(10.0**-3.0,symZ,mXref1,mZ),', r1=', r1a(10.0**-3.0,1.0,mXref1))


def P0Tot(k, mX):
    return p0a(k, mX, mElec)+p0a(k, mX, mMu)+p0a(k, mX, mTau)+3.0*p0a(k, mX, mU)+3.0*p0a(k, mX, mDown)\
     +3.0*p0a(k, mX, mS)+3.0*p0a(k, mX, mC)+3.0*p0a(k, mX, mB)+3.0*p0a(k, mX, mT)+q0a(k,0.5,mX,mZ)\
     +q0a(k,1.0,mX,mW)+r0a(k,1,mX)
     
def P1Tot(k, mX):
    return p1a(k, mX, mElec)+p1a(k, mX, mMu)+p1a(k, mX, mTau)+3.0*p1a(k, mX, mU)+3.0*p1a(k, mX, mDown)\
     +3.0*p1a(k, mX, mS)+3.0*p1a(k, mX, mC)+3.0*p1a(k, mX, mB)+3.0*p1a(k, mX, mT)+q1a(k,0.5,mX,mZ)\
     +q1a(k,1.0,mX,mW)+r1a(k,1,mX)     
     
print('sigmaS = ', P0Tot(10.0**-3.0,mXref1),'sigmaP = ', P1Tot(10.0**-3.0,mXref1))

def sigv(sig0,sig2,mX,Tc):
    return sig0 + (1.5*sig2*Tc/mX)
################################################################################
# Defining xf
def MMD(mX,Tc,sig0,sig2,r):
    return (45.0/28.0)**0.5*(g/pi**3.0)*(gsG**-0.5)*Mpl*sigv(sig0,sig2,mX,Tc)\
    *(mX**1.5)*(Tc**-0.5)*(1-r)**-0.5
# Defining 'Dilution factor'
def Zeta(TRH,Tc,r):
    return (90.0/(7.0*pi**3.0*gsD*(1.0-r))*(TRH/Tc))
    
mXexpt = np.arange(-3.0,3.0,0.1)
mX1 = np.linspace(10**-3.0,10**3.0,100)  

#Defining the relic density    
def omegah2MD(mX,k,dil):
    return dil*(gsG**-0.5)*(10.0**9.0*1.5*(1.0-r)**0.5*((mX/Tc)**-0.5)*(np.log(MMD(mX,Tc,P0Tot(k,mX),0,r)))**1.5)\
    *(0.12*Mpl*P0Tot(k,mX))**-1.0
    
print('value of omega normalized to 0.12 is = ',omegah2MD(10.0**3.0,10.0**-3.0,10.0**-5.0))    
    
expr1 = lambda k1 : 1.0 - np.abs(omegah2MD(mXref1,10.0**k1,10.0**-5.0))
sol1 = fsolve(expr1,-3.0)


print('solution for log10(k) is =', "Result:\n %f" % sol1, 'for 1TeV DM and dilution 10^-5')
    
#######################################################################################
########### Solving for 'k' as a function of 'mX' #####################################
#######################################################################################

print(fsolve(lambda k2: 1.0 - np.abs(omegah2MD(50,10.0**k2,Zeta(10.0**2.0,10.0**5.0,r))),-3.0)[0])

mX_dil1_list_a = []
k_dil1_list_a = []
guess = -3.0

for mX in np.geomspace(mHiggs*2.0,10.0**4.0,100):
    mX_dil1_list_a+=[mX]
    sol2_dil1_a = fsolve(lambda k2: 1.0 - np.abs(omegah2MD(mX,10.0**k2,Zeta(10.0**2.0,10.0**5.0,r))),guess)[0]
    k_dil1_list_a+=[sol2_dil1_a]
    guess = sol2_dil1_a
########################################################################################################    
a=np.geomspace(10.0,mHiggs*2.0,20)
b = list(a)
print(a,b)

mX_dil1_list_b = []
mX_dil1_list_B = [10.0, 11.114833509294149, 12.353952393932802, 13.731212404030899, 15.26201397515581,\
                  16.963474435037732, 18.8546194084612, 20.956595560615238, 23.292907057785126, \
                  25.889678389474415, 28.775946490817883, 31.983985431779782, 35.54966730379218,\
                  39.51286333924479, 43.91788974911983, 48.81400326410031, 54.25595192026158, \
                  60.304587248197535, 67.02754471104186, 74.5]
k_dil1_list_b = []
guess2 = -2.0

def func1A(k2,mX):
    return 1.0 - np.abs(omegah2MD(mX,10.0**k2,Zeta(10.0**2.0,10.0**5.0,r)))

for mX in mX_dil1_list_B:
    mX_dil1_list_b+=[mX]
    sol2_dil1_b = fsolve(lambda k2: 1.0 - np.abs(omegah2MD(mX,10.0**k2,Zeta(10.0**2.0,10.0**5.0,r))),guess2)[0]
    k_dil1_list_b+=[sol2_dil1_b]
    guess2 = sol2_dil1_b

print(k_dil1_list_b[:2], mX_dil1_list_b[:2],func1A(30.0,-2.0),mX_dil1_list_B) 
print(fsolve(lambda k2: 1.0 - np.abs(omegah2MD(17.5,10.0**k2,Zeta(10.0**2.0,10.0**5.0,r))),guess2)[0])

#################################################################################################################

mX_dil1_list_c = []
mX_dil1_list_C=[74.5, 75.02525252525253, 75.55050505050505, 76.07575757575758, 76.6010101010101, \
                77.12626262626263, 77.65151515151516, 78.17676767676768, 78.70202020202021,\
                79.22727272727273, 79.75252525252526, 80.27777777777777, 80.8030303030303, \
                81.32828282828282, 81.85353535353535, 82.37878787878788, 82.9040404040404, \
                83.42929292929293, 83.95454545454545, 84.47979797979798, 85.0050505050505, 85.53030303030303,\
                86.05555555555556, 86.58080808080808, 87.10606060606061, 87.63131313131314, 88.15656565656566,\
                88.68181818181819, 89.20707070707071, 89.73232323232324, 90.25757575757576, 90.78282828282829,\
                91.3080808080808, 91.83333333333334, 92.35858585858585, 92.88383838383838, 93.4090909090909,\
                93.93434343434343, 94.45959595959596, 94.98484848484848, 95.51010101010101, 96.03535353535354,\
                96.56060606060606, 97.08585858585859, 97.61111111111111, 98.13636363636364, 98.66161616161617,\
                99.18686868686869, 99.71212121212122, 100.23737373737374, 100.76262626262627, 101.28787878787878,\
                101.81313131313132, 102.33838383838383, 102.86363636363637, 103.38888888888889, 103.91414141414143,\
                104.43939393939394, 104.96464646464646, 105.48989898989899, 106.01515151515152, 106.54040404040404,\
                107.06565656565657, 107.5909090909091, 108.11616161616162, 108.64141414141415, 109.16666666666667,\
                109.6919191919192, 110.21717171717172, 110.74242424242425, 111.26767676767676, 111.7929292929293,\
                112.31818181818181, 112.84343434343435, 113.36868686868686, 113.8939393939394, 114.41919191919192,\
                114.94444444444446, 115.46969696969697, 115.99494949494951, 116.52020202020202, 117.04545454545455,\
                117.57070707070707, 118.0959595959596, 118.62121212121212, 119.14646464646465, 119.67171717171718,\
                120.1969696969697, 120.72222222222223, 121.24747474747475, 121.77272727272728, 122.29797979797979,\
                122.82323232323233, 123.34848484848484, 123.87373737373738, 124.3989898989899, 124.92424242424244,\
                125.44949494949495, 125.97474747474749, 126.5]

k_dil1_list_c = []
guessC = -3.0

for mXc in mX_dil1_list_C:
    mX_dil1_list_c+=[mXc]
    sol2_dil1_c = fsolve(lambda k2c: 1.0 - np.abs(omegah2MD(mXc,10.0**k2c,Zeta(10.0**2.0,10.0**5.0,r))),guessC)[0]
    k_dil1_list_c+=[sol2_dil1_c]
    guessC = sol2_dil1_c
    
print(k_dil1_list_c[:2])

#######################################################################################################################

mX_dil1_list_d = []
mX_dil1_list_D=[126.5, 127.3743736722416, 128.25479105451254, 129.14129392120736, 130.0339243354676, \
                130.9327246511766, 131.8377375149699, 132.74900586825834, 133.6665729492657, \
                134.59048229508073, 135.520777743722, 136.45750343621856, 137.40070381870416, \
                138.35042364452664, 139.3067079763705, 140.26960218839568, 141.23915196839044,\
                142.21540331993884, 143.19840256460427, 144.18819634412637, 145.18483162263473,\
                146.1883556888771, 147.19881615846307, 148.2162609761239, 149.24073841798645, \
                150.27229709386458, 151.31098594956532, 152.35685426921117, 153.40995167757916,\
                154.47032814245452, 155.53803397700221, 156.6131198421539, 157.6956367490124,\
                158.785636061271, 159.88316949765132, 160.98828913435716, 162.10104740754517,\
                163.2214971158135, 164.3496914227062, 165.48568385923622, 166.62952832642526,\
                167.78127909786116, 168.94099082227373, 170.10871852612675, 171.28451761622952,\
                172.4684438823656, 173.66055349994045, 174.860903032646, 176.06954943514512,\
                177.28655005577383, 178.5119626392623, 179.74584532947532, 180.98825667217022,\
                182.23925561777537, 183.49890152418715, 184.7672541595862, 186.04437370527407,\
                187.3303207585276, 188.62515633547488, 189.92894187399008, 191.24173923660922,\
                192.56361071346444, 193.89461902524022, 195.2348273261492, 196.58429920692862,\
                197.9430986978583, 199.31129027179765, 200.6889388472456, 202.07610979142058,\
                203.47286892336206, 204.87928251705418, 206.2954173045693, 207.721340479235,\
                209.15711969882219, 210.60282308875506, 212.05851924534448, 213.52427723904148,\
                215.00016661771528, 216.4862574099529, 217.98262012838282, 219.48932577301917, \
                221.00644583463173, 222.53405229813762, 224.07221764601667, 225.62101486175158,\
                227.1805174332895, 228.75079935652977, 230.3319351388347, 231.92399980256454,\
                233.5270688886383, 235.1412184601164, 236.76652510581076, 238.40306594391868,\
                240.0509186256816, 241.7101613390706, 243.38087281249474, 245.06313231853764,\
                246.75701967771835, 248.46261526227963, 250.18]


k_dil1_list_d = []
guessD = -3.0

for mXd in mX_dil1_list_D:
    mX_dil1_list_d+=[mXd]
    sol2_dil1_d = fsolve(lambda k2d: 1.0 - np.abs(omegah2MD(mXd,10.0**k2d,Zeta(10.0**2.0,10.0**5.0,r))),guessD)[0]
    k_dil1_list_d+=[sol2_dil1_d]
    guessD = sol2_dil1_d
    
print(k_dil1_list_d[:2])



mX_dil1_list = mX_dil1_list_b + mX_dil1_list_c+ mX_dil1_list_d+ mX_dil1_list_a
k_dil1_list = k_dil1_list_b + k_dil1_list_c+ k_dil1_list_d+ k_dil1_list_a

plt.semilogx(mX_dil1_list, k_dil1_list,'b-')    
plt.xlabel(r'($m_{\chi}$/GeV)')
plt.ylabel(r'${\rm log}_{10}k$')

plt.text(1000, -2.5, '$T_{\\rm RH} = 10^{2}$ GeV', fontsize = 12,  
         bbox = dict(facecolor = 'blue', alpha = 0.5)) 
plt.text(1000, -2.7, '$T_{\star} = 10^{5}$ GeV', fontsize = 12,  
         bbox = dict(facecolor = 'blue', alpha = 0.5)) 
plt.text(1000, -2.9, 'r=0.99', fontsize = 12,  
         bbox = dict(facecolor = 'blue', alpha = 0.5)) 
  
plt.show()
