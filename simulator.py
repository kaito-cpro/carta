from collections import defaultdict
from colorama import init, Fore, Back, Style
import random
import copy

path = 'distribution.txt'
init()  # colorama initialization

cards = ['む', 'す', 'め', 'ふ', 'さ', 'ほ', 'せ',
         'うか', 'うら', 'つき', 'つく', 'しら', 'しの', 'もも', 'もろ', 'ゆう', 'ゆら',
         'いに', 'いまは', 'いまこ', 'ちは', 'ちぎりお', 'ちぎりき', 'ひさ', 'ひとは', 'ひとも', 'きり', 'きみがためお', 'きみがためは',
         'はなさ', 'はなの', 'はるす', 'はるの', 'やえ', 'やす', 'やまが', 'やまざ', 'よを', 'よも', 'よのなかは', 'よのなかよ', 'かく', 'かさ', 'かぜを', 'かぜそ',
         'みせ', 'みち', 'みよ', 'みかき', 'みかの',
         'たか', 'たき', 'たご', 'たち', 'たま', 'たれ',
         'こい', 'こぬ', 'この', 'これ', 'こころあ', 'こころに',
         'おく', 'おぐ', 'おと', 'おも', 'おおえ', 'おおけ', 'おおこ', 
         'なつ', 'ながか', 'ながら', 'なげき', 'なげけ', 'なにし', 'なにわえ', 'なにわが',
         'わび', 'わすら', 'わすれ', 'わがい', 'わがそ', 'わたのはらこ', 'わたのはらや',
         'あい', 'あけ', 'あし', 'あきか', 'あきの', 'あまつ', 'あまの', 'あわじ', 'あわれ', 'ありあ', 'ありま', 'あらし', 'あらざ', 'あさじ', 'あさぼらけあ', 'あさぼらけう']
pos = ['左上段', '左中段', '左下段', '右上段', '右中段', '右下段', '未配置']

def _colourize(card, color):
    if color == False:
        return ''
    c = ''
    if len(card) == 1:
        c = Fore.LIGHTYELLOW_EX
    if len(card) == 2:
        c = Fore.LIGHTGREEN_EX
    if len(card) == 3:
        c = Fore.LIGHTCYAN_EX
    if len(card) == 4:
        c = Fore.LIGHTMAGENTA_EX
    if len(card) >= 5:
        c = Fore.LIGHTRED_EX
    if card[0] in ['う', 'つ', 'し', 'も', 'ゆ']:
        c += Back.LIGHTBLACK_EX
    if card[0] == 'た':
        c = Fore.LIGHTYELLOW_EX + Back.LIGHTBLACK_EX
    if card in ['いに', 'ちは', 'ひさ', 'きり', 'こぬ', 'おと']:
        c += Back.BLUE
    return c

def load():
    f = open(path, 'r', encoding='utf-8')
    content = f.read().split('\n')
    for i in range(min(len(grid), len(content))):
        grid[i] = content[i].split()
    f.close()

def init():
    f = open(path, 'w', encoding='utf-8')
    for i in range(6):
        f.write('\n')
    for card in cards:
        f.write(card + ' ')
    f.close()

def remove(card):
    if card not in cards:
        print(Back.RED + f'Error: {card} is not valid' + Back.RESET)
        return
    load()
    f = open(path, 'r', encoding='utf-8')
    content = f.read().split('\n')
    f.close()
    for i in range(len(content)):
        content[i] = content[i].split()
        if card in content[i]:
            content[i].remove(card)
    if len(content) < 7:
        content.append([card])
    else:
        content[6].append(card)
    f = open(path, 'w', encoding='utf-8')
    for i in range(7):
        for j in range(len(content[i])):
            f.write(content[i][j] + ' ')
        f.write('\n')
    f.close()
    check()
    return

def set(col, idx, card):
    if not 0 <= col < 6:
        print(Back.RED + f'Error: invalid column' + Back.RESET)
        return
    if card not in cards:
        print(Back.RED + f'Error: {card} is not valid' + Back.RESET)
        return
    load()
    f = open(path, 'r', encoding='utf-8')
    content = f.read().split('\n')
    f.close()
    for i in range(len(content)):
        content[i] = content[i].split()
        if card in content[i]:
            content[i].remove(card)
    if not idx <= len(content[col]):
        print(Back.RED + f'Error: invalid index' + Back.RESET)
        return
    content[col].insert(idx, card)
    f = open(path, 'w', encoding='utf-8')
    for i in range(7):
        for j in range(len(content[i])):
            f.write(content[i][j] + ' ')
        f.write('\n')
    f.close()
    check()
    return    
    
def show(color=True, width=43):
    check()
    print(' ' * 3 + '▽'.center(width, '　'))
    height = 7
    for i in range(3 * height):
        col = i // height  # 0 or 1 or 2
        print(str(len(grid[col])).ljust(3, ' ') if i % height == 0 else ' ' * 3, end='')
        for j in range(width):
            if j < len(grid[col]) and i % height < len(grid[col][j]):
                c = _colourize(grid[col][j], color)
                print(c + grid[col][j][i % height] + Back.RESET + Fore.RESET + Style.RESET_ALL, end='')
            elif j >= width - len(grid[col + 3]) and i % height < len(grid[col + 3][j - width + len(grid[col + 3])]):
                c = _colourize(grid[col + 3][j - width + len(grid[col + 3])], color)
                print(c + grid[col + 3][j - width + len(grid[col + 3])][i % height] + Back.RESET + Fore.RESET + Style.RESET_ALL, end='')
            else:
                print('　', end='')
        print(str(len(grid[col + 3])).rjust(3, ' ') if i % height == 0 else ' ' * 3)
    print(' ' * 3 + '△'.center(width, '　'))
    print('未配置: [', end='')
    for card in grid[6]:
        c = _colourize(card, color)
        print(c + card + Back.RESET + Fore.RESET + Style.RESET_ALL + ', ', end='')
    print(('\b\b' if len(grid[6]) else '') + ']')
    return

def random_show(color=True, width=29):
    load()
    if len(grid[6]) > 75:
        print(Back.RED + f'Error: grid has not enough cards' + Back.RESET)
        return
    rem_cards = copy.deepcopy(cards)
    dump_cards = []
    for card in grid[6]:
        rem_cards.remove(card)
        dump_cards.append(card)
    dump_cards += random.sample(rem_cards, 75 - len(dump_cards))
    use_grid = copy.deepcopy(grid)
    for card in dump_cards:
        for i in range(6):
            if card in use_grid[i]:
                use_grid[i].remove(card)
                break
    print(' ' * 3 + '▽'.center(width, '　'))
    height = 7
    for i in range(3 * height):
        col = i // height  # 0 or 1 or 2
        print(str(len(use_grid[col])).ljust(3, ' ') if i % height == 0 else ' ' * 3, end='')
        for j in range(width):
            if j < len(use_grid[col]) and i % height < len(use_grid[col][j]):
                c = _colourize(use_grid[col][j], color)
                print(c + use_grid[col][j][i % height] + Back.RESET + Fore.RESET + Style.RESET_ALL, end='')
            elif j >= width - len(use_grid[col + 3]) and i % height < len(use_grid[col + 3][j - width + len(use_grid[col + 3])]):
                c = _colourize(use_grid[col + 3][j - width + len(use_grid[col + 3])], color)
                print(c + use_grid[col + 3][j - width + len(use_grid[col + 3])][i % height] + Back.RESET + Fore.RESET + Style.RESET_ALL, end='')
            else:
                print('　', end='')
        print(str(len(use_grid[col + 3])).rjust(3, ' ') if i % height == 0 else ' ' * 3)
    print(' ' * 3 + '△'.center(width, '　'))
    return

def check():  
    load()  
    cnt = 0
    dict = defaultdict(int)
    for i in range(100):
        dict[cards[i]] = 1
    ok = True
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] not in cards:
                print(Back.RED + f'Error: {grid[i][j]} is not valid ({pos[i]})' + Back.RESET)
                ok = False
            elif dict[grid[i][j]] != 1:
                print(Back.RED + f'Error: {grid[i][j]} duplicates ({pos[i]})' + Back.RESET)
                ok = False
            cnt += 1
            dict[grid[i][j]] -= 1
    if not ok:
        return False
    if cnt != 100:
        print(Back.RED + f'Error: {cnt} cards are given' + Back.RESET)
        if cnt < 100:
            for key, val in dict.items():
                if val != 0:
                    print(Back.RED + f'{key} does not exist' + Back.RESET)
        return False
    return True

grid = [[] for _ in range(7)]
load()