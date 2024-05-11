#creative element: player's life was added to the game, each player has three lifes
# in the beginning of the game, there will be a three seconds counter, after the counter is over,
# player one should press key s, palyer two should press key k, whoever presses first will receive the initiative to shoot'
from cmu_graphics import *
import string, math,random

def onAppStart(app):
    app.width=600
    app.height=600
    app.buildingCount=10
    app.playerRadius=15
    app.holeRadius=40
    startNewGame(app)


def startNewGame(app):
    app.gameOver=False
    app.buildingHeights=[random.randrange(50,250) for _ in range(app.buildingCount)]
    colors=['red','orange','yellow','green','blue','purple']
    app.buildingColors = [random.choice(colors) for _ in range(app.buildingCount)]
    buildingWidth=app.width/app.buildingCount
    #place new players
    cx0=buildingWidth/2
    cy0=app.height-app.buildingHeights[0]-app.playerRadius
    cx1=app.width-buildingWidth/2
    cy1=app.height-app.buildingHeights[-1]-app.playerRadius
    app.players=[(cx0,cy0,'blue'),(cx1,cy1,'pink')]
    app.showBlot=False
    app.currentPlayer=0
    app.holes=[]
    app.livesRemain1=3
    app.livesRemain2=3
    app.counter=4
    app.pressed=False
def onKeyPress(app,key):
    if(key=='n'):
        startNewGame(app)
    # press to get turn
    if(app.counter<0 and app.pressed==False):
        if(key=='s'):
            app.currentPlayer=0
            app.pressed=True
        elif(key=='k'):
            app.currentPlayer=1
            app.pressed=True
    
def getBuildingBounds(app,i):
    width=app.width/app.buildingCount
    height=app.buildingHeights[i]
    left=i*width
    top=app.height-height
    return (left,top,width,height)
    
    
def redrawAll(app):
    drawRect(0,0,app.width,app.height,fill='cyan')
    if(app.counter>=0):
        drawLabel(int(app.counter),300,200,fill='red',size=40)
        drawLabel('Press s to get your turn!!!',120,300,fill='red',size=20)
        drawLabel('Press k to get your turn!!!',480,300,fill='red',size=20)
    #draw player's turn
    drawLabel(f'Player BlotShooter',app.width/2,25,size=20)
    drawLabel(f'Current Player: {app.currentPlayer}',app.width/2,50,size=16)
    drawLabel(f'player 1 lifes remain: \t{app.livesRemain1}',100,100,size=16)
    drawLabel(f'player 2 lifes remain: \t{app.livesRemain2}',500,100,size=16)
    #draw buildings
    for i in range(app.buildingCount):
        color=app.buildingColors[i]
        left,top,width,height=getBuildingBounds(app,i)
        drawRect(left,top,width,height,fill=color, border='black',borderWidth=2)
    #draw hole
    for cx,cy in app.holes:
        drawCircle(cx,cy,app.holeRadius,fill='cyan')
    #draw player
    for player in range(len(app.players)):
        cx,cy,color=app.players[player]
        drawCircle(cx,cy,app.playerRadius,fill=color)
    if app.showBlot:
        drawCircle(app.blotCx,app.blotCy,app.playerRadius,fill=app.blotColor)
    if(app.gameOver):
        drawLabel('Game Over',300,100,opacity=50,size=70,bold=True)

    
def onMousePress(app,mouseX,mouseY):
    if(app.counter>0):
        return
    if(app.gameOver):
        return
    if(not app.showBlot):
        if(app.currentPlayer==0):
            app.dx,app.dy=mouseX/20, -(app.height-mouseY)*30/app.height
        else:
            app.dx,app.dy=-(app.width-mouseX)/20,-(app.height-mouseY)*30/app.height
        app.showBlot=True
        app.blotCx,app.blotCy,app.blotColor=app.players[app.currentPlayer]

def onStep(app):
    app.counter-=0.03
    if(app.gameOver):
        return 
    if app.showBlot:
        app.blotCx+=app.dx
        app.blotCy+=app.dy
        app.dy+=1
        #check if off board
        if(app.blotCx<0 or app.blotCx>app.width or app.blotCy>app.height):
            app.showBlot=False
            app.currentPlayer=1-app.currentPlayer
        else:
            #checkif hit player
            otherCx,otherCy,x=app.players[1-app.currentPlayer]
            if distance(otherCx,otherCy,app.blotCx,app.blotCy)<=app.playerRadius*2:
                # player's life
                if(app.currentPlayer==1):
                    app.livesRemain1-=1
                    app.currentPlayer=0
                else:
                    app.livesRemain2-=1
                    app.currentPlayer=1
                app.pressed==False
                app.counter=4
                app.showBlot=False
            if(app.livesRemain2==0 or app.livesRemain1==0):
                app.gameOver=True
                app.counter=0
                
                
                
        #check off building
            for i in range(app.buildingCount):
                for cx,cy in app.holes:
                    if distance(cx,cy,app.blotCx,app.blotCy)<=40:
                        return
                left,top,width,height=getBuildingBounds(app,i)
                if(left<=app.blotCx<=left+width and top <= app.blotCy <=top+height):
                    app.showBlot=False
                    app.holes.append((app.blotCx,app.blotCy))
                    app.currentPlayer=1-app.currentPlayer
def distance(x0,y0,x1,y1):
    return ((x1-x0)**2+(y1-y0)**2)**0.5
def main():
    runApp()

main()