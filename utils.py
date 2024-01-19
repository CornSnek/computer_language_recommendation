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
class HeapSortContext:
  """Used to make heap sort generic in add_as_heap and pop_as_heap"""
  def __init__(self,sortf,sortf_inv):
    self.sortf=sortf
    self.sortf_inv=sortf_inv
  def copy_inv(self):
    return HeapSortContext(self.sortf_inv,self.sortf) #For heapsort because it sorts the context values backwards
class HeapSortMinIntContext(HeapSortContext):
  def __init__(self):
    super().__init__(sortf=HeapSortMinIntContext.l_lt_r,sortf_inv=HeapSortMinIntContext.l_gt_r)
  def l_lt_r(arr:list[int],l:int,r:int):
    return arr[l]<arr[r]
  def l_gt_r(arr:list[int],l:int,r:int):
    return arr[l]>arr[r]
class AlphabeticalHeapSortContext(HeapSortContext):
  def __init__(self):
    super().__init__(sortf=AlphabeticalHeapSortContext.l_lt_r,sortf_inv=AlphabeticalHeapSortContext.l_gt_r)
  def l_lt_r(arr:list[str],l:int,r:int):
    return arr[l].lower()<arr[r].lower()
  def l_gt_r(arr:list[str],l:int,r:int):
    return arr[l].lower()>arr[r].lower()
def is_valid_heap_recurse(arr,at_i,context:HeapSortContext):
  left_i=(at_i<<1)+1
  right_i=left_i+1
  if left_i<len(arr):
    if context.sortf_inv(arr,at_i,left_i): return False
    if not is_valid_heap_recurse(arr,left_i,context): return False #Recursively check child nodes if violating the min heap property
  if right_i<len(arr):
    if context.sortf_inv(arr,at_i,right_i): return False
    return is_valid_heap_recurse(arr,right_i,context)
  return True #Base case if both nodes are non-existent/out-of-bounds
def is_valid_heap(arr,context:HeapSortContext): #For unit testing if an array is still a min heap
  if len(arr)==0: return True
  else: return is_valid_heap_recurse(arr,0,context)
def sift_down(heap_arr:list,start:int,end:int,context:HeapSortContext):
  #start is included, but end is excluded
  next_i=start
  while True:
    left_i=(next_i<<1)+1
    if left_i>=end: break
    child_i=left_i
    right_i=left_i+1
    if right_i<end: #If valid, check if right is smaller than left
      if context.sortf(heap_arr,right_i,left_i): child_i=right_i
    if context.sortf(heap_arr,child_i,next_i): #Check if the smallest child_i violates the min heap
      temp=heap_arr[child_i]
      heap_arr[child_i]=heap_arr[next_i]
      heap_arr[next_i]=temp
      next_i=child_i #Check the other children of child_i
    else: break
def add_as_heap(heap_arr:list,elem,context:HeapSortContext,check_if_still_heap=False):
  """To always be a min heap when inserting elem, assuming heap_arr is always a min heap"""
  heap_arr.append(elem)
  higher_i_p1=len(heap_arr) #_p1 means to get the index (+ 1). To get the index, subtract by 1.
  lower_i_p1=higher_i_p1>>1
  while lower_i_p1!=0: #Sift up
    if context.sortf_inv(heap_arr,lower_i_p1-1,higher_i_p1-1):
      temp=heap_arr[lower_i_p1-1]
      heap_arr[lower_i_p1-1]=heap_arr[higher_i_p1-1]
      heap_arr[higher_i_p1-1]=temp
    else: break
    higher_i_p1>>=1
    lower_i_p1>>=1
  if check_if_still_heap: assert(is_valid_heap(heap_arr,context))
def pop_as_heap(heap_arr:list,context:HeapSortContext,check_if_still_heap=False):
  """Used for heapsort to get the alphabetically ordered strings first"""
  if len(heap_arr)==0: return None
  return_value=heap_arr[0]
  heap_arr[0]=heap_arr[-1]
  heap_arr[-1]=return_value
  del heap_arr[-1]
  for i in reversed(range(len(heap_arr)>>1)): sift_down(heap_arr,i,len(heap_arr),context)
  if check_if_still_heap: assert(is_valid_heap(heap_arr,context))
  return return_value
def heapsort(arr:list,context:HeapSortContext):
  """Using the pseudocode from https://en.wikipedia.org/wiki/Heapsort"""
  use_context=context.copy_inv() #Inverse context sort functions to make the sorting context valid from left to right.
  for i in reversed(range(len(arr)>>1)): sift_down(arr,i,len(arr),use_context) #Heapify array
  for end in reversed(range(len(arr))):
    temp=arr[end]
    arr[end]=arr[0]
    arr[0]=temp
    for i in reversed(range(end>>1)): sift_down(arr,i,end,use_context) #Heapify again (excluding the end) after placing the extreme value at the end.
class MinHeapMethods(unittest.TestCase): #Check if the methods can work with random integers
  UseContext=HeapSortMinIntContext()
  def test_add_as_heap(self):
    for _ in range(100):
      use_heap=[]
      for elem in random.sample(range(0,100),100):
        add_as_heap(use_heap,elem,MinHeapMethods.UseContext,True)
  def test_pop_as_heap(self):
    use_heap=[]
    for _ in range(100):
      rand_ints=random.sample(range(0,100),100)
      for elem in rand_ints:
        add_as_heap(use_heap,elem,MinHeapMethods.UseContext,True)
      while pop_as_heap(use_heap,MinHeapMethods.UseContext,check_if_still_heap=True)!=None: pass
  def test_heapsort(self):
    for _ in range(100):
      should_be_sorted=random.sample(range(0,100),100)
      heapsort(should_be_sorted,MinHeapMethods.UseContext)
      for i in range(len(should_be_sorted)-1):
        assert(MinHeapMethods.UseContext.sortf(should_be_sorted,i,i+1))
if __name__ == '__main__':
  unittest.main()