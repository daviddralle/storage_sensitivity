# -*- coding: utf-8 -*-
'''
Library of functions for meteorology.

Meteorological function names
=============================

    - cp_calc:    Calculate specific heat 
    - Delta_calc: Calculate slope of vapour pressure curve
    - es_calc:    Calculate saturation vapour pressures
    - ea_calc:    Calculate actual vapour pressures
    - gamma_calc: Calculate psychrometric constant
    - L_calc:     Calculate latent heat of vapourisation
    - pottemp:    Calculate potential temperature (1000 hPa reference pressure)
    - rho_calc:   Calculate air density
    - sun_NR:     Maximum sunshine duration [h] and extraterrestrial radiation [J/day]
    - vpd_calc:   Calculate vapour pressure deficits
    - windvec:    Calculate average wind direction and speed
    
Module requires and imports math and scipy modules.

Tested for compatibility with Python 2.7.

Function descriptions
=====================

'''

__author__ = "Maarten J. Waterloo <maarten.waterloo@acaciawater.com> and\
 J. Delsman"
__version__ = "1.0"
__release__ = "1.0.1"
__date__ = "November 2014"

# Make a help entry for this library
def meteolib():
    '''
    A libray of functions for calculation of micrometeorological
    parameters.

    This is the help function which prints a list of functions and contact
    information about the author, version and last modification date.

    Functions
    ---------

    The metolib module includes the following functions:
        - es_calc:    Calculate saturation vapour pressures.
        - ea_calc:    Calculate actual vapour pressures.
        - vpd_calc:   Calculate vapour pressure deficits.
        - Delta_calc: Calculate slope of vapour pressure curve.
        - L_calc:     Calculate latent heat of vapourisation.
        - cp_calc:    Calculate specific heat.
        - gamma_calc: Calculate psychrometric constant.
        - rho_calc:   Calculate air density.
        - sun_NR:     Calculate extraterrestrial radiation and daylenght.
        - pottemp:    Calculate potential temperature (1000 hPa reference\
        pressure).
        - windvec:    Calculate average wind direction and speed.
            
    Author: Maarten J. Waterloo <m.j.waterloo@vu.nl>
    Version: 1.0
    Date: November 2014
    
    '''
    print('Python library with functions meteorology.\n')
    print('Functions:\n')
    print('- cp_calc: Calculate specific heat.')
    print('- Delta_calc: Calculate slope of vapour pressure curve.')
    print('- ea_calc: Calculate actual vapour pressures.')
    print('- es_calc: Calculate saturation vapour pressures.')
    print('- gamma_calc: Calculate psychrometric constant.')
    print('- L_calc: Calculate latent heat of vapourisation.')
    print('- pottemp: Calculate potential temperature (1000 hPa reference pressure)')
    print('- rho_calc: Calculate air density.')
    print('- sun_NR: Calculate extraterrestrial radiation and daylenght.')
    print('- vpd_calc: Calculate vapour pressure deficits.')
    print('- windvec: Calculate average wind direction and speed.\n')
    print('Author: '),__author__
    print('Version: '),__version__ 
    print('Date: '),__date__
    return
    
# Load relevant python functions
import math     # import math library
import scipy    # import scientific python functions


def _arraytest(*args):
    '''
    Function to convert input parameters in as lists or tuples to
    arrays, while leaving single values intact.

    Test function for single values or valid array parameter input
    (J. Delsman).

    Parameters:
        args (array, list, tuple, int, float): Input values for functions.

    Returns:
        rargs (array, int, float): Valid single value or array function input.

    Examples
    --------
    
        >>> _arraytest(12.76)
        12.76
        >>> _arraytest([(1,2,3,4,5),(6,7,8,9)])
        array([(1, 2, 3, 4, 5), (6, 7, 8, 9)], dtype=object)
        >>> x=[1.2,3.6,0.8,1.7]
        >>> _arraytest(x)
        array([ 1.2,  3.6,  0.8,  1.7])
        >>> _arraytest('This is a string')
        'This is a string'

    '''
    
    rargs=[]
    for a in args:
        if isinstance(a, (list, tuple)):
            rargs.append(scipy.array(a))
        else:
            rargs.append(a)
    if len(rargs) == 1:
        return rargs[0] # no unpacking if single value, return value i/o list
    else:
        return rargs


def cp_calc(airtemp= scipy.array([]),\
            rh= scipy.array([]),\
            airpress= scipy.array([])):
    '''
    Function to calculate the specific heat of air:
    
    .. math::
        c_p = 0.24 \\cdot 4185.5 \\cdot \\left(1 + 0.8 \\cdot \\frac{0.622 \\cdot e_a}{p - e_a}\\right)
        
    where ea is the actual vapour pressure calculated from the relative 
    humidity and p is the ambient air pressure.
    
    Parameters:
        - airtemp: (array of) air temperature [Celsius].
        - rh: (array of) relative humidity data [%].
        - airpress: (array of) air pressure data [Pa].
        
    Returns:
        cp: array of saturated c_p values [J kg-1 K-1].

    References
    ----------

    R.G. Allen, L.S. Pereira, D. Raes and M. Smith (1998). Crop
    Evaporation Guidelines for computing crop water requirements,
    FAO - Food and Agriculture Organization of the United Nations.
    Irrigation and drainage paper 56, Chapter 3. Rome, Italy.
    (http://www.fao.org/docrep/x0490e/x0490e07.htm)
    
    Examples
    --------
    
        >>> cp_calc(25,60,101300)
        1014.0749457208065
        >>> t = [10, 20, 30]
        >>> rh = [10, 20, 30]
        >>> airpress = [100000, 101000, 102000]
        >>> cp_calc(t,rh,airpress)
        array([ 1005.13411289,  1006.84399787,  1010.83623841])
        
    '''
    
    # Test input array/value
    airtemp,rh,airpress = _arraytest(airtemp,rh,airpress)
    
    # calculate vapour pressures
    eact = ea_calc(airtemp, rh)
    # Calculate cp
    cp = 0.24 * 4185.5 * (1 + 0.8 * (0.622 * eact / (airpress - eact)))
    return cp # in J/kg/K


def Delta_calc(airtemp= scipy.array([])):
    '''
    Function to calculate the slope of the temperature - vapour pressure curve
    (Delta) from air temperature T:

    .. math::    
        \\Delta = 1000 \\cdot \\frac{e_s \\cdot 4098}{(T + 237.3)^2}
        
    where es is the saturated vapour pressure at temperature T.
    
    Parameters:
        - airtemp: (array of) air temperature [Celsius].
    
    Returns:
        - Delta: (array of) slope of saturated vapour curve [Pa K-1].
    
    References
    ----------

    Technical regulations 49, World Meteorological Organisation, 1984.
    Appendix A. 1-Ap-A-3.

    Examples
    --------
        >>> Delta_calc(30.0)
        243.34309166827094
        >>> x = [20, 25]
        >>> Delta_calc(x)
        array([ 144.6658414 ,  188.62504569])
        
    '''
    
    # Test input array/value
    airtemp = _arraytest(airtemp)
   
    # calculate saturation vapour pressure at temperature
    es = es_calc(airtemp) # in Pa
    # Convert es (Pa) to kPa
    es = es / 1000.0
    # Calculate Delta
    Delta = es * 4098.0 / ((airtemp + 237.3)**2) * 1000
    return Delta # in Pa/K


def ea_calc(airtemp= scipy.array([]),\
            rh= scipy.array([])):
    '''
    Function to calculate actual vapour pressure from relative humidity:
    
    .. math::    
        e_a = \\frac{rh \\cdot e_s}{100}
        
    where es is the saturated vapour pressure at temperature T.

    Parameters:
        - airtemp: array of measured air temperatures [Celsius].
        - rh: Relative humidity [%].

    Returns:
        - ea: array of actual vapour pressure [Pa].

    Examples
    --------
    
        >>> ea_calc(25,60)
        1900.0946514729308

    '''
    
    # Test input array/value
    airtemp,rh = _arraytest(airtemp, rh)

    # Calculate saturation vapour pressures
    es = es_calc(airtemp)
    # Calculate actual vapour pressure
    eact = rh / 100.0 * es
    return eact # in Pa


def es_calc(airtemp= scipy.array([])):
    '''
    Function to calculate saturated vapour pressure from temperature.

    For T<0 C the saturation vapour pressure equation for ice is used
    accoring to Goff and Gratch (1946), whereas for T>=0 C that of
    Goff (1957) is used.
    
    Parameters:
        - airtemp : (data-type) measured air temperature [Celsius].
        
    Returns:
        - es : (data-type) saturated vapour pressure [Pa].

    References
    ----------
    
    - Goff, J.A.,and S. Gratch, Low-pressure properties of water from -160 \
    to 212 F. Transactions of the American society of heating and \
    ventilating engineers, p. 95-122, presented at the 52nd annual \
    meeting of the American society of \
    heating and ventilating engineers, New York, 1946.
    - Goff, J. A. Saturation pressure of water on the new Kelvin \
    temperature scale, Transactions of the American \
    society of heating and ventilating engineers, pp 347-354, \
    presented at the semi-annual meeting of the American \
    society of heating and ventilating engineers, Murray Bay, \
    Quebec. Canada, 1957.

    Examples
    --------    
        >>> es_calc(30.0)
        4242.725994656632
        >>> x = [20, 25]
        >>> es_calc(x)
        array([ 2337.08019792,  3166.82441912])
    
    '''

    # Test input array/value
    airtemp = _arraytest(airtemp)

    # Determine length of array
    n = scipy.size(airtemp)
    # Check if we have a single (array) value or an array
    if n < 2:
        # Calculate saturated vapour pressures, distinguish between water/ice
        if airtemp < 0:
            # Calculate saturation vapour pressure for ice
            log_pi = - 9.09718 * (273.16 / (airtemp + 273.15) - 1.0) \
                     - 3.56654 * math.log10(273.16 / (airtemp + 273.15)) \
                     + 0.876793 * (1.0 - (airtemp + 273.15) / 273.16) \
                     + math.log10(6.1071)
            es = math.pow(10, log_pi)   
        else:
            # Calculate saturation vapour pressure for water
            log_pw = 10.79574 * (1.0 - 273.16 / (airtemp + 273.15)) \
                     - 5.02800 * math.log10((airtemp + 273.15) / 273.16) \
                     + 1.50475E-4 * (1 - math.pow(10, (-8.2969 * ((airtemp +\
                     273.15) / 273.16 - 1.0)))) + 0.42873E-3 * \
                     (math.pow(10, (+4.76955 * (1.0 - 273.16\
                     / (airtemp + 273.15)))) - 1) + 0.78614
            es = math.pow(10, log_pw)
    else:   # Dealing with an array     
        # Initiate the output array
        es = scipy.zeros(n)
        # Calculate saturated vapour pressures, distinguish between water/ice
        for i in range(0, n):              
            if airtemp[i] < 0:
                # Saturation vapour pressure equation for ice
                log_pi = - 9.09718 * (273.16 / (airtemp[i] + 273.15) - 1.0) \
                         - 3.56654 * math.log10(273.16 / (airtemp[i] + 273.15)) \
                         + 0.876793 * (1.0 - (airtemp[i] + 273.15) / 273.16) \
                         + math.log10(6.1071)
                es[i] = math.pow(10, log_pi)
            else:
                # Calculate saturation vapour pressure for water  
                log_pw = 10.79574 * (1.0 - 273.16 / (airtemp[i] + 273.15)) \
                         - 5.02800 * math.log10((airtemp[i] + 273.15) / 273.16) \
                         + 1.50475E-4 * (1 - math.pow(10, (-8.2969\
                         * ((airtemp[i] + 273.15) / 273.16 - 1.0)))) + 0.42873E-3\
                         * (math.pow(10, (+4.76955 * (1.0 - 273.16\
                         / (airtemp[i] + 273.15)))) - 1) + 0.78614
                es[i] = pow(10, log_pw)
    # Convert from hPa to Pa
    es = es * 100.0
    return es # in Pa


def gamma_calc(airtemp= scipy.array([]),\
               rh= scipy.array([]),\
               airpress=scipy.array([])):
    '''
    Function to calculate the psychrometric constant gamma.

    .. math::    
        \\gamma = \\frac{c_p \\cdot p}{0.66 \\cdot \lambda}
        
    where p is the air pressure and lambda the latent heat of vapourisation.
        
    Parameters:
        - airtemp: array of measured air temperature [Celsius].
        - rh: array of relative humidity values[%].
        - airpress: array of air pressure data [Pa].
        
    Returns:
        - gamma: array of psychrometric constant values [Pa K-1].

    References
    ----------

    J. Bringfelt. Test of a forest evapotranspiration model. Meteorology and
    Climatology Reports 52, SMHI, NorrkÃ¶pping, Sweden, 1986.
        
    Examples
    --------
    
        >>> gamma_calc(10,50,101300)
        66.26343318657227
        >>> t = [10, 20, 30]
        >>> rh = [10, 20, 30]
        >>> airpress = [100000, 101000, 102000]
        >>> gamma_calc(t,rh,airpress)
        array([ 65.25518798,  66.65695779,  68.24239285])
        
    '''

    # Test input array/value 
    airtemp,rh,airpress = _arraytest(airtemp,rh,airpress)
    
    # Calculate cp and Lambda values
    cp = cp_calc(airtemp, rh, airpress)
    L = L_calc(airtemp)
    # Calculate gamma
    gamma = cp * airpress / (0.622 * L)
    return gamma # in Pa\K


def L_calc(airtemp= scipy.array([])):
    '''
    Function to calculate the latent heat of vapourisation from air temperature.
    
    Parameters:
        - airtemp: (array of) air temperature [Celsius].
        
    Returns:
        - L: (array of) lambda [J kg-1 K-1].
        
    References
    ----------

    J. Bringfelt. Test of a forest evapotranspiration model. Meteorology and
    Climatology Reports 52, SMHI, NorrkÃ¶pping, Sweden, 1986.
    
    Examples
    --------
    
        >>> L_calc(25)
        2440883.8804625
        >>> t=[10, 20, 30]
        >>> L_calc(t)
        array([ 2476387.3842125,  2452718.3817125,  2429049.3792125])

    '''
    
    # Test input array/value
    airtemp = _arraytest(airtemp)

    # Calculate lambda
    L = 4185.5 * (751.78 - 0.5655 * (airtemp + 273.15))
    return L # in J/kg 


def pottemp(airtemp= scipy.array([]),\
            rh=scipy.array([]),\
            airpress=scipy.array([])):
    '''
    Function to calculate the potential temperature air, theta, from air
    temperatures, relative humidity and air pressure. Reference pressure
    1000 hPa.
    
    Parameters:
        - airtemp: (array of) air temperature data [Celsius].
        - rh: (array of) relative humidity data [%].
        - airpress: (array of) air pressure data [Pa].
        
    Returns:
        - theta: (array of) potential air temperature data [Celsius].
        
    Examples
    --------
    
        >>> t = [5, 10, 20]
        >>> rh = [45, 65, 89]
        >>> airpress = [101300, 102000, 99800]
        >>> pottemp(t,rh,airpress)
        array([  3.97741582,   8.40874555,  20.16596828])
        >>> pottemp(5,45,101300)
        3.977415823848844
        
    '''
    # Test input array/value
    airtemp,rh,airpress = _arraytest(airtemp,rh,airpress)

    # Determine cp
    cp = cp_calc(airtemp, rh, airpress)
    # Determine theta
    theta = (airtemp + 273.15) * pow((100000.0 / airpress), \
                                   (287.0 / cp)) - 273.15
    return theta # in degrees celsius



def rho_calc(airtemp= scipy.array([]),\
             rh= scipy.array([]),\
             airpress= scipy.array([])):
    '''
    Function to calculate the density of air, rho, from air
    temperatures, relative humidity and air pressure.

    .. math::    
        \\rho = 1.201 \\cdot \\frac{290.0 \\cdot (p - 0.378 \\cdot e_a)}{1000 \\cdot (T + 273.15)} / 100
        
    Parameters:
        - airtemp: (array of) air temperature data [Celsius].
        - rh: (array of) relative humidity data [%].
        - airpress: (array of) air pressure data [Pa].
        
    Returns:
        - rho: (array of) air density data [kg m-3].
        
    Examples
    --------
    
        >>> t = [10, 20, 30]
        >>> rh = [10, 20, 30]
        >>> airpress = [100000, 101000, 102000]
        >>> rho_calc(t,rh,airpress)
        array([ 1.22948419,  1.19787662,  1.16635358])
        >>> rho_calc(10,50,101300)
        1.2431927125520903
        
    '''

    # Test input array/value    
    airtemp,rh,airpress = _arraytest(airtemp,rh,airpress)
    
    # Calculate actual vapour pressure
    eact = ea_calc(airtemp, rh)
    # Calculate density of air rho
    rho = 1.201 * (290.0 * (airpress - 0.378 * eact)) \
             / (1000.0 * (airtemp + 273.15)) / 100.0
    return rho # in kg/m3


def sun_NR(doy=scipy.array([]),\
           lat=float):
    '''
    Function to calculate the maximum sunshine duration [h] and incoming
    radiation [MJ/day] at the top of the atmosphere from day of year and
    latitude.
    
    Parameters:
     - doy: (array of) day of year.
     - lat: latitude in decimal degrees, negative for southern hemisphere.

    Returns:
    - N: (float, array) maximum sunshine hours [h].
    - Rext: (float, array) extraterrestrial radiation [J day-1].

    Notes
    -----
    Only valid for latitudes between 0 and 67 degrees (i.e. tropics
    and temperate zone).

    References
    ----------

    R.G. Allen, L.S. Pereira, D. Raes and M. Smith (1998). Crop
    Evaporation - Guidelines for computing crop water requirements,
    FAO - Food and Agriculture Organization of the United Nations.
    Irrigation and drainage paper 56, Chapter 3. Rome, Italy.
    (http://www.fao.org/docrep/x0490e/x0490e07.htm)
    
    Examples
    --------
    
        >>> sun_NR(50,60)
        (9.1631820597268163, 9346987.824773483)
        >>> days = [100,200,300]
        >>> latitude = 52.
        >>> sun_NR(days,latitude)
        (array([ 13.31552077,  15.87073276,   9.54607624]), array([ 29354803.66244921,  39422316.42084264,  12619144.54566777]))

    '''
    
    # Test input array/value
    doy,lat = _arraytest(doy,lat)
    
    # Set solar constant [W/m2]
    S = 1367.0 # [W/m2]
    # Print warning if latitude is above 67 degrees
    if abs(lat) > 67.:
        print('WARNING: Latitude outside range of application (0-67 degrees).\n)')
    # Convert latitude [degrees] to radians
    latrad = lat * math.pi / 180.0
    # calculate solar declination dt [radians]
    dt = 0.409 * scipy.sin(2 * math.pi / 365 * doy - 1.39)
    # calculate sunset hour angle [radians]
    ws = scipy.arccos(-scipy.tan(latrad) * scipy.tan(dt))
    # Calculate sunshine duration N [h]
    N = 24 / math.pi * ws
    # Calculate day angle j [radians]
    j = 2 * math.pi / 365.25 * doy
    # Calculate relative distance to sun
    dr = 1.0 + 0.03344 * scipy.cos(j - 0.048869)
    # Calculate Rext
    Rext = S * 86400 / math.pi * dr * (ws * scipy.sin(latrad) * scipy.sin(dt)\
           + scipy.sin(ws) * scipy.cos(latrad) * scipy.cos(dt))
    return N, Rext

def vpd_calc(airtemp= scipy.array([]),\
             rh= scipy.array([])):
    '''
    Function to calculate vapour pressure deficit.

    Parameters:
        - airtemp: measured air temperatures [Celsius].
        - rh: (array of) rRelative humidity [%].
        
    Returns:
        - vpd: (array of) vapour pressure deficits [Pa].
        
    Examples
    --------
    
        >>> vpd_calc(30,60)
        1697.090397862653
        >>> T=[20,25]
        >>> RH=[50,100]
        >>> vpd_calc(T,RH)
        array([ 1168.54009896,     0.        ])
        
    '''
    
    # Test input array/value
    airtemp,rh = _arraytest(airtemp, rh)
    
    # Calculate saturation vapour pressures
    es = es_calc(airtemp)
    eact = ea_calc(airtemp, rh) 
    # Calculate vapour pressure deficit
    vpd = es - eact
    return vpd # in hPa


def airpress_calc(elevation):
    '''
    Function to calculate air pressure.

    Parameters:
        - elevation: elevation in meters
        
    Returns:
        - airpress: (array of) pressure [Pa].

        
    '''
    
    airpress = 101325.0*( (293.0 - 0.0065*elevation)/293.0)**5.26
    return airpress

def windvec(u= scipy.array([]),\
            D=scipy.array([])):
    '''
    Function to calculate the wind vector from time series of wind
    speed and direction.
    
    Parameters:
        - u: array of wind speeds [m s-1].
        - D: array of wind directions [degrees from North].
        
    Returns:
        - uv: Vector wind speed [m s-1].
        - Dv: Vector wind direction [degrees from North].
        
    Examples
    --------
    
        >>> u = scipy.array([[ 3.],[7.5],[2.1]])
        >>> D = scipy.array([[340],[356],[2]])
        >>> windvec(u,D)
        (4.162354202836905, array([ 353.2118882]))
        >>> uv, Dv = windvec(u,D)
        >>> uv
        4.162354202836905
        >>> Dv
        array([ 353.2118882])
        
    '''
    
    # Test input array/value    
    u,D = _arraytest(u,D)

    ve = 0.0 # define east component of wind speed
    vn = 0.0 # define north component of wind speed
    D = D * math.pi / 180.0 # convert wind direction degrees to radians
    for i in range(0, len(u)):
        ve = ve + u[i] * math.sin(D[i]) # calculate sum east speed components
        vn = vn + u[i] * math.cos(D[i]) # calculate sum north speed components
    ve = - ve / len(u) # determine average east speed component
    vn = - vn / len(u) # determine average north speed component
    uv = math.sqrt(ve * ve + vn * vn) # calculate wind speed vector magnitude
    # Calculate wind speed vector direction
    vdir = scipy.arctan2(ve, vn)
    vdir = vdir * 180.0 / math.pi # Convert radians to degrees
    if vdir < 180:
        Dv = vdir + 180.0
    else:
        if vdir > 180.0:
            Dv = vdir - 180
        else:
            Dv = vdir
    return uv, Dv # uv in m/s, Dv in dgerees from North


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    print('Ran all tests...')