import random, sqlite3, os

players = []
bunker = []
spec_cards = []

area = random.randint(30, 100)
time_of_life = random.randint(4, 36)

def main():
	print('\n1. Создать карточки\n\n2. Заменить здоровье\n\n3. Заменить фобию\n\n4. Заменить хобби\n\n5. Заменить Профессию')
	print('\n6. Заменить черту характера\n\n7. Заменить багаж\n\n8. Заменить доп инфу\n\n9. Заменить биологическую характеристику')
	print('\n10. Правила\n')
	choice = int(input())
	if (choice == 1):
		print('Введите кол-во игроков:')
		amount_of_players = int(input())
		if (amount_of_players <= 0 or amount_of_players > 16):
			print('Неверное кол-во игроков(0 < Кол-во <= 16')
			main()
		Create_cards(amount_of_players)
	elif (choice == 2):
		change_stat('health')
	elif (choice == 3):
		change_stat('phobies')
	elif (choice == 4):
		change_stat('hobbies')
	elif (choice == 5):
		print(get_stat('professions'))
		main()
	elif (choice == 6):
		change_stat('psychosis')
	elif (choice == 7):
		change_stat('baggage')
	elif (choice == 8):
		change_stat('dop_info')
	elif (choice == 9):
		file = open('stat.txt', 'w')
		file.write(write_sex())
		file.close()
		print('\nDone')
	elif (choice == 10):
		print('https://vk.com/topic-196140718_41352139\n')

class player:
	def __init__(self, prof, hobbi, phobia, health, dop_info, psycho, spec_card, baggage):
		self.prof = prof
		self.hobbi = hobbi
		self.phobia = phobia
		self.health = health
		self.dop_info = dop_info
		self.psycho = psycho
		self.spec_card = spec_card
		self.baggage = baggage

def create_player(player, number, catastrophe, bunker):
	file = open(str(number + 1) + '.txt', 'w')
	file.write('Катастрофа: ' + catastrophe + '\n')
	file.write('Бункер:\tПлощадь ' + str(area) + 'кв.м\nВ бункере располагается: ' + str(bunker[0]) + ', ' + str(bunker[1]) + ', ' + str(bunker[2]) + '\n')
	file.write('Время пребывания в бункере: ' + str(time_of_life) + ' месяцев\n\nХарактеристики:\n')
	file.write(write_sex())
	file.write('Профессия:\t' + str(player.prof) + '\n')
	file.write('Хобби:\t' + str(player.hobbi) + '\n')
	file.write('Фобия:\t' + str(player.phobia) + '\n')
	file.write(write_health(player.health))
	file.write('Доп. информация:\t' + str(player.dop_info) + '\n')
	file.write('Человеская черта:\t' + str(player.psycho) + '\n')
	file.write('Багаж:\t' + str(player.baggage) + '\n')
	file.write('Карты действий:\n1)\t' + str(player.spec_card[0]) + '\n2)\t' + str(player.spec_card[1]) + '\n')
	file.close()

def Create_cards(amount_of_players):
	catastrophe = get_stat('catastrophes')
	
	bunker.append(get_stat('bunkers'))
	bunker.append(check_bunker(get_stat('bunkers')))
	bunker.append(check_bunker(get_stat('bunkers')))

	for i in range(0, amount_of_players):
		prof = get_stat('professions')
		dop_info = get_stat('dop_info')
		health = get_stat('health')
		hobbies = get_stat('hobbies')
		psychosis = get_stat('psychosis')

		spec_cards.append(get_stat('spec_cards'))
		spec_cards.append(get_stat('spec_cards'))
		if ((spec_cards[0] == spec_cards[1]) or ('Карта' in spec_cards[0] and 'Карта' in spec_cards[1])):
			while (spec_cards[0] == spec_cards[1] or ('Карта' in spec_cards[0] and 'Карта' in spec_cards[1])):
				spec_cards.pop()
				spec_cards.append(get_stat('spec_cards'))

		phobies = get_stat('phobies')
		baggage = get_stat('baggage')

		players.append(player(prof, hobbies, phobies, health, dop_info, psychosis, spec_cards, baggage))
		create_player(players[i], i, catastrophe, bunker)

	bunker.clear()
	players.clear()
	players.clear()
	spec_cards.clear()
	print('Done!')
	main()

def check_bunker(stat) -> str:
	flag = False
	for i in bunker:
		if (i == stat):
			stat = check_bunker(get_stat('bunkers'))
		else:
			flag = True
	return stat

def get_stat(stat) -> str:
	conn = sqlite3.connect('Base.db')
	cursor = conn.cursor()

	cursor.execute("SELECT " + stat[:-1] + " FROM " + stat)
	index = random.randint(0, len(cursor.fetchall())) - 1
	cursor.execute("SELECT " + stat[:-1] + " FROM " + stat)
	temp_stat = str(cursor.fetchall()[index])[2:-3]

	conn.close()
	return temp_stat

def change_stat(stat):
	file = open(str(stat) + '.txt', 'w')
	file.write(get_stat(stat))
	file.close()
	print('Done\nСоздан файл ' + stat)
	main()

def check_connection():
	conn = sqlite3.connect('Base.db')
	cursor = conn.cursor()
	try:
		cursor.execute("SELECT catastrophe FROM catastrophes")
		conn.close()
		print('===========Ошибок с БД не обнаруженно===========\n')
	except sqlite3.OperationalError:
		print('!!Отсутствует БД!!')
		conn.close()
		os.system('del Base.db')
		exit(0)

def write_sex() -> str:
	stat = 'Пол и возраст: '
	if (random.randint(0, 1)):
		stat += 'Мужщина, '
	else:
		stat += 'Женщина, '
	if (random.randint(0, 10) > 3):
		stat += str(random.randint(18, 49))
	else:
		stat += str(random.randint(50, 80))
	if (random.randint(0, 10) > 3):
		stat += '\n'
	else:
		stat += ' childfree\n'
	return stat

def write_health(health) -> str:
	stat = 'Состояние здоровья: ' + health
	if (health != 'Идеально здоров'):
		stat += ' ' + str(random.randint(0, 100)) + '%\n'
	return stat


if __name__ == '__main__':
	check_connection()
	main()