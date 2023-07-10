from typing import List, Tuple, Any


def find_sibling_pairs(ids: list) -> list[tuple[Any, Any]]:
  sibling_pairs = []
  id_dict = {}

  for id_str in ids:
    # Extract the last digit from the ID
    print(id_str)
    last_digit = id_str.split('_')[-1]

    # Check if the last d igit is already in the dictionary
    if last_digit in id_dict:
      # Append the current ID and the sibling ID to the sibling_pairs list
      sibling_pairs.append((id_str, id_dict[last_digit]))
    else:
      # Add the current ID to the dictionary with the last digit as the key
      id_dict[last_digit] = id_str

  return sibling_pairs
