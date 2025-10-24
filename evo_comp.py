import pygame


class Bot:
	def __init__(self, toggle_key=pygame.K_b):
		self.enabled = False
		self.toggle_key = toggle_key
		self.last_toggle_time = 0
		self.toggle_delay = 300  # ms debounce for toggle

	def get_input(self, game_logic):
		# Read current keyboard state for toggle handling
		real_keys = pygame.key.get_pressed()
		current_time = pygame.time.get_ticks()

		# Toggle bot when user presses the toggle key (debounced)
		if real_keys[self.toggle_key] and current_time - self.last_toggle_time > self.toggle_delay:
			self.enabled = not self.enabled
			#print(f"Bot enabled: {self.enabled}")
			self.last_toggle_time = current_time

		# If bot is off, just return the real input so the user can start the game
		if not self.enabled:
			return {
				'keys': real_keys,
				'mouse_pos': pygame.mouse.get_pos(),
				'mouse_buttons': pygame.mouse.get_pressed()
			}

		# Build a mutable copy of the keys state and clear movement keys
		keys_list = list(real_keys)
		for k in (pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s):
			try:
				keys_list[k] = False
			except IndexError:
				# Safety: if key index is out of range, ignore (unlikely)
				pass

		# Locate apple on the grid
		apple_pos = None
		for y, row in enumerate(game_logic.grid):
			for x, cell in enumerate(row):
				if cell.apple:
					apple_pos = (x, y)
					break
			if apple_pos:
				break

		# If no apple, don't press movement keys (game will spawn one shortly)
		if not apple_pos:
			return {
				'keys': tuple(keys_list),
				'mouse_pos': pygame.mouse.get_pos(),
				'mouse_buttons': pygame.mouse.get_pressed()
			}

		head = game_logic.snake[0]
		last_action = game_logic.last_action

		# Candidate moves: key -> vector
		moves = {
			pygame.K_a: (-1, 0),
			pygame.K_d: (1, 0),
			pygame.K_w: (0, -1),
			pygame.K_s: (0, 1)
		}

		def is_reverse(vec):
			return last_action is not None and (vec[0] == -last_action[0] and vec[1] == -last_action[1])

		candidates = []
		for key, vec in moves.items():
			if is_reverse(vec):
				continue
			new_pos = (head[0] + vec[0], head[1] + vec[1])
			nx, ny = new_pos
			# Basic bounds check (grid contains walls but be safe)
			if ny < 0 or ny >= len(game_logic.grid) or nx < 0 or nx >= len(game_logic.grid[0]):
				continue
			cell = game_logic.grid[ny][nx]
			safe = not (cell.wall or cell.snake)
			manhattan = abs(nx - apple_pos[0]) + abs(ny - apple_pos[1])
			candidates.append((safe, manhattan, key))

		# Prefer safe moves that minimize distance
		candidates.sort(key=lambda t: (0 if t[0] else 1, t[1]))

		chosen_key = None
		if candidates:
			chosen_key = candidates[0][2]

		if chosen_key is not None:
			try:
				keys_list[chosen_key] = True
			except IndexError:
				pass

		return {
			'keys': tuple(keys_list),
			'mouse_pos': pygame.mouse.get_pos(),
			'mouse_buttons': pygame.mouse.get_pressed()
		}


if __name__ == "__main__":
	print("evo_comp.Bot: import this module and call Bot().get_input(game_logic) each frame.")