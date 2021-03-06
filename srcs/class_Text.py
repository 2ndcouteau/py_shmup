#!/usr/bin/env python3.7
# _*_ coding: Utf-8 -*

import pygame
import time

from pygame.locals	import *

from constants			import (Y_WINDOW, X_WINDOW,
								FONT,
								WHITE, BLACK, RED, GREEN, BLUE, YELLOW,
								POS_HP, POS_LIVES, POS_SCORE, POS_TIME, POS_SHIELD,
								TITLE_MENU, PLAY, OPTIONS_MAIN, QUIT,
								RESUME, RESTART, OPTIONS_LEVEL, MAIN_MENU,
								REMAINING_LIVES, CONTINUE, RESTART_DEATH, OPTIONS_DEATH, MAIN_MENU_DEATH,
								SCORE_GAMEOVER, TIME_GAMEOVER, OPTIONS_GAMEOVER, MAIN_MENU_GAMEOVER,
								OPT_MUSIC, OPT_SFX, OPT_AUTOSHOOT, OPT_RETURN_MENU,
								)

class Text_line(pygame.sprite.Sprite):
	def __init__(self, font_size, text, pos, cx=False, cy=True, selected=False):
		pygame.sprite.Sprite.__init__(self)

		self.font_size = font_size
		self.text = text
		self.cx = cx
		self.cy = cy
		self.pos = list(pos)
		self.selected = selected

		self.font_low = pygame.font.Font(FONT, font_size)
		self.font_big = pygame.font.Font(FONT, font_size * 2)

		self.image_low = self.font_low.render(self.text, True, WHITE)
		self.image_big = self.font_big.render(self.text, True, WHITE)

		self.rect_low = self.image_low.get_rect()
		self.size_low = self.image_low.get_size()

		self.rect_big = self.image_big.get_rect()
		self.size_big = self.image_big.get_size()

		if selected:
			self.image = self.image_big
			self.rect = self.rect_big
		else:
			self.image = self.image_low
			self.rect = self.rect_low

		# self.old_size = self.new_size * 2
		self.position_text()


	def position_text(self):
		#cx= center_x, cy= center_y
		self.pos_low = self.pos
		self.pos_big = self.pos

		# Can't facto code because of layout centering layout issue
		if self.cx :
			self.rect_low.x = self.pos_low[0] - (self.size_low[0] / 2)
			self.rect_big.x = self.pos_big[0] - (self.size_big[0] / 2)
		else:
			self.rect_low.x = self.pos_low[0]
			self.rect_big.x = self.pos_big[0]

		if self.cy :
			self.rect_low.y = self.pos_low[1] - (self.size_low[1] / 2)
			self.rect_big.y = self.pos_big[1] - (self.size_big[1] / 2)
		else:
			self.rect_low.y = self.pos_low[1]
			self.rect_big.y = self.pos_big[1]

class Text():
	def __init__(self):
		self.all_text = []

	def draw_text(self, window):
		for text in self.all_text:
			window.blit(text.image, text.rect)


class Text_level(Text):
	def __init__(self, g):
		Text.__init__(self)

		self.x_right_time_offset = 170
		self.x_right_life_offset = 100
		self.x_left_offset = 5
		self.y_bottom_offset = 25

		self.title_font_size = 24
		self.font_size = 18
		self.g = g

		self.str_time = time.strftime("%M:%S.", time.gmtime(self.g.player.time)) + str(repr(self.g.player.time).split('.')[1][:3])
		self.all_text.insert(POS_HP, Text_line(self.font_size, "Hp: {0}".format(str(g.player.hp)), (self.x_left_offset, Y_WINDOW - self.y_bottom_offset), cx=False, cy=False))
		self.all_text.insert(POS_LIVES, Text_line(self.font_size, "Lifes: {0}".format(str(g.player.lives)), ((X_WINDOW - 100), Y_WINDOW - self.y_bottom_offset), cx=False, cy=False))
		self.all_text.insert(POS_SCORE, Text_line(self.font_size, "Score: {0}".format(str(g.player.score)), (self.x_left_offset, 0), cx=False, cy=False))
		self.all_text.insert(POS_TIME, Text_line(self.font_size, "Time: {0}".format(self.str_time), ((X_WINDOW - self.x_right_time_offset), 0), cx=False, cy=False))
		self.all_text.insert(POS_SHIELD, Text_line(self.font_size, "Shield: {0}".format(str(g.player.shield)), ((X_WINDOW / 2), Y_WINDOW - self.y_bottom_offset), cx=True, cy=False))

		self.len_all_text = len(self.all_text)

	def update(self):
		self.str_time = time.strftime("%M:%S.", time.gmtime(self.g.player.time)) + str(repr(self.g.player.time).split('.')[1][:3])

		self.all_text[POS_HP] = Text_line(self.font_size, "Hp: {0}".format(str(self.g.player.hp)), (self.x_left_offset, Y_WINDOW - self.y_bottom_offset), cx=False, cy=False)
		self.all_text[POS_LIVES] = Text_line(self.font_size, "Lifes: {0}".format(str(self.g.player.lives)), ((X_WINDOW - self.x_right_life_offset), Y_WINDOW - self.y_bottom_offset), cx=False, cy=False)
		self.all_text[POS_SCORE] = Text_line(self.font_size, "Score: {0}".format(str(self.g.player.score)), (self.x_left_offset, 0), cx=False, cy=False)
		self.all_text[POS_TIME] = Text_line(self.font_size, "Time: {0}".format(self.str_time), (X_WINDOW - self.x_right_time_offset, 0), cx=False, cy=False)
		self.all_text[POS_SHIELD] = Text_line(self.font_size, "Shield: {0}".format(str(self.g.player.shield)), ((X_WINDOW / 2), Y_WINDOW - self.y_bottom_offset), cx=True, cy=False)

class Text_menu():
	def __init__(self, offset):
		self.y_offset_pos = 50
		self.prev_pos = offset
		self.new_pos = offset
		self.offset = offset

	def move_up(self):
		if (self.new_pos > self.offset):
			self.new_pos -= 1
		else:
			self.new_pos = self.len_all_text - 1

	def move_down(self):
		if (self.new_pos < self.len_all_text - 1):
			self.new_pos += 1
		else:
			self.new_pos = self.offset

	def update(self):
		if self.prev_pos != self.new_pos:
			self.all_text[self.prev_pos].image = self.all_text[self.prev_pos].image_low
			self.all_text[self.prev_pos].rect = self.all_text[self.prev_pos].rect_low

			self.all_text[self.new_pos].image = self.all_text[self.new_pos].image_big
			self.all_text[self.new_pos].rect = self.all_text[self.new_pos].rect_big

			self.prev_pos = self.new_pos


class Text_level_menu(Text, Text_menu):
	def __init__(self):
		Text.__init__(self)
		self.offset_title_select = 1
		Text_menu.__init__(self, self.offset_title_select)

		self.title_font_size = 24
		self.font_size = 12

		self.all_text.insert(TITLE_MENU, Text_line(self.title_font_size, "- Menu -", ((X_WINDOW / 2), Y_WINDOW / 4), cx=True, cy=False))
		self.all_text.insert(RESUME, Text_line(self.font_size, "* Resume *", ((X_WINDOW / 2), (Y_WINDOW / 2) - (self.y_offset_pos * 1) - 15), cx=True, selected=True))
		self.all_text.insert(RESTART, Text_line(self.font_size, "* Restart *", ((X_WINDOW / 2), (Y_WINDOW / 2) + (self.y_offset_pos * 0) - 15), cx=True, selected=False))
		self.all_text.insert(OPTIONS_LEVEL, Text_line(self.font_size, "* Options *", ((X_WINDOW / 2), (Y_WINDOW / 2) + (self.y_offset_pos * 1) - 15), cx=True, selected=False))
		self.all_text.insert(MAIN_MENU, Text_line(self.font_size, "* Main Menu *", ((X_WINDOW / 2), (Y_WINDOW / 2) + (self.y_offset_pos * 2) - 15), cx=True, selected=False))

		self.len_all_text = len(self.all_text)


class Text_death_menu(Text, Text_menu):
	def __init__(self, g):
		Text.__init__(self)
		self.g = g
		self.offset_title_select = 2
		Text_menu.__init__(self, self.offset_title_select)

		self.title_font_size = 24
		self.font_size = 12

		self.all_text.insert(TITLE_MENU, Text_line(self.title_font_size, "! YOU ARE DEAD !", ((X_WINDOW / 2), (Y_WINDOW / 4) + 10), cx=True, cy=False))
		self.all_text.insert(REMAINING_LIVES, Text_line(self.title_font_size, "{0} ship(s) left".format(self.g.player.lives), ((X_WINDOW / 2), (Y_WINDOW / 4) + 75), cx=True, cy=False))
		self.all_text.insert(CONTINUE, Text_line(self.font_size, "* Continue *", ((X_WINDOW / 2), (Y_WINDOW / 2) + (self.y_offset_pos * 0) - 15), cx=True, selected=True))
		# else:
		# 	self.all_text.insert(GAME_OVER, Text_line(self.title_font_size, "GAME OVER", ((X_WINDOW / 2), (Y_WINDOW / 4) + 15), cx=True, cy=False))
		# 	self.all_text.insert(CONTINUE, Text_line(self.title_font_size, "", ((X_WINDOW / 2), (Y_WINDOW / 4) + 15), cx=True, cy=False))
		# 	self.offset_title_select = 3
			# self.all_text.insert(SOUL_SELL, Text_line(self.font_size, "* Sell your soul *", ((X_WINDOW / 2), (Y_WINDOW / 2) + (self.y_offset_pos * 0) - 15), cx=True, selected=False))
		self.all_text.insert(RESTART_DEATH, Text_line(self.font_size, "* Restart Level *", ((X_WINDOW / 2), (Y_WINDOW / 2) + (self.y_offset_pos * 1) - 15), cx=True, selected=False))
		self.all_text.insert(OPTIONS_DEATH, Text_line(self.font_size, "* Options *", ((X_WINDOW / 2), (Y_WINDOW / 2) + (self.y_offset_pos * 2) - 15), cx=True, selected=False))
		self.all_text.insert(MAIN_MENU_DEATH, Text_line(self.font_size, "* Main Menu *", ((X_WINDOW / 2), (Y_WINDOW / 2) + (self.y_offset_pos * 3) - 15), cx=True, selected=False))

		self.len_all_text = len(self.all_text)

class Text_gameover_menu(Text, Text_menu):
	def __init__(self, g):
		Text.__init__(self)
		self.g = g
		self.offset_title_select = 3
		Text_menu.__init__(self, self.offset_title_select)

		self.title_font_size = 24
		self.font_size = 12

		self.all_text.insert(TITLE_MENU, Text_line(self.title_font_size, "! GAMEOVER !", ((X_WINDOW / 2), (Y_WINDOW / 4) + 10), cx=True, cy=False))
		self.all_text.insert(SCORE_GAMEOVER, Text_line(self.title_font_size, "SCORE : {0}".format(self.g.player.score), ((X_WINDOW / 2), (Y_WINDOW / 4) + (self.y_offset_pos * 2) - 15), cx=True, cy=False))
		self.all_text.insert(TIME_GAMEOVER, Text_line(self.title_font_size, "TIME : {0} ".format(self.g.level_text.str_time), ((X_WINDOW / 2), (Y_WINDOW / 4) + (self.y_offset_pos * 3) - 35), cx=True, cy=False))
		self.all_text.insert(OPTIONS_GAMEOVER, Text_line(self.font_size, "* Options *", ((X_WINDOW / 2), (Y_WINDOW / 2) + (self.y_offset_pos * 1) - 15), cx=True, selected=True))
		self.all_text.insert(MAIN_MENU_GAMEOVER, Text_line(self.font_size, "* Main Menu *", ((X_WINDOW / 2), (Y_WINDOW / 2) + (self.y_offset_pos * 2) - 15), cx=True, selected=False))

		self.len_all_text = len(self.all_text)


	def update(self):
		Text_menu.update(self)
		self.all_text[SCORE_GAMEOVER] = Text_line(self.title_font_size, "SCORE : {0}".format(self.g.player.score), ((X_WINDOW / 2), (Y_WINDOW / 4) + (self.y_offset_pos * 2) - 15), cx=True, cy=False)
		self.all_text[TIME_GAMEOVER] = Text_line(self.title_font_size, "TIME : {0} ".format(self.g.level_text.str_time), ((X_WINDOW / 2), (Y_WINDOW / 4) + (self.y_offset_pos * 3) - 35), cx=True, cy=False)


class Text_opt_level_menu(Text, Text_menu):
	def __init__(self, g):
		Text.__init__(self)
		self.g = g
		self.offset_title_select = 1
		Text_menu.__init__(self, self.offset_title_select)

		self.title_font_size = 24
		self.font_size = 12

		self.all_text.insert(TITLE_MENU, Text_line(self.title_font_size, "OPTIONS", ((X_WINDOW / 2), (Y_WINDOW / 4) + 10), cx=True, cy=False))
		self.all_text.insert(OPT_MUSIC, Text_line(self.font_size, "MUSIC : {0}".format(self.check_state(g.opt_music)), ((X_WINDOW / 2), (Y_WINDOW / 4) + (self.y_offset_pos * 3) - 15), cx=True, cy=False, selected=True))
		self.all_text.insert(OPT_SFX, Text_line(self.font_size, "SFX : {0}".format(self.check_state(g.opt_sfx)), ((X_WINDOW / 2), (Y_WINDOW / 4) + (self.y_offset_pos * 4) - 15), cx=True, cy=False))
		self.all_text.insert(OPT_AUTOSHOOT, Text_line(self.font_size, "AUTOSHOOT : {0}".format(self.check_state(g.opt_autoshoot)), ((X_WINDOW / 2), (Y_WINDOW / 4) + (self.y_offset_pos * 5) - 15), cx=True, cy=False))

		self.all_text.insert(OPT_RETURN_MENU, Text_line(self.font_size, "RETURN", ((X_WINDOW / 2), (Y_WINDOW / 4) + (self.y_offset_pos * 6) - 15), cx=True, cy=False))


		self.len_all_text = len(self.all_text)

	def check_state(self, state):
		if (state is True):
			return "ON"
		return "OFF"

	def update(self):
		Text_menu.update(self)
		if (self.new_pos == OPT_MUSIC):
			self.all_text[OPT_MUSIC] = Text_line(self.font_size, "MUSIC : {0}".format(self.check_state(self.g.opt_music)), ((X_WINDOW / 2), (Y_WINDOW / 4) + (self.y_offset_pos * 3) - 15), cx=True, cy=False, selected=True)
			self.all_text[OPT_SFX] = Text_line(self.font_size, "SFX : {0}".format(self.check_state(self.g.opt_sfx)), ((X_WINDOW / 2), (Y_WINDOW / 4) + (self.y_offset_pos * 4) - 15), cx=True, cy=False)
			self.all_text[OPT_AUTOSHOOT] = Text_line(self.font_size, "AUTOSHOOT : {0}".format(self.check_state(self.g.opt_autoshoot)), ((X_WINDOW / 2), (Y_WINDOW / 4) + (self.y_offset_pos * 5) - 15), cx=True, cy=False)
		elif (self.new_pos == OPT_SFX) :
			self.all_text[OPT_MUSIC] = Text_line(self.font_size, "MUSIC : {0}".format(self.check_state(self.g.opt_music)), ((X_WINDOW / 2), (Y_WINDOW / 4) + (self.y_offset_pos * 3) - 15), cx=True, cy=False)
			self.all_text[OPT_SFX] = Text_line(self.font_size, "SFX : {0}".format(self.check_state(self.g.opt_sfx)), ((X_WINDOW / 2), (Y_WINDOW / 4) + (self.y_offset_pos * 4) - 15), cx=True, cy=False, selected=True)
			self.all_text[OPT_AUTOSHOOT] = Text_line(self.font_size, "AUTOSHOOT : {0}".format(self.check_state(self.g.opt_autoshoot)), ((X_WINDOW / 2), (Y_WINDOW / 4) + (self.y_offset_pos * 5) - 15), cx=True, cy=False)
		elif (self.new_pos == OPT_AUTOSHOOT) :
			self.all_text[OPT_MUSIC] = Text_line(self.font_size, "MUSIC : {0}".format(self.check_state(self.g.opt_music)), ((X_WINDOW / 2), (Y_WINDOW / 4) + (self.y_offset_pos * 3) - 15), cx=True, cy=False)
			self.all_text[OPT_SFX] = Text_line(self.font_size, "SFX : {0}".format(self.check_state(self.g.opt_sfx)), ((X_WINDOW / 2), (Y_WINDOW / 4) + (self.y_offset_pos * 4) - 15), cx=True, cy=False)
			self.all_text[OPT_AUTOSHOOT] = Text_line(self.font_size, "AUTOSHOOT : {0}".format(self.check_state(self.g.opt_autoshoot)), ((X_WINDOW / 2), (Y_WINDOW / 4) + (self.y_offset_pos * 5) - 15), cx=True, cy=False, selected=True)
		else :
			self.all_text[OPT_MUSIC] = Text_line(self.font_size, "MUSIC : {0}".format(self.check_state(self.g.opt_music)), ((X_WINDOW / 2), (Y_WINDOW / 4) + (self.y_offset_pos * 3) - 15), cx=True, cy=False)
			self.all_text[OPT_SFX] = Text_line(self.font_size, "SFX : {0}".format(self.check_state(self.g.opt_sfx)), ((X_WINDOW / 2), (Y_WINDOW / 4) + (self.y_offset_pos * 4) - 15), cx=True, cy=False)
			self.all_text[OPT_AUTOSHOOT] = Text_line(self.font_size, "AUTOSHOOT : {0}".format(self.check_state(self.g.opt_autoshoot)), ((X_WINDOW / 2), (Y_WINDOW / 4) + (self.y_offset_pos * 5) - 15), cx=True, cy=False)


class Text_main_menu(Text, Text_menu):
	def __init__(self):
		Text.__init__(self)
		self.offset_title_select = 1
		Text_menu.__init__(self, self.offset_title_select)

		self.title_font_size = 32
		self.font_size = 16

		self.all_text.insert(TITLE_MENU, Text_line(self.title_font_size, "Hard SHMUP 42", ((X_WINDOW / 2), Y_WINDOW / 4), cx=True))
		self.all_text.insert(PLAY, Text_line(self.font_size, "* Play *", ((X_WINDOW / 2), (Y_WINDOW / 2) + (self.y_offset_pos * 0)), cx=True, selected=True))
		self.all_text.insert(OPTIONS_MAIN, Text_line(self.font_size, "* Options *", ((X_WINDOW / 2), (Y_WINDOW / 2) + (self.y_offset_pos * 1)), cx=True, selected=False))
		self.all_text.insert(QUIT, Text_line(self.font_size, "* Quit *", ((X_WINDOW / 2), (Y_WINDOW / 2) + (self.y_offset_pos * 2)), cx=True, selected=False))

		self.len_all_text = len(self.all_text)
