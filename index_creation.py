import csv

#### Create a list of lists that contain the x and y in this form: [[x,y],[x,y],...]
def positions_in_space(list_of_coordinates):
    xylist=[]      ### List of x and y
    x_and_y=[]     ### Create [x,y] 


    for i in range(0,len(list_of_coordinates)):
            x,y=list_of_coordinates[i].split(' ')
            x_and_y.append(float(x))
            x_and_y.append(float(y))
            xylist.append(x_and_y) 
            x_and_y=[]

    return xylist


# Find the MBR for every linestring

def MBR(list):
    MBR_max=[]
    MBR_min=[]
    x_list=[]
    y_list=[]
    list_of_MBR=[]

    for i in range(0,len(list)):
        x_list.append(list[i][0])
        y_list.append(list[i][1])

    x_list.sort()
    y_list.sort()

    MBR_max.append(x_list[-1])
    MBR_max.append(y_list[-1])
    MBR_min.append(x_list[0])
    MBR_min.append(y_list[0])

    list_of_MBR.append(MBR_min)
    list_of_MBR.append(MBR_max)
    
    return list_of_MBR
     

# Finds the minimum and maximum x and y from the file

def minmax(big_list):
    max_X=0
    min_X=0
    max_Y=0
    min_Y=0
    x_list=[]
    y_list=[]

    for i in range(0,len(big_list)):
        x_list.append(big_list[i][0])
        y_list.append(big_list[i][1])

    max_X=max(x_list)
    min_X=min(x_list)
    max_Y=max(y_list)
    min_Y=min(y_list)

    return max_X,min_X,max_Y,min_Y


### Creates the grid

def grid_maker(max_X,min_X,max_Y,min_Y):
    x_distance=[]       ### A list with x values on the axis
    y_distance=[]       ### A list with y values on the axis
    grid_ofX=[]         ### A list that contains all the x_distance lists
    grid_ofY=[]         ### ### A list that contains all the y_distance lists
    

    for i in range(0,10):
        x_distance.append(min_X+i*(max_X-min_X)/10)
        x_distance.append(min_X+(i+1)*(max_X-min_X)/10)
        grid_ofX.append(x_distance)
        x_distance=[]

        y_distance.append(min_Y+i*(max_Y-min_Y)/10)
        y_distance.append(min_Y+(i+1)*(max_Y-min_Y)/10)
        grid_ofY.append(y_distance)
        y_distance=[]
        
    return grid_ofX,grid_ofY


### A function that counts how many linestrings are in every cell

def position_counter(xlist,ylist,listofMBR,listofeverything):
    dir_list=[0]*100      ### List for grid.dir file
    grd_list=[]           ### List for grid.grd file
    for i in range(100):
        grd_list.append([])
    c2=0

    
    for i in range(0,len(listofMBR)):
            x_value_distance=0          ### x_value_distance = x_value2 - x_value1
            y_value_distance=0          ### y_value_distance = y_value2 - y_value1
            x_value1=0
            x_value2=0
            y_value1=0
            y_value2=0


            x_check=0
            y_check=0
            distance_check=0
            j=0

            ### When distance_check == 2 stop the while loop because both x_value_distance and y_value_distance have been calculated
            while distance_check<2:
                # for the distance of x
                if listofMBR[i][0][0]>=xlist[j][0]:
                    if listofMBR[i][0][0]<=xlist[j][1]:
                        x_value1=j
                        x_check+=1

                if listofMBR[i][1][0]>=xlist[j][0]:
                    if listofMBR[i][1][0]<=xlist[j][1]:
                        x_value2=j
                        x_check+=1
                
                # for the distance of y
                if listofMBR[i][0][1]>=ylist[j][0]:
                    if listofMBR[i][0][1]<=ylist[j][1]:
                        y_value1=j
                        y_check+=1
                
                if listofMBR[i][1][1]>=ylist[j][0]: 
                    if listofMBR[i][1][1]<=ylist[j][1]:
                        y_value2=j
                        y_check+=1

                ### when x_check or y_check are equal to 2 calculate x_value_distance and y_value_distance
                if x_check==2:
                    x_value_distance=x_value2-x_value1+1
                    x_check=0
                    distance_check+=1
                
                if y_check==2:
                    y_value_distance=y_value2-y_value1+1
                    y_check=0
                    distance_check+=1
                
                j+=1
            distance_check=0
    

            ### Add on the specific cells the number of linestings
            for x in range (x_value_distance):
                for y in range(y_value_distance):
                    dir_list[(x_value1+x)*10+(y_value1+y)]+=1
                    c2+=1
                    grd_list[(x_value1+x)*10+(y_value1+y)-1].append(listofeverything[i])

    return dir_list,grd_list




#####  MAIN  #######
parent_list=[]              ### This list has all the lines in lists from the file
child_list=[]               ### This list has a single line  from the file
for_minmax=[]               ### This has the values of all x and y from the file
for_position_counter=[]     ### A list that contains all the MBR


with open("./tiger_roads.csv",'r') as file:
    csvreader = csv.reader(file)
    counter=0
    for row in csvreader:

        if counter<1:
            #### If reading the first line don't add it in the lists
            number_of_linestring=float(row[0])

        if counter>=1:

            #### Make a line into a list with ID,[MBR],[every x and y from the file]

            child_list.append(counter)                       ### Add the ID
            xy_list=positions_in_space(row)                  ### Create a list that contains x and y in lists
            MBR_list= MBR(xy_list)                           ### Make a list with the MBR
            child_list.append(MBR_list)                      ### Add the MBR
            child_list.append(xy_list)                       ### Add the x and y
            parent_list.append(child_list)                   ### Add the line inside the parent list
            for_position_counter.append(MBR_list)            ### Fill the list with all the MBR
            for i in range(0,len(xy_list)):
                for_minmax.append(xy_list[i])                ### Fill the list with all the x and y
            
        counter+=1
        child_list=[]

maxX,minX,maxY,minY=minmax(for_minmax)            #### Find the minimum and maximum of all the x and y from the file
Xaxis,Yaxis=grid_maker(maxX,minX,maxY,minY)       #### Use the max and min of x and y to create two lists that represent the grid



grid_dir,grid_grd=position_counter(Xaxis,Yaxis,for_position_counter,parent_list)   #### Function to create lists for the files grid.dir and grid.grd
counter=1

# to make the file grid.dir
with open('grid.dir','w') as f:

    f.write(str(counter))
    f.write(' ')
    f.write(str(minX))
    f.write(' ')
    f.write(str(maxX))
    f.write(' ')
    f.write(str(minY))
    f.write(' ')
    f.write(str(maxY))
    f.write('\n')

    for i in range(0,10):
        for j in range(0,10):
            counter+=1
            f.write(str(counter))
            f.write(' ')
            f.write(str(i))
            f.write(' ')
            f.write(str(j))
            f.write(' ')
            f.write(str(grid_dir[i*10+j]))
            f.write('\n')
            

# to make the file grid.grd
with open('grid.grd','w') as f:
    for i in range(0,len(grid_grd)):
        for i1 in range(0,len(grid_grd[i])):
            f.write(str(grid_grd[i][i1][0]))
            f.write('|')
            for j in range(len(grid_grd[i][i1][1])):
                f.write(str(grid_grd[i][i1][1][j][0]))
                f.write(',')
                f.write(str(grid_grd[i][i1][1][j][1]))
                f.write(',')
            f.write('|')
            for j in range(len(grid_grd[i][i1][2])):
                f.write(str(grid_grd[i][i1][2][j][0]))
                f.write(',')
                f.write(str(grid_grd[i][i1][2][j][1]))
                f.write('/')
            f.write('\n')
