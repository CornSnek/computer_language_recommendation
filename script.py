import math
with open('wikipedia_programming_languages.txt') as wpl:
  text_arr=wpl.readlines()
is_alphanum='0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
CategoryE=int
CategoryDict=dict[str:CategoryE]
CategoryDictRev=list[str]
LanguageCategories=dict[str:list[CategoryE]]
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
def main():
  categories:CategoryDict={} #As Enum dictionary
  categories_rev:CategoryDictRev={} #Enum -> str
  language_types:LanguageCategories={} #A language may have multiple categories
  parse_wiki(text_arr,categories,categories_rev,language_types)
  while True:
    input_c=input(
"""Usage: Search programming languages based on their category or by name.
  e to exit the program
  c to search by language category
  l to search by language name
>>> """)
    if input_c not in "ecl": continue
    if input_c=='e':
      print("Goodbye!")
      break
    elif input_c=='c': search_by_category(categories,categories_rev,language_types)
    elif input_c=='l': raise NotImplementedError("TODO")
def all_false(arr):
  all_is_false=False
  for v in arr:
    if v==True: break
  else: all_is_false=True
  return all_is_false
def binary_search(sorted_arr,value) -> int|None:
  left=0
  right=len(sorted_arr)-1
  while left!=right:
    middle=math.ceil((left+right)/2)
    if(sorted_arr[middle]>value): right=middle-1
    else: left=middle
  if sorted_arr[left]==value: return left
  return None
def search_by_category(categories:CategoryDict,categories_rev:CategoryDictRev,language_types:LanguageCategories):
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
        print(using_categories_list)
        for language,lc in language_types.items():
          for e in using_categories_list:
            if binary_search(lc,e)==None: break
          else: matched_languages.append(language) #If a language has all categories mentioned in using_categories, append
        print("Recommended language(s) for you based on the enabled categories:")
        for ml in matched_languages:
          print(ml)
        if not matched_languages: print("(None. A language does not have all of these categories.)")
    else:
      searching_categories=[]
      for k,v in categories.items():
        if input_str in k:
          searching_categories.append(v)
      print(f"Searching {len(searching_categories)} category/categories")
      if len(searching_categories)==1:
        toggle_category=searching_categories[0]
        print(f"Toggling '{categories_rev[toggle_category]}' to {not using_categories[toggle_category]}")
        using_categories[toggle_category]=not using_categories[toggle_category]
      else:
        for e in searching_categories:
          print(categories_rev[e])
if __name__ == '__main__':
  main()