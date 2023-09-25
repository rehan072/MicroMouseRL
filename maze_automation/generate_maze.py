
##import os for reading mazes and  and writing to wordl file. will have to be your own paths
import os


##Collects and stores maze should be global
maze_store = []
#defaults to first maze in maze archive
def collect_maze(store_name = maze_store, maze_name = "1stworld.txt"):    
    ## change this according to your own directory
    os.chdir("/Users/rehanm/Documents/my_project/mazes")    
    maze_file = open(maze_name, "r")
    for chunk in iter(lambda: maze_file.read(), ''):
        store_name.append(chunk)
    


##parses global store and generates maze in the world file
##make sure to change the directories according to your projects needs

class auto_gen():
    def __init__(self) -> None:
        ##coordinates for rotation and translation this might differ accordng to your floor size
        ## is defaulted to standard micromouse maze size in webots
        self.coordinates = [-1.432, 1.432, 0.02]
        self.rotation_coordinates = [-0.577351, -0.57735, -0.57735, -2.09439]
        
        ##for proto naming purposes
        self.wall_count = 0
        self.interval_count = 0
        
        ##what finally gets appended to world file
        self.master_string = ""
        
        #protos used in maze file
        self.protos = ("o", "-", "|", " ", "\n")
        
        #to check if new line has been reached
        self.been_reset = 0
    
    ##adds wall proto
    def add_wall(self):
        self.wall_count += 1
        command = "LegoWall {{\n\ttranslation {} {} {}\n\trotation {} {} {} {}\n\tname \"LegoWall{}\"\n}}\n".format(self.coordinates[0], self.coordinates[1], 
                                                                                      self.coordinates[2], self.rotation_coordinates[0], 
                                                                                      self.rotation_coordinates[1], self.rotation_coordinates[2],
                                                                                      self.rotation_coordinates[3], self.wall_count)
        
        return command
    
    ##adds interval proto
    def add_interval(self):
        self.interval_count += 1
        command = "LegoInterval {{\n\ttranslation {} {} {}\n\trotation {} {} {} {}\n\tname \"LegoInterval{}\"\n}}\n".format(self.coordinates[0], self.coordinates[1], 
                                                                                      self.coordinates[2], self.rotation_coordinates[0], 
                                                                                      self.rotation_coordinates[1], self.rotation_coordinates[2],
                                                                                      self.rotation_coordinates[3], self.interval_count)
        
        return command
    
    ##resets when \n found equivalent of new line
    ##always assuming you are generating the same way
    def reset_translation(self):
        self.coordinates[0] = -1.432
        self.coordinates[1] -= 0.056
        self.coordinates[2] = 0.02
        self.been_reset += 1
        
    ##rotates angular coordinates by 90
    def rotate(self):
        vertical = [1.69525e-09, 0.707107, 0.707107, 3.14159]
        horizantal = [-0.577351, -0.57735, -0.57735, -2.09439]
        
        if (self.rotation_coordinates == horizantal):
            self.rotation_coordinates = vertical
            
        elif (self.rotation_coordinates == vertical):
            self.rotation_coordinates = horizantal

    def parse_maze(self):
        
        ##account for three ---
        dash_count = 0
        gap_count = 0
        four_count = 0
        
        for proto in maze_store[0]:
            
            ##interval
            if (proto == self.protos[0]):
                ##THE FIRST ONE ON THE TOP CORNER
                four_count = 0 
                
                if self.interval_count == 0: 
                    self.master_string += self.add_interval()
                    #self.coordinates[0] += 0.056
                    
                #first ones on the y axis
                elif (self.been_reset == 1):
                    self.master_string += self.add_interval()
                    #self.coordinates[0] += 0.056
                    self.been_reset = 0
                #every other one
                else:
                    self.coordinates[0] += 0.056
                    self.master_string += self.add_interval()
                    
                    
                    
            ## wall
            elif proto == self.protos[1]:
                dash_count += 1
                if dash_count == 3:
                    self.coordinates[0] += 0.056
                    self.master_string += self.add_wall()
                    dash_count = 0
                    
            ##pipe |
            if proto == self.protos[2]:
                four_count = 0
                #first one on the y axis
                if self.been_reset == 1:
                    self.rotate()
                    #self.coordinates[0] += 0.056
                    self.master_string += self.add_wall()
                    #self.coordinates[0] += 0.056
                    self.been_reset = 0
                    self.rotate()
                #every other | including the last row
                else: 
                    self.rotate()
                    self.coordinates[0] += 0.056
                    self.master_string += self.add_wall()
                    self.rotate()
            
            ## 
            ##gap
            if proto == self.protos[3]:
                gap_count += 1
                four_count += 1
                if gap_count == 3:
                    self.coordinates[0] += 0.056
                    gap_count = 0
                    
                if four_count == 4:
                    self.coordinates[0] += 0.056
                    gap_count = 0
                    four_count = 0
                
            
             ##  gap_count = 0
                
            
            ##new line
            if proto == self.protos[4]:
                self.reset_translation()
        
    ##this is the final function that finalizes world
    def generate_world(self, world_name):
        #print(f"master string{self.master_string}")
        os.chdir("/Users/rehanm/Documents/my_project/worlds")
        with open(world_name,"a") as world:
            world.write(self.master_string)
        


