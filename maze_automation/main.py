from generate_maze import auto_gen, collect_maze


def main():
    
    automation_maze = auto_gen()
    
    collect_maze()
    automation_maze.parse_maze()
    automation_maze.generate_world(world_name="mms.wbt")
        
        
if __name__ == "__main__":
    main()