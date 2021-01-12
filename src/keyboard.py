import math

class KeyboardLayout():
  def __init__(self, keys: list):
    self.keys = keys
    self.key_map = {}

    # create character map
    for row in range(len(keys)):
      for column in range(len(keys[row])):
        char = keys[row][column]
        self.key_map[char] = [column, row]

  def get_char_pos(self, char: str) -> [int, int]:
    # char to upper case
    char = char.upper()
    # find char in keys
    if not char in self.key_map:
      return -1, -1
    
    return self.key_map[char]

  def get_char_distance(self, a: str, b: str) -> float:
    pos_a = self.get_char_pos(a)
    if pos_a[0] == -1:
      return -1

    pos_b = self.get_char_pos(b)
    if  pos_b[0] == -1:
      return -1

    distance_a = abs(pos_a[0] - pos_b[0])
    distance_b = abs(pos_a[1] - pos_b[1])

    return math.sqrt((distance_a*distance_a) + (distance_b*distance_b))

  def get_word_distance(self, a: str, b: str) -> float:
    if len(a) != len(b):
      return -1

    distance: float = 0
    
    for i in range(len(a)):
      char_a = a[i]
      char_b = b[i]
      if char_a == char_b:
        continue
      char_distance = self.get_char_distance(char_a, char_b)
      if char_distance != -1:
        distance += char_distance
    
    return distance