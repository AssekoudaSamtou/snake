from tkinter import *
import tkinter.font as tkFont
from tkinter.messagebox import *

from snake import Serpent
import random

class SnakeControl:

	def __init__(self, master, snake, restart=False):
		self.snake = snake
		self.can = Canvas(master, height=500, width=500, bg="#afc1c4")
		self.boule = self.can.create_oval(400, 400, 425, 425, fill='red')
		r1 = self.can.create_rectangle(0, 0, 25, 25, fill='#1b90d4')
		r2 = self.can.create_rectangle(25, 0, 50, 25, fill='#1b90d4')
		r3 = self.can.create_rectangle(50, 0, 75, 25, fill='yellow')
		self.directions = {'droite':self.droite, 'gauche':self.gauche, 'haut':self.haut, 'bas':self.bas, "pause":self.pause}
		self.body = {r1:self.can.coords(r1), r2:self.can.coords(r2), r3:self.can.coords(r3)}
		self.pivot = r3
		self.can.bind_all("<KeyPress-Down>", self.bas)
		self.can.bind_all("<KeyPress-Up>", self.haut)
		self.can.bind_all("<KeyPress-Right>", self.droite)
		self.can.bind_all("<KeyPress-Left>", self.gauche)
		self.can.bind_all("<space>", self.pause)
		self.can.bind_all("<Return>", self.reprendre)
		self.can.grid(column=0, row=1)
		self.commencer()
		# win.after(2000, self.commencer)

	def commencer(self):
		if self.snake.direction != "pause":
			self.directions[self.snake.direction]()
			self.after_cancel_id = win.after(400, self.commencer)
			print(self.after_cancel_id)

	def pause(self, event=None):
		self.snake.direction = "pause"

	def reprendre(self, event=None):
		self.snake.direction = "droite"

	def deplacer(self):
		items = list(self.body.items())
		aug_position = items[0][1]
		n = len(items)-1
			
		for i in range(n):
			before = items[n-i][1]
			actu = self.can.coords(items[n-i-1][0])
			increment = self.calculer(before, actu)
			self.can.move(items[n-i-1][0], increment[0], increment[1])
			self.body[items[n-i-1][0]] = self.can.coords(items[n-i-1][0])

		if self.boule_is_eat():
			self.incrementer_longueur(aug_position)
			self.update_score()

	def droite(self, event=None):
		self.can.unbind_all("<KeyPress-Right>")
		self.can.unbind_all("<KeyPress-Left>")
		self.can.bind_all("<KeyPress-Down>", self.bas)
		self.can.bind_all("<KeyPress-Up>", self.haut)
		self.can.bind_all("<KeyPress-Right>", self.droite)
		if self.snake_is_over():
			self.gameover()
		else:
				
			self.snake.direction = 'droite'
			self.body[self.pivot] = self.can.coords(self.pivot)
			self.can.move(self.pivot, 25, 0)
			self.deplacer()

	def gauche(self, event=None):
		self.can.unbind_all("<KeyPress-Right>")
		self.can.unbind_all("<KeyPress-Left>")
		self.can.bind_all("<KeyPress-Down>", self.bas)
		self.can.bind_all("<KeyPress-Up>", self.haut)
		self.can.bind_all("<KeyPress-Left>", self.gauche)
		if self.snake_is_over():
			self.gameover()
		else:
			self.snake.direction = 'gauche'
			self.body[self.pivot] = self.can.coords(self.pivot)
			self.can.move(self.pivot, -25, 0)
			self.deplacer()

	def haut(self, event=None):
		self.can.unbind_all("<KeyPress-Down>")
		self.can.unbind_all("<KeyPress-Up>")
		self.can.bind_all("<KeyPress-Up>", self.haut)
		self.can.bind_all("<KeyPress-Right>", self.droite)
		self.can.bind_all("<KeyPress-Left>", self.gauche)
		if self.snake_is_over():
			self.gameover()
		else:
			self.snake.direction = 'haut'
			self.body[self.pivot] = self.can.coords(self.pivot)
			self.can.move(self.pivot, 0, -25)
			self.deplacer()

	def bas(self, event=None):
		self.can.unbind_all("<KeyPress-Down>")
		self.can.unbind_all("<KeyPress-Up>")
		self.can.bind_all("<KeyPress-Down>", self.bas)
		self.can.bind_all("<KeyPress-Right>", self.droite)
		self.can.bind_all("<KeyPress-Left>", self.gauche)
		if self.snake_is_over():
			self.gameover()
		else:
			self.snake.direction = 'bas'
			self.body[self.pivot] = self.can.coords(self.pivot)
			self.can.move(self.pivot, 0, 25)
			self.deplacer()

	def calculer(self, now, before):
		return (now[0]-before[0], now[1]-before[1])

	def incrementer_longueur(self, coords):
		r = self.can.create_rectangle(coords[0], coords[1], coords[2], coords[3], fill='#1b90d4')
		tmp = self.body
		self.body = {r:self.can.coords(r)}
		for elt in tmp:self.body[elt] = tmp[elt]
		self.move_boule()

	def boule_is_eat(self):
		head_coords = self.can.coords(self.pivot)
		boule_coords = self.can.coords(self.boule)
		if head_coords == boule_coords:
			self.snake.score += 1
			return True
		return False
	
	def move_boule(self):
		x0 = random.randrange(19) * 25
		y0 = random.randrange(19) * 25
		x1 = x0 + 25
		y1 = y0 + 25
		self.can.delete(self.boule)
		self.boule = self.can.create_oval(x0, y0, x1, y1, fill='red')

	def snake_is_over(self):
		coords = self.can.coords(self.pivot)
		if (self.snake.direction == "droite") and (coords[2] >= 500):
			# self.can.bell()
			return True
		if (self.snake.direction == "gauche") and (coords[0] <= 0):
			# self.can.bell()
			return True
		if (self.snake.direction == "haut") and (coords[1] <= 0):
			# self.can.bell()
			return True
		if (self.snake.direction == "bas") and (coords[3] >= 500):
			# self.can.bell()
			return True

	def restart(self):
		print(self.after_cancel_id)
		last = int(self.after_cancel_id.split("after#")[1])
		win.after_cancel(self.after_cancel_id)
		snake = self.snake
		self.can.destroy()
		self.__init__(win, Serpent(), True)

	def gameover(self):
		self.snake.direction = "pause"
		self.can.create_text(250, 250, text="GAME OVER", font=font)
		self.can.unbind_all("<KeyPress-Down>")
		self.can.unbind_all("<KeyPress-Up>")
		self.can.unbind_all("<KeyPress-Right>")
		self.can.unbind_all("<KeyPress-Left>")
		self.can.unbind_all("<space>")
		self.can.unbind_all("<Return>")
		if askokcancel("Nouvelle partie", "Voulez-vous recommencer ?"):
			self.restart()
		else:
			print("cancel")
			win.destroy()

	def update_score(self):
		score_label["text"] = f"SCORE : {self.snake.score}"

win=Tk()
font = tkFont.Font(family='OCR A', slant='italic', size=-40, weight='bold')
score_label = Label(text="SCORE : 0", font=font)
# print(score_label.winfo_screenmmwidth())
score_label.grid(column=0, row=0, sticky="e")
win.geometry()

SnakeControl(win, Serpent())
win.mainloop()