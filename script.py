with open('wikipedia_programming_languages.txt') as wpl:
  text_arr=wpl.readlines()
is_alphanum='0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
CategoryE=int
CategoryDict=dict[str:CategoryE]
CategoryDictRev=dict[CategoryE:str]
LanguageCategories=dict[str:list[CategoryE]]
categories:CategoryDict={} #As Enum dictionary
categories_rev:CategoryDictRev={} #Enum -> str
language_types:LanguageCategories={} #A language may have multiple categories
def add_language(line:str,first_i:int,categories:CategoryDict,language_types:LanguageCategories,last_category:CategoryE) -> int:
  last_i=line.index(']]',first_i)
  new_first_i=None #Not none if | is found
  try: new_first_i=line.index("|",first_i)
  except: pass
  if new_first_i:
    language=line[new_first_i+1:last_i]
  else:
    language=line[first_i+2:last_i]
  if not categories.get(language):
    if list_exist:=language_types.get(language):
      if list_exist[-1]!=last_category:
        list_exist.append(last_category)
    else:
      language_types[language]=[last_category]
  return len(line[first_i:last_i+2]) #Skip all characters after ']]'
def parse_wiki(text_arr,categories:CategoryDict,categories_rev:CategoryDictRev,language_types:LanguageCategories):
  last_category:CategoryE|None=None
  for line in text_arr:
    if line.startswith("== "):
      maybe_category=line[3:line.index(" ==")] #Extract the category surrounding '== ' and ' =='
      if "language" not in maybe_category and "Language" not in maybe_category:
        last_category=None
        continue
      last_category=len(categories)
      categories[maybe_category]=last_category
    elif line[0]=='*':
      if not last_category: continue #Don't read lines without proper Category
      first_i=1
      while line[first_i]=='*':
        first_i=first_i+1
      first_i=first_i+1
      if line[first_i] in is_alphanum:
        print("Next line at",line[first_i])
        while line[first_i]!='\n':
          if line[first_i]=='[' and line[first_i+1]=='[':
            first_i += add_language(line,first_i,categories,language_types,last_category)
          else:
            first_i += 1
      else:
        if line[first_i]=='{': continue #The only line that contained '* {'
        while line[first_i]!='\n':
          if line[first_i]=='[' and line[first_i+1]=='[':
            first_i += add_language(line,first_i,categories,language_types,last_category)
          else:
            first_i += 1
  for k,v in categories.items(): categories_rev[v]=k
parse_wiki(text_arr,categories,categories_rev,language_types)
print(language_types)