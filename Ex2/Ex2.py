#!/usr/bin/env python
# coding: utf-8

# In[23] :


def donuts(count):
    if isinstance(count, int):
        if count < 10:
            return f'number of donuts: {count}'
        else:
            return 'number of donuts: many'
    else:
        return 'Invalid input: please enter an integer'

def verbing(s):
    if len(s) >= 3:
        if s[-3:] == 'ing':
            return s + 'ly'
        else:
            return s + 'ing'
    else:
        return s
def remove_adjacent(nums):
    if not nums:
        return []
    
    result = [nums[0]] 
    
    for num in nums[1:]:
        if num != result[-1]:
            result.append(num)
          
    return result
def main():
    print('donuts')
    print(donuts(4))
    print(donuts(9))
    print(donuts(10))
    print(donuts('twentyone'))
    print('verbing')
    print(verbing('hail'))
    print(verbing('swiming'))
    print(verbing('do'))
    print('remove_adjacent')
    print(remove_adjacent([1, 2, 2, 3]))
    print(remove_adjacent([2, 2, 3, 3, 3]))
    print(remove_adjacent([]))

# Standard boilerplate to call the main() function.
if __name__ == '__main__':
    main()


# In[ ]:




