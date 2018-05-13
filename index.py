def get_index(ctx):
	for s in ctx.syms.sorted_name:
		if s[2] != True:
			continue # Skip symbols that don't want to appear in the index
		ctx.link_sources.add(s[0])
		yield {
			'name': s[1],
			'address': s[0]
		}
