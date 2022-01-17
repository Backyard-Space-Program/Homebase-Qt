# import math
from math import *
euler = e

def calculate_landing_burn(gravity, alt, vel, isp, mass, thrust):
    #time = (mass-(mass/math.e*(vel+math.sqrt(2*gravity*alt)/gravity*isp))) / (thrust/(gravity*isp))
    #height = (vel+math.sqrt(2*gravity*alt))/2*time
    
    # time = ( mass - ( mass / ( math.e**( ( vel + math.sqrt(2 * gravity * alt) ) / gravity*isp ) ) ) ) / ( thrust / gravity*isp )

	time = (mass - (
				mass / euler ** 
					vel + sqrt(2*gravity*alt)
                        )
				) / (thrust / (gravity * isp))

	return time# , height

print(calculate_landing_burn(9.8, 100, 10, 49.61, 1, 14.48))
