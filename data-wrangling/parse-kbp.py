import csv


'''
todo:
	[ ] when multiple victims die in same incident, kbp puts them all in one row -_- deal with that

'''

def read_file(filename):
	f = open(filename,'r')
	data = f.read()
	f.close()
	return data

def write_answer2(answer,filename='output.txt'):
	f = open(filename,'w')
	# f.write(answer)
	# for line in answer:
	# 	for col in line:
	# 		f.write(col)
	# 		f.write('\n')
	# 	f.write('\n\n')
	line = ''
	for x in range(len(answer)):
	    for y in answer[x]:
	    	line = y + '\t: '+answer[x][y]+'\n'
	        f.write(line)
	    f.write('=============================================\n')
	f.close()
def write_answer(answer,filename='output.csv'):
	'''
		row_profile['date'] = date
		row_profile['number'] = number
		row_profile['name'] = name
		row_profile['age'] = age
		row_profile['img'] = img
		row_profile['state'] = row[2]
		row_profile['g/r'] = row[3]
		row_profile['how'] = row[5]
		row_profile['kbp_link'] = get_url(row[6])
		row_profile['news_link_text'] = get_url(row[7])
	'''

	with open(filename, 'w') as csvfile:
	    fieldnames = ['number', 'date', 'state','g/r','g','r','name','img','age','how','kbp_link','news_link_text']
	    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

	    writer.writeheader()
	    for row in answer:
	    	writer.writerow(row)
	    

def break_into_table(data):
	rows = data.split('<tr>')
	table = []
	for r in rows:
		table.append(r.split('<td>'))
	return table

def get_url(foo):
	foo = foo.lstrip('<a href=').split('>')[0]
	return foo

def parse_name_col(cell):
	# return img, name, age
	cell.strip()

	age = ''
	name = ''
	img = ''
	if len(cell) < 3:
		return 'unknown','unknown','unknown'

	if cell.count(', ') == 0:
		age = 'unknown'
	else:
		age = cell.split(', ')[1]	

	if cell.startswith('<'):
		foo = cell.lstrip('<a href=').split('>')
		img = foo[0]
		name = foo[1].split(', ')[0] 
	else:
		name = cell.split(', ')[0] 

	return img.strip(),name.strip(),age.strip()

def parse_gr(cell):
	# return g, r
	if cell.count('/') > 0:
		return cell.split('/')[0], cell.split('/')[1]

	return cell.strip(), 'unknown'	
def parse_date_col(cell):
	# return number, date
	number = ''
	date = ''

	if cell.startswith('('):
		date = cell.split(') ')[1]
		number = cell.split(') ')[0].lstrip('(')
		return number, date

	return number, date

def row_to_dict(row):
	row_profile = {}

	# todo what if ') ' isnt there?
	number, date = parse_date_col(row[1])
	row_profile['date'] = date
	row_profile['number'] = number

	img, name, age = parse_name_col(row[4])
	row_profile['name'] = name
	row_profile['age'] = age
	row_profile['img'] = img


	row_profile['state'] = row[2]
	row_profile['g/r'] = row[3]
	row_profile['g'],row_profile['r'] = parse_gr(row[3])
	row_profile['how'] = row[5]
	row_profile['kbp_link'] = get_url(row[6])
	row_profile['news_link_text'] = get_url(row[7])


	return row_profile

def make_answer(table):
	ans = []
	for r in table:
		if len(r) < 3:
			continue
		ans.append(row_to_dict(r))
	return ans

dump_truck = read_file('kbp.txt')
tbl = break_into_table(dump_truck)
answer = make_answer(tbl)
write_answer(answer)