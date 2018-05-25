def has_index(ctx):
	return len(ctx.syms.sorted_name)>0 # Not really good enough, but will do for now (what about 'al' syms?)

def get_index(ctx):
	for s in ctx.syms.sorted_name:
		if not s[2]:
			continue # skip symbols that don't want to appear in the index
		if not ctx.is_destination(s[0]):
			continue # skip if we've got nothing to link to
		ctx.link_add_referenced(s[0]) # reference so the anchor is generated
		yield {
			'name': s[1],
			'address': s[0]
		}
