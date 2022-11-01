# This file was automatically created by FeynRules 2.3.36
# Mathematica version: 12.0.0 for Mac OS X x86 (64-bit) (April 7, 2019)
# Date: Thu 13 Aug 2020 19:00:08



from object_library import all_parameters, Parameter


from function_library import complexconjugate, re, im, csc, sec, acsc, asec, cot

# This is a default parameter object representing 0.
ZERO = Parameter(name = 'ZERO',
                 nature = 'internal',
                 type = 'real',
                 value = '0.0',
                 texname = '0')

# User-defined parameters.
cabi = Parameter(name = 'cabi',
                 nature = 'external',
                 type = 'real',
                 value = 0.227591,
                 texname = '\\theta _c',
                 lhablock = 'CKMBLOCK',
                 lhacode = [ 1 ])

th13 = Parameter(name = 'th13',
                 nature = 'external',
                 type = 'real',
                 value = 0.003508,
                 texname = '\\theta _{13}',
                 lhablock = 'CKMBLOCK',
                 lhacode = [ 2 ])

th23 = Parameter(name = 'th23',
                 nature = 'external',
                 type = 'real',
                 value = 0.041539,
                 texname = '\\theta _{23}',
                 lhablock = 'CKMBLOCK',
                 lhacode = [ 3 ])

del13 = Parameter(name = 'del13',
                  nature = 'external',
                  type = 'real',
                  value = 1.2,
                  texname = '\\delta _{13}',
                  lhablock = 'CKMBLOCK',
                  lhacode = [ 4 ])

VeN1 = Parameter(name = 'VeN1',
                 nature = 'external',
                 type = 'real',
                 value = 1.,
                 texname = 'V_{\\text{eN1}}',
                 lhablock = 'NUMIXING',
                 lhacode = [ 1 ])

VeN2 = Parameter(name = 'VeN2',
                 nature = 'external',
                 type = 'real',
                 value = 0.,
                 texname = 'V_{\\text{eN2}}',
                 lhablock = 'NUMIXING',
                 lhacode = [ 2 ])

VeN3 = Parameter(name = 'VeN3',
                 nature = 'external',
                 type = 'real',
                 value = 0.,
                 texname = 'V_{\\text{eN3}}',
                 lhablock = 'NUMIXING',
                 lhacode = [ 3 ])

VmuN1 = Parameter(name = 'VmuN1',
                  nature = 'external',
                  type = 'real',
                  value = 0.,
                  texname = 'V_{\\text{muN1}}',
                  lhablock = 'NUMIXING',
                  lhacode = [ 4 ])

VmuN2 = Parameter(name = 'VmuN2',
                  nature = 'external',
                  type = 'real',
                  value = 1.,
                  texname = 'V_{\\text{muN2}}',
                  lhablock = 'NUMIXING',
                  lhacode = [ 5 ])

VmuN3 = Parameter(name = 'VmuN3',
                  nature = 'external',
                  type = 'real',
                  value = 0.,
                  texname = 'V_{\\text{muN3}}',
                  lhablock = 'NUMIXING',
                  lhacode = [ 6 ])

VtaN1 = Parameter(name = 'VtaN1',
                  nature = 'external',
                  type = 'real',
                  value = 0.,
                  texname = 'V_{\\text{taN1}}',
                  lhablock = 'NUMIXING',
                  lhacode = [ 7 ])

VtaN2 = Parameter(name = 'VtaN2',
                  nature = 'external',
                  type = 'real',
                  value = 0.,
                  texname = 'V_{\\text{taN2}}',
                  lhablock = 'NUMIXING',
                  lhacode = [ 8 ])

VtaN3 = Parameter(name = 'VtaN3',
                  nature = 'external',
                  type = 'real',
                  value = 1.,
                  texname = 'V_{\\text{taN3}}',
                  lhablock = 'NUMIXING',
                  lhacode = [ 9 ])

aEWM1 = Parameter(name = 'aEWM1',
                  nature = 'external',
                  type = 'real',
                  value = 127.94,
                  texname = '\\text{aEWM1}',
                  lhablock = 'SMINPUTS',
                  lhacode = [ 1 ])

Gf = Parameter(name = 'Gf',
               nature = 'external',
               type = 'real',
               value = 0.0000117456,
               texname = 'G_f',
               lhablock = 'SMINPUTS',
               lhacode = [ 2 ])

aS = Parameter(name = 'aS',
               nature = 'external',
               type = 'real',
               value = 0.1184,
               texname = '\\alpha _s',
               lhablock = 'SMINPUTS',
               lhacode = [ 3 ])

ymdo = Parameter(name = 'ymdo',
                 nature = 'external',
                 type = 'real',
                 value = 0.00504,
                 texname = '\\text{ymdo}',
                 lhablock = 'YUKAWA',
                 lhacode = [ 1 ])

ymup = Parameter(name = 'ymup',
                 nature = 'external',
                 type = 'real',
                 value = 0.00255,
                 texname = '\\text{ymup}',
                 lhablock = 'YUKAWA',
                 lhacode = [ 2 ])

yms = Parameter(name = 'yms',
                nature = 'external',
                type = 'real',
                value = 0.101,
                texname = '\\text{yms}',
                lhablock = 'YUKAWA',
                lhacode = [ 3 ])

ymc = Parameter(name = 'ymc',
                nature = 'external',
                type = 'real',
                value = 1.27,
                texname = '\\text{ymc}',
                lhablock = 'YUKAWA',
                lhacode = [ 4 ])

ymb = Parameter(name = 'ymb',
                nature = 'external',
                type = 'real',
                value = 4.7,
                texname = '\\text{ymb}',
                lhablock = 'YUKAWA',
                lhacode = [ 5 ])

ymt = Parameter(name = 'ymt',
                nature = 'external',
                type = 'real',
                value = 173.3,
                texname = '\\text{ymt}',
                lhablock = 'YUKAWA',
                lhacode = [ 6 ])

yme = Parameter(name = 'yme',
                nature = 'external',
                type = 'real',
                value = 0.000511,
                texname = '\\text{yme}',
                lhablock = 'YUKAWA',
                lhacode = [ 11 ])

ymm = Parameter(name = 'ymm',
                nature = 'external',
                type = 'real',
                value = 0.10566,
                texname = '\\text{ymm}',
                lhablock = 'YUKAWA',
                lhacode = [ 13 ])

ymtau = Parameter(name = 'ymtau',
                  nature = 'external',
                  type = 'real',
                  value = 1.777,
                  texname = '\\text{ymtau}',
                  lhablock = 'YUKAWA',
                  lhacode = [ 15 ])

MZ = Parameter(name = 'MZ',
               nature = 'external',
               type = 'real',
               value = 91.1876,
               texname = '\\text{MZ}',
               lhablock = 'MASS',
               lhacode = [ 23 ])

Me = Parameter(name = 'Me',
               nature = 'external',
               type = 'real',
               value = 0.000511,
               texname = '\\text{Me}',
               lhablock = 'MASS',
               lhacode = [ 11 ])

MMU = Parameter(name = 'MMU',
                nature = 'external',
                type = 'real',
                value = 0.10566,
                texname = '\\text{MMU}',
                lhablock = 'MASS',
                lhacode = [ 13 ])

MTA = Parameter(name = 'MTA',
                nature = 'external',
                type = 'real',
                value = 1.777,
                texname = '\\text{MTA}',
                lhablock = 'MASS',
                lhacode = [ 15 ])

MU = Parameter(name = 'MU',
               nature = 'external',
               type = 'real',
               value = 0.00255,
               texname = 'M',
               lhablock = 'MASS',
               lhacode = [ 2 ])

MC = Parameter(name = 'MC',
               nature = 'external',
               type = 'real',
               value = 1.27,
               texname = '\\text{MC}',
               lhablock = 'MASS',
               lhacode = [ 4 ])

MT = Parameter(name = 'MT',
               nature = 'external',
               type = 'real',
               value = 173.3,
               texname = '\\text{MT}',
               lhablock = 'MASS',
               lhacode = [ 6 ])

MD = Parameter(name = 'MD',
               nature = 'external',
               type = 'real',
               value = 0.00504,
               texname = '\\text{MD}',
               lhablock = 'MASS',
               lhacode = [ 1 ])

MS = Parameter(name = 'MS',
               nature = 'external',
               type = 'real',
               value = 0.101,
               texname = '\\text{MS}',
               lhablock = 'MASS',
               lhacode = [ 3 ])

MB = Parameter(name = 'MB',
               nature = 'external',
               type = 'real',
               value = 4.7,
               texname = '\\text{MB}',
               lhablock = 'MASS',
               lhacode = [ 5 ])

MH = Parameter(name = 'MH',
               nature = 'external',
               type = 'real',
               value = 125.7,
               texname = '\\text{MH}',
               lhablock = 'MASS',
               lhacode = [ 25 ])

mN1 = Parameter(name = 'mN1',
                nature = 'external',
                type = 'real',
                value = 300.,
                texname = '\\text{mN1}',
                lhablock = 'MASS',
                lhacode = [ 9900012 ])

mN2 = Parameter(name = 'mN2',
                nature = 'external',
                type = 'real',
                value = 500.,
                texname = '\\text{mN2}',
                lhablock = 'MASS',
                lhacode = [ 9900014 ])

mN3 = Parameter(name = 'mN3',
                nature = 'external',
                type = 'real',
                value = 1000.,
                texname = '\\text{mN3}',
                lhablock = 'MASS',
                lhacode = [ 9900016 ])

WZ = Parameter(name = 'WZ',
               nature = 'external',
               type = 'real',
               value = 2.4952,
               texname = '\\text{WZ}',
               lhablock = 'DECAY',
               lhacode = [ 23 ])

WW = Parameter(name = 'WW',
               nature = 'external',
               type = 'real',
               value = 2.085,
               texname = '\\text{WW}',
               lhablock = 'DECAY',
               lhacode = [ 24 ])

WT = Parameter(name = 'WT',
               nature = 'external',
               type = 'real',
               value = 1.35,
               texname = '\\text{WT}',
               lhablock = 'DECAY',
               lhacode = [ 6 ])

WH = Parameter(name = 'WH',
               nature = 'external',
               type = 'real',
               value = 0.00417,
               texname = '\\text{WH}',
               lhablock = 'DECAY',
               lhacode = [ 25 ])

WN1 = Parameter(name = 'WN1',
                nature = 'external',
                type = 'real',
                value = 0.303,
                texname = '\\text{WN1}',
                lhablock = 'DECAY',
                lhacode = [ 9900012 ])

WN2 = Parameter(name = 'WN2',
                nature = 'external',
                type = 'real',
                value = 1.5,
                texname = '\\text{WN2}',
                lhablock = 'DECAY',
                lhacode = [ 9900014 ])

WN3 = Parameter(name = 'WN3',
                nature = 'external',
                type = 'real',
                value = 12.3,
                texname = '\\text{WN3}',
                lhablock = 'DECAY',
                lhacode = [ 9900016 ])

aEW = Parameter(name = 'aEW',
                nature = 'internal',
                type = 'real',
                value = '1/aEWM1',
                texname = '\\alpha _{\\text{EW}}')

G = Parameter(name = 'G',
              nature = 'internal',
              type = 'real',
              value = '2*cmath.sqrt(aS)*cmath.sqrt(cmath.pi)',
              texname = 'G')

CKM1x1 = Parameter(name = 'CKM1x1',
                   nature = 'internal',
                   type = 'complex',
                   value = 'cmath.cos(cabi)*cmath.cos(th13)',
                   texname = '\\text{CKM1x1}')

CKM1x2 = Parameter(name = 'CKM1x2',
                   nature = 'internal',
                   type = 'complex',
                   value = 'cmath.cos(th13)*cmath.sin(cabi)',
                   texname = '\\text{CKM1x2}')

CKM1x3 = Parameter(name = 'CKM1x3',
                   nature = 'internal',
                   type = 'complex',
                   value = 'cmath.exp(-(del13*complex(0,1)))*cmath.sin(th13)',
                   texname = '\\text{CKM1x3}')

CKM2x1 = Parameter(name = 'CKM2x1',
                   nature = 'internal',
                   type = 'complex',
                   value = '-(cmath.cos(th23)*cmath.sin(cabi)) - cmath.cos(cabi)*cmath.exp(del13*complex(0,1))*cmath.sin(th13)*cmath.sin(th23)',
                   texname = '\\text{CKM2x1}')

CKM2x2 = Parameter(name = 'CKM2x2',
                   nature = 'internal',
                   type = 'complex',
                   value = 'cmath.cos(cabi)*cmath.cos(th23) - cmath.exp(del13*complex(0,1))*cmath.sin(cabi)*cmath.sin(th13)*cmath.sin(th23)',
                   texname = '\\text{CKM2x2}')

CKM2x3 = Parameter(name = 'CKM2x3',
                   nature = 'internal',
                   type = 'complex',
                   value = 'cmath.cos(th13)*cmath.sin(th23)',
                   texname = '\\text{CKM2x3}')

CKM3x1 = Parameter(name = 'CKM3x1',
                   nature = 'internal',
                   type = 'complex',
                   value = '-(cmath.cos(cabi)*cmath.cos(th23)*cmath.exp(del13*complex(0,1))*cmath.sin(th13)) + cmath.sin(cabi)*cmath.sin(th23)',
                   texname = '\\text{CKM3x1}')

CKM3x2 = Parameter(name = 'CKM3x2',
                   nature = 'internal',
                   type = 'complex',
                   value = '-(cmath.cos(th23)*cmath.exp(del13*complex(0,1))*cmath.sin(cabi)*cmath.sin(th13)) - cmath.cos(cabi)*cmath.sin(th23)',
                   texname = '\\text{CKM3x2}')

CKM3x3 = Parameter(name = 'CKM3x3',
                   nature = 'internal',
                   type = 'complex',
                   value = 'cmath.cos(th13)*cmath.cos(th23)',
                   texname = '\\text{CKM3x3}')

MW = Parameter(name = 'MW',
               nature = 'internal',
               type = 'real',
               value = 'cmath.sqrt(MZ**2/2. + cmath.sqrt(MZ**4/4. - (aEW*cmath.pi*MZ**2)/(Gf*cmath.sqrt(2))))',
               texname = 'M_W')

ee = Parameter(name = 'ee',
               nature = 'internal',
               type = 'real',
               value = '2*cmath.sqrt(aEW)*cmath.sqrt(cmath.pi)',
               texname = 'e')

sw2 = Parameter(name = 'sw2',
                nature = 'internal',
                type = 'real',
                value = '1 - MW**2/MZ**2',
                texname = '\\text{sw2}')

cw = Parameter(name = 'cw',
               nature = 'internal',
               type = 'real',
               value = 'cmath.sqrt(1 - sw2)',
               texname = 'c_w')

sw = Parameter(name = 'sw',
               nature = 'internal',
               type = 'real',
               value = 'cmath.sqrt(sw2)',
               texname = 's_w')

g1 = Parameter(name = 'g1',
               nature = 'internal',
               type = 'real',
               value = 'ee/cw',
               texname = 'g_1')

gN = Parameter(name = 'gN',
               nature = 'internal',
               type = 'real',
               value = 'ee/sw',
               texname = 'g_N')

gw = Parameter(name = 'gw',
               nature = 'internal',
               type = 'real',
               value = 'ee/sw',
               texname = 'g_w')

vev = Parameter(name = 'vev',
                nature = 'internal',
                type = 'real',
                value = '(2*MW*sw)/ee',
                texname = '\\text{vev}')

lam = Parameter(name = 'lam',
                nature = 'internal',
                type = 'real',
                value = 'MH**2/(2.*vev**2)',
                texname = '\\text{lam}')

yb = Parameter(name = 'yb',
               nature = 'internal',
               type = 'real',
               value = '(ymb*cmath.sqrt(2))/vev',
               texname = '\\text{yb}')

yc = Parameter(name = 'yc',
               nature = 'internal',
               type = 'real',
               value = '(ymc*cmath.sqrt(2))/vev',
               texname = '\\text{yc}')

ydo = Parameter(name = 'ydo',
                nature = 'internal',
                type = 'real',
                value = '(ymdo*cmath.sqrt(2))/vev',
                texname = '\\text{ydo}')

ye = Parameter(name = 'ye',
               nature = 'internal',
               type = 'real',
               value = '(yme*cmath.sqrt(2))/vev',
               texname = '\\text{ye}')

ym = Parameter(name = 'ym',
               nature = 'internal',
               type = 'real',
               value = '(ymm*cmath.sqrt(2))/vev',
               texname = '\\text{ym}')

ys = Parameter(name = 'ys',
               nature = 'internal',
               type = 'real',
               value = '(yms*cmath.sqrt(2))/vev',
               texname = '\\text{ys}')

yt = Parameter(name = 'yt',
               nature = 'internal',
               type = 'real',
               value = '(ymt*cmath.sqrt(2))/vev',
               texname = '\\text{yt}')

ytau = Parameter(name = 'ytau',
                 nature = 'internal',
                 type = 'real',
                 value = '(ymtau*cmath.sqrt(2))/vev',
                 texname = '\\text{ytau}')

yup = Parameter(name = 'yup',
                nature = 'internal',
                type = 'real',
                value = '(ymup*cmath.sqrt(2))/vev',
                texname = '\\text{yup}')

muH = Parameter(name = 'muH',
                nature = 'internal',
                type = 'real',
                value = 'cmath.sqrt(lam*vev**2)',
                texname = '\\mu')

