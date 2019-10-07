> **This bot will work only for 1920x720 resolution screen**

# Dofus retro bot

## record.py

### Description

the script waits 3 seconds before taking a screenshot of the game, then it prints the RGB color of the position of the mouse in the game each time the "z" key is pressed

### argument

  - pos : print also the position of the mouse
  - stream : takes new screenshot each time the "z" key is pressed 

### usage

```shell
pyhton3 record.py
pyhton3 record.py pos
pyhton3 record.py stream
```

## play.py

### Description

it runs the bot

### how it works ?

1. You go into a resources map
2. You add the resource(s) you want to pick up in the `resources` variables
3. you create a recursive trajectory in the *play/maps* folder
4. You run the bot and he will pick up resource, move and fight automatically 
