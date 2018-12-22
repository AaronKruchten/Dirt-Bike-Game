# code I've written but don't need. Keeping this for reference if necessary
'''
    maxNumberOfIndices = 10000
    lst = self.points[self.index:maxNumberOfIndices]
    frontWheelHeight = lst[self.frontWheelIndex][0]
    backWheelHeight = lst[self.backWheelIndex][0]
    if frontWheelHeight != backWheelHeight:
        #print(backWheelHeight-frontWheelHeight)
        if backWheelHeight- frontWheelHeight > self.wheelHeightDifference:
            self.wheelHeightDifference = backWheelHeight- frontWheelHeight
            # width of the dirtbiker self.bikerWidth we can treat this as a 
            #hypotenuse connecting frntwheelheight and backwheelheight
            leg_one = self.wheelHeightDifference
            hypotenuse = self.bikerWidth
            angle = asin(leg_one//2/hypotenuse)*(180/pi)
            #print(angle)
            image = pygame.image.load('dirtBike.png').convert_alpha()
            self.DirtBiker = rot_center(image,angle)
    midPoint = (frontWheelHeight + backWheelHeight)//2
    difference = self.YBikerPostion - frontWheelHeight + self.bikerHeight
    self.YBikerPostion = self.YBikerPostion - difference
    print(self.YBikerPostion)



def physics(self):
    
    image = pygame.image.load('dirtBike.png').convert_alpha()
    lst = self.points[self.index:]
    actualHeight = self.bikerHeight + self.YBikerPostion 
    frontWheelHeight = lst[self.frontWheelIndex][0]
    obstacle = lst[self.frontWheelIndex][-1]
    backWheelHeight = lst[self.backWheelIndex][0]
    margin_of_error = -5
    if lst[self.frontWheelIndex+3][0] - lst[self.frontWheelIndex+3][0] == 0 and lst[self.frontWheelIndex][0] - lst[self.frontWheelIndex-1][0] != 0:
        self.increaseheight = True
        self.timer =0 
            
            
        self.climbing = True
    if abs(self.actualFrontHeight  - self.actualBackHeight) >= 10:
        pass


def inertia(self):
    #antigravity = 10 
    #y_increase = self.speed * sin(self.angle)
    #self.YBikerPostion -= y_increase + antigravity
    pass
    

def animateImage(image):
    if image == 'dirtBike.png':
        return 'dirtBike.png'
    if image == 'direBike_one.png':
        return 'dirtBike.png'
    else:
         return 'dirtBike.png'


'''

import HomeScreenList

print(HomeScreenList.starting_lst)