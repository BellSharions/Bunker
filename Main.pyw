import PySimpleGUI as gui
from Bunker import *

layout = [
	[gui.Text('Введите кол-во игроков:'), gui.InputText(), gui.Button('Создать карточки')],
	[gui.Button('Заменить здоровье'), 
		gui.Button('Заменить фобию'), 
		gui.Button('Заменить хобби'), 
		gui.Button('Заменить профессию'),
		gui.Button('Заменить телосложение')],
	[gui.Button('Заменить черту характера'),
		gui.Button('Заменить багаж'),
		gui.Button('Заменить доп инфу'),
		gui.Button('Заменить биологическую характеристику')],
	[gui.Output(size = (95, 20))]
]

window = gui.Window('"Bunker" Game', layout)

def main(base):
	if (not base):
		download_data_base()
	while True:
		event, values = window.read()

		if event == gui.WIN_CLOSED:
			break

		if event in ('Создать карточки'):
			try:
				amount = int(values[0])
				Create_cards(amount)
			except:
				print('Вы ввели неверное значение кол-ва игроков (0 < кол-во <= 16')

		if event in ('Заменить здоровье'):
			change_stat('health')

		if event in ('Заменить фобию'):
			change_stat('phobies')

		if event in ('Заменить хобби'):
			change_stat('hobbies')

		if event in ('Заменить телосложение'):
			file = open('body_type.txt', 'w')
			file.write(write_body_type())
			file.close()
			print('Создан файл: body_type.txt')

		if event in ('Заменить профессию'):
			print('Новая профессия:\t' + get_stat('professions'))

		if event in ('Заменить черту характера'):
			change_stat('psychosis')

		if event in ('Заменить багаж'):
			change_stat('baggage')

		if event in ('Заменить доп инфу'):
			change_stat('dop_info')
			
		if event in ('Заменить биологическую характеристику'):
			file = open('stat.txt', 'w')
			file.write(write_sex())
			file.close()
			print('Создан файл: stat.txt')

if __name__ == '__main__':
	if (not check_connetion()):
		main(base = False)
	main(base = True)