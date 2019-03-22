import argparse
parser = argparse.ArgumentParser()
parser.add_argument("x", help="le nombre a mettre au carré")
parser.parse_args()

class Serpent:
	def __init__(self):
		self.longeur_initiale = 2
		self.longueur = self.longeur_initiale
		self.score = 0
		# self.position = None
		self.direction = "droite"

	def update_score(self):
		self.score = self.longueur - self.longeur_initiale