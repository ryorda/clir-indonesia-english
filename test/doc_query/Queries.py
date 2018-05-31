import re

class Queries : 
	def __init__(self, lang) :
		queries = open('queries/CLIR-%s-06.txt' % lang, 'r', encoding="latin-1", errors='ignore')
		self.titles = []
		self.descs = []
		self.narrs = []
		self.idx = -1

		regex_title = re.compile('</?%s-title>' % lang)
		regex_desc = re.compile('</?%s-desc>' % lang)
		regex_narr = re.compile('</?%s-narr>' % lang)

		for q in queries :
			if '<%s-title>' % lang in q :
				q = regex_title.sub('', q.strip()).strip()
				self.titles.append(q)
			elif '<%s-desc>' % lang in q :
				q = regex_desc.sub('', q.strip()).strip()
				self.descs.append(q)
			elif '<%s-narr>' % lang in q :
				q = regex_narr.sub('', q.strip()).strip()
				self.narrs.append(q)

		self.titles_len = len(self.titles)
		self.descs_len = len(self.descs)
		self.narrs_len = len(self.narrs)

		self.title = None
		self.desc = None
		self.narr = None

	def hasnext(self) :
		return min(self.titles_len, self.descs_len, self.narrs_len) > self.idx + 1

	def next(self) :
		self.idx += 1
		self.title = self.titles[self.idx]
		self.desc = self.descs[self.idx]
		self.narr = self.narrs[self.idx]
