def get_index(ctx):
	for s in ctx.syms.sorted_name:
		if not s[2]:
			continue # skip symbols that don't want to appear in the index
		if not s[0] in ctx.link_destinations:
			continue # skip if we've got nothing to link to
		ctx.add_link_source(s[0]) # reference so the anchor is generated
		yield {
			'name': s[1],
			'address': s[0]
		}
