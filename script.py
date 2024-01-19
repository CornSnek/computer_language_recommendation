from utils import all_false,binary_search,kmp_exists,AlphabeticalHeapSortContext,add_as_heap,pop_as_heap
with open('wikipedia_programming_languages.txt') as wpl:
  text_arr=wpl.readlines()
is_alphanum='0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
CategoryE=int
CategoryDict=dict[str:CategoryE]
CategoryDictRev=list[str]
LanguageCategories=dict[str:list[CategoryE]]
def add_language(line:str,first_i:int,categories:CategoryDict,language_types:LanguageCategories,last_category:CategoryE,language_blacklist:set[str]) -> int:
  """Returns int that retrurns characters to skip after ']]'"""
  last_i=line.index(']]',first_i)
  new_first_i=None #Not none if | is found
  try: new_first_i=line.index("|",first_i)
  except: pass
  if new_first_i:
    language=line[new_first_i+1:last_i]
  else:
    language=line[first_i+2:last_i]
  if not categories.get(language) and language not in language_blacklist:
    if list_exist:=language_types.get(language):
      if list_exist[-1]!=last_category: #Don't add the same number.
        list_exist.append(last_category)
    else:
      language_types[language]=[last_category]
  return len(line[first_i:last_i+2])
def parse_wiki(text_arr,categories:CategoryDict,categories_rev:CategoryDictRev,language_types:LanguageCategories,language_blacklist:set[str],language_table:list[str]):
  last_category:CategoryE|None=None
  is_systems=False
  for line in text_arr:
    if line.startswith("== "):
      maybe_category=line[3:line.index(" ==")] #Extract the category surrounding '== ' and ' =='
      if "language" not in maybe_category and "Language" not in maybe_category:
        last_category=None
        continue
      if maybe_category=="System languages": is_systems=True
      last_category=len(categories)
      categories[maybe_category]=last_category
    if not is_systems and line[0]=='*':
      if not last_category: continue #Don't read lines without proper Category
      first_i=1
      while line[first_i]=='*':
        first_i=first_i+1
      first_i=first_i+1
      if line[first_i] in is_alphanum:
        while line[first_i]!='\n':
          if line[first_i:first_i+2]=='[[':
            first_i += add_language(line,first_i,categories,language_types,last_category,language_blacklist)
          else:
            first_i += 1 #Keep searching for a '[['
      else:
        if line[first_i]=='{': continue #The only line that contained '* {'
        while line[first_i]!='\n':
          if line[first_i:first_i+2]=='[[':
            first_i += add_language(line,first_i,categories,language_types,last_category,language_blacklist)
          else:
            first_i += 1
    elif is_systems and line[0:2]=='| ':
      first_i=2
      while line[first_i]!='\n':
        if line[first_i:first_i+2]=='[[':
          first_i += add_language(line,first_i,categories,language_types,last_category,language_blacklist)
        else:
          first_i+=1
  for k,v in categories.items(): categories_rev[v]=k
  ahs_context=AlphabeticalHeapSortContext() #Sort considering a-z and A-Z as equal
  heap_language_table=[]
  for language in language_types.keys():
    add_as_heap(heap_language_table,language,ahs_context,True)
  while len(heap_language_table)!=0:
    language_table.append(pop_as_heap(heap_language_table,ahs_context,check_if_still_heap=True))
def search_by_category(categories:CategoryDict,categories_rev:CategoryDictRev,language_types:LanguageCategories,use_case:bool):
  using_categories=[False for _ in range(len(categories))]
  while True:
    print("Current categories enabled: ")
    for e in range(len(using_categories)):
      if using_categories[e]: print(categories_rev[e])
    if(all_false(using_categories)): print("(None)")
    input_str=input("What language category do you want to search for? Type 'exit' to exit or 'done' to see the recommended languages for the project >>> ")
    if input_str=='exit':
      return
    elif input_str=='done':
      if all_false(using_categories):
        print("At least 1 or more categories must be enabled to see recommended languages.")
      else:
        matched_languages=[]
        using_categories_list=[e for e,b in enumerate(using_categories) if b] #Get enums that are True only
        for language,lc in language_types.items():
          for e in using_categories_list:
            if binary_search(lc,e)==None: break
          else: matched_languages.append(language) #If a language has all categories mentioned in using_categories, append
        print("Recommended language(s) for you based on the enabled categories:")
        for ml in matched_languages:
          print(ml)
        if not matched_languages: print("(None. No language has all of these categories.)")
    else:
      searching_categories=[]
      for c,e in categories.items():
        if input_str in (c if use_case else c.lower()):
          searching_categories.append(e)
      print(f"Searching {len(searching_categories)} category/categories")
      if len(searching_categories)==1:
        toggle_category=searching_categories[0]
        print(f"Toggling '{categories_rev[toggle_category]}' to {not using_categories[toggle_category]}")
        using_categories[toggle_category]=not using_categories[toggle_category]
      else:
        for e in searching_categories:
          print(categories_rev[e])
def search_by_language(use_case:bool,language_table:list[str]):
  while True:
    language_searched=[]
    input_str=input("What language name do you want to search for? Type 'exit' to exit >>> ")
    for language in language_table:
      if kmp_exists(language,input_str,use_case): language_searched.append(language)
    print(f"Found {len(language_searched)} language/languages")
    for language in language_searched: print(language)
    if input_str=='exit': return
def main():
  categories:CategoryDict={} #As Enum dictionary
  categories_rev:CategoryDictRev={} #Enum -> str
  language_blacklist:set[str]=set([
    "AutoCAD","CA-DATACOM/DB","Unisys/Sperry","Sterling/Informatics","optimization","scheduling","cross-platform","Horn logic","logical resolution",
    "32-bit","64-bit","18-bit","12-bit","36-bit","16-bit:","16-bit x86","8-bit",
  ]) #Some links are not languages.
  language_types:LanguageCategories={} #A language may have multiple categories
  language_table:list[str]=[]
  use_case=True
  parse_wiki(text_arr,categories,categories_rev,language_types,language_blacklist,language_table)
  while True:
    input_c=input(
f"""Usage: Search programming languages based on their category or by name.
  e to exit the program
  c to search by language category
  a to see all category names
  l to search by language name
  s to toggle case-sensitivity (Currently {use_case})
>>> """)
    if input_c not in "aecls": continue
    if input_c=='a':
      print('\n'.join(c for c in categories.keys()))
    elif input_c=='e':
      print("Goodbye!")
      break
    elif input_c=='c': search_by_category(categories,categories_rev,language_types,use_case)
    elif input_c=='l': search_by_language(use_case,language_table)
    else: use_case=not use_case
if __name__ == '__main__':
  main()