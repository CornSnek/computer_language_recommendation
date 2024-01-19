import math
import unittest
import random
def all_false(arr):
  for v in arr:
    if v==True: return False
  return True
def binary_search(sorted_arr,value) -> int|None:
  left=0
  right=len(sorted_arr)-1
  while left!=right:
    middle=math.ceil((left+right)/2)
    if(sorted_arr[middle]>value): right=middle-1
    else: left=middle
  if sorted_arr[left]==value: return left
  return None
def lps_array(pattern):
  """Array of (L)ongest proper (P)refix which is also (S)uffix. For the KMP algorithm."""
  pattern_len=len(pattern)
  this_len=0
  i=1
  lps=[0]*pattern_len
  while i<pattern_len:
    if pattern[i]==pattern[this_len]:
      lps[i]=this_len+1
      this_len+=1
      i+=1
    else:
      if this_len!=0:
        this_len=lps[this_len-1]
      else:
        lps[i]=0
        i+=1
  return lps
def kmp_exists(text,pattern,case_sensitive=True):
  """True if pattern exists in text. Algorithm from https://en.wikipedia.org/wiki/Knuth-Morris-Pratt_algorithm"""
  text=text if case_sensitive else text.lower()
  pattern=pattern if case_sensitive else pattern.lower()
  text_len=len(text)
  pattern_len=len(pattern)
  lps=lps_array(pattern)
  i=0
  j=0
  while i<text_len:
    if text[i]==pattern[j]:
      i+=1
      j+=1
      if j==pattern_len:
        return True
    else:
      if j!=0:
        j=lps[j-1]
      else:
        i+=1
  return False
def is_valid_min_heap_recurse(arr,at_i):
  left_i=(at_i<<1)+1
  right_i=left_i+1
  if left_i<len(arr):
    if arr[at_i]>arr[left_i]: return False
    if not is_valid_min_heap_recurse(arr,left_i): return False #Recursively check child nodes if violating the min heap property
  if right_i<len(arr):
    if arr[at_i]>arr[right_i]: return False
    return is_valid_min_heap_recurse(arr,right_i)
  return True #Base case if both nodes are non-existent/out-of-bounds
def is_valid_min_heap(arr): #For unit testing if an array is still a min heap
  if len(arr)==0: return True
  else: return is_valid_min_heap_recurse(arr,0)
def sift_down_min(heap_arr:list,at_i):
  next_i=at_i
  while True:
    left_i=(next_i<<1)+1
    if left_i>=len(heap_arr): break
    child_i=left_i
    right_i=left_i+1
    if right_i<len(heap_arr): #If valid, check if right is smaller than left
      if heap_arr[right_i]<heap_arr[left_i]: child_i=right_i
    if heap_arr[child_i]<heap_arr[next_i]: #Check if the smallest child_i violates the min heap
      temp=heap_arr[child_i]
      heap_arr[child_i]=heap_arr[next_i]
      heap_arr[next_i]=temp
      next_i=child_i #Check the other children of child_i
    else: break
def add_as_min_heap(heap_arr:list,elem,check_if_still_heap=False):
  """To always be a min heap when inserting elem, assuming heap_arr is always a min heap"""
  heap_arr.append(elem)
  higher_i_p1=len(heap_arr) #_p1 means to get the index (+ 1). To get the index, subtract by 1.
  lower_i_p1=higher_i_p1>>1
  while lower_i_p1!=0: #Sift up
    if heap_arr[lower_i_p1-1]>heap_arr[higher_i_p1-1]:
      temp=heap_arr[lower_i_p1-1]
      heap_arr[lower_i_p1-1]=heap_arr[higher_i_p1-1]
      heap_arr[higher_i_p1-1]=temp
    else: break
    higher_i_p1>>=1
    lower_i_p1>>=1
  if check_if_still_heap: assert(is_valid_min_heap(heap_arr))
def pop_as_min_heap(heap_arr:list,check_if_still_heap=False):
  """Used for heapsort to get the alphabetically ordered strings first"""
  if len(heap_arr)==0: return None
  return_value=heap_arr[0]
  heap_arr[0]=heap_arr[-1]
  heap_arr[-1]=return_value
  del heap_arr[-1]
  for i in range(len(heap_arr)>>1,-1,-1): sift_down_min(heap_arr,i)
  if check_if_still_heap: assert(is_valid_min_heap(heap_arr))
  return return_value
class MinHeapMethods(unittest.TestCase): #Check if the methods can work with random integers
  def test_add_as_min_heap(self):
    for _ in range(1000):
      use_heap=[]
      for elem in random.sample(range(0,100),100):
        add_as_min_heap(use_heap,elem,True)
  def test_pop_as_min_heap(self):
    use_heap=[]
    for _ in range(1000):
      rand_ints=random.sample(range(0,100),100)
      for elem in rand_ints:
        add_as_min_heap(use_heap,elem,True)
      while pop_as_min_heap(use_heap,True)!=None: pass
if __name__ == '__main__':
  unittest.main()