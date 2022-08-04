import PygameFunctions as PF

PF.winningData("dataCollectionAI1.csv", "AIWiningLineGraph", tail=5)
"""
this function plots two lines in which one repersents people saved and the other represents turns survived
X-axis in all my graphs is the iteration or the game rounds the AI played
In this function and in other functions you can specify after the second str parameter the range you want to graph
for exaple if we say [200, 301] this will get all the data from 200th to 300th (the stop isn't included) 
this is an optional parameter
another optional parameter is the tail parameter, you don't need to use both the range and the tail parameters
if you do the function will ignore the tail parameter 
so if we say tail = 100 basicly the tail gets the last 100th data and graphs that 
"""
PF.winingDataPeopleSaved("dataCollectionAI1.csv", "AIWiningLineGraph", tail=5)
PF.winingDataTurnsSurvived("dataCollectionAI1.csv", "AITurnsSurvived", tail=100)
PF.winingDataResourcesRemaining("dataCollectionAI1.csv", "AIResourcesRemaining", [300,501])
"""
All three of the functions above are very similar to how they work with the first function I described
they are more specific and only graph one line
note: the tail and the range was put there for demonstration we don't need to use them
"""
PF.getWinCases("dataCollectionAI1.csv", "AIwincases", "people saved")
"""
This function is a little bit different 
it takes three str parameters (all three required/ not optional)
the last two are still the same optional ones I disscused 
what this function does is it plots two different lines, one for win and one for lose 
the x-axis is still the iteration 
but the y-axis is determined by us which in this case is people saved
so it basicly compares how many people have been saved in each iteration and was it a win or a lose(smth like this)
"""


