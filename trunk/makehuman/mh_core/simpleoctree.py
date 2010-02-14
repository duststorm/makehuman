#!/usr/bin/python
# -*- coding: utf-8 -*-

import math


class SimpleOctree:

    nVerts = 0
    nVolumes = 0
    nLeafs = 0
    root = ''

    def __init__(self, verts, minsize=0.4):
        minX = verts[0][0]
        maxX = minX
        minY = verts[0][1]
        maxY = minY
        minZ = verts[0][2]
        maxZ = minZ
        self.minsize = minsize
        for v in verts:
            if v[0] < minX:
                minX = v[0]
            if v[0] > maxX:
                maxX = v[0]
            if v[1] < minY:
                minY = v[1]
            if v[1] > maxY:
                maxY = v[1]

            if v[2] < minZ:
                minZ = v[2]
            if v[2] > maxZ:
                maxZ = v[2]
        margin = 2 * minsize
        minX -= margin
        maxX += margin
        minY -= margin
        maxY += margin
        minZ -= margin
        maxZ += margin

        bounds = [[minX, minY, minZ], [minX, maxY, minZ], [maxX, maxY, minZ], [maxX, minY, minZ], [minX, minY, maxZ], [minX, maxY, maxZ], [maxX, maxY, maxZ], [maxX,
                  minY, maxZ]]
        self.root = SimpleOctreeVolume(bounds, verts, minsize)

        # self.root.metricz(0)....

    def search(self, vert):
        vertTarget = self.root.deepSearch(vert)
        return vertTarget

    def inVolume(self, vert):
        return self.root.isIn(vert)


class SimpleOctreeVolume:

    MinSize = 0.4

    def metricz(self, level):

        # tab = ""
        # for i in range(0, level):
            # tab += "   "
        # print tab + str(self) + " " + str(level) + " " + str(len(self.children)) + " " + str(len(self.verts))

        if len(self.children) == 0:
            SimpleOctree.nVerts += len(self.verts)
            SimpleOctree.nLeafs += 1
        else:
            SimpleOctree.nVolumes += 1
            for c in self.children:
                c.metricz(level + 1)

    def deepSearch(self, vert):

        # caso base: foglia. Verifica dei vertici e restituzione di quello piu' vicino al baricentro

        if len(self.children) == 0:
            i = self.verts[0]
            distMinim = math.sqrt(math.pow(vert[0] - i[0], 2) + math.pow(vert[1] - i[1], 2) + math.pow(vert[2] - i[2], 2))
            minim = self.verts[0]
            for i in self.verts:
                dist = math.sqrt(math.pow(vert[0] - i[0], 2) + math.pow(vert[1] - i[1], 2) + math.pow(vert[2] - i[2], 2))
                if dist < distMinim:
                    distMinim = dist
                    minim = i
            return minim
        else:

        # passo induttivo: tra tutti i figli del nodo considerato seleziono quello piu' vicino
            # cerco il figlio giusto

            pos = self.chooseChildren(vert)
            return self.children[pos].deepSearch(vert)

    def chooseChildren(self, vert):
        node = self.children[0]
        dist = math.sqrt(math.pow(vert[0] - (node.bounds[0][0] + (node.bounds[2][0] - node.bounds[0][0]) / 2), 2) + math.pow(vert[1] - (node.bounds[0][1]
                          + (node.bounds[1][1] - node.bounds[0][1]) / 2), 2) + math.pow(vert[2] - (node.bounds[0][2] + (node.bounds[4][2] - node.bounds[0][2]) / 2), 2))
        near = 0
        for v in range(1, len(self.children)):

                # calcolo veloce se si trova all'interno del settore

            if vert[0] >= self.children[v].bounds[0][0] and vert[0] <= self.children[v].bounds[2][0] and vert[1] >= self.children[v].bounds[0][1] and vert[1]\
                 <= self.children[v].bounds[1][1] and vert[2] >= self.children[v].bounds[0][2] and vert[2] <= self.children[v].bounds[4][2]:

                # restituisco il volume che contiene il baricentro del marcatore

                return v
            distTemp = math.sqrt(math.pow(vert[0] - (self.children[v].bounds[0][0] + (self.children[v].bounds[2][0] - self.children[v].bounds[0][0]) / 2), 2)
                                  + math.pow(vert[1] - (self.children[v].bounds[0][1] + (self.children[v].bounds[1][1] - self.children[v].bounds[0][1]) / 2), 2)
                                  + math.pow(vert[2] - (self.children[v].bounds[0][2] + (self.children[v].bounds[4][2] - self.children[v].bounds[0][2]) / 2), 2))

            # caso in cui nessun volume contiene il baricentro

            if distTemp < dist:
                dist = distTemp
                near = v

        # restituisco il volume piu' vicino al marcatore

        return near

    def __init__(self, bounds, verts, minsize=0.4):
        self.children = []
        self.verts = []
        self.bounds = bounds
        SimpleOctreeVolume.MinSize = minsize

        cX = 0
        cY = 0
        cZ = 0
        for i in range(0, 8):
            cX += bounds[i][0]
            cY += bounds[i][1]
            cZ += bounds[i][2]
        self.center = [cX / 8, cY / 8, cZ / 8]

        self.halfX = float(bounds[3][0] - bounds[0][0]) / 2
        self.halfY = float(bounds[1][1] - bounds[0][1]) / 2
        self.halfZ = float(bounds[4][2] - bounds[0][2]) / 2

        # I need empty leaves as well so we dont assume that verts should be less than 8

        if self.halfX <= minsize or self.halfY <= minsize or self.halfZ <= minsize or len(verts) < 1:  # or len(verts) <= 8:
            self.verts = verts
        else:
            self.children = self.__spawnVolumes(verts)

    def __spawnVolumes(self, verts):
        ret = []
        subBounds = []
        subVerts = [[], [], [], [], [], [], [], []]

        for i in range(0, 8):
            subBounds.append(self.__getSubvolume(i))

        for v in verts:
            ix = int(math.ceil((v[0] - self.bounds[0][0]) / self.halfX) - 1)
            iy = int(math.ceil((v[1] - self.bounds[0][1]) / self.halfY) - 1)
            iz = int(math.ceil((v[2] - self.bounds[0][2]) / self.halfZ) - 1)

            if ix == 0:
                if iy == 0:
                    idx = 0
                else:
                    idx = 1
            else:
                if iy == 0:
                    idx = 3
                else:
                    idx = 2

            if iz == 1:
                idx += 4

            subVerts[idx].append(v)

        for i in range(0, 8):
            if len(subVerts[i]) > 0:
                ret.append(SimpleOctreeVolume(subBounds[i], subVerts[i], SimpleOctreeVolume.MinSize))

        return ret

    def __getSubvolume(self, idx):
        zBase = self.bounds[0][2]
        xBase = self.bounds[0][0]
        yBase = self.bounds[0][1]

        if idx > 3:
            zBase += self.halfZ

        if idx == 2 or idx == 3 or idx == 6 or idx == 7:
            xBase += self.halfX

        if idx == 1 or idx == 2 or idx == 5 or idx == 6:
            yBase += self.halfY

        yyBase = yBase + self.halfY
        xxBase = xBase + self.halfX
        zzBase = zBase + self.halfZ
        return [[xBase, yBase, zBase], [xBase, yyBase, zBase], [xxBase, yyBase, zBase], [xxBase, yBase, zBase], [xBase, yBase, zzBase], [xBase, yyBase, zzBase], [xxBase,
                yyBase, zzBase], [xxBase, yBase, zzBase]]


