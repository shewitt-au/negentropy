def get_index(syms):
	for s in syms.sorted_name:
		if s[2] != True:
			continue # Skip symbols that don't want to appear in the index
		yield {
			'name': s[1],
			'address': s[0]
		}
