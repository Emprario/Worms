"""
Outil de debug divers
"""


def have_duplicated_obj_in_list(master: list[list]) -> bool:
    """Returns true if there are duplicated objects"""
    lisflat = [obj for lsobj in master for obj in lsobj]
    setflat = set(lisflat)
    return len(setflat) != len(lisflat)
