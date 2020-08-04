import random as rand, sqlite3, os, requests, progressbar as pbar
import sys

players = []
bunker = []
spec_cards = []
percents = [str(rand.randint(5, 30)), str(rand.randint(30, 80))]# [0] - Процент выжевшего населения, [1] - Процент разрушений в мире

area = rand.randint(30, 100)
time_of_life = rand.randint(4, 36)

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
	file.write('Катастрофа:\n{}\n'.format(catastrophe))
	file.write(write_info())
	file.write('\nБункер:\nПлощадь {} кв. м.\nВ бункере располагается: {}, {}, {}\n'.format(area, bunker[0], bunker[1], bunker[2]))
	file.write('Время пребывания в бункере: {} месяцев\n\nХарактеристики:\n'.format(time_of_life))
	file.write(write_sex())
	file.write(write_body_type())
	file.write('Профессия: {}\n'.format(player.prof))
	file.write('Хобби: {}\n'.format(player.hobbi))
	file.write('Фобия: {}\n'.format(player.phobia))
	file.write(write_health(player.health))
	file.write('Доп. информация: {}\n'.format(player.dop_info))
	file.write('Человеская черта: {}\n'.format(player.psycho))
	file.write('Багаж: {}\n'.format(player.baggage))
	file.write('Карты действий:\n1) {}\n2) {}\n'.format(player.spec_card[0], player.spec_card[1]))
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
		phobies = get_stat('phobies')
		baggage = get_stat('baggage')

		spec_cards.append(get_stat('spec_cards'))
		spec_cards.append(get_stat('spec_cards'))
		if ((spec_cards[0] == spec_cards[1]) or ('Карта' in spec_cards[0] and 'Карта' in spec_cards[1])):
			while (spec_cards[0] == spec_cards[1] or ('Карта' in spec_cards[0] and 'Карта' in spec_cards[1])):
				spec_cards.pop()
				spec_cards.append(get_stat('spec_cards'))

		players.append(player(prof, hobbies, phobies, health, dop_info, psychosis, spec_cards, baggage))
		create_player(players[i], i, catastrophe, bunker)

	bunker.clear()
	players.clear()
	players.clear()
	spec_cards.clear()
	print('\nКарточки располагаются в папке с программой!')

def check_bunker(stat) -> str:
	for i in bunker:
		if (i == stat):
			stat = check_bunker(get_stat('bunkers'))
	return stat

def get_stat(stat) -> str:
	conn = sqlite3.connect('Base.db')
	cursor = conn.cursor()

	cursor.execute("SELECT " + stat[:-1] + " FROM " + stat)
	index = rand.randint(0, len(cursor.fetchall())) - 1
	cursor.execute("SELECT " + stat[:-1] + " FROM " + stat)
	temp_stat = str(cursor.fetchall()[index])[2:-3]

	conn.close()
	return temp_stat

def change_stat(stat):
	file = open(str(stat) + '.txt', 'w')
	file.write(get_stat(stat))
	file.close()
	print('Создан файл: {}.txt'.format(stat))

def write_sex() -> str:
	stat = 'Пол и возраст: '
	if (rand.randint(0, 1)):
		stat += 'Мужщина, '
	else:
		stat += 'Женщина, '
	if (rand.randint(0, 10) > 3):
		age = str(rand.randint(18, 49))
		stat += age
	else:
		age = str(rand.randint(50, 80))
		stat += age
	if (rand.randint(0, 10) < 3):
		stat += ', childfree'
	stat += '. Стаж работы: '
	work_experience = int(age) - 20 - rand.randint(0, 7)
	if (work_experience > 0):
		stat += str(work_experience) + ' лет\n'
	else:
		stat += '0 лет\n'
	return stat

def write_health(health) -> str:
	stat = 'Состояние здоровья: ' + health
	if (health != 'Идеально здоров'):
		stat += ' ' + str(rand.randint(0, 100)) + '%\n'
	return stat

def write_info() -> str:
	out = 'Процент выжившего населения: ' + percents[0] + '%\n'
	out += 'Процент разрушений в мире: ' + percents[1] + '%\n'
	return out

def write_body_type() -> str:
	stat = 'Телосложение: '
	#Генерация роста
	if (rand.randint(0, 100) > 5):
		height = rand.randint(140, 190)
	else:
		height = rand.randint(190, 272)
	#Генерация роста

	#Генерация веса
	if (rand.randint(0, 100) < 70):
		weight = rand.randint(40, 85)
	elif (rand.randint(0, 100) >= 70 and rand.randint(0, 100) <= 95):
		weight = rand.randint(85, 150)
	else:
		weight = rand.randint(150, 200)
	#Генерация веса
	stat += 'рост: ' + str(height) + 'см, вес: ' + str(weight) + 'кг. '
	#Вычисление ИМТ
	IMT = (weight / (height * height)) * 10000
	if (IMT < 18.5):
		stat += 'Недостаток массы (ИМТ = ' + str(IMT) + ')\n'
	elif (IMT >= 18.5 and IMT <= 24.9):
		stat += 'Нормальный вес (ИМТ = ' + str(IMT) + ')\n'
	elif (IMT >= 25 and IMT <= 29.9):
		stat += 'Избыточный вес (ИМТ = ' + str(IMT) + ')\n'
	else:
		stat += 'Ожирение (ИМТ = ' + str(IMT) + '), нет возможности рожать\n'
	#Вычисление ИМТ
	return stat

def download_data_base():
	Base_url = 'https://github.com/KBrooMi/Bunker/raw/master/Goods/Base.db'
	bar = pbar.ProgressBar(maxval=100.0, widgets = [
		'Downloading database: ',
		pbar.Bar(left='[', right=']', marker='|')
	]).start()
	code = 0
	while (code != 200):
		bar.update()
		r = requests.get(Base_url)
		code = r.status_code
	with open('Base.db', 'wb') as f:
		f.write(r.content)
		f.close()
	bar.finish()
	return

def check_connetion() -> bool:
	conn = sqlite3.connect('Base.db')
	cursor = conn.cursor()
	try:
		cursor.execute('SELECT catastrophe FROM catastrophes')
		conn.close()
		return True
	except:
		conn.close()
		os.system('del Base.db')
		return False