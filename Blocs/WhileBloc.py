from dataclasses import dataclass
from pygame import Color, Surface, Vector2 as Vec2

from AST import ASTNodeWhile
from Constantes import BT_SIZE, FONT_20, MARGIN, INNER_MARGIN, SMALL_RADIUS

from Blocs.ParentBloc import ParentBloc
from Blocs.Containers import Sequence, Slot

from MyPygameLibrary.Camera import Camera
from MyPygameLibrary.UI_elements import change_color, darker, draw_text, hsv_color
from MyPygameLibrary.World import draw_poly, draw_rect

COLOR: Color = hsv_color(230, 30, 100)

TEXT_WHILE: str = "WHILE"
TEXT_WHILE_SIZE: Vec2 = Vec2(FONT_20.size(TEXT_WHILE))

TEXT_DO_WHILE: str = "DO WHILE"
TEXT_DO_WHILE_SIZE: Vec2 = Vec2(FONT_20.size(TEXT_DO_WHILE))

DO_WHILE_COLOR: Color = change_color(COLOR, s_fonc=lambda _: .1, v_fonc=lambda _: .9)


@dataclass(slots=True)
class WhileBloc(ParentBloc):
	"""Bloc de logique - tant que la variable booléenne sur le côté gauche du bloc est vraie,
	la séquence de droite est exécutée."""
	is_do: bool
	
	def __init__(self):
		self.is_do = False
		super(WhileBloc, self).__init__(
		  COLOR,
		  [Slot(COLOR, "False")],
		  [Sequence(COLOR)],
		  ["is_do"])
	
	def __repr__(self):
		return f"While( {self.slots[0]}:  {self.sequences[0]} )"
	
	def get_size(self) -> Vec2:
		width = self.sequences[0].size.x + self.slots[0].size.x + self.text_width
		height = max(self.slots[0].size.y, self.sequences[0].size.y)
		return Vec2(width, height) + Vec2(2 * MARGIN) + Vec2(3, 0) * INNER_MARGIN
	
	def slot_position(self, slot_id: int) -> Vec2:
		position_x = self.text_width + INNER_MARGIN
		if self.is_do:
			return Vec2(position_x, self.size.y - self.slots[0].size.y) + Vec2(1, -1) * MARGIN
		else:
			return Vec2(position_x, 0) + Vec2(1, 1) * MARGIN
	
	def sequence_position(self, sequence_id: int) -> Vec2:
		position_x = self.slots[0].size.x + self.text_width + 3 * INNER_MARGIN
		position_y = sum([sequence.size.y for sequence in self.sequences[:sequence_id]]) +\
		             sequence_id * INNER_MARGIN
		return Vec2(position_x, position_y) + Vec2(1, 1) * MARGIN
	
	def post_draw(self, surface: Surface, camera: Camera, origin: Vec2):
		if self.is_do:
			text = TEXT_DO_WHILE
			position = Vec2(0, self.size.y - self.slots[0].size.y / 2) + Vec2(1, -1) * MARGIN
		else:
			text = TEXT_WHILE
			position = Vec2(0, self.slots[0].size.y / 2) + Vec2(1, 1) * MARGIN
		
		draw_text(surface, text, origin + position, 20, align="left", camera=camera)
	
	def button_size(self, button_id: int) -> Vec2:
		match self.buttons[button_id]:
			case "is_do":
				return BT_SIZE
	
	def button_position(self, button_id: int) -> Vec2:
		match self.buttons[button_id]:
			case "is_do":
				position_x = (self.text_width - BT_SIZE.x) / 2 + MARGIN
				position_y = self.slots[0].size.y / 2 + TEXT_DO_WHILE_SIZE.y / 2 + MARGIN
				if self.is_do:
					position_y = self.size.y - BT_SIZE.y - position_y
				return Vec2(position_x, position_y)
	
	def draw_button(self, surface: Surface, camera: Camera, origin: Vec2, hovered: bool, button_id: int):
		position = self.button_position(button_id)
		size = self.button_size(button_id)
		
		match self.buttons[button_id]:
			case "is_do":
				color = darker(DO_WHILE_COLOR, .7) if hovered else DO_WHILE_COLOR
				draw_rect(surface, camera, color, origin + position, size, border_radius=SMALL_RADIUS)
				
				color = darker(DO_WHILE_COLOR, .7 * .6) if hovered else darker(DO_WHILE_COLOR, .6)
				vertices = [Vec2(4, 4), Vec2(BT_SIZE.x - 4, 4), Vec2(BT_SIZE.x / 2, BT_SIZE.y - 4)]
				if self.is_do:
					vertices = [BT_SIZE - vertex for vertex in vertices]
				draw_poly(surface, camera, color, [vertex + position + origin for vertex in vertices])
	
	def button_function(self, button_id: int) -> bool:
		match self.buttons[button_id]:
			case "is_do":
				self.is_do = not self.is_do
				return True
	
	@property
	def text_width(self) -> int:
		return int(TEXT_DO_WHILE_SIZE.x if self.is_do else TEXT_WHILE_SIZE.x)
	
	def as_ASTNode(self) -> ASTNodeWhile:
		return ASTNodeWhile(self.slots[0].as_AST(), self.sequences[0].as_AST(), self.is_do)
