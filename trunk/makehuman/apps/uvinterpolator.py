#!/usr/bin/python
# -*- coding: utf-8 -*-

""" 
**Project Name:**      MakeHuman

**Product Home Page:** http://www.makehuman.org/

**Code Home Page:**    http://code.google.com/p/makehuman/

**Authors:**           Hannes 

**Copyright(c):**      MakeHuman Team 2001-2013

**Licensing:**         AGPL3 (see also http://www.makehuman.org/node/318)

**Coding Standards:**  See http://www.makehuman.org/node/165

Abstract
--------

TODO
"""

__docformat__ = 'restructuredtext'

import math

import log

# first version of uv interpolator
# picks a start solution (1/nth of each of the n-targets)
# then tries to improve the solution in a given amount of iterations
# distance to current character measured by euclidian distance of the morph target values
# each iteration shifts the current solution in the direction of the n-targets, with a given step size
# best improvement is chosen as new current solution
# if no improvement can be achieved, the step size is divided by 2
# best solution is returned

class UVFinder:
	def __init__(self, debug_output):
		
		self.targetFolder = 'data/targets/macrodetails'
		self.debug_output = debug_output
		self.init_uvs()
	        

		return

	def targetName(self,s):
		return '%s/%s' % (self.targetFolder, s)

	def init_uvs(self):
		self.uvs = { }
		self.uvs_by_index = { }

		#todo: replace this with dynamic lookup

		self.uvs[ self.targetName('neutral-male-young.target.uv') ] = [ [ self.targetName('neutral-male-young.target'), 1.0 ] ]
		self.uvs[ self.targetName('universal-male-young-flaccid-heavy.target.uv') ] = [ [ self.targetName('neutral-male-young.target'), 1.0 ],  [ self.targetName('universal-male-young-flaccid-heavy.target'), 1.0 ]]


		
		self.numUVs = len(self.uvs.keys())

		idx = 0
		for (k,v) in self.uvs.iteritems():
			self.uvs_by_index[idx] = k
			idx = idx + 1

		return

	def targets4UVs(self, uvsets):
		targets = {}
		for (i,v) in enumerate(uvsets):
			for t in self.uvs[ self.uvs_by_index[i] ]:
				if t[0] in targets:
					targets[t[0]] += v * t[1]
				else:
					targets[t[0]] = v * t[1]

		return targets

	def distanceUVs(self, targets1, targets2 ):
		distance = 0.0
		for(k,v) in targets1.iteritems( ):
			if k in targets2:
				distance += (v - targets2[k]) * (v - targets2[k])
			else:
				distance += v * v
		for(k,v) in targets2.iteritems( ):
			if k not in targets1:
				distance += v * v

		return distance
	
	def shiftUVs(self, sol, dimension, mult):
		diff=[0.0 for i in range(self.numUVs)]
		diff[dimension] = 1.0



		length=0.0
		for i in range(self.numUVs):
			diff[i]-=sol[i]
			length += diff[dimension]*diff[dimension]
		length = math.sqrt(length)
		if not length: 
			return None

		result = [0.0 for i in range(self.numUVs)]
		for i in range(self.numUVs):
			diff[i]/=length
			result[i] = sol[i] + mult*diff[i]
			if self.debug_output: 
				log.message('--: %s', result[i])
			if result[i] < 0.0 or result[i]>1.0:
				return None
		if self.debug_output:
			for i in range(self.numUVs):
				log.message('++ %s %s', diff[i], sol[i])

		return result
		
	def dump_solution(self, sol, dist, step):
		log.debug('solution:')
		for i in range(self.numUVs):
                    log.debug('%s %s', self.uvs_by_index[i], sol[i])
		log.debug('dist: %s', dist)
		log.debug('step: %s', step)
		
	def improve(self, best, step):
		found = 0
		dist = self.distanceUVs(self.targets4UVs(best), self.targets)
		if self.debug_output:
			self.dump_solution(best, dist, step)
		best3 = []
		for i in range(self.numUVs):
			best2 = self.shiftUVs(best, i, step)
			if not best2: 
				continue
			dist2 = self.distanceUVs(self.targets4UVs(best2), self.targets)
			if self.debug_output:
				self.dump_solution(best2, dist2, step)
			if dist2 < dist:
				found = 1
				dist = dist2
				best3 = best2

		for i in range(self.numUVs):
			best2 = self.shiftUVs(best, i, -step)
			if not best2: 
				continue
			dist2 = self.distanceUVs(self.targets4UVs(best2), self.targets)
			if self.debug_output:
				self.dump_solution(best2, dist2, step)
			if dist2 < dist:
				found = 1
				dist = dist2
				best3 = best2

		if not found:
			return (best, step/2.0)
		else:
			return (best3, step)

	def solve(self, targets):
		if self.debug_output:
			log.debug('----')
			for(k,v) in targets.iteritems():
                            if v > 0.0:
                                log.debug('searching: %s %s', k, v)
		self.targets = targets
		start = 1.0 / self.numUVs
		best = [ start for i in range(self.numUVs) ]
		step = 0.5

		# change precision by modifying the number of iterations here
		for i in range(5):
			(best,step) = self. improve(best,step)
		
		solution = []

		if self.debug_output:
			log.debug('----')
			for i in range(self.numUVs):
                            if(best[i] > 0.0):
                                log.debug('UVSolution: ', self.uvs_by_index[i], best[i])
			log.debug('----')


		for i in range(self.numUVs):
			if(best[i] > 0.0):
				solution.append((self.uvs_by_index[i], best[i]))
		return best

