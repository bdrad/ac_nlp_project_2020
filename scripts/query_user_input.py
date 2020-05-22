## Get query input from user to feed into algorithm

def get_user_input():
	query = input('\nPatient Clnical History:')
	print('Press enter to skip')
	q_age = input('\tPatient Age:\t')
	if q_age == '':
		q_age = None
	else:
		q_age = int(q_age)
	
	q_sex = str.lower(input('\tPatient Sex:\t'))
	if q_sex == '':
		q_sex = None
	
	q_bodypart = str.lower(input('\tBody Part:\t'))
	while q_bodypart not in ['head','spine','chest','abdomen','musculoskeletal','other','']:
		print('Invalid body part entered! Please choose from: head/spine/chest/abdomen/musculoskeletal/other')
		q_bodypart = str.lower(input('\tBody Part:\t'))
	if q_bodypart == '':
		q_bodypart = None
	
	return [query, q_age, q_sex, q_bodypart]

# Method to process batch queries
# There are slightly different classificaitons for "body part" in this method
def process_input(each_query):
	[query, q_age, q_sex, q_bodypart] = each_query

	if q_age == '':
		q_age = None
	else:
		q_age = float(q_age)
	
	q_sex = str.lower(q_sex)
	if q_sex == '':
		q_sex = None
	
	q_bodypart = str.lower(q_bodypart)
	if q_bodypart not in ['head','spine','chest','abdomen/pelvis','extremity','other']:
		q_bodypart = ''

	if q_bodypart == '':
		q_bodypart = None
	
	return [query, q_age, q_sex, q_bodypart]