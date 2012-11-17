import random

import simplejson as json

class Assimilation:

	def __init__(self, id=None, size=None, players=None, JSON=None):
		self.id = None
		self.claims = []
		self.pile = []
		self.players = []
		self.board = []
		self.history = []
		self.playersById = {}
		
		#initialization of a new game		
		if id is not None and size is not None and players is not None:
			self.id = id
			self.width = size
			self.height = size
			for player in players:
				self.players.append(Player(player))
			for x in range(size):
				self.board.append([])
				for y in range(size):
					self.board[x].append(None)
					self.pile.append(Tile(x,y))

			for player in self.players:
				self.playersById[player.id] = player
				for x in range(6):
					self.giveTile(player.id)
		elif JSON is not None:
			self.deserialize(JSON)

	def serialize(self):
		result = {}
		result['i'] = self.id
		result['w'] = self.width
		result['he'] = self.height
		result['c'] = []
		result['h'] = []
		result['p'] = []
		result['pi'] = []
		result['b'] = self.board

		for claim in self.claims:
			result['c'].append(claim.serialize())
		for player in self.players:
			result['p'].append(player.serialize())
		for claim in self.history:
			result['h'].append(claim.serialize())
		for tile in self.pile:
			result['pi'].append(tile.serialize())
		return result

	def deserialize(self, JSON):
		g = json.loads(JSON)
		self.id = g['i']
		self.width = g['w']
		self.height = g['he']
		self.board = g['b']

		for claim in g['c']:
			self.claims.append(Claim(JSON=claim))
		for player in g['p']:
			self.players.append(Player(JSON=player))
		for claim in g['h']:
			self.history.append(Claim(JSON=claim))
		for tile in g['pi']:
			self.pile.append(Tile(JSON=tile))

		for player in self.players:
			self.playersById[player.id] = player

	def export(self):
		return json.dumps(self.serialize())
		
	def giveTile(self, playerid):
		if len(self.pile) == 0:
			return
		select = random.randint(0,len(self.pile)-1)
		tile = self.pile[select]
		self.pile = self.pile[:select] + self.pile[select+1:]
		self.playersById[playerid].hand.append(tile)

	def placeTile(self, tile, player):
		if tile in self.playersById[player].hand:
			self.playersById[player].hand.remove(tile)
			self.giveTile(player)
			self.setOwner(tile, player)

			armies = {}
			neighbors = []
			self.getNeighbors(tile, neighbors)

			for t in neighbors:
				if not armies.has_key(self.getOwner(t)):
					armies[self.getOwner(t)] = 0
				armies[self.getOwner(t)]+=1

			largest = armies[player]
			owner = player
			for id in armies:
				if armies[id] > largest:
					largest = armies[id]
					owner = id
				elif armies[id] == largest:
					owner = player

			for t in neighbors:
				self.setOwner(t, owner)

			self.history.append(Claim(tile,player))
			self.calculateScores()
			return True

		else:
			print tile, player, self.playersById[player].hand
			return False

	def calculateScores(self):
		for player in self.players:
			player.score = 0
		for claim in self.claims:
			self.playersById[claim.owner].score+=1

	def setOwner(self, tile, owner):
		self.board[tile.x][tile.y] = owner
		for claim in self.claims:
			if claim.tile == tile:
				claim.owner = owner
				return
		self.claims.append(Claim(tile,owner))

	def getOwner(self, tile):
		if tile.x < 0 or tile.y < 0 or tile.x >= self.width or tile.y >= self.height:
			return None
		return self.board[tile.x][tile.y]

	def getNeighbors(self, tile, tiles):
		if(self.getOwner(tile) == None or tile in tiles):
			return
		tiles.append(tile)
		self.getNeighbors(Tile(tile.x-1,tile.y),tiles)
		self.getNeighbors(Tile(tile.x+1,tile.y),tiles)
		self.getNeighbors(Tile(tile.x,tile.y-1),tiles)
		self.getNeighbors(Tile(tile.x,tile.y+1),tiles)

	def makeMove(self, id):
		self.placeTile(self.playersById[id].hand[0], id)
		self.printMe()

	def printMe(self):
		for x in range(self.width):
			for y in range(self.height):
				if self.board[x][y] == None:
					print ' ',
				else:
					print self.board[x][y],
			print ''
	def getStateFor(self, playerid, includeHistory=False):
		result = {}
		result['i'] = self.id
		result['w'] = self.width
		result['he'] = self.height
		result['c'] = []
		result['p'] = []
		result['pi'] = len(self.pile)
		if includeHistory:
			result['h'] = []
			for claim in self.history:
				result['h'].append(claim.serialize())

		for claim in self.claims:
			result['c'].append(claim.serialize())
		for player in self.players:
			if player.id == playerid:
				result['p'].append(player.serialize())
			else:
				result['p'].append(player.serializeHidden())
		return json.dumps(result)

class Tile:

	def __init__(self, x=0, y=0, JSON=None):
		self.x = int(x)
		self.y = int(y)
		if JSON is not None:
			self.x = JSON['x']
			self.y = JSON['y']

	def __str__(self):
		return "(" + str(self.x) + "," + str(self.y) + ")"

	def __repr__(self):
		return "(" + str(self.x) + "," + str(self.y) + ")"

	def __eq__(self, other):
		return self.x == other.x and self.y == other.y

	def serialize(self):
		result = {}
		result['x'] = self.x
		result['y'] = self.y
		return result

class Player:

	def __init__(self, id=None, JSON=None):
		self.score = 0
		self.hand = []
		self.id = None
		if id is not None:
			self.id = id
		elif JSON is not None:
			self.id = JSON['i']
			self.score = JSON['s']
			for tile in JSON['h']:
				self.hand.append(Tile(JSON=tile))

	def __repr__(self):
		return 'score: ' + str(self.score) + " " + self.hand.__str__()


	def serialize(self):
		result = {}
		result['i'] = self.id
		result['s'] = self.score
		result['h'] = []
		for tile in self.hand:
			result['h'].append(tile.serialize())
		return result

	def serializeHidden(self):
		result = {}
		result['i'] = self.id
		result['s'] = self.score
		result ['h'] = len(self.hand)
		return result

	def addTile(tile):
		self.hand.append(tile)

class Claim:

	def __init__(self, tile=None, playerid=None, JSON=None):
		self.tile = tile
		self.owner = playerid
		if JSON is not None:
			self.tile = Tile(JSON=JSON['t'])
			self.owner = JSON['o']

	def serialize(self):
		result = {}
		result['t'] = self.tile.serialize()
		result['o'] = self.owner
		return result