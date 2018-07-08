#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  things.py
#
#  Copyright 2017 John Coppens <john@jcoppens.com>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#


from rt_math import *
from camera import Hit, Hit_list


class Thing():
    def __init__(self, props):
        self.props = props
        self.ambient = Vec3(props['ambient'])
        self.diffuse = Vec3(props['diffuse'])
        self.reflection = Vec3(props['reflection'])


    def intersection(self, ray):
        pass



class Plane(Thing):
    def __init__(self, props):
        super(Plane, self).__init__(props)
        self.dist = float(props['distance'])
        self.normal = Vec3(props['normal'])


    def intersection(self, ray):
        #~ print(str(ray))
        #~ pdb.set_trace()
        ln = self.normal.dot(ray.direct)

        if (ln == 0):
            return []

        numerador = self.normal.scale(self.dist).subtract(ray.orig).dot(self.normal)
        t = numerador/ln

        return [] if t <= 0 else [Hit(t, self.normal, self)]



class Sphere(Thing):
    def __init__(self, props):
        super(Sphere, self).__init__(props)
        self.center = props['location']
        self.radius = float(props['radius'])


    def intersection(self, ray):
        a = ray.direct.dot(ray.direct)
        aux = Vec3(ray.orig).subtract(Vec3(self.center))
        b = 2 * (ray.direct.dot(aux))
        c = ((Vec3(ray.orig).subtract(Vec3(self.center))).dot(Vec3(ray.orig).subtract(Vec3(self.center)))) - self.radius**2
        square_root = b**2 - 4*a*c

        if(square_root < 0):
            return []
        elif (square_root == 0):
            d = -b / (2*a)
            n = ray.direct.scale(d).subtract(Vec3(self.center))
            return [Hit(d, n, self)]
        else:
            d1 = (-b + np.sqrt(square_root)) / (2*a)
            d2 = (-b - np.sqrt(square_root)) / (2*a)
            if(d1<=0 and d2<=0):
                return []

            d = self.closest(d1, d2)
            n = ray.direct.scale(d).subtract(Vec3(self.center))
            return [Hit(d, n, self)]

    def closest(self, d1, d2):
        if(d1 <= 0):
            return d2
        elif(d2 <= 0):
            return d1
        elif (d1 <= d2):
            return d1
        else:
            return d2



class Triangle(Thing):
    def __init__(self, props):
        super(Triangle, self).__init__(props)
        self.props = props
        self.puntoA = Vec3(props['puntoA'])
        self.puntoB = Vec3(props['puntoB'])
        self.puntoC = Vec3(props['puntoC'])


    def intersection(self, ray):
        a = Vec3 (0,0,0)
        b = Vec3 (0,0,0)
        bordeA = Vec3(0, 0, 0)
        bordeB = Vec3(0, 0, 0)
        bordeC = Vec3(0, 0, 0)
        vpA = Vec3(0, 0, 0)
        vpB = Vec3(0, 0, 0)
        vpC = Vec3(0, 0, 0)
        c = Vec3(0, 0, 0)
        p = Vec3(0, 0, 0)
        n = Vec3(0, 0, 0)

        a = self.puntoB.subtract(self.puntoA)
        b = self.puntoC.subtract(self.puntoA)
        n = a.cross(b).normalize()
        
        ln = n.dot(ray.direct)

        if (ln == 0):
            return []

         
        d = (n.x * self.puntoA.x + n.y * self.puntoA.y + n.z * self.puntoA.z)
         
        numerador = n.scale(d).subtract(ray.orig).dot(n)
        t = numerador / ln

        if t <= 0:
            return []

        p = ray.orig.add( ray.direct.scale(t))


        bordeA = self.puntoB.subtract( self.puntoA)
        vpA = p.subtract(self.puntoA)
        c = bordeA.cross(vpA)

        if (n.dot(c) < 0):
            return []


        bordeB = self.puntoC.subtract(self.puntoB)
        vpB = p.subtract(self.puntoB)
        c = bordeB.cross(vpB)

        if (n.dot(c) < 0):
            return []


        bordeC = self.puntoA.subtract( self.puntoC)
        vpC = p.subtract(self.puntoC)
        c = bordeC.cross(vpC)

        if (n.dot(c) < 0):
            return []

        return  [Hit(t, n.normalize(), self)]



class Cylinder(Thing):
    def __init__(self, props):
        super(Cylinder, self).__init__()
        self.props = props


    def intersection(self, ray):
        pass



class Box(Thing):

    def __init__(self, props):
        super(Box, self).__init__(props)
        self.props = props
        self.high = Vec3(props['high'])
        self.low = Vec3(props['low'])


    def intersection(self, ray):
        Tnear = -1e99
        Tfar = 1e99
        n = Vec3(-1,0,0)
        
        if ray.direct.x == 0:
            if (0 < self.low.x or 0 > self.high.x):
                return []
        
        T1 = (self.low.x - ray.orig.x) / ray.direct.x
        T2 = (self.high.x - ray.orig.x) / ray.direct.x

        if T1 > T2:
            suport = T1
            T1 = T2
            T2 = suport
            n.x=1
        if T1 > Tnear:
            Tnear = T1
        if T2 < Tfar:
            Tfar = T2
        if Tfar < Tnear:
            return []
        if Tfar < 0:
            return []

        if ray.direct.y == 0:
            if  (0 < self.low.y or 0 > self.high.y):
                return []

        T1 = (self.low.y - ray.orig.y) / ray.direct.y
        T2 = (self.high.y - ray.orig.y) / ray.direct.y

        if T1 > T2:
            suport = T1
            T1 = T2
            T2 = suport
            if T1>Tnear:
                n.y=1
        if T1 > Tnear:
            Tnear= T1
            n.x=0
            if(n.y==0):
                n.y=-1
        if T2 < Tfar:
            Tfar = T2
        if Tfar < Tnear:
            return []
        if Tfar < 0:
            return []


        if ray.direct.z == 0:
            if  (0 < self.low.z or 0 > self.high.z):
                return []

        T1 = (self.low.z - ray.orig.z) / ray.direct.z
        T2 = (self.high.z - ray.orig.z) / ray.direct.z

        if T1 > T2:
            suport = T1
            T1 = T2
            T2 = suport
            if T1 > Tnear: 
                n.z=1
        if T1 > Tnear:
            Tnear = T1
            n.y=0
            n.x=0
            if(n.z==0):
                n.z=-1
            
        if T2 < Tfar:
            Tfar = T2
        if Tfar < Tnear:
            return []
        if Tfar < 0:
            return []

        return [Hit(Tnear,n,self)]
     

class Cone(Thing):
    def __init__(self, props):
        super(Cone, self).__init__(props)
        self.center = props['location']
        self.radius = float(props['radius'])
        self.height = float(props['height'])
        self.angle = np.arctan(self.radius/self.height)

    def intersection(self, ray):
        c = Vec3(self.center).add(Vec3(0,self.height,0))
        v = Vec3("0 -1 0") #Es (0,-1,0) porque el verser v en las fórmulas va hacia abajo

        a = ((ray.direct.dot(v))**2) - np.cos(self.angle)**2

        b = 2 * ((ray.direct.dot(v) * (ray.orig.subtract(c).dot(v))) - ((ray.direct.dot(ray.orig.subtract(c)) * np.cos(self.angle) ** 2)))

        ce = (ray.orig.subtract(c).dot(v)) ** 2 - ((ray.orig.subtract(c).dot(ray.orig.subtract(c))) * np.cos(self.angle) ** 2)

        square_root = b**2 - 4*a*ce

        if(square_root < 0):
            return []
        elif (square_root == 0):
            d = -b / (2*a)
            aux = ray.orig.add(ray.direct.scale(d)).subtract(c).dot(v)
            if(aux>0):
                v = Vec3(ray.orig.add(ray.direct.scale(d)).subtract(Vec3(self.center)))
                v2 = Vec3(ray.orig.add(ray.direct.scale(d)).subtract(c))

                prod = v.cross(v2)
                n = v2.cross(prod).normalize()

                return [Hit(d, n, self)]
            else:
                return []
        else:
            d1 = (-b + np.sqrt(square_root)) / (2 * a)
            d2 = (-b - np.sqrt(square_root)) / (2 * a)
            if (d1 <= 0 and d2 <= 0):
                return []

            d = self.closest(d1, d2)
            aux = ray.orig.add(ray.direct.scale(d)).subtract(c).dot(v)
            if(aux>0):
                v = Vec3(ray.orig.add(ray.direct.scale(d)).subtract(Vec3(self.center)))
                v2 = Vec3(ray.orig.add(ray.direct.scale(d)).subtract(c))

                prod = v.cross(v2)
                n = v2.cross(prod).normalize()

                return [Hit(d, n, self)]
            else:
                return []

    def closest(self, d1, d2):
        if(d1 <= 0):
            return d2
        elif(d2 <= 0):
            return d1
        elif (d1 <= d2):
            return d1
        else:
            return d2



obj_dict = {
            'sphere'  : Sphere,
            'plane'   : Plane,
            'box'     : Box,
            'triangle': Triangle,
            'cylinder': Cylinder,
            'cone': Cone}


def main(args):

    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
