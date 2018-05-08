def get_index(syms):
	for s in syms.get_index(2): # index 2 is sorted by name
		if s[2] != True:
			continue # Skip symbols that don't want to appear in the index
		yield {
			'name': s[1],
			'address': s[0]
		}
