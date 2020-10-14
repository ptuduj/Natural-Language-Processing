import regex
from os import listdir
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

addition_regex = r'dodaje się (art|pkt|lit|ust|§)'
removal_regex = r'(skreśla się (pkt|art|ust|lit|§))|([0-9]+[a-z]? skreśla się)'
change_regex = r'(pkt|art\.|ust\.|§|lit\.) ([0-9]*[a-z]?( | i |, |-))+otrzymuj(e|ą) brzmienie'

additions, removals, changes = {}, {}, {}

#task 4
law_regex1 = r'\bustaw(a|y|ie|ę|ą|o|y|om|ami|ach)?\b'
#task 5
law_regex2 =  r'\bustaw(a|y|ie|ę|ą|o|y|om|ami|ach)?\b z dnia'
#task 6
law_regex3 =  r'\bustaw(a|y|ie|ę|ą|o|y|om|ami|ach)?\b(?! z dnia)'
#task 7
law_regex4 =  r'(?<!o zmianie )(\bustaw(a|y|ie|ę|ą|o|y|om|ami|ach)?\b)'

law_occurances1, law_occurances2, law_occurances3, law_occurances4 = 0, 0, 0, 0

#test_law_regex =  r'(\o zmianie )(?=\bustaw(a|y|ie|ę|ą|o|y|om|ami|ach)?\b)'
#test_occurances = 0

data = [f for f in listdir('dane')]
for i,file_name in enumerate(data):
    file = None
    with open('dane/'+file_name, 'r', encoding='utf-8') as f:
        file = f.read().lower()

    year = file_name.split('_')[0]
    with open('dane/' + file_name, 'r', encoding='utf-8') as f:
        file = f.read().lower()
    if year in additions:
        additions[year] += len(regex.findall(addition_regex, file))
    else:
        additions[year] = len(regex.findall(addition_regex, file))
    if year in removals:
        removals[year] += len(regex.findall(removal_regex, file))
    else:
        removals[year] = len(regex.findall(removal_regex, file))
    if year in changes:
        changes[year] += len(regex.findall(change_regex, file))
    else:
        changes[year] = len(regex.findall(change_regex, file))

    law_occurances1 += len(regex.findall(law_regex1, file))
    law_occurances2 += len(regex.findall(law_regex2, file))
    law_occurances3 += len(regex.findall(law_regex3, file))
    law_occurances4 += len(regex.findall(law_regex4, file))
    #test_occurances += len(regex.findall(test_law_regex, file))

additions_sum = sum(list(additions.values()))
removals_sum = sum(list(removals.values()))
changes_sum = sum(list(changes.values()))

#task 1
print('additions: {}\tremovals: {}\tchanges: {}'.format(additions_sum, removals_sum, changes_sum))
#task 4
print('all law occurances: {}'.format(law_occurances1))
#task 5
print('law occurances followed by \"z dnia\": {}'.format(law_occurances2))
#task 6
print('law occurances not followed by \"z dnia\": {}'.format(law_occurances3))
#print(law_occurances2 + law_occurances3 == law_occurances1)
#task 7
print('law occurances not following \"o zmianie\": {}'.format(law_occurances4))
#print(law_occurances4 + test_occurances == law_occurances1)


xs = list(additions.keys())
additions_prcnt = [(additions[year]*100)/(additions[year]+removals[year]+changes[year]) for year in xs]
removals_prcnt = [(removals[year]*100)/(additions[year]+removals[year]+changes[year]) for year in xs]
changes_prcnt = [(changes[year]*100)/(additions[year]+removals[year]+changes[year]) for year in xs]

plt.plot(xs,additions_prcnt,color = 'green')
plt.plot(xs,removals_prcnt,color = 'blue')
plt.plot(xs,changes_prcnt,color = 'purple')

green_patch = mpatches.Patch(color='green', label='additions')
blue_patch = mpatches.Patch(color='blue', label='removals')
purple_patch = mpatches.Patch(color='purple', label='changes')
plt.xlabel('Year')
plt.ylabel('% of occurances')
plt.legend(handles = [green_patch,blue_patch,purple_patch])
plt.show()

patches =[]
pink_patch = mpatches.Patch(color='pink', label='all law occurances')
purple_patch = mpatches.Patch(color='purple', label='law occurances followed by \"z dnia\"')
blue_patch = mpatches.Patch(color='blue', label='law occurances not followed by \"z dnia\"')
green_patch = mpatches.Patch(color='green', label='law occurances not following \"o zmianie\"')
tick_label = ['' for i in range(4)]
plt.bar(0.5,law_occurances1,color ='pink', width=0.4)
plt.bar(1.5,law_occurances2,color='purple', width=0.4)
plt.bar(2.5,law_occurances3,color='blue', width=0.4)
plt.bar(3.5,law_occurances4,color='green', width=0.4)
plt.legend(handles =[pink_patch,purple_patch,blue_patch,green_patch])
plt.ylabel('total occurances')
plt.show()


